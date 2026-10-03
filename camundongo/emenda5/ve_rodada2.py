"""
ve_rodada2.py — desenha o que o motor pintou na RODADA 2 (coroa excluida).

NAO MEDE NADA NOVO. Importa roda_rodada2.py (420ff85b...) e chama
roda_motor_ar() com a mesma coroa. Antes de desenhar, CONFERE que a area de
cada mascara e a gravada em camundongo_r2.json; se diferir, PARA.

So imagens de classe n ou d por padrao: o Fabio vai tracar as v as cegas
(Adendo 19), entao nao pode ver a mascara do motor nelas.

O QUE SE VE
  VERDE        o que o motor pegou na rodada 2
  cinza        a coroa excluida (5 a 8 mm) — o "muro" da rodada 2
  AMARELO      o campo declarado pelo Fabio (CAMPO.txt) — o muro da rodada 3
  CIANO        o nulo de 6 mm

Uso:
    python ve_rodada2.py <pasta_tiffs> <pasta_saida>
Escreve: <pasta_saida>/mosaico_r2_buraco.jpg e mosaico_r2_fora.jpg
"""
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import binary_dilation

import roda_camundongo as R
import motor_v0_funcoes as M
import roda_rodada2 as R2

GRUPOS = {
    'buraco': ['Day 10_A8-3-R.tiff', 'Day 10_A8-5-R.tiff', 'Day 10_Y8-4-L.tiff',
               'Day 1_A8-1-R.tiff', 'Day 1_A8-3-L.tiff', 'Day 1_A8-3-R.tiff',
               'Day 1_A8-4-L.tiff', 'Day 2_A8-1-R.tiff', 'Day 2_A8-3-L.tiff',
               'Day 2_Y8-2-L.tiff', 'Day 4_A8-3-L.tiff', 'Day 4_Y8-1-L.tiff'],
    'fora': ['Day 10_A8-3-L.tiff', 'Day 10_A8-4-L.tiff', 'Day 11_Y8-2-L.tiff',
             'Day 13_A8-4-R.tiff', 'Day 14_A8-3-R.tiff', 'Day 3_Y8-1-L.tiff',
             'Day 3_Y8-2-R.tiff', 'Day 5_A8-4-L.tiff', 'Day 8_Y8-3-R.tiff'],
}
TITULO = {'buraco': 'RODADA 2 - motor DENTRO do buraco: as 12 imagens n/d',
          'fora': 'RODADA 2 - motor FORA do anel: 9 de 60 imagens n/d (sorteio 20261003)'}
T = 330


def desenha(rgb, m, campo):
    a = rgb.astype(np.float32).copy()
    a[R2.COROA] = a[R2.COROA] * 0.45 + 70
    a = a.astype(np.uint8)
    borda = binary_dilation(m, iterations=3) & ~m
    a[borda] = (0, 255, 0)
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    c = R2.C0; r = 3.0 * R2.PXMM
    d.ellipse([c - r, c - r, c + r, c + r], outline=(0, 230, 230), width=2)
    if campo:
        cx, cy, rb, rc = campo
        d.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], outline=(255, 220, 0), width=3)
    return im.resize((T, T))


def main(pasta, saida):
    r2 = json.load(open(os.path.join(saida, 'camundongo_r2.json'), encoding='utf-8'))['imagens']
    campo = R2.le_campo(os.path.join(saida, 'CAMPO.txt'))
    for g, nomes in GRUPOS.items():
        lin = (len(nomes) + 2) // 3
        out = Image.new('RGB', (3 * T, lin * (T + 18) + 30), (16, 16, 16))
        dd = ImageDraw.Draw(out)
        dd.text((8, 8), TITULO[g] + '   VERDE=motor  cinza=coroa excluida  AMARELO=seu campo  ciano=nulo',
                fill=(235, 235, 235))
        for i, nome in enumerate(nomes):
            v = r2[nome]
            im, _ = R.abre_rgb8(os.path.join(pasta, nome))
            rgb, _ = R.recorta(im, v['centro_px'][0], v['centro_px'][1], v['px_mm'])
            _, m, _ = R2.roda_motor_ar(rgb, R.DIAM_EF, 'prim', R2.COROA)
            area = float(m.sum() * (R.LADO_1380 / M.L) ** 2 / (R.S_1380 ** 2))
            if abs(area - v['area']) > 1e-6:
                sys.exit('PARADO: %s area %.6f, JSON %.6f' % (nome, area, v['area']))
            x = (i % 3) * T; y = 30 + (i // 3) * (T + 18)
            out.paste(desenha(rgb, m, campo.get(nome)), (x, y + 18))
            dd.text((x + 4, y + 3), '%s  %.1f mm2' % (os.path.splitext(nome)[0], area), fill=(235, 235, 235))
            print('\r%s %2d/%d' % (g, i + 1, len(nomes)), end='', flush=True)
        print()
        p = os.path.join(saida, 'mosaico_r2_%s.jpg' % g)
        out.save(p, quality=88)
        print('ok', p)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
