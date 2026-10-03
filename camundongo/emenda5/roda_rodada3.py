"""
roda_rodada3.py — RODADA 3: o motor v0 congelado vendo SO o campo declarado
pelo operador (CAMPO.txt, Adendo 15).

NENHUMA LINHA DO MOTOR MUDA. Importa roda_camundongo.py (8c1f6e4d...),
motor_v0_funcoes.py (16028493...) e roda_rodada2.py (420ff85b...).

COMO O CAMPO ENTRA — e por que nao basta `ar = tudo fora do circulo`
mapa_t() estima a PELE pela mediana da moldura de 8 % do quadro, menos o `ar`.
No quadro de 700 o campo tem raio <= 122 px; a moldura inteira fica fora dele.
Com `ar` = fora do circulo, a moldura fica VAZIA, a mediana vira NaN e o motor
nao mede nada. Isto e testado no ensaio sintetico (modo A) e fica registrado.

O desenho usado (modo B), sem mudar o motor:
  1. recorte QUADRADO circunscrito ao campo amarelo, na MESMA escala do quadro
     de 700 (29,167 px/mm) — sem reamostrar, para que o termo de tamanho do
     motor continue em milimetro certo;
  2. ar = os pixels desse quadrado que ficam FORA do circulo (os 4 cantos).
A moldura de 8 % do quadrado cai, no meio de cada lado, DENTRO do campo, junto
da borda: e a pele em volta da ferida que o motor usa como referencia.

So as 201 com campo 'ok'. As 3 NAO_DA e as 51 SEM_ANEL nao rodam.

Uso:
    python roda_rodada3.py sintetico
    python roda_rodada3.py rodar <pasta_tiffs> <pasta_saida>
"""
import os, sys, json, time, hashlib, warnings
import numpy as np

import roda_camundongo as R
import motor_v0_funcoes as M
import roda_rodada2 as R2

L = M.L
PXMM = R2.PXMM


def recorte_campo(rgb700, cx, cy, rc):
    """quadrado circunscrito ao circulo (cx, cy, rc), na escala do quadro de 700.
    Devolve (sub, ar, (x0, y0)). Fora do quadro de 700 -> replica a borda."""
    lado = int(np.ceil(2 * rc)) + 1
    x0 = int(round(cx - lado / 2.0)); y0 = int(round(cy - lado / 2.0))
    pad = max(0, -x0, -y0, x0 + lado - L, y0 + lado - L)
    im = np.pad(rgb700, ((pad, pad), (pad, pad), (0, 0)), mode='edge') if pad else rgb700
    sub = im[y0 + pad:y0 + pad + lado, x0 + pad:x0 + pad + lado]
    yy, xx = np.mgrid[0:lado, 0:lado]
    ccx, ccy = cx - x0, cy - y0
    ar = np.hypot(xx - ccx, yy - ccy) > rc
    return np.ascontiguousarray(sub), ar, (x0, y0)


def volta_ao_700(m, x0, y0):
    out = np.zeros((L, L), bool)
    h, w = m.shape
    xs, ys = max(0, x0), max(0, y0)
    xe, ye = min(L, x0 + w), min(L, y0 + h)
    out[ys:ye, xs:xe] = m[ys - y0:ye - y0, xs - x0:xe - x0]
    return out


def roda_campo(rgb700, campo):
    cx, cy, rb, rc = campo
    sub, ar, (x0, y0) = recorte_campo(rgb700, cx, cy, rc)
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        nota, m, aj = R2.roda_motor_ar(sub, R.DIAM_EF, 'prim', ar)
    if m is None:
        return None, None, None
    return nota, volta_ao_700(m, x0, y0), aj


