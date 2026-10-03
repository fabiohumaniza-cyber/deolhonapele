"""
ve_rodada3c.py — igual ao ve_rodada3b.py (f5bf8fe4...), mas desenha as `v`
(limpas primeiro, depois com plastico; Adendo 33 registra que o Fabio as ve), em paginas de 12, em ordem de dia. Desenha o que o motor pintou na RODADA 3 (campo declarado).

NAO MEDE NADA NOVO. Importa roda_rodada3.py (72cfb5cc...) e chama roda_campo()
com o mesmo CAMPO.txt. Confere a area de cada mascara contra camundongo_r3.json;
se diferir, PARA.

Imagens de classe v. O Fabio deixou de ser tracador cego das v (Adendo 33). Doze,
sorteadas com semente 20261003, uma por dia quando havia, em ordem de dia.

  VERDE    o que o motor pegou     AMARELO  o campo do Fabio     CIANO  nulo 6 mm

Uso:
    python ve_rodada3.py <pasta_tiffs> <pasta_saida>
Escreve: <pasta_saida>/mosaico_r3_v_limpas_01..06.jpg e mosaico_r3_v_plastico_01..06.jpg
"""
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import binary_dilation

import roda_camundongo as R
import motor_v0_funcoes as M
import roda_rodada2 as R2
import roda_rodada3 as R3

NOMES_12 = ['Day 1_A8-3-L.tiff', 'Day 2_Y8-2-L.tiff', 'Day 3_A8-1-L.tiff', 'Day 3_Y8-1-R.tiff',
         'Day 5_A8-3-L.tiff', 'Day 5_A8-1-R.tiff', 'Day 7_A8-3-L.tiff', 'Day 9_A8-3-R.tiff',
         'Day 11_Y8-2-L.tiff', 'Day 13_Y8-2-R.tiff', 'Day 14_Y8-2-L.tiff', 'Day 15_A8-3-L.tiff']
T = 330


def dia(n):
    return int(n.split('_')[0][4:])


def todas_nd(saida, r3):
    cl = {}
    for l in open(os.path.join(saida, 'CLASSIFICACAO.txt'), encoding='utf-8'):
        if l.startswith('#') or not l.strip():
            continue
        x = l.rstrip('\n').split('\t'); cl[x[0]] = (x[1], x[2] if len(x) > 2 else '')
    lim = sorted((n for n in r3 if cl.get(n, ('', ''))[0] == 'v' and cl[n][1] != 'S'), key=lambda n: (dia(n), n))
    pla = sorted((n for n in r3 if cl.get(n, ('', ''))[0] == 'v' and cl[n][1] == 'S'), key=lambda n: (dia(n), n))
    return lim, pla


def main(pasta, saida):
    r3 = json.load(open(os.path.join(saida, 'camundongo_r3.json'), encoding='utf-8'))['imagens']
    for rot, todos in zip(('limpas', 'plastico'), todas_nd(saida, r3)):
        for pg in range(0, len(todos), 12):
            pagina(pasta, saida, r3, todos[pg:pg + 12], pg // 12 + 1, (len(todos) + 11) // 12, rot)


def pagina(pasta, saida, r3, NOMES, k, tot, rot):
    v0 = json.load(open(os.path.join(saida, 'camundongo_v0.json'), encoding='utf-8'))['imagens']
    campo = R2.le_campo(os.path.join(saida, 'CAMPO.txt'))
    lin = (len(NOMES) + 2) // 3
    out = Image.new('RGB', (3 * T, lin * (T + 18) + 30), (16, 16, 16))
    dd = ImageDraw.Draw(out)
    dd.text((8, 8), 'RODADA 3 - imagens v %s, em ordem de dia, pagina %d de %d' % (rot.upper(), k, tot) + '   VERDE=motor  AMARELO=seu campo  ciano=nulo',
            fill=(235, 235, 235))
    for i, nome in enumerate(NOMES):
        v = v0[nome]
        im, _ = R.abre_rgb8(os.path.join(pasta, nome))
        rgb, _ = R.recorta(im, v['centro_px'][0], v['centro_px'][1], v['px_mm'])
        _, m, _ = R3.roda_campo(rgb, campo[nome])
        area = float(m.sum() * (R.LADO_1380 / M.L) ** 2 / (R.S_1380 ** 2))
        if abs(area - r3[nome]['area']) > 1e-6:
            sys.exit('PARADO: %s area %.6f, JSON %.6f' % (nome, area, r3[nome]['area']))
        a = rgb.copy()
        a[binary_dilation(m, iterations=3) & ~m] = (0, 255, 0)
        p = Image.fromarray(a); d = ImageDraw.Draw(p)
        cx, cy, rb, rc = campo[nome]
        d.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], outline=(255, 220, 0), width=3)
        c = R2.C0; r = 3.0 * R2.PXMM
        d.ellipse([c - r, c - r, c + r, c + r], outline=(0, 230, 230), width=2)
        x = (i % 3) * T; y = 30 + (i // 3) * (T + 18)
        out.paste(p.resize((T, T)), (x, y + 18))
        dd.text((x + 4, y + 3), '%s  %.1f mm2' % (os.path.splitext(nome)[0], area), fill=(235, 235, 235))
        print('\r%2d/%d' % (i + 1, len(NOMES)), end='', flush=True)
    print()
    p = os.path.join(saida, 'mosaico_r3_v_%s_%02d.jpg' % (rot, k))
    out.save(p, quality=88)
    print('ok', p)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
