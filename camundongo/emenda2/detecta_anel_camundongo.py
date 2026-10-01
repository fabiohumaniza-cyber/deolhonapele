"""
detecta_anel_camundongo.py — detector do anel de contencao de 16 mm.

CONGELADO PELA EMENDA 2 do pre-registro do camundongo (01/10/2026).
Escrito e calibrado ANTES de qualquer imagem do banco Dryad 10.25338/B84W8Q
ser aberta. Testado somente em imagens sinteticas desenhadas por codigo, com a
geometria dos NOMINAIS DO README (EMENDA 1): parede do splint de 10 mm (interna)
a 16 mm (externa), coverslip de 16 mm, ferida de punch de 6 mm.

Nao contem nenhuma constante do motor v0 e nao altera nenhuma.
Devolve apenas: centro do anel e diametro do eixo maior, em px da imagem original.

O protocolo manda medir o ANEL EXTERNO. Como a cena tem ate tres curvas
concentricas (16 mm, 10 mm e a ferida de 6 mm), o detector extrai varias elipses
e escolhe, entre as concentricas, a de MAIOR eixo com apoio angular.
"""
import numpy as np
from PIL import Image
from skimage.feature import canny

# ----------------------------------------------------------------------
# CONSTANTES DO DETECTOR — fixadas pela Emenda 2, nenhuma por imagem
# ----------------------------------------------------------------------
SIGMA        = 2.0       # suavizacao gaussiana do Canny
Q_BAIXO      = 0.98      # quantil do gradiente -> limiar baixo do Canny
Q_ALTO       = 0.995     # quantil do gradiente -> limiar alto do Canny
MAX_PTS      = 40000     # teto de pixels de borda usados (subamostragem por passo)
N_BINS       = 200       # bins do histograma radial que acha as curvas concentricas
PICO_FRAC    = 0.25      # altura minima de um pico, fracao do maior pico
BANDA_H      = 0.25      # banda do pico radial; cobre b/a ate MIN_ACHATA
N_TRIM       = 3         # reajustes com corte dos pontos fora da banda (fixo)
MIN_PTS_FIT  = 60        # pontos minimos para ajustar uma elipse
CONCENT      = 0.15      # centros a <=0,15*eixo maior sao concentricos
R_MIN_FRAC   = 0.08      # eixo maior minimo, fracao do menor lado do quadro
R_MAX_FRAC   = 0.95      # eixo maior maximo, fracao do menor lado do quadro
MIN_ACHATA   = 0.80      # b/a minimo aceito (tolera inclinacao da camera)
N_SETORES    = 36        # setores angulares de 10 graus
MIN_SETORES  = 0.90      # fracao minima de setores com pixel de apoio
BANDA        = 0.10      # banda em r_norm para contar apoio e residuo
MAX_RESID    = 0.02      # mediana de |r_norm - 1| aceita
ANEL_MM      = 16.0      # nominal externo do splint (EMENDA 1)


def _lstar(im):
    """L* exatamente como no motor congelado v0_congelado_2026-09-22/rodar.py.
    Copiado verbatim; nenhuma constante alterada."""
    q = im.astype(np.float64) / 255.
    def lin(c): return np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    R, G, B = [lin(q[:, :, i]) for i in range(3)]
    Y = R * .2126 + G * .7152 + B * .0722
    f = np.where(Y > 0.008856, np.cbrt(Y), 7.787 * Y + 16 / 116)
    return (116 * f - 16) * 2.55


def _bordas(cinza):
    """Canny com limiares por quantil do proprio gradiente da imagem — quantil,
    e nao valor absoluto, para nao depender do brilho de cada foto."""
    return canny(cinza / 255.0, sigma=SIGMA, low_threshold=Q_BAIXO,
                 high_threshold=Q_ALTO, use_quantiles=True)


