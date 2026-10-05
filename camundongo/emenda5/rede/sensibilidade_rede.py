"""
sensibilidade_rede.py — analises de sensibilidade da comparacao motor x rede (Adendo 68).

Reusa, sem mudar, as funcoes do analisa_rede.py (e3c5e9d0...): rasterizacao do tracado, pos-
processamento da rede, colagem no quadro de 700 px, Dice, nulo, bootstrap registrado.

Para uma pasta de predicoes (pred_dobra0..3.npz) e uma referencia, calcula:
  S1  o veredito P19/P20 do jeito registrado (2000 sorteios, semente 20261004), para comparacao;
  S2  estabilidade do IC: 10 sementes (20261004..20261013) x 10 000 sorteios por ferida,
      faixa dos limites inferiores; BCa (10 000 sorteios, semente 20261004, jackknife por ferida);
  S3  analise ao nivel da ferida: mediana da diferenca por ferida, depois mediana entre feridas,
      IC por bootstrap das feridas (10 000, semente 20261004); feridas e fotos por ferida;
  S4  sem as fotos em que a rede deixou a mascara vazia: diferenca pareada com IC (10 000);
  S5  a rede SEM o pos-processamento (pos='bruta'): ferida = todo pixel com argmax == 2.

Uso: python sensibilidade_rede.py <pasta_pred> <rotulo_rede> <pos: orig|bruta> <rede_dados.npz>
       <pasta_saida_motor> <tracado.json> <_ORDEM.json> <rotulo_ref> <SELECAO_ENFERMEIROS_v3.json> <saida.md>
"""
import os, sys, json
import numpy as np
from scipy.stats import norm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import analisa_rede as A

N_B, SEMENTES = 10000, [20261004 + i for i in range(10)]


def por_ferida(L, a, b):
    fer = sorted(set(r['ferida'] for r in L))
    return fer, {f: np.array([r[a] - r[b] for r in L if r['ferida'] == f]) for f in fer}


def boot_med(fer, por, sem, n=N_B):
    rnd = np.random.RandomState(sem); out = np.empty(n)
    for j in range(n):
        out[j] = np.median(np.concatenate([por[fer[i]] for i in rnd.randint(len(fer), size=len(fer))]))
    return out


def bca(fer, por, sem):
    theta = float(np.median(np.concatenate([por[f] for f in fer])))
    b = boot_med(fer, por, sem)
    z0 = norm.ppf(np.clip((b < theta).mean() + 0.5 * (b == theta).mean(), 1e-6, 1 - 1e-6))
    jk = np.array([np.median(np.concatenate([por[g] for g in fer if g != f])) for f in fer])
    d = jk.mean() - jk; a = (d ** 3).sum() / (6 * ((d ** 2).sum()) ** 1.5) if (d ** 2).sum() else 0.0
    q = lambda al: norm.cdf(z0 + (z0 + norm.ppf(al)) / (1 - a * (z0 + norm.ppf(al))))
    return float(np.percentile(b, 100 * q(0.025))), float(np.percentile(b, 100 * q(0.975)))


def nivel_ferida(fer, por, sem):
    med = np.array([np.median(por[f]) for f in fer]); rnd = np.random.RandomState(sem)
    bs = [np.median(med[rnd.randint(len(fer), size=len(fer))]) for _ in range(N_B)]
    return float(np.median(med)), float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def linhas(ppred, pos, pdados, psaida, ptr, pord, psel):
    z = np.load(pdados); pred = {}
    for k in range(4):
        q = np.load(os.path.join(ppred, 'pred_dobra%d.npz' % k))
        for i, c in zip(q['idx'], q['classe']):
            pred[int(i)] = c
    if len(pred) != len(z['nome']):
        sys.exit('PARADO: %d predicoes para %d fotos' % (len(pred), len(z['nome'])))
    T = json.load(open(ptr, encoding='utf-8'))['E']
    O = {o['nome']: o for o in json.load(open(pord, encoding='utf-8'))['ordem']}
    imp = set(json.load(open(psel, encoding='utf-8'))['impossiveis'])
    nula = A.mascara_nula(); L = []
    for i, nome in enumerate(z['nome']):
        o = O[nome]; e = T[o['id']]
        ref = A.rasteriza(e['t'], o) if e['estado'] != 'FECHADA' else np.zeros((A.L700, A.L700), bool)
        r352 = A.pos_rede(pred[i]) if pos == 'orig' else (pred[i] == 2)
        rm = A.para_700(r352, int(z['vx0'][i]), int(z['vy0'][i]), int(z['vl'][i]))
        mz = np.load(os.path.join(psaida, 'mascaras_r4', nome + '.npz'))
        m4 = mz['m4'] if mz['m4'].size else np.zeros((A.L700, A.L700), bool)
        m3 = mz['m3'] if mz['m3'].size else np.zeros((A.L700, A.L700), bool)
        ok = ref.any()
        L.append({'nome': nome, 'ferida': str(z['ferida'][i]), 'estado': e['estado'], 'impossivel': nome in imp,
                  'rede_vazia': not rm.any(),
                  'motor_r4': (A.dice(m4, ref) or 0.0) if ok else None, 'motor_r3': (A.dice(m3, ref) or 0.0) if ok else None,
                  'rede': (A.dice(rm, ref) or 0.0) if ok else None, 'nulo': A.dice(nula, ref) if ok else None,
                  'rede_ss': A.dice_ss(z['Y'][i], pred[i])})
    return L


