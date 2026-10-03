"""
analisa_rodada3.py — placar da rodada 3, com os criterios do Adendo 28,
escrito ANTES de a rodada 3 rodar. So le; escreve CAMUNDONGO_R3_RELATORIO.md.

Uso: python analisa_rodada3.py <pasta_saida>
"""
import os, sys, json
import numpy as np
from scipy.stats import spearmanr


def dia(n):
    return int(n.split('_')[0].replace('Day', '').strip())


def curva(r, nomes, nmin):
    por = {}
    for n in nomes:
        if r[n].get('obtida'):
            por.setdefault(dia(n), []).append(r[n]['area'])
    dd = sorted(d for d in por if len(por[d]) >= nmin)
    if len(dd) < 4:
        return None, dd, por
    rho = spearmanr(dd, [np.median(por[d]) for d in dd]).correlation
    return float(rho), dd, por


def main(saida):
    r3 = json.load(open(os.path.join(saida, 'camundongo_r3.json'), encoding='utf-8'))['imagens']
    r2 = json.load(open(os.path.join(saida, 'camundongo_r2.json'), encoding='utf-8'))['imagens']
    cl = {}
    for l in open(os.path.join(saida, 'CLASSIFICACAO.txt'), encoding='utf-8'):
        if l.startswith('#') or not l.strip():
            continue
        x = l.rstrip('\n').split('\t'); cl[x[0]] = (x[1], x[2] if len(x) > 2 else '')
    todas = sorted(r3)
    lim = [n for n in todas if cl.get(n, ('', ''))[0] == 'v' and cl[n][1] != 'S']
    pla = [n for n in todas if cl.get(n, ('', ''))[1] == 'S']
    cn = [n for n in todas if cl.get(n, ('', ''))[0] == 'n']
    ob = [n for n in todas if r3[n].get('obtida')]
    dpos = lambda s: sum(1 for n in s if r3[n].get('obtida') and r3[n]['dice_motor_vs_nulo'] > 0)
    inteiro = lambda s: sum(1 for n in s if r3[n].get('obtida') and r3[n]['frac_do_campo'] >= 0.8)
    T = ['# RODADA 3 — campo declarado', '', 'imagens com campo: %d · com medida: %d' % (len(todas), len(ob)), '',
         '| grupo | n | com medida | Dice > 0 vs nulo | mascara >= 80 % do campo | area mediana mm2 |',
         '|---|---|---|---|---|---|']
    for rot, s in (('todas', todas), ('limpas (v sem p)', lim), ('com plastico (p)', pla), ('classe n', cn)):
        a = [r3[n]['area'] for n in s if r3[n].get('obtida')]
        T.append('| %s | %d | %d | %d | %d | %s |' % (rot, len(s), len(a), dpos(s), inteiro(s),
                                                     '%.2f' % np.median(a) if a else '-'))
    d2 = sum(1 for n in r2 if not r2[n].get('copiada_da_rodada1') and r2[n].get('obtida')
             and r2[n]['dice_motor_vs_nulo'] > 0)
    rho_t, dd_t, _ = curva(r3, todas, 8)
    rho_l, dd_l, por_l = curva(r3, lim, 3)
    v = lambda ok: 'confirmada' if ok else 'FALHOU'
    T += ['', '## Placar (criterios do Adendo 28)', '', '| | criterio | resultado | |', '|---|---|---|---|',
          '| P11.1 Fabio "vai mudar mais" | Dice > 0 nas 201 > %d (rodada 2) | %d | %s |' % (d2, dpos(todas), v(dpos(todas) > d2)),
          '| P11.2 Fabio "tirando artefato vai surpreender" | rodada 4 | — | avaliada na rodada 4 |',
          '| P10.1 Opus: a curva NAO cai (todas) | Spearman(dia, mediana) > -0,8, dias com n >= 8 | %s (%d dias) | %s |'
          % ('%.3f' % rho_t if rho_t is not None else '-', len(dd_t), '-' if rho_t is None else v(rho_t > -0.8)),
          '| P10.2 Opus: a curva NAO cai (limpas) | Spearman > -0,8, dias com n >= 3 | %s (%d dias) | %s |'
          % ('%.3f' % rho_l if rho_l is not None else '-', len(dd_l), 'nao avaliavel' if rho_l is None else v(rho_l > -0.8)),
          '| P10.3 Opus: motor pega o campo inteiro | >= 20 das 201 com mascara >= 80 %% do campo | %d | %s |'
          % (inteiro(todas), v(inteiro(todas) >= 20)),
          '', 'Curva das limpas (dia: n, mediana mm2): ' +
          ' · '.join('%d: %d, %.1f' % (d, len(por_l[d]), np.median(por_l[d])) for d in sorted(por_l))]
    open(os.path.join(saida, 'CAMUNDONGO_R3_RELATORIO.md'), 'w', encoding='utf-8').write('\n'.join(T) + '\n')
    print('\n'.join(T))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
