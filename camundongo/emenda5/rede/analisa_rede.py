"""
analisa_rede.py — motor (regra escrita) x rede (U-Net treinada) contra um tracador (Adendo 52).

Le as predicoes fora-da-dobra da rede, as mascaras do motor (saida/mascaras_r4/*.npz: m3, m4)
e o tracado de referencia. Tudo no QUADRO INTEIRO de 700 px, como no analisa_emilio.py.

Rede -> mascara: ferida = argmax == 2; das manchas 8-conexas com >= 50 px (em 352), fica a de
centro de caixa mais perto do centro da vista (distancia L1), como o single_mask_size_wound
deles. Nenhuma mancha = "sem ferida". Redimensiona 352 -> vl (vizinho mais proximo) e cola em (vx0, vy0).

CONJUNTO PRIMARIO: fotos que o tracador de referencia marcou TRACADA.
P19: o motor (r4) NAO e pior que a rede: limite inferior do IC 95 % da mediana da diferenca
     pareada Dice(motor) - Dice(rede) > -0,05. IC por bootstrap por FERIDA (2000 sorteios,
     semente 20261004).
Ao lado, sem veredito: r3, nulo, todas as tracadas (inclusive imaginadas), as 30 impossiveis,
as 5 cicatrizadas (a rede disse "sem ferida"?), e o Dice no estilo Semantic-Shapes (3 canais
achatados, na vista 352) para mostrar o quanto o fundo e o anel inflam o numero.

Uso: python analisa_rede.py <pasta_rede> <rede_dados.npz> <pasta_saida_motor> <tracado.json> <_ORDEM.json> <rotulo> <SELECAO_ENFERMEIROS_v3.json>
"""
import os, sys, json, random
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

L700, LADO, SEMENTE, MARGEM = 700, 352, 20261004, -0.05
CICATRIZADAS = ['Day 10_Y8-2-R', 'Day 10_Y8-3-L', 'Day 10_Y8-4-L', 'Day 13_Y8-2-L', 'Day 15_A8-3-L']


def ilhas(pts):
    out, cur = [], []
    for p in pts:
        if p.get('novo') and cur:
            out.append(cur); cur = []
        cur.append(p)
    if cur:
        out.append(cur)
    return [i for i in out if len(i) >= 3]


def rasteriza(pts, o):                                   # igual ao analisa_emilio.py
    img = Image.new('L', (L700, L700), 0); d = ImageDraw.Draw(img)
    for il in ilhas(pts):
        d.polygon([(o['vx0'] + p['x'] * o['vl'], o['vy0'] + p['y'] * o['vl']) for p in il], fill=255)
    return np.asarray(img) > 0


def pos_rede(cl):
    w = cl == 2
    lab, n = ndimage.label(w, structure=np.ones((3, 3)))
    best, bd = None, None
    for i, s in enumerate(ndimage.find_objects(lab), 1):
        if (lab[s] == i).sum() < 50:
            continue
        cy, cx = (s[0].start + s[0].stop) / 2, (s[1].start + s[1].stop) / 2
        dd = abs(cx - LADO / 2) + abs(cy - LADO / 2)
        if bd is None or dd < bd:
            best, bd = i, dd
    return (lab == best) if best else np.zeros_like(w)


def para_700(m, vx0, vy0, vl):
    big = np.asarray(Image.fromarray(m.astype(np.uint8) * 255).resize((vl, vl), Image.NEAREST)) > 127
    out = np.zeros((L700, L700), bool)
    x0, y0 = max(vx0, 0), max(vy0, 0); x1, y1 = min(vx0 + vl, L700), min(vy0 + vl, L700)
    out[y0:y1, x0:x1] = big[y0 - vy0:y1 - vy0, x0 - vx0:x1 - vx0]
    return out


def dice(a, b):
    s = a.sum() + b.sum()
    return float(2 * (a & b).sum() / s) if s else None


def dice_ss(yt, yp):                                    # estilo Semantic-Shapes: 3 canais achatados
    t = np.eye(3)[yt]; p = np.eye(3)[yp]
    return float((2 * (t * p).sum() + 1) / (t.sum() + p.sum() + 1))


def mascara_nula():
    import roda_camundongo as R
    return R.mascara_nula(L700)


def boot(linhas, chave_a, chave_b):
    fer = sorted(set(r['ferida'] for r in linhas))
    por = {f: [r[chave_a] - r[chave_b] for r in linhas if r['ferida'] == f] for f in fer}
    rnd = random.Random(SEMENTE); meds = []
    for _ in range(2000):
        d = [x for f in (rnd.choice(fer) for _ in fer) for x in por[f]]
        meds.append(float(np.median(d)))
    dd = [r[chave_a] - r[chave_b] for r in linhas]
    return float(np.median(dd)), float(np.percentile(meds, 2.5)), float(np.percentile(meds, 97.5))


