"""
reanalise_revisor2.py — segunda rodada de reanalises pedidas pelo revisor (Adendo 65). EXPLORATORIAS.
Le dados/REANALISE_REVISOR.json (saida do reanalise_revisor.py, Adendo 64). Escreve dados/REANALISE_REVISOR2.md
e artigo/FIGURA_4_BLAND_ALTMAN.png.
"""
import json, random, numpy as np
from scipy import stats
import statsmodels.formula.api as smf
import pandas as pd
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
SEM, NB = 20261004, 5000
R = json.load(open('dados/REANALISE_REVISOR.json'))
for r in R: r['ferida'] = r['nome'].split('_')[1]
def boot(rows, f):
    an = sorted(set(r['animal'] for r in rows)); por = {a: [r for r in rows if r['animal'] == a] for a in an}
    rnd = random.Random(SEM); v = []
    for _ in range(NB):
        s = [r for a in (rnd.choice(an) for _ in an) for r in por[a]]
        try:
            x = f(s)
            if x == x: v.append(x)
        except Exception: pass
    return np.percentile(v, 2.5), np.percentile(v, 97.5)
S = ['# REANALISES DO REVISOR, RODADA 2 (Adendo 65) — EXPLORATORIAS', '', 'IC 95 % bootstrap agrupado por animal (8), 5000 sorteios.', '',
     '## R9 · Bland-Altman completo (S_r), motor r4 − leitor, mm²', '',
     '| leitor | n | viés (IC) | DP | LoA | inclinação diferença ~ média (IC) | razão geométrica motor/leitor (LoA) |', '|---|---|---|---|---|---|---|']
fig, axs = plt.subplots(1, 2, figsize=(10, 4.2), dpi=200, sharey=True); fig.patch.set_facecolor('#fcfcfb')
for ax, k, nome in zip(axs, 'EH', ['leitor 1', 'leitora 2']):
    rs = [r for r in R if r['principal'] and r[k] == 'TRACADA' and r['area_' + k] > 0]
    a, b = np.array([r['area_m4'] for r in rs]), np.array([r['area_' + k] for r in rs])
    d, m = a - b, (a + b) / 2; bias, sd = d.mean(), d.std(ddof=1)
    lo, hi = boot(rs, lambda s: np.mean([x['area_m4'] - x['area_' + k] for x in s]))
    sl = stats.linregress(m, d).slope
    slo, shi = boot(rs, lambda s: stats.linregress([(x['area_m4'] + x['area_' + k]) / 2 for x in s], [x['area_m4'] - x['area_' + k] for x in s]).slope)
    lr = np.log(a / b); gm, gsd = lr.mean(), lr.std(ddof=1)
    S.append('| %s | %d | %+.2f (%+.2f a %+.2f) | %.2f | %+.2f a %+.2f | %+.3f (%+.3f a %+.3f) | %.3f (%.2f a %.2f) |' % (nome, len(rs), bias, lo, hi, sd, bias - 1.96 * sd, bias + 1.96 * sd, sl, slo, shi, np.exp(gm), np.exp(gm - 1.96 * gsd), np.exp(gm + 1.96 * gsd)))
    ax.set_facecolor('#fcfcfb'); ax.scatter(m, d, s=16, color='#2a78d6', alpha=.7, lw=0)
    for y, ls in ((bias, '-'), (bias - 1.96 * sd, '--'), (bias + 1.96 * sd, '--')): ax.axhline(y, color='#52514e', lw=1, ls=ls)
    ax.axhline(0, color='#c9c8c3', lw=.8); xx = np.linspace(m.min(), m.max(), 10)
    ax.plot(xx, stats.linregress(m, d).intercept + sl * xx, color='#eb6834', lw=1.5)
    ax.set_title('motor − %s (n = %d)' % (nome, len(rs)), fontsize=10, loc='left'); ax.set_xlabel('média das duas áreas (mm²)')
    [ax.spines[s].set_visible(False) for s in ('top', 'right')]
