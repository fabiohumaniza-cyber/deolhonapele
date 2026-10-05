"""trajetoria_69g.py — E3 do Adendo 69-G: motor - rede por ferida ao longo dos dias (leitora 2). Descritivo."""
import sys, csv, collections
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

tsv, png, md = sys.argv[1:4]
H = [x for x in csv.DictReader(open(tsv), delimiter='\t') if x['estado'] == 'TRACADA']
dia = lambda n: int(n.split('_')[0].split()[1])
por = collections.defaultdict(list)
for x in H:
    por[x['ferida']].append((dia(x['nome']), float(x['motor_r4']) - float(x['rede']), x['rede_vazia'] == 'True'))
fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
for f in sorted(por):
    p = sorted(por[f]); d = [a for a, _, _ in p]; v = [b for _, b, _ in p]
    ax.plot(d, v, '-o', ms=3, lw=1, alpha=.8, color='#2b6cb0' if f.startswith('A') else '#c05621')
    for a, b, z in p:
        if z: ax.plot(a, b, 'kx', ms=7)
ax.axhline(0, color='k', lw=.8); ax.axvspan(4.5, 9.5, color='#999', alpha=.12)
ax.set_xlabel('dia'); ax.set_ylabel('Dice(motor r4) − Dice(rede)')
ax.set_title('Por ferida, contra a leitora 2 (azul = idosos, laranja = jovens; × = rede vazia)', fontsize=9)
fig.tight_layout(); fig.savefig(png)
S = ['# Adendo 69-G · E3, trajetoria por ferida (leitora 2, rede original)', '', '## Feridas TRACADA por dia', '',
     '| dia | ' + ' | '.join(str(d) for d in range(16)) + ' |', '|---' * 17 + '|',
     '| feridas | ' + ' | '.join(str(sum(1 for x in H if dia(x['nome']) == d)) for d in range(16)) + ' |', '',
     '## Dias 5 a 9, por ferida', '', '| ferida | fotos | diferencas (dia: motor - rede) | mediana |', '|---|---|---|---|']
tot = []
for f in sorted(por):
    q = [(a, b, z) for a, b, z in por[f] if 5 <= a <= 9]
    if q:
        tot += [b for _, b, _ in q]
        S.append('| %s | %d | %s | %+.3f |' % (f, len(q), ', '.join('d%d: %+.3f%s' % (a, b, ' (rede vazia)' if z else '') for a, b, z in sorted(q)), np.median([b for _, b, _ in q])))
neg = sum(1 for f in por if [b for a, b, _ in por[f] if 5 <= a <= 9] and np.median([b for a, b, _ in por[f] if 5 <= a <= 9]) < 0)
S += ['', 'mediana das %d fotos: %+.3f; feridas com mediana negativa: %d' % (len(tot), np.median(tot), neg)]
open(md, 'w').write('\n'.join(S) + '\n'); print('\n'.join(S))
