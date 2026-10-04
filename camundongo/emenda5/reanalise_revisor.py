"""
reanalise_revisor.py — reanalises EXPLORATORIAS pedidas pelo revisor (Adendo 63).

Uso: python reanalise_revisor.py <pasta_mascaras_r4> <saida.md>
Le so arquivos publicados em dados/. Escreve um relatorio markdown e um JSON ao lado.
"""
import sys, os, json, random
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage, stats

AQ = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(AQ, 'dados')
L, PXMM, SEM, NB = 700, 700 / 24.0, 20261004, 5000
MM2 = 1 / PXMM ** 2


def j(p): return json.load(open(os.path.join(D, p), encoding='utf-8'))


def ilhas(pts):
    out, cur = [], []
    for p in pts:
        if p.get('novo') and cur: out.append(cur); cur = []
        cur.append(p)
    if cur: out.append(cur)
    return [i for i in out if len(i) >= 3]


def rast(pts, o):
    img = Image.new('L', (L, L), 0); d = ImageDraw.Draw(img)
    for il in ilhas(pts):
        d.polygon([(o['vx0'] + p['x'] * o['vl'], o['vy0'] + p['y'] * o['vl']) for p in il], fill=255)
    return np.asarray(img) > 0


def dice(a, b):
    s = a.sum() + b.sum(); return float(2 * (a & b).sum() / s) if s else np.nan


def borda(m): return m & ~ndimage.binary_erosion(m)


def hd_assd(a, b):
    if not a.any() or not b.any(): return np.nan, np.nan
    ba, bb = borda(a), borda(b)
    da = ndimage.distance_transform_edt(~bb)[ba]; db = ndimage.distance_transform_edt(~ba)[bb]
    allv = np.concatenate([da, db])
    return float(np.percentile(allv, 95) / PXMM), float(allv.mean() / PXMM)


def circ(cx, cy, r):
    yy, xx = np.mgrid[0:L, 0:L]; return (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r


def nulo():
    r = 3.0 * PXMM; c = (L - 1) / 2.0; return circ(c, c, r)


def animal(n): return n.split('_')[1].rsplit('-', 1)[0]


def boot(rows, f, nb=NB):
    an = sorted(set(r['animal'] for r in rows)); por = {a: [r for r in rows if r['animal'] == a] for a in an}
    rnd = random.Random(SEM); v = []
    for _ in range(nb):
        s = [r for a in (rnd.choice(an) for _ in an) for r in por[a]]
        try:
            x = f(s)
            if x == x: v.append(x)
        except Exception:
            pass
    return (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))) if v else (np.nan, np.nan)


def kap(a, b):
    a = np.asarray(a, bool); b = np.asarray(b, bool); po = (a == b).mean()
    pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    return float((po - pe) / (1 - pe)) if pe < 1 else np.nan


