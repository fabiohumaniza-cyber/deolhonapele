"""
confere_declaracao.py — confere que cada correcao da declaracao cai NO LUGAR
CERTO da imagem que o motor vai rodar. Roda ANTES da rodada 4.

Motivo: no suino, coordenadas gravadas num canvas com deslocamento (ox) deram
trabalho para voltar a imagem. Aqui o caminho e um so e e conferido:

  1. refaz o recorte de 700 exatamente como a rodada 3 (roda_camundongo.recorta);
  2. recorta a MESMA vista (vx0, vy0, vl) gravada no JSON;
  3. compara com a foto que estava EMBUTIDA na pagina (pixel a pixel, tolerancia
     de JPEG). Se diferir, PARA: a vista nao e a mesma, e nada e convertido;
  4. desenha conta-gotas e artefato no quadro de 700 (ponto = vx0 + x, vy0 + y)
     e grava um PNG por imagem, lado a lado: a vista da pagina com as marcas e
     o quadro de 700 com as mesmas marcas, para o operador ver que bateu.

So le. Escreve PNG em <pasta_png>.

Uso:
    python confere_declaracao.py <pasta_tiffs> <pasta_saida> <declaracao_vN.html> <declaracao.json> <pasta_png>
"""
import os, sys, json, io, re, base64
import numpy as np
from PIL import Image, ImageDraw

import roda_camundongo as R

TOL_MEDIA = 4.0          # diferenca media por pixel aceita (JPEG q=90)


def fotos_da_pagina(html):
    t = open(html, encoding='utf-8').read()
    m = re.search(r'var FIG = (\[.*?\]);\nvar META', t, re.S)
    return {f['nome']: f for f in json.loads(m.group(1))}


def marca(img, e, ox, oy):
    d = ImageDraw.Draw(img, 'RGBA')
    for k in e.get('corr', []):
        r = k['r']; cor = tuple(k['cor'])
        pts = [(x + ox, y + oy) for x, y in k['pts']]
        if len(pts) > 1:
            d.line(pts, fill=cor + (255,), width=max(1, int(round(2 * r))), joint='curve')
        for x, y in pts:
            d.ellipse([x - r, y - r, x + r, y + r], fill=cor + (255,))
    cores = {'reflexo': (0, 230, 255), 'filme': (255, 0, 255), 'sangue': (255, 40, 40),
             'ponto': (255, 230, 0), 'outra_lesao': (40, 90, 255)}
    for t in e.get('art', []):
        x, y, r = t['x'] + ox, t['y'] + oy, t['r']
        d.ellipse([x - r, y - r, x + r, y + r], fill=cores.get(t['motivo'], (255, 255, 255)) + (130,))
    return img


def main(pasta, saida, html, pj, destino):
    fig = fotos_da_pagina(html)
    dec = json.load(open(pj, encoding='utf-8'))['E']
    v0 = json.load(open(os.path.join(saida, 'camundongo_v0.json'), encoding='utf-8'))['imagens']
    os.makedirs(destino, exist_ok=True)
    com = {n: e for n, e in dec.items() if e.get('corr') or e.get('art')}
    print('%d imagens na declaracao | %d com correcao' % (len(dec), len(com)))
    ruins = []
    for nome, e in sorted(com.items()):
        f = fig[nome]
        if (f['vx0'], f['vy0'], f['vl']) != (e['vx0'], e['vy0'], e['vl']):
            sys.exit('PARADO: %s — vista do JSON difere da vista da pagina' % nome)
        v = v0[f['arquivo']]
        im, _ = R.abre_rgb8(os.path.join(pasta, f['arquivo']))
        rgb, _ = R.recorta(im, v['centro_px'][0], v['centro_px'][1], v['px_mm'])
        vl, vx0, vy0 = e['vl'], e['vx0'], e['vy0']
        big = np.pad(rgb, ((vl, vl), (vl, vl), (0, 0)), mode='edge')
        refeita = big[vy0 + vl:vy0 + 2 * vl, vx0 + vl:vx0 + 2 * vl].astype(np.float32)
        pagina = np.asarray(Image.open(io.BytesIO(base64.b64decode(f['img'].split(',', 1)[1]))).convert('RGB')).astype(np.float32)
        dif = float(np.abs(refeita - pagina).mean())
        if dif > TOL_MEDIA:
            ruins.append((nome, dif))
            continue
        a = marca(Image.fromarray(pagina.astype(np.uint8)), e, 0, 0)
        b = marca(Image.fromarray(rgb), e, vx0, vy0).crop((vx0, vy0, vx0 + vl, vy0 + vl))
        lado = Image.new('RGB', (2 * vl + 10, vl + 22), (16, 16, 16))
        lado.paste(a, (0, 22)); lado.paste(b, (vl + 10, 22))
        ImageDraw.Draw(lado).text((4, 4), '%s   esquerda: pagina   direita: quadro do motor   dif %.2f' % (nome, dif),
                                  fill=(235, 235, 235))
        lado.save(os.path.join(destino, nome + '_confere.png'))
        print('ok  %-22s dif %.2f' % (nome, dif))
    if ruins:
        sys.exit('PARADO: vista diferente em %d imagem(ns): %s' % (len(ruins), ruins[:5]))
    print('TODAS as correcoes cairam no mesmo lugar. PNG em %s' % destino)


if __name__ == '__main__':
    if len(sys.argv) != 6:
        sys.exit(__doc__)
    main(*sys.argv[1:])