def _ajusta_elipse(pts):
    """Ajuste algebrico direto de elipse (Halir & Flusser, 1998), vetorizado.
    Devolve (xc, yc, a, b, theta) ou None. Sem iteracao de otimizacao, sem
    semente: dado o mesmo conjunto de pontos, devolve sempre o mesmo resultado."""
    if len(pts) < 5:
        return None
    m = pts.mean(0)
    e = max(1e-9, float(np.abs(pts - m).max()))
    x = (pts[:, 0] - m[0]) / e
    y = (pts[:, 1] - m[1]) / e
    D1 = np.column_stack([x * x, x * y, y * y])
    D2 = np.column_stack([x, y, np.ones_like(x)])
    S1, S2, S3 = D1.T @ D1, D1.T @ D2, D2.T @ D2
    try:
        T = -np.linalg.solve(S3, S2.T)
    except np.linalg.LinAlgError:
        return None
    M = S1 + S2 @ T
    M = np.array([M[2] / 2.0, -M[1], M[0] / 2.0])
    try:
        val, vec = np.linalg.eig(M)
    except np.linalg.LinAlgError:
        return None
    cond = 4 * vec[0] * vec[2] - vec[1] ** 2
    k = np.nonzero(cond > 0)[0]
    if len(k) == 0:
        return None
    a1 = np.real(vec[:, k[0]])
    A, B, C = a1
    D, E, F = np.real(T @ a1)
    den = B * B - 4 * A * C
    if den >= -1e-12:          # B^2-4AC < 0 e a condicao de elipse
        return None
    xc = (2 * C * D - B * E) / den
    yc = (2 * A * E - B * D) / den
    # conica centrada: autovalores da forma quadratica dao as direcoes dos eixos
    F0 = F + (D * xc + E * yc) / 2.0
    W = np.array([[A, B / 2.0], [B / 2.0, C]])
    w, v = np.linalg.eigh(W)
    if np.any(np.abs(w) < 1e-15) or np.any(-F0 / w <= 0):
        return None
    semi = np.sqrt(-F0 / w)
    k = int(np.argmax(semi))
    ax1, ax2 = float(semi[k]), float(semi[1 - k])
    th = float(np.arctan2(v[1, k], v[0, k]))
    return (float(xc * e + m[0]), float(yc * e + m[1]),
            float(ax1 * e), float(ax2 * e), float(th))


def _norm(pts, par):
    """raio normalizado e angulo de cada ponto na elipse par=(xc,yc,a,b,theta)"""
    xc, yc, a, b, th = par
    X = (pts[:, 0] - xc) * np.cos(th) + (pts[:, 1] - yc) * np.sin(th)
    Y = -(pts[:, 0] - xc) * np.sin(th) + (pts[:, 1] - yc) * np.cos(th)
    return np.hypot(X / a, Y / b), np.arctan2(Y, X)


def _ordena(par):
    xc, yc, a, b, th = par
    return (xc, yc, b, a, th + np.pi / 2) if a < b else (xc, yc, a, b, th)


