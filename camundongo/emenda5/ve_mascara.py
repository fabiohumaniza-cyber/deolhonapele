"""
ve_mascara.py — desenha o que o motor v0 pintou, por cima da imagem.

POR QUE EXISTE
Em 02/10/2026, as 20h59, depois de a rodada das 255 terminar, o Fabio pediu
para ver. O roda_camundongo.py grava numero, nao imagem: o JSON diz que a
area deu 28,99 mm2 e que o Dice contra o nulo deu zero, mas nao diz ONDE.

ESTA FERRAMENTA NAO MEDE E NAO ALTERA NADA. Ela IMPORTA o
roda_camundongo.py (8c1f6e4d...) e chama as funcoes dele — recorta(),
quadrado_central(), roda_motor(), mascara_nula() — exatamente como a etapa 3
chamou. O que aparece na tela e o que o motor fez, nao uma reconstrucao.

Nao escreve no MEDIDAS.txt, no CLASSIFICACAO.txt, no camundongo_v0.json nem
em nada do motor. So cria PNG numa pasta nova.

O QUE SE VE
  contorno VERMELHO   o que o motor pintou
  contorno CIANO      o comparador nulo: circulo de 6 mm no centro do anel,
                      desenhado sem olhar a imagem
  texto no topo       area, nota, Dice contra o nulo, e se o proprio motor
                      marcou "parece anel do splint"

Quando os dois contornos nao se encostam, o Dice e zero — e da para ver, numa
olhada, o que ele pegou no lugar da ferida.

Uso:
    python ve_mascara.py <pasta_tiffs> <pasta_saida> <pasta_png> [<lista.txt>]

Sem lista, desenha as imagens em que o Dice contra o nulo deu ZERO entre as
que tem escala propria — que sao as que interessam. Com lista (um nome por
linha), desenha so aquelas.
"""
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw

import roda_camundongo as R
import motor_v0_funcoes as M


def contorno(m):
    """borda de 1 px da mascara booleana, sem scipy: dilata por deslocamento."""
    d = np.zeros_like(m)
    d[1:, :] |= m[:-1, :]
    d[:-1, :] |= m[1:, :]
    d[:, 1:] |= m[:, :-1]
    d[:, :-1] |= m[:, 1:]
    return d & ~m


def pinta(rgb, m, nulo):
    im = Image.fromarray(rgb.astype(np.uint8)).convert('RGB')
    a = np.asarray(im).copy()
    if nulo is not None:
        c = contorno(nulo)
        a[c] = [0, 230, 230]
    if m is not None:
        c = contorno(m)
        a[c] = [255, 0, 0]
    return Image.fromarray(a)


def faixa(img, texto):
    L = img.width
    alt = 54
    fundo = Image.new('RGB', (L, img.height + alt), (16, 16, 16))
    fundo.paste(img, (0, alt))
    d = ImageDraw.Draw(fundo)
    for i, linha in enumerate(texto.split('\n')[:3]):
        d.text((8, 4 + i * 16), linha, fill=(235, 235, 235))
    return fundo


def main(pasta, saida, destino, lista=None):
    reg = json.load(open(os.path.join(saida, 'camundongo_v0.json'),
                        encoding='utf-8'))['imagens']
    med = json.load(open(os.path.join(saida, 'camundongo_v0.json'),
                         encoding='utf-8'))['_meta'].get('mediana_pxmm_banco')

    if lista:
        nomes = [l.strip() for l in open(lista, encoding='utf-8')
                 if l.strip() and not l.startswith('#')]
    else:
        nomes = sorted(n for n, v in reg.items()
                       if v.get('dice_motor_vs_nulo') == 0.0)
    faltam = [n for n in nomes if n not in reg]
    if faltam:
        sys.exit('PARADO: nao estao no JSON: %s' % ', '.join(faltam[:5]))

    os.makedirs(destino, exist_ok=True)
    print('%d imagem(ns) para desenhar' % len(nomes))

    for i, nome in enumerate(nomes, 1):
        v = reg[nome]
        im, _modo = R.abre_rgb8(os.path.join(pasta, nome))   # ndarray
        if v.get('px_mm'):
            cx, cy = v['centro_px']
            rgb, _ = R.recorta(im, cx, cy, v['px_mm'])
            nulo = R.mascara_nula(M.L)
        else:
            rgb = R.quadrado_central(im)
            nulo = None
        _, m, _ = R.roda_motor(rgb, R.DIAM_EF, v.get('criterio', 'prim'))

        t = ('%s   %s' % (nome, v.get('estrato', ''))
             + '\narea %.2f %s   nota %.3f   dice vs nulo %s'
             % (v.get('area') or 0, v.get('unidade', ''), v.get('nota') or 0,
                ('%.3f' % v['dice_motor_vs_nulo'])
                if v.get('dice_motor_vs_nulo') is not None else '—')
             + ('\nO PROPRIO MOTOR MARCOU: parece anel do splint'
                if v.get('parece_anel_do_splint') else
                '\nmarcas do operador: %s' % (', '.join(v.get('marcas') or []) or '—')))

        faixa(pinta(rgb, m, nulo), t).save(
            os.path.join(destino, os.path.splitext(nome)[0] + '.png'))
        print('\r%4d/%d' % (i, len(nomes)), end='', flush=True)
    print()
    print('PNG em: %s' % destino)
    print('vermelho = o motor · ciano = circulo nulo de 6 mm')


if __name__ == '__main__':
    if len(sys.argv) not in (4, 5):
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3],
         sys.argv[4] if len(sys.argv) == 5 else None)
