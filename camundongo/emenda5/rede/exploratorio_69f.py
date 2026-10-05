"""exploratorio_69f.py — E1 (tamanho/dia) e E2 (classificacao), Adendo 69-F. Exploratorio."""
import os, sys, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analisa_rede as A

PXMM = 700 / 24.0


def main(prede, pdados, psaida, ptr, pord, psel, psai):
    z = np.load(pdados); pred = {}
    for k in range(4):
        q = np.load(os.path.join(prede, 'pred_dobra%d.npz' % k))
        for i, c in zip(q['idx'], q['classe']):
            pred[int(i)] = c
    T = json.load(open(ptr, encoding='utf-8'))['E']
    O = {o['nome']: o for o in json.load(open(pord, encoding='utf-8'))['ordem']}
    imp = set(json.load(open(psel, encoding='utf-8'))['impossiveis'])
    nula = A.mascara_nula(); L = []
    for i, nome in enumerate(z['nome']):
        o = O[nome]; e = T[o['id']]
        ref = A.rasteriza(e['t'], o) if e['estado'] != 'FECHADA' else np.zeros((A.L700, A.L700), bool)
        rm = A.para_700(A.pos_rede(pred[i]), int(z['vx0'][i]), int(z['vy0'][i]), int(z['vl'][i]))
        mz = np.load(os.path.join(psaida, 'mascaras_r4', nome + '.npz'))
        m4 = mz['m4'] if mz['m4'].size else np.zeros((A.L700, A.L700), bool)
        ok = ref.any()
        L.append({'nome': nome, 'ferida': str(z['ferida'][i]), 'dia': int(nome.split('_')[0].split()[1]),
                  'estado': e['estado'], 'imp': nome in imp, 'cic': nome in A.CICATRIZADAS,
                  'area': ref.sum() / PXMM ** 2, 'motor_vazio': not m4.any(), 'rede_vazia': not rm.any(),
                  'motor': (A.dice(m4, ref) or 0.0) if ok else None, 'rede': (A.dice(rm, ref) or 0.0) if ok else None,
                  'nulo': A.dice(nula, ref) if ok else None})
    P = [r for r in L if r['estado'] == 'TRACADA']
    a = np.array([r['area'] for r in P]); c1, c2 = np.percentile(a, [100 / 3, 200 / 3])
    md = lambda s, k: float(np.median([r[k] for r in s]))
    S = ['# Adendo 69-F · resultado dos exploratorios (leitora 2, rede original)', '',
         '## E1 · por tamanho (tercis da area da leitora 2) e por dia', '',
         'cortes dos tercis: %.2f e %.2f mm2' % (c1, c2), '',
         '| estrato | n | feridas | area mediana mm2 | motor | rede | nulo | motor - rede (IC 95 %) |', '|---|---|---|---|---|---|---|---|']
    est = [('tercil 1 (< %.1f mm2)' % c1, [r for r in P if r['area'] < c1]),
           ('tercil 2', [r for r in P if c1 <= r['area'] < c2]),
           ('tercil 3 (>= %.1f mm2)' % c2, [r for r in P if r['area'] >= c2]),
           ('dias 0-4', [r for r in P if r['dia'] <= 4]), ('dias 5-9', [r for r in P if 5 <= r['dia'] <= 9]),
           ('dias 10-15', [r for r in P if r['dia'] >= 10])]
    for rot, s in est:
        nf = len(set(r['ferida'] for r in s))
        ic = '%+.3f (%+.3f a %+.3f)' % A.boot(s, 'motor', 'rede') if nf >= 4 else 'menos de 4 feridas'
        S.append('| %s | %d | %d | %.1f | %.3f | %.3f | %.3f | %s |' % (rot, len(s), nf, md(s, 'area'), md(s, 'motor'), md(s, 'rede'), md(s, 'nulo'), ic))
    S += ['', '## E2 · mascara vazia ("sem ferida / nao medido")', '',
          '| grupo | n | motor vazio | rede vazia | leitura |', '|---|---|---|---|---|']
    for rot, s, lei in [('leitora 2 TRACADA (ha ferida)', P, 'vazio = falso negativo'),
                        ('30 sem borda visivel', [r for r in L if r['imp']], 'vazio = recusa'),
                        ('5 com suspeita de fechamento', [r for r in L if r['cic']], 'vazio = esperado se fechou')]:
        S.append('| %s | %d | %d | %d | %s |' % (rot, len(s), sum(r['motor_vazio'] for r in s), sum(r['rede_vazia'] for r in s), lei))
    open(psai, 'w', encoding='utf-8').write('\n'.join(S) + '\n'); print('\n'.join(S))


if __name__ == '__main__':
    main(*sys.argv[1:])
