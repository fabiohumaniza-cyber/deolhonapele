"""
monta_declaracao_v6.py — monta a declaracao_camundongo_v6.html (rodada 4).

NAO RODA O MOTOR. Recorta cada uma das imagens com campo 'ok' como a rodada 3
recorta (roda_camundongo.recorta, 8c1f6e4d...), e corta uma VISTA quadrada de
3,2 x o raio do campo, centrada no campo, com o anel em volta. Embute a vista
como JPEG no HTML, junto com o circulo amarelo em coordenadas da vista.

A pagina e a declaracao_d3_exploratorio.html do porco, copiada e adaptada; o
original nao e tocado. O modelo esta em declaracao_camundongo_modelo_v6.html.

Uso:
    python monta_declaracao.py <pasta_tiffs> <pasta_saida> <arquivo_html_novo>
"""
import os, sys, json, io, base64, hashlib, time
import numpy as np
from PIL import Image

import roda_camundongo as R
import roda_rodada2 as R2

AQUI = os.path.dirname(os.path.abspath(__file__))


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def main(pasta, saida, destino):
    if os.path.exists(destino):
        sys.exit('PARADO: %s ja existe. Versao nova vai para nome novo.' % destino)
    v0 = json.load(open(os.path.join(saida, 'camundongo_v0.json'), encoding='utf-8'))['imagens']
    pc = os.path.join(saida, 'CAMPO.txt')
    campo = R2.le_campo(pc)
    nomes = sorted(n for n in campo if v0.get(n, {}).get('px_mm'))
    fig = []
    t0 = time.time()
    for i, nome in enumerate(nomes, 1):
        v = v0[nome]
        im, _ = R.abre_rgb8(os.path.join(pasta, nome))
        rgb, _ = R.recorta(im, v['centro_px'][0], v['centro_px'][1], v['px_mm'])
        cx, cy, rb, rc = campo[nome]
        meio = 1.6 * rc
        vx0, vy0 = int(round(cx - meio)), int(round(cy - meio))
        vl = int(round(2 * meio))
        big = np.pad(rgb, ((vl, vl), (vl, vl), (0, 0)), mode='edge')
        vista = big[vy0 + vl:vy0 + 2 * vl, vx0 + vl:vx0 + 2 * vl]
        b = io.BytesIO()
        Image.fromarray(vista).save(b, 'JPEG', quality=90)
        fig.append({'nome': os.path.splitext(nome)[0], 'arquivo': nome,
                    'img': 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode(),
                    'vx0': vx0, 'vy0': vy0, 'vl': vl,
                    'cx': round(cx - vx0, 2), 'cy': round(cy - vy0, 2), 'rc': round(rc, 2)})
        print('\r%3d/%d  %.0f s' % (i, len(nomes), time.time() - t0), end='', flush=True)
    print()
    meta = {'montado': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'n': len(fig),
            'sha': {'CAMPO.txt': sha(pc), 'camundongo_v0.json': sha(os.path.join(saida, 'camundongo_v0.json')),
                    'monta_declaracao_v6.py': sha(os.path.abspath(__file__)),
                    'declaracao_camundongo_modelo_v6.html': sha(os.path.join(AQUI, 'declaracao_camundongo_modelo_v6.html'))}}
    t = open(os.path.join(AQUI, 'declaracao_camundongo_modelo_v6.html'), encoding='utf-8').read()
    t = t.replace('__FIG__', json.dumps(fig)).replace('__META__', json.dumps(meta)).replace('__N__', str(len(fig)))
    open(destino, 'w', encoding='utf-8').write(t)
    print('ok %s  (%.1f MB, %d imagens)' % (destino, os.path.getsize(destino) / 1e6, len(fig)))
    print('sha256 %s' % sha(destino))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