def detecta(caminho_ou_array):
    """Devolve dict com cx, cy (px da original), diam_px (eixo maior), b/a,
    setores apoiados, residuo e 'ok'. Se nao achar anel: {'ok': False, ...}."""
    if isinstance(caminho_ou_array, (str, bytes)):
        im = np.asarray(Image.open(caminho_ou_array).convert('RGB'))
    else:
        im = np.asarray(caminho_ou_array)[:, :, :3]
    H, W = im.shape[:2]
    menor = min(H, W)

    eo = _bordas(_lstar(im))
    ys, xs = np.nonzero(eo)
    if len(xs) < MIN_PTS_FIT:
        return {'ok': False, 'motivo': 'bordas insuficientes'}
    passo = max(1, int(np.ceil(len(xs) / MAX_PTS)))
    pts0 = np.column_stack([xs[::passo], ys[::passo]]).astype(float)

    # --- 1. curvas concentricas pelo histograma radial a partir do centro
    #        provisorio (mediana das bordas). Os picos sao as curvas candidatas:
    #        anel de 16 mm, parede de 10 mm e ferida de 6 mm.
    c0 = np.median(pts0, axis=0)
    r = np.hypot(pts0[:, 0] - c0[0], pts0[:, 1] - c0[1])
    rmin, rmax = R_MIN_FRAC * menor / 2, R_MAX_FRAC * menor / 2
    dentro = (r >= rmin) & (r <= rmax)
    if int(np.sum(dentro)) < MIN_PTS_FIT:
        return {'ok': False, 'motivo': 'bordas fora da faixa de raio'}
    hist, bordas_bin = np.histogram(r[dentro], bins=N_BINS, range=(rmin, rmax))
    centros = (bordas_bin[:-1] + bordas_bin[1:]) / 2
    alto = hist.max()
    picos = [i for i in range(N_BINS)
             if hist[i] >= PICO_FRAC * alto
             and hist[i] >= hist[max(0, i - 1)] and hist[i] >= hist[min(N_BINS - 1, i + 1)]]
    if not picos:
        return {'ok': False, 'motivo': 'sem pico radial'}

    # --- 2. para cada pico, elipse ajustada e aparada N_TRIM vezes
    cands = []
    for i in picos:
        rp = centros[i]
        sel = np.abs(r - rp) <= BANDA_H * rp
        if int(np.sum(sel)) < MIN_PTS_FIT:
            continue
        par = _ajusta_elipse(pts0[sel])
        for _ in range(N_TRIM):
            if par is None:
                break
            rn, _a = _norm(pts0, par)
            sel = np.abs(rn - 1.0) <= BANDA
            if int(np.sum(sel)) < MIN_PTS_FIT:
                break
            par = _ajusta_elipse(pts0[sel])
        if par is None or par[2] <= 0:
            continue
        if not (R_MIN_FRAC * menor <= 2 * par[2] <= R_MAX_FRAC * menor):
            continue
        rn, _a = _norm(pts0, par)
        cands.append((par, int(np.sum(np.abs(rn - 1.0) <= BANDA))))
    if not cands:
        return {'ok': False, 'motivo': 'nenhuma elipse ajustada'}

    # --- 3. entre as concentricas a mais apoiada, a de MAIOR eixo (anel externo)
    base = max(cands, key=lambda c: c[1])[0]
    grupo = [c for c in cands
             if np.hypot(c[0][0] - base[0], c[0][1] - base[1]) <= CONCENT * base[2]]
    par = max(grupo, key=lambda c: c[0][2])[0] if grupo else base

    xc, yc, a, b, th = par
    rn, ang = _norm(pts0, par)
    sel = np.abs(rn - 1.0) <= BANDA
    n_ap = int(np.sum(sel))
    if n_ap < N_SETORES:
        return {'ok': False, 'motivo': 'apoio insuficiente'}
    resid = float(np.median(np.abs(rn[sel] - 1.0)))
    setores = len(np.unique(((ang[sel] + np.pi) / (2 * np.pi) * N_SETORES)
                            .astype(int) % N_SETORES))
    frac_set = setores / N_SETORES
    achata = b / a

    ok = (achata >= MIN_ACHATA and frac_set >= MIN_SETORES and resid <= MAX_RESID)
    motivo = '' if ok else ';'.join(m for m, c in [
        ('achatamento', achata < MIN_ACHATA),
        ('setores', frac_set < MIN_SETORES),
        ('residuo', resid > MAX_RESID)] if c)
    return {'ok': bool(ok), 'cx': float(xc), 'cy': float(yc),
            'diam_px': float(2 * a), 'eixo_menor_px': float(2 * b),
            'theta': float(th), 'achatamento': float(achata),
            'setores_apoiados': int(setores), 'fracao_setores': float(frac_set),
            'residuo': resid, 'n_apoio': n_ap, 'n_candidatas': len(cands),
            'motivo': motivo}


def px_por_mm(res):
    """px/mm = diametro ajustado em px / 16 mm (EMENDA 1, item 2)."""
    return res['diam_px'] / ANEL_MM