def main(ppred, rot_rede, pos, pdados, psaida, ptr, pord, rot_ref, psel, psai):
    L = linhas(ppred, pos, pdados, psaida, ptr, pord, psel)
    P = [r for r in L if r['estado'] == 'TRACADA']
    md = lambda s, c: float(np.median([r[c] for r in s]))
    S = ['# Sensibilidade · rede %s · pos-processamento %s · referencia %s' % (rot_rede, pos, rot_ref), '',
         '| conjunto | n | motor r4 | motor r3 | rede | nulo |', '|---|---|---|---|---|---|']
    for rot, s in [('TRACADA (primario)', P), ('todas as tracadas', [r for r in L if r['motor_r4'] is not None]),
                   ('30 impossiveis', [r for r in L if r['impossivel'] and r['motor_r4'] is not None])]:
        S.append('| %s | %d | %.3f | %.3f | %.3f | %.3f |' % (rot, len(s), md(s, 'motor_r4'), md(s, 'motor_r3'), md(s, 'rede'), md(s, 'nulo')))
    S += ['', 'rede vazia: %d de %d fotos; no primario, %d de %d' % (sum(r['rede_vazia'] for r in L), len(L),
          sum(r['rede_vazia'] for r in P), len(P)),
          'Dice da rede contado como no original (3 classes achatadas, vista 352, rotulo do leitor 1): mediana %.3f' % md(L, 'rede_ss'), '']
    for mot in ('motor_r4', 'motor_r3'):
        fer, por = por_ferida(P, mot, 'rede')
        m, lo, hi = A.boot(P, mot, 'rede')
        S += ['## %s - rede' % mot, '',
              '- feridas no conjunto: %d; fotos por ferida: %s' % (len(fer), ', '.join('%s=%d' % (f, len(por[f])) for f in fer)),
              '- S1 registrado (2000, semente 20261004): mediana %+.3f, IC [%+.3f, %+.3f] -> P19 %s, P20 %s' % (
                  m, lo, hi, 'confirmada' if lo > A.MARGEM else 'FALHOU', 'confirmada' if lo > 0 else 'nao confirmada')]
        lows = []
        for sem in SEMENTES:
            b = boot_med(fer, por, sem); lows.append((np.percentile(b, 2.5), np.percentile(b, 97.5)))
        lo_min, lo_max = min(x[0] for x in lows), max(x[0] for x in lows)
        S.append('- S2 10 sementes x 10 000: limite inferior de %+.3f a %+.3f; superior de %+.3f a %+.3f; '
                 'P20 (> 0) em %d de 10 sementes' % (lo_min, lo_max, min(x[1] for x in lows), max(x[1] for x in lows),
                                                     sum(x[0] > 0 for x in lows)))
        bl, bh = bca(fer, por, SEMENTES[0])
        S.append('- S2 BCa (10 000): IC [%+.3f, %+.3f]' % (bl, bh))
        fm, fl, fh = nivel_ferida(fer, por, SEMENTES[0])
        S.append('- S3 nivel da ferida (mediana das medianas por ferida): %+.3f, IC [%+.3f, %+.3f]' % (fm, fl, fh))
        Pn = [r for r in P if not r['rede_vazia']]
        fer2, por2 = por_ferida(Pn, mot, 'rede'); b = boot_med(fer2, por2, SEMENTES[0])
        S.append('- S4 sem as vazias (n = %d): mediana %+.3f, IC [%+.3f, %+.3f]' % (
            len(Pn), float(np.median(np.concatenate(list(por2.values())))), np.percentile(b, 2.5), np.percentile(b, 97.5)))
        S.append('- fotos em que o motor teve Dice maior que a rede: %d de %d' % (sum(r[mot] > r['rede'] for r in P), len(P)))
        S.append('')
    open(psai, 'w', encoding='utf-8').write('\n'.join(S) + '\n')
    print('\n'.join(S))


if __name__ == '__main__':
    if len(sys.argv) != 11:
        sys.exit(__doc__)
    main(*sys.argv[1:])
