"""
prepara_rede.py — monta os dados de treino da rede (Adendo 52).

Entradas (todas publicadas, so leitura):
  painel   tracador_camundongo_v2_emilio.html (008f863d...): as 201 vistas, as MESMAS que o tracador viu
  ordem    dados/_ORDEM_v2_emilio.json (e44ee2e7...): id -> nome, vx0, vy0, vl
  tracado  dados/tracado_camundongo_v2_emilio_2026-10-04.json (afcbf928...): o rotulo
  campo    dados/CAMPO.txt (91160713...): circulo r_borda = interior do anel (classe Ring_inner)

Saida: rede_dados.npz com
  X  (201, 352, 352, 3) uint8   a vista redimensionada para 352 (tamanho dos recortes do Carrion et al.)
  Y  (201, 352, 352)    uint8   0 fundo, 1 interior do anel, 2 ferida (rotulo do Emilio)
  nome, ferida, vx0, vy0, vl, estado_emilio

Como no trabalho original, a ferida rotulada e o tracado inteiro, inclusive o
imaginado (TRACADA, PARCIAL e IMAGINADA). FECHADA = sem ferida.

Uso: python prepara_rede.py <painel.html> <_ORDEM.json> <tracado.json> <CAMPO.txt> <saida.npz>
"""
import sys, json, re, base64, io, hashlib
import numpy as np
from PIL import Image, ImageDraw

LADO = 352


def le_campo(p):
    c = {}
    for l in open(p, encoding='utf-8'):
        if l.startswith('#') or not l.strip():
            continue
        x = l.rstrip('\n\r').split('\t')
        n = x[0][:-5] if x[0].endswith('.tiff') else x[0]
        if x[8] != 'ok':
            c.pop(n, None); continue
        c[n] = {'cx': float(x[1]), 'cy': float(x[2]), 'r': float(x[3]), 'estado': x[8]}   # vale a ultima linha
    return c


def ilhas(pts):
    out, cur = [], []
    for p in pts:
        if p.get('novo') and cur:
            out.append(cur); cur = []
        cur.append(p)
    if cur:
        out.append(cur)
    return [i for i in out if len(i) >= 3]


def main(phtml, pord, ptr, pcampo, psaida):
    t = open(phtml, encoding='utf-8').read()
    FIG = {f['id']: f for f in json.loads(re.search(r'var FIG = (\[.*?\]);', t, re.S).group(1))}
    O = json.load(open(pord, encoding='utf-8'))['ordem']
    E = json.load(open(ptr, encoding='utf-8'))['E']
    C = le_campo(pcampo)
    X, Y, meta = [], [], {k: [] for k in ('nome', 'ferida', 'vx0', 'vy0', 'vl', 'estado_emilio')}
    for o in sorted(O, key=lambda o: o['nome']):
        f = FIG[o['id']]; b = base64.b64decode(f['img'].split(',', 1)[1])
        if hashlib.sha256(b).hexdigest() != o['sha256_imagem']:
            sys.exit('PARADO: sha da vista %s' % o['id'])
        im = Image.open(io.BytesIO(b)).convert('RGB').resize((LADO, LADO), Image.BILINEAR)
        k = LADO / o['vl']
        lab = Image.new('L', (LADO, LADO), 0); d = ImageDraw.Draw(lab)
        c = C[o['nome']]
        cx, cy, r = (c['cx'] - o['vx0']) * k, (c['cy'] - o['vy0']) * k, c['r'] * k
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=1)
        e = E[o['id']]
        if e['estado'] != 'FECHADA':
            for il in ilhas(e['t']):
                d.polygon([(p['x'] * LADO, p['y'] * LADO) for p in il], fill=2)
        X.append(np.asarray(im, np.uint8)); Y.append(np.asarray(lab, np.uint8))
        meta['nome'].append(o['nome']); meta['ferida'].append(o['nome'].split('_', 1)[1])
        for q in ('vx0', 'vy0', 'vl'):
            meta[q].append(o[q])
        meta['estado_emilio'].append(e['estado'])
    np.savez_compressed(psaida, X=np.stack(X), Y=np.stack(Y), **{q: np.array(v) for q, v in meta.items()})
    print('%d vistas · %d feridas · %s' % (len(X), len(set(meta['ferida'])), psaida))
    print('sha256', hashlib.sha256(open(psaida, 'rb').read()).hexdigest())


if __name__ == '__main__':
    if len(sys.argv) != 6:
        sys.exit(__doc__)
    main(*sys.argv[1:])