def main(pm, psaida):
    DEC = j('declaracao_camundongo_r4.json')['E']; R4 = j('camundongo_r4.json')['imagens']
    cl = {}
    for l in open(os.path.join(D, 'CLASSIFICACAO.txt'), encoding='utf-8'):
        if not l.startswith('#') and l.strip():
            x = l.rstrip('\n').split('\t'); cl[x[0][:-5]] = (x[1] if len(x) > 1 else '', x[2] if len(x) > 2 else '')
    camp = {}
    for l in open(os.path.join(D, 'CAMPO.txt'), encoding='utf-8'):
        if l.startswith('#') or not l.strip(): continue
        x = l.rstrip('\n\r').split('\t'); n = x[0][:-5]
        camp[n] = None if x[8] != 'ok' else (float(x[1]), float(x[2]), float(x[4]))
    OE = {o['nome']: o for o in j('_ORDEM_v2_emilio.json')['ordem']}; OH = {o['nome']: o for o in j('_ORDEM_v2_Helga.json')['ordem']}
    TE = j('tracado_camundongo_v2_emilio_2026-10-04.json')['E']; TH = j('tracado_camundongo_v2_Helga_2026-10-04.json')['E']
    NU = nulo(); rows = []
    for n in sorted(OE):
        e, h = TE[OE[n]['id']], TH[OH[n]['id']]
        z = np.load(os.path.join(pm, n + '.npz')); m4 = z['m4'] if z['m4'].size else np.zeros((L, L), bool)
        m3 = z['m3'] if z['m3'].size else np.zeros((L, L), bool)
        me = rast(e['t'], OE[n]) if e['estado'] != 'FECHADA' else np.zeros((L, L), bool)
        mh = rast(h['t'], OH[n]) if h['estado'] != 'FECHADA' else np.zeros((L, L), bool)
        cf = camp.get(n); CF = circ(*cf) if cf else None
        r = {'nome': n, 'animal': animal(n), 'idade': n.split('_')[1][0], 'dia': int(n.split('_')[0].split()[1]),
             'filme': cl.get(n, ('', ''))[1] == 'S', 'op': DEC[n]['estado'], 'E': e['estado'], 'H': h['estado'],
             'limpa': cl.get(n, ('', ''))[0] == 'v' and cl.get(n, ('', ''))[1] == 'N', 'area_r3': R4[n + '.tiff']['area_r3'],
             'area_m4': float(m4.sum() * MM2), 'area_E': float(me.sum() * MM2), 'area_H': float(mh.sum() * MM2)}
        r['principal'] = r['op'] in ('ok', 'nada') and not r['filme']
        for k, mr in (('E', me), ('H', mh)):
            r['d4' + k], r['d3' + k], r['dn' + k] = dice(m4, mr), dice(m3, mr), dice(NU, mr)
            r['dc' + k] = dice(CF, mr) if CF is not None else np.nan
            r['hd' + k], r['as' + k] = hd_assd(m4, mr)
        r['dEH'] = dice(me, mh); r['hdEH'], r['asEH'] = hd_assd(me, mh)
        rows.append(r)
    S = ['# REANALISES PEDIDAS PELO REVISOR (Adendo 63) — EXPLORATORIAS', '',
         'IC 95 % por bootstrap agrupado por animal (8), 5000 sorteios. Mediana [IQR] {IC95}.', '']
    med = lambda v: float(np.nanmedian(v)) if len(v) else np.nan
    def fmt(rs, key):
        v = [r[key] for r in rs if r[key] == r[key]]
        if not v: return '-'
        lo, hi = boot(rs, lambda s: med([x[key] for x in s if x[key] == x[key]]))
        return '%.3f [%.3f–%.3f] {%.3f–%.3f}' % (med(v), np.percentile(v, 25), np.percentile(v, 75), lo, hi)
    def esc(rs, k):
        v = [(r['d4' + k] - r['dn' + k]) / (1 - r['dn' + k]) for r in rs if r['d4' + k] == r['d4' + k] and r['dn' + k] < 1]
        return '%.2f' % med(v) if v else '-'
    def dif(rs, k):
        f = lambda s: med([x['d4' + k] - x['dn' + k] for x in s])
        lo, hi = boot(rs, f); return '%+.3f {%+.3f–%+.3f}' % (f(rs), lo, hi)
    C = [r for r in rows if r['E'] == 'TRACADA' and r['H'] == 'TRACADA']
    S += ['## R1 · Dice contra cada leitor', '', '| conjunto | leitor | n | motor r4 | motor r3 | nulo | r4 − nulo | escalonado |', '|---|---|---|---|---|---|---|---|']
    for rot, sel in [('S_r (placar)', lambda r, k: r['principal'] and r[k] == 'TRACADA'),
                     ('L_r (leitores, sem filme)', lambda r, k: (not r['filme']) and r[k] == 'TRACADA'),
                     ('C, sem filme', lambda r, k: r['E'] == r['H'] == 'TRACADA' and not r['filme']),
                     ('C, com filme', lambda r, k: r['E'] == r['H'] == 'TRACADA' and r['filme'])]:
        for k in 'EH':
            rs = [r for r in rows if sel(r, k)]
            S.append('| %s | %s | %d | %s | %s | %s | %s | %s |' % (rot, k, len(rs), fmt(rs, 'd4' + k), fmt(rs, 'd3' + k), fmt(rs, 'dn' + k), dif(rs, k), esc(rs, k)))
    for rot, rs in [('C sem filme', [r for r in C if not r['filme']]), ('C com filme', [r for r in C if r['filme']]), ('C todas', C)]:
        S.append('| %s | E × H | %d | %s | | | | |' % (rot, len(rs), fmt(rs, 'dEH')))
    S += ['', '## R2 · segundo nulo: o campo inteiro', '', '| leitor | n | Dice campo inteiro | Dice motor r4 |', '|---|---|---|---|']
    for k in 'EH':
        rs = [r for r in rows if r['principal'] and r[k] == 'TRACADA']
        S.append('| %s | %d | %s | %s |' % (k, len(rs), fmt(rs, 'dc' + k), fmt(rs, 'd4' + k)))
    S += ['', '## R3 · Bland-Altman da área (mm²), motor r4 − leitor', '', '| conjunto | leitor | n | área leitor mediana | viés médio {IC95} | limites 95 % | viés relativo mediano |', '|---|---|---|---|---|---|---|']
    for rot, base in [('S_r', lambda r: r['principal']), ('L_r', lambda r: not r['filme'])]:
        for k in 'EH':
            rs = [r for r in rows if base(r) and r[k] == 'TRACADA']
            d = np.array([r['area_m4'] - r['area_' + k] for r in rs]); sd = d.std(ddof=1)
            lo, hi = boot(rs, lambda s: float(np.mean([x['area_m4'] - x['area_' + k] for x in s])))
            rel = med([100 * (r['area_m4'] - r['area_' + k]) / r['area_' + k] for r in rs if r['area_' + k] > 0])
            S.append('| %s | %s | %d | %.1f | %+.2f {%+.2f–%+.2f} | %+.2f a %+.2f | %+.1f %% |' % (rot, k, len(rs), med([r['area_' + k] for r in rs]), d.mean(), lo, hi, d.mean() - 1.96 * sd, d.mean() + 1.96 * sd, rel))
    S += ['', '## R4 · distância de borda (mm)', '', '| conjunto | comparação | n | HD95 | ASSD |', '|---|---|---|---|---|']
    for k in 'EH':
        rs = [r for r in rows if r['principal'] and r[k] == 'TRACADA']
        S.append('| S_r | motor × %s | %d | %s | %s |' % (k, len(rs), fmt(rs, 'hd' + k), fmt(rs, 'as' + k)))
    for k in 'EH':
        S.append('| C | motor × %s | %d | %s | %s |' % (k, len(C), fmt(C, 'hd' + k), fmt(C, 'as' + k)))
    S.append('| C | E × H | %d | %s | %s |' % (len(C), fmt(C, 'hdEH'), fmt(C, 'asEH')))
    S += ['', '## R5 · kappa (TRACADA ou não; operador: ok/nada)', '', '| par | κ | IC95 |', '|---|---|---|']
    for rot, fa, fb in [('E × H', lambda r: r['E'] == 'TRACADA', lambda r: r['H'] == 'TRACADA'),
                        ('operador × E', lambda r: r['op'] in ('ok', 'nada'), lambda r: r['E'] == 'TRACADA'),
                        ('operador × H', lambda r: r['op'] in ('ok', 'nada'), lambda r: r['H'] == 'TRACADA')]:
        f = lambda s: kap([fa(x) for x in s], [fb(x) for x in s]); lo, hi = boot(rows, f)
        S.append('| %s | %.3f | %.3f–%.3f |' % (rot, f(rows), lo, hi))
    S += ['', '## R6 · Spearman (dia, área)', '']
    for rot, rs, key in [('braço principal, r4', [r for r in rows if r['principal']], 'area_m4'), ('limpas, r3', [r for r in rows if r['limpa']], 'area_r3')]:
        f = lambda s: stats.spearmanr([x['dia'] for x in s], [x[key] for x in s])[0]; lo, hi = boot(rs, f)
        S.append('- %s (n = %d): ρ = %.3f, IC95 %.3f a %.3f' % (rot, len(rs), f(rs), lo, hi))
    S += ['', '## R7 · subgrupos (S_r)', '', '| grupo | n E | Dice r4×E | n H | Dice r4×H | % TRACADA E (das 201) | % TRACADA H |', '|---|---|---|---|---|---|---|']
    grupos = [('idade ' + g, lambda r, g=g: r['idade'] == g) for g in 'AY'] + \
             [('animal ' + a, lambda r, a=a: r['animal'] == a) for a in sorted(set(r['animal'] for r in rows))] + \
             [('dias %d–%d' % (a, b), lambda r, a=a, b=b: a <= r['dia'] <= b) for a, b in ((0, 4), (5, 9), (10, 15))]
    for rot, g in grupos:
        tot = [r for r in rows if g(r)]
        cel = []
        for k in 'EH':
            rs = [r for r in tot if r['principal'] and r[k] == 'TRACADA']
            cel += [str(len(rs)), '%.3f' % med([r['d4' + k] for r in rs]) if rs else '-']
        S.append('| %s | %s | %s | %s | %s | %.0f %% | %.0f %% |' % (rot, cel[0], cel[1], cel[2], cel[3],
                 100 * np.mean([r['E'] == 'TRACADA' for r in tot]), 100 * np.mean([r['H'] == 'TRACADA' for r in tot])))
    pr = [r for r in rows if r['principal']]
    S += ['', '## R8 · fluxo', '',
          '255 imagens → 204 com anel medível (51 sem anel) → 201 com campo (3 NAO_DA) → declaração: 137 medidas (81 nada + 56 ok), 64 excluídas (49 não traçável, 11 borda parcial, 4 pelo) → braço principal %d (sem filme) / com filme %d → TRACADA no principal: leitor 1 %d, leitora 2 %d; ambos TRACADA em todo o banco: %d.'
          % (len(pr), sum(1 for r in rows if r['op'] in ('ok', 'nada') and r['filme']), sum(r['E'] == 'TRACADA' for r in pr), sum(r['H'] == 'TRACADA' for r in pr), len(C))]
    open(psaida, 'w', encoding='utf-8').write('\n'.join(S) + '\n')
    json.dump(rows, open(psaida.replace('.md', '.json'), 'w'), default=float)
    print('\n'.join(S))


if __name__ == '__main__':
    main(*sys.argv[1:])
