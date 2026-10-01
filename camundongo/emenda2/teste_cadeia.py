"""
teste_cadeia.py — prova da CADEIA inteira em imagem sintetica:
detector -> px/mm -> recorte de 24 mm -> 1380 px -> motor v0 congelado.

Verifica a identidade algebrica da escala (a mesma da reauditoria d3):
o motor congelado calcula resp = pi*(diam/2 * 30 * L/1380)^2, com 30 px/mm
FIXO no quadro de 1380. Aqui o quadro de 1380 px cobre 24 mm, logo
s = 1380/24 = 57,5 px/mm, e o diametro a declarar ao motor e

    diam_ef = DIAM_MM * s / 30 = 6 * 57,5/30 = 11,5 mm

Nenhuma imagem do banco e aberta. Semente 20260928.
"""
import sys, numpy as np
sys.path.insert(0, '/home/claude/cam')
from PIL import Image
from detecta_anel_camundongo import detecta, px_por_mm
import motor_v0_funcoes as M

RNG = np.random.default_rng(20260928)
RECORTE_MM = 24.0
LADO_1380 = 1380
DIAM_MM = 6.0
S_1380 = LADO_1380 / RECORTE_MM              # 57,5 px/mm
DIAM_EF = DIAM_MM * S_1380 / 30.0            # 11,5 mm
print('s no quadro de 1380 = %.4f px/mm  |  diam_ef = %.4f mm' % (S_1380, DIAM_EF))
assert abs(S_1380 - 57.5) < 1e-9 and abs(DIAM_EF - 11.5) < 1e-9


def cena(H, W, cx, cy, a, b, th, pxmm, fundo=185., cor_anel=40., cor_fer=45.):
    """splint 10->16 mm + ferida de 6 mm, com escala pxmm conhecida"""
    yy, xx = np.mgrid[0:H, 0:W]
    X = (xx - cx) * np.cos(th) + (yy - cy) * np.sin(th)
    Y = -(xx - cx) * np.sin(th) + (yy - cy) * np.cos(th)
    r = np.hypot(X / a, Y / b)
    im = np.full((H, W, 3), fundo)
    im[(r >= 10 / 16) & (r <= 1.0)] = cor_anel
    im[np.hypot(xx - cx, yy - cy) <= (DIAM_MM / 2) * pxmm] = cor_fer
    return np.clip(im + RNG.normal(0, 4, im.shape), 0, 255).astype(np.uint8)


def recorta(im, res):
    """recorte de 24 mm -> 1380 px -> 700 px, espelhando prepara_grupo1.py do porco"""
    pxmm = px_por_mm(res)
    lado = int(round(RECORTE_MM * pxmm))
    x0 = int(round(res['cx'] - lado / 2)); y0 = int(round(res['cy'] - lado / 2))
    cai_fora = (x0 < 0 or y0 < 0 or x0 + lado > im.shape[1] or y0 + lado > im.shape[0])
    pil = Image.fromarray(im).crop((x0, y0, x0 + lado, y0 + lado))
    q1380 = pil.resize((LADO_1380, LADO_1380), Image.LANCZOS)
    q700 = q1380.resize((M.L, M.L), Image.LANCZOS)
    return np.asarray(q700.convert('RGB')), pxmm, cai_fora


print('\n%-34s %8s %9s %9s %8s %7s' % ('cena', 'px/mm', 'px/mm med', 'erro %', 'area mm2', 'nota'))
ALVO = np.pi * (DIAM_MM / 2) ** 2
linhas = []
for nome, H, W, pxmm, ba, thd in [
        ('A frontal, 40 px/mm', 900, 900, 40.0, 1.00, 0.),
        ('B frontal, 25 px/mm', 700, 700, 25.0, 1.00, 0.),
        ('C inclinada b/a 0,88', 900, 900, 38.0, 0.88, 20.),
        ('D alta resolucao 70 px/mm', 1600, 1600, 70.0, 1.00, 0.),
        ('E quadro retangular', 900, 1400, 45.0, 1.00, 10.)]:
    a = 8.0 * pxmm                      # semieixo maior = 16 mm / 2
    b = a * ba
    th = np.deg2rad(thd)
    im = cena(H, W, W / 2, H / 2, a, b, th, pxmm)
    res = detecta(im)
    if not res['ok']:
        print('%-34s  RECUSOU  [%s]' % (nome, res['motivo'])); continue
    rec, pxmm_med, fora = recorta(im, res)
    cache, mel = {}, (-1, None, None)
    if True:
        for gama, can, g, dsl, al, (lo, hi) in M.grade:
            ka = (gama, can)
            if ka not in cache: cache[ka] = M.canais[can](M.clareia(rec, gama))
            kt = (gama, can, g, dsl, al)
            if kt not in cache: cache[kt] = M.mapa_t(cache[ka], g, dsl, al, 4, None)
            r_ = M.anel(cache[kt], lo, hi, 3, None, DIAM_EF)
            if r_ is None: continue
            if r_[1] > mel[0]: mel = (r_[1], r_[0], (gama, can, g, dsl, al, lo, hi))
    nota, m, aj = mel
    if m is None:
        print('%-34s  MOTOR NAO DEVOLVEU MEDIDA' % nome); continue
    area = m.sum() * (LADO_1380 / M.L) ** 2 / (S_1380 ** 2)
    err = 100 * (pxmm_med - pxmm) / pxmm
    print('%-34s %8.2f %9.2f %+9.3f %8.2f %7.3f' % (nome, pxmm, pxmm_med, err, area, nota))
    linhas.append((nome, err, area, nota))

print('\nalvo da ferida de 6 mm: %.2f mm2' % ALVO)
if linhas:
    e = np.array([abs(l[1]) for l in linhas]); a_ = np.array([l[2] for l in linhas])
    print('erro de escala: mediana %.3f %% | maximo %.3f %%' % (np.median(e), e.max()))
    print('area recuperada: mediana %.2f mm2 | de %.2f a %.2f (desvio do alvo: %+.1f %%)'
          % (np.median(a_), a_.min(), a_.max(), 100 * (np.median(a_) - ALVO) / ALVO))