def main(prede, pdados, psaida, ptr, pord, rotulo, psel):
    z = np.load(pdados)
    pred = {}
    for k in range(4):
        q = np.load(os.path.join(prede, 'pred_dobra%d.npz' % k))
        for i, c in zip(q['idx'], q['classe']):
            pred[int(i)] = c
    if len(pred) != len(z['nome']):
        sys.exit('PARADO: %d predicoes para %d fotos' % (len(pred), len(z['nome'])))
    T = json.load(open(ptr, encoding='utf-8'))['E']
    O = {o['nome']: o for o in json.load(open(pord, encoding='utf-8'))['ordem']}
    imp = set(json.load(open(psel, encoding='utf-8'))['impossiveis'])
    nula = mascara_nula()
    L = []
    for i, nome in enumerate(z['nome']):
        o = O[nome]; e = T[o['id']]
        ref = rasteriza(e['t'], o) if e['estado'] != 'FECHADA' else np.zeros((L700, L700), bool)
        rm352 = pos_rede(pred[i])
        rm = para_700(rm352, int(z['vx0'][i]), int(z['vy0'][i]), int(z['vl'][i]))
        mz = np.load(os.path.join(psaida, 'mascaras_r4', nome + '.npz'))
        m4 = mz['m4'] if mz['m4'].size else np.zeros((L700, L700), bool)
        m3 = mz['m3'] if mz['m3'].size else np.zeros((L700, L700), bool)
        ok = ref.any()
        L.append({'nome': nome, 'ferida': str(z['ferida'][i]), 'estado': e['estado'], 'impossivel': nome in imp,
                  'cicatrizada': nome in CICATRIZADAS, 'rede_vazia': not rm.any(),
                  'motor_r4': dice(m4, ref) or 0.0 if ok else None, 'motor_r3': dice(m3, ref) or 0.0 if ok else None,
                  'rede': dice(rm, ref) or 0.0 if ok else None, 'nulo': dice(nula, ref) if ok else None,
                  'rede_estilo_ss': dice_ss(z['Y'][i], pred[i])})
    md = lambda s, c: '%.3f' % np.median([r[c] for r in s]) if s else '-'
    prim = [r for r in L if r['estado'] == 'TRACADA']
    S = ['# MOTOR x REDE — referencia: %s' % rotulo, '',
         '| conjunto | n | motor r4 | motor r3 | rede | nulo |', '|---|---|---|---|---|---|']
    for rot, s in [('**primario: %s TRACADA**' % rotulo, prim),
                   ('todas as tracadas (inclusive imaginadas)', [r for r in L if r['motor_r4'] is not None]),
                   ('so as 30 impossiveis', [r for r in L if r['impossivel'] and r['motor_r4'] is not None])]:
        S.append('| %s | %d | %s | %s | %s | %s |' % (rot, len(s), md(s, 'motor_r4'), md(s, 'motor_r3'), md(s, 'rede'), md(s, 'nulo')))
    if prim:
        m, lo, hi = boot(prim, 'motor_r4', 'rede')
        v = 'confirmada' if lo > MARGEM else 'FALHOU'
        S += ['', '**P19** (motor nao pior que a rede, margem 0,05): mediana da diferenca motor - rede = '
              '%+.3f, IC 95 %% [%+.3f, %+.3f] -> **%s**' % (m, lo, hi, v)]
        m3, lo3, hi3 = boot(prim, 'motor_r3', 'rede')
        S.append('ao lado, r3 - rede: %+.3f [%+.3f, %+.3f]' % (m3, lo3, hi3))
    S += ['', 'cicatrizadas, a rede disse "sem ferida" em: %d de %d (%s)' % (
              sum(r['rede_vazia'] for r in L if r['cicatrizada']), len(CICATRIZADAS),
              ', '.join('%s %s' % (r['nome'], 'vazia' if r['rede_vazia'] else 'marcou') for r in L if r['cicatrizada'])),
          'rede vazia no total: %d de %d fotos' % (sum(r['rede_vazia'] for r in L), len(L)),
          '', 'Dice da rede no estilo Semantic-Shapes (3 canais achatados, contra o rotulo do Emilio, vista 352): '
              'mediana %s' % md(L, 'rede_estilo_ss')]
    open(os.path.join(prede, 'REDE_x_MOTOR_%s.md' % rotulo), 'w', encoding='utf-8').write('\n'.join(S) + '\n')
    cols = ['nome', 'ferida', 'estado', 'impossivel', 'cicatrizada', 'rede_vazia', 'motor_r4', 'motor_r3', 'rede', 'nulo', 'rede_estilo_ss']
    with open(os.path.join(prede, 'rede_por_imagem_%s.tsv' % rotulo), 'w', encoding='utf-8') as f:
        f.write('\t'.join(cols) + '\n')
        for r in L:
            f.write('\t'.join('' if r[c] is None else ('%.4f' % r[c] if isinstance(r[c], float) else str(r[c])) for c in cols) + '\n')
    print('\n'.join(S))


if __name__ == '__main__':
    if len(sys.argv) != 8:
        sys.exit(__doc__)
    main(*sys.argv[1:])
