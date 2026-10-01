"""
teste_sintetico.py — prova do detector do anel em imagens DESENHADAS POR CODIGO.
Nenhuma imagem do banco Dryad e aberta aqui. Semente fixa 20260928.

A geometria sintetica vem dos NOMINAIS DO README (EMENDA 1), nao de observacao:
splint de silicone com parede de 10 mm (interno) a 16 mm (externo), coverslip de
16 mm por cima, ferida de punch de 6 mm no centro.
"""
import numpy as np, json, sys
sys.path.insert(0, '/home/claude/cam')
from detecta_anel_camundongo import detecta

RNG = np.random.default_rng(20260928)
H = W = 900
INT_EXT = 10.0 / 16.0          # razao parede interna / externa, do README
PUNCH   = 6.0 / 16.0           # razao ferida / anel externo, do README


def base(fundo):
    return np.full((H, W, 3), float(fundo))


def splint(im, cx, cy, a, b, theta=0.0, cor=40.0, cor_int=None):
    """parede do splint: anel cheio de r_norm INT_EXT ate 1,0 (geometria do README)"""
    yy, xx = np.mgrid[0:H, 0:W]
    X = (xx - cx) * np.cos(theta) + (yy - cy) * np.sin(theta)
    Y = -(xx - cx) * np.sin(theta) + (yy - cy) * np.cos(theta)
    r = np.hypot(X / a, Y / b)
    im[(r >= INT_EXT) & (r <= 1.0)] = cor
    if cor_int is not None:
        im[r < INT_EXT] = cor_int
    return im


def disco(im, cx, cy, r, cor):
    yy, xx = np.mgrid[0:H, 0:W]
    im[np.hypot(xx - cx, yy - cy) <= r] = cor
    return im


def ruido(im, s):
    return np.clip(im + RNG.normal(0, s, im.shape), 0, 255)


CASOS = []
A = 300.0                      # semieixo maior padrao -> diametro 600 px

im = splint(base(185.), 450, 450, A, A)
CASOS.append(('1 splint frontal', ruido(im, 4), 600.0, True))

im = splint(base(185.), 450, 450, A, A * 0.85, np.deg2rad(25))
CASOS.append(('2 inclinado b/a 0,85', ruido(im, 4), 600.0, True))

im = splint(base(55.), 450, 450, 290., 290., cor=130.)
CASOS.append(('3 pelo escuro + ruido', ruido(im, 12), 580.0, True))

im = splint(base(185.), 450, 450, A, A, cor_int=120.)   # borda interna marcada
CASOS.append(('4 borda interna 10 mm', ruido(im, 4), 600.0, True))

im = splint(base(185.), 450, 450, A, A)
im = disco(im, 560, 330, 70, 252.)                      # reflexo do Tegaderm
CASOS.append(('5 reflexo especular', ruido(im, 4), 600.0, True))

im = splint(base(185.), 450, 450, A, A)                 # setor de 60 graus coberto
yy, xx = np.mgrid[0:H, 0:W]
ang = np.arctan2(yy - 450, xx - 450)
im[(np.abs(ang) < np.deg2rad(30)) & (np.hypot(xx - 450, yy - 450) > 0.9 * A)] = 185.
CASOS.append(('6 ocluido 60 graus', ruido(im, 4), 600.0, True))

im = splint(base(185.), 300, 560, 250., 250.)
CASOS.append(('7 descentralizado', ruido(im, 4), 500.0, True))

im = splint(base(185.), 450, 450, A, A)
im = disco(im, 450, 450, PUNCH * A, 45.)                # ferida de 6 mm
CASOS.append(('8 com ferida de 6 mm', ruido(im, 5), 600.0, True))

im = splint(base(185.), 450, 450, A, A * 0.70, np.deg2rad(15))
CASOS.append(('9 b/a 0,70 (reprova)', ruido(im, 4), 600.0, False))

CASOS.append(('10 sem anel (reprova)', ruido(base(150.), 20), None, False))

im = splint(base(185.), 450, 450, A, A)                 # so metade do anel visivel
im[:, :450] = 185.
CASOS.append(('11 metade ausente (reprova)', ruido(im, 4), 600.0, False))


# --- casos adversos acrescentados antes do congelamento ---
def pelo(im, s_=14, escala=3):
    """textura direcional, analoga a pelo raspado do dorso"""
    t = RNG.normal(0, s_, (H // escala, W // escala))
    t = np.repeat(np.repeat(t, escala, 0), escala, 1)[:H, :W]
    return np.clip(im + t[:, :, None], 0, 255)

im = pelo(splint(base(120.), 450, 450, A, A, cor=55.))
CASOS.append(('12 textura de pelo', ruido(im, 5), 600.0, True))

im = splint(base(185.), 250, 250, 180., 180.)            # anel pequeno, canto
CASOS.append(('13 anel pequeno no canto', ruido(im, 4), 360.0, True))

im = splint(base(185.), 450, 450, A, A)                  # halo claro do coverslip
yy2, xx2 = np.mgrid[0:H, 0:W]
rr = np.hypot(xx2 - 450, yy2 - 450)
im[(rr > A) & (rr < A * 1.06)] = 240.
CASOS.append(('14 halo do coverslip', ruido(im, 4), 600.0, True))

from scipy import ndimage as _ndi
im = splint(base(185.), 450, 450, A, A)
im = _ndi.gaussian_filter(im, (3, 3, 0))                 # foco ruim
CASOS.append(('15 desfocado', ruido(im, 4), 600.0, True))

im = splint(base(185.), 760, 450, A, A)                  # anel cortado pela moldura
CASOS.append(('16 cortado pela moldura', ruido(im, 4), 600.0, False))

print('%-28s %8s %9s %8s %7s %7s %8s  %s' % (
    'caso', 'esperado', 'medido', 'erro %', 'b/a', 'setor', 'residuo', 'veredito'))
linhas, erros, acertos = [], [], 0
for nome, im, esp, deve_ok in CASOS:
    r = detecta(np.clip(im, 0, 255).astype(np.uint8))
    bateu = (r['ok'] == deve_ok); acertos += bateu
    ba = '%.3f' % r['achatamento']   if 'achatamento'   in r else '-'
    fs = '%.2f' % r['fracao_setores'] if 'fracao_setores' in r else '-'
    rs = '%.4f' % r['residuo']        if 'residuo'       in r else '-'
    if r['ok']:
        err = 100 * (r['diam_px'] - esp) / esp if esp else float('nan')
        if esp: erros.append(abs(err))
        print('%-28s %8s %9.1f %+8.2f %7s %7s %8s  %s' % (
            nome, ('%.1f' % esp) if esp else '-', r['diam_px'], err, ba, fs, rs,
            'OK' if bateu else 'DIVERGE'))
    else:
        print('%-28s %8s %9s %8s %7s %7s %8s  %s  [%s]' % (
            nome, ('%.1f' % esp) if esp else '-', 'recusou', '-', ba, fs, rs,
            'OK' if bateu else 'DIVERGE', r.get('motivo', '')))
    linhas.append({'caso': nome, 'esperado_px': esp, 'deve_aceitar': deve_ok,
                   'aceitou': r['ok'], 'resultado': r})
print()
print('vereditos corretos: %d de %d' % (acertos, len(CASOS)))
if erros:
    print('erro absoluto de diametro: mediana %.3f %% | maximo %.3f %%' % (
        float(np.median(erros)), float(np.max(erros))))
json.dump(linhas, open('/home/claude/cam/teste_sintetico_resultado.json', 'w'), indent=1)