# ------------------------------------------------------------ ensaio sintetico
def ensaio(n=30):
    rng = np.random.default_rng(20260928)
    res = {'A': {'ferida': 0, 'None': 0, 'outro': 0}, 'B': {'ferida': 0, 'None': 0, 'outro': 0}}
    t0 = time.time()
    for i in range(n):
        rgb, fer = R2.cena(rng)
        # o operador encosta o verde no laranja visivel; campo 0,3 mm para dentro
        rb = 4.3 * PXMM; rc = rb - 0.3 * PXMM
        campo = (R2.C0, R2.C0, rb, rc)
        # modo A: ar = tudo fora do circulo, no quadro de 700
        yy, xx = np.mgrid[0:L, 0:L]
        arA = np.hypot(xx - R2.C0, yy - R2.C0) > rc
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            _, mA, _ = R2.roda_motor_ar(rgb, R.DIAM_EF, 'prim', arA)
        # modo B: recorte circunscrito
        _, mB, _ = roda_campo(rgb, campo)
        for k, m in (('A', mA), ('B', mB)):
            if m is None:
                res[k]['None'] += 1
            elif M.dice(m, fer) >= 0.5:
                res[k]['ferida'] += 1
            else:
                res[k]['outro'] += 1
        print('\r%2d/%d  %.0f s  %s' % (i + 1, n, time.time() - t0, json.dumps(res)), end='', flush=True)
    print()
    print('RESUMO', json.dumps(res))
    return res


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def rodar(pasta, saida):
    v0 = json.load(open(os.path.join(saida, 'camundongo_v0.json'), encoding='utf-8'))['imagens']
    campo = R2.le_campo(os.path.join(saida, 'CAMPO.txt'))
    nomes = sorted(n for n in v0 if v0[n].get('px_mm') and n in campo)
    res = {}
    t0 = time.time()
    for i, nome in enumerate(nomes, 1):
        v = v0[nome]
        im, _ = R.abre_rgb8(os.path.join(pasta, nome))
        rgb, _ = R.recorta(im, v['centro_px'][0], v['centro_px'][1], v['px_mm'])
        nota, m, aj = roda_campo(rgb, campo[nome])
        d = {'arquivo': nome, 'unidade': 'mm2', 'campo': list(campo[nome])}
        if m is None:
            d.update({'obtida': False, 'area': None})
        else:
            area = float(m.sum() * (R.LADO_1380 / L) ** 2 / (R.S_1380 ** 2))
            cx, cy, rb, rc = campo[nome]
            area_campo = np.pi * rc * rc * (R.LADO_1380 / L) ** 2 / (R.S_1380 ** 2)
            d.update({'obtida': True, 'area': area, 'nota': float(nota), 'ajuste': list(aj),
                      'area_campo_mm2': float(area_campo),
                      'frac_do_campo': float(area / area_campo),
                      'dice_motor_vs_nulo': float(M.dice(m, R.mascara_nula(L)))})
            d.update({k: (float(x) if not isinstance(x, str) else x)
                      for k, x in R2.zonas(m, campo[nome]).items()})
        res[nome] = d
        dt = time.time() - t0
        print('\r%4d/%d  %4.0f min restantes' % (i, len(nomes), dt / i * (len(nomes) - i) / 60),
              end='', flush=True)
    print()
    meta = {'rodada': 3, 'campo': 'CAMPO.txt, recorte circunscrito + ar = cantos',
            'quando': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'sha_codigo': {'roda_rodada3.py': sha(__file__), 'roda_rodada2.py': sha(R2.__file__),
                           'roda_camundongo.py': sha(R.__file__), 'motor_v0_funcoes.py': sha(M.__file__)},
            'sha_entrada': {'CAMPO.txt': sha(os.path.join(saida, 'CAMPO.txt')),
                            'camundongo_v0.json': sha(os.path.join(saida, 'camundongo_v0.json'))}}
    json.dump({'_meta': meta, 'imagens': res},
              open(os.path.join(saida, 'camundongo_r3.json'), 'w', encoding='utf-8'),
              indent=1, ensure_ascii=False)
    print('gravado: camundongo_r3.json  (%d imagens)' % len(res))


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'sintetico':
        ensaio()
    elif len(sys.argv) == 4 and sys.argv[1] == 'rodar':
        rodar(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