axs[0].set_ylabel('diferença de área (mm²)')
fig.suptitle('Figura 4 · Bland-Altman: linha cheia = viés; tracejadas = limites de 95 %; laranja = regressão da diferença sobre a média', fontsize=9.5, x=0.01, ha='left')
fig.tight_layout(); fig.savefig('artigo/FIGURA_4_BLAND_ALTMAN.png', facecolor=fig.get_facecolor())
S += ['', '## R10 · distância de borda por faixa de dia, absoluta e relativa ao raio equivalente da ferida do leitor', '',
      '| leitor | dias | n | HD95 mm | ASSD mm | raio equivalente mm | HD95 / raio | ASSD / raio |', '|---|---|---|---|---|---|---|---|']
for k in 'EH':
    for a0, a1 in ((0, 4), (5, 9), (10, 15)):
        rs = [r for r in R if r['principal'] and r[k] == 'TRACADA' and a0 <= r['dia'] <= a1 and r['area_' + k] > 0]
        if not rs: continue
        rad = np.array([np.sqrt(r['area_' + k] / np.pi) for r in rs]); hd = np.array([r['hd' + k] for r in rs]); asd = np.array([r['as' + k] for r in rs])
        S.append('| %s | %d–%d | %d | %.2f | %.2f | %.2f | %.2f | %.2f |' % ('leitor 1' if k == 'E' else 'leitora 2', a0, a1, len(rs), np.median(hd), np.median(asd), np.median(rad), np.median(hd / rad), np.median(asd / rad)))
C = [r for r in R if r['E'] == r['H'] == 'TRACADA' and r['area_E'] > 0]
for a0, a1 in ((0, 4), (5, 9), (10, 15)):
    rs = [r for r in C if a0 <= r['dia'] <= a1]
    if rs:
        rad = np.array([np.sqrt(r['area_E'] / np.pi) for r in rs]); hd = np.array([r['hdEH'] for r in rs])
        S.append('| leitor 1 × leitora 2 (C) | %d–%d | %d | %.2f | %.2f | %.2f | %.2f | %.2f |' % (a0, a1, len(rs), np.median(hd), np.median([r['asEH'] for r in rs]), np.median(rad), np.median(hd / rad), np.median(np.array([r['asEH'] for r in rs]) / rad)))
S += ['', '## R11 · área × dia por ferida (braço principal, r4)', '']
pr = [r for r in R if r['principal']]
rhos = []
for w in sorted(set(r['ferida'] for r in pr)):
    rs = [r for r in pr if r['ferida'] == w]
    if len(rs) >= 4: rhos.append(stats.spearmanr([r['dia'] for r in rs], [r['area_m4'] for r in rs])[0])
S.append('- ρ de Spearman por ferida (feridas com ≥ 4 imagens, n = %d): mediana %.2f, IQR %.2f a %.2f, mínimo %.2f, máximo %.2f' % (len(rhos), np.median(rhos), np.percentile(rhos, 25), np.percentile(rhos, 75), min(rhos), max(rhos)))
df = pd.DataFrame([{'area': r['area_m4'], 'dia': r['dia'], 'ferida': r['ferida'], 'animal': r['animal']} for r in pr])
try:
    md = smf.mixedlm('area ~ dia', df, groups=df['ferida'], re_formula='~dia').fit(reml=True)
    ci = md.conf_int().loc['dia']
    S.append('- modelo misto (área ~ dia, intercepto e inclinação aleatórios por ferida; n = %d imagens, %d feridas): inclinação fixa %.2f mm²/dia (IC 95 %% %.2f a %.2f), intercepto %.1f mm²' % (len(df), df['ferida'].nunique(), md.params['dia'], ci[0], ci[1], md.params['Intercept']))
except Exception as e:
    S.append('- modelo misto: falhou (%s)' % e)
open('dados/REANALISE_REVISOR2.md', 'w', encoding='utf-8').write('\n'.join(S) + '\n'); print('\n'.join(S))
