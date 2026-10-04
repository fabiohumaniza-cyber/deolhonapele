"""
analisa_rodada4.py — placar da rodada 4, com os criterios do Adendo 36,
escrito ANTES de a rodada 4 rodar. So le; escreve CAMUNDONGO_R4_RELATORIO.md.

Bracos (Adendo 35, nunca somados):
  principal  = estado ok ou nada, SEM filme na ferida (CLASSIFICACAO plastico N)
  com filme  = estado ok ou nada, COM filme (plastico S) — exploratorio
  excluidas  = NAO_TRACAVEL, PELO, BORDA_PARCIAL — so descritivo
  cicatrizadas = as 5 nomeadas no Adendo 36 — exploratorio, resposta certa ~0

Uso: python analisa_rodada4.py <pasta_saida>
"""
import os, sys, json
import numpy as np
from scipy.stats import spearmanr

CICATRIZADAS = ['Day 10_Y8-2-R', 'Day 10_Y8-3-L', 'Day 10_Y8-4-L', 'Day 13_Y8-2-L', 'Day 15_A8-3-L']
VISTAS_PELO_OPUS = ['Day 0_A8-1-L', 'Day 0_A8-1-R', 'Day 0_Y8-3-L', 'Day 8_Y8-2-L']  # Adendo 36, sec. 1
SEM_EFEITO = 0.95      # Dice r3 x r4 a partir do qual a correcao "nao mudou nada"
BF_LIMIAR = 0.30       # borda falsa: >= 30 % do contorno colado no artefato


def dia(n):
    return int(n.split('_')[0].replace('Day', '').strip())


def curva(r, nomes, chave, nmin):
    por = {}
    for n in nomes:
        if r[n].get(chave) is not None:
            por.setdefault(dia(n), []).append(r[n][chave])
    dd = sorted(d for d in por if len(por[d]) >= nmin)
    if len(dd) < 4:
        return None, dd, por
    return float(spearmanr(dd, [np.median(por[d]) for d in dd]).correlation), dd, por


def main(saida):
    r = json.load(open(os.path.join(saida, 'camundongo_r4.json'), encoding='utf-8'))['imagens']
    cl = {}
    for l in open(os.path.join(saida, 'CLASSIFICACAO.txt'), encoding='utf-8'):
        if l.startswith('#') or not l.strip():
            continue
        x = l.rstrip('\n').split('\t'); cl[x[0]] = x[2] if len(x) > 2 else ''
    chave = lambda arq: os.path.splitext(arq)[0]
    todas = sorted(r)
    med = [n for n in todas if r[n]['estado'] in ('ok', 'nada')]
    princ = [n for n in med if cl[n] != 'S']
    filme = [n for n in med if cl[n] == 'S']
    exc = [n for n in todas if r[n]['estado'] not in ('ok', 'nada')]
    cic = [n for n in todas if chave(n) in CICATRIZADAS]
    corr = [n for n in med if r[n]['estado'] == 'ok']
    nada = [n for n in med if r[n]['estado'] == 'nada']
    v = lambda ok: 'confirmada' if ok else 'FALHOU'
    md = lambda xs: '%.2f' % np.median(xs) if xs else '-'

    T = ['# RODADA 4 — campo declarado + declaracao do operador', '',
         'imagens: %d · medidas (ok + nada): %d · principal %d · com filme %d · excluidas %d'
         % (len(todas), len(med), len(princ), len(filme), len(exc)), '',
         '## Trava', '',
         'imagens sem correcao (nada): %d · r4 identico a r3 em todas: %s'
         % (len(nada), all(r[n].get('dice_r3_r4', 1.0) == 1.0 and r[n]['area_r3'] == r[n]['area_r4'] for n in nada)),
         '', '## Bracos', '',
         '| braco | n | com medida r4 | area mediana r3 | area mediana r4 |', '|---|---|---|---|---|']
    for rot, s in (('principal (sem filme)', princ), ('com filme (exploratorio)', filme),
                   ('excluidas (descritivo)', exc), ('cicatrizadas (exploratorio)', cic)):
        a3 = [r[n]['area_r3'] for n in s if r[n]['area_r3'] is not None]
        a4 = [r[n]['area_r4'] for n in s if r[n]['area_r4'] is not None]
        T.append('| %s | %d | %d | %s | %s |' % (rot, len(s), len(a4), md(a3), md(a4)))

    # P11.2
    rho4, dd4, por4 = curva(r, princ, 'area_r4', 3)
    rho3, dd3, _ = curva(r, princ, 'area_r3', 3)
    p112 = rho4 is not None and rho3 is not None and rho4 <= -0.8 and rho4 < rho3
    # P14 (Fabio, efeito da correcao)
    dc = [r[n]['dice_r3_r4'] for n in corr if r[n].get('dice_r3_r4') is not None]
    sem = sum(1 for x in dc if x >= SEM_EFEITO)
    p14 = len(corr) > 0 and sem >= len(corr) / 2.0
    # P13 (Opus, borda falsa) — sem as imagens que o Opus ja viu
    com_art = [n for n in med if r[n]['frac_campo_artefato'] > 0 and chave(n) not in VISTAS_PELO_OPUS]
    bf = [r[n]['borda_falsa'] for n in com_art if r[n].get('borda_falsa') is not None]
    nbf = sum(1 for x in bf if x >= BF_LIMIAR)
    p13 = len(com_art) > 0 and nbf >= 0.25 * len(com_art)

    T += ['', '## Placar (criterios do Adendo 36)', '', '| | criterio | resultado | |', '|---|---|---|---|',
          '| P11.2 Fabio "tirando artefato vai surpreender" | principal: Spearman(dia, mediana r4) <= -0,8 (dias n >= 3) E mais negativo que r3 nas mesmas | r4 %s · r3 %s (%d dias) | %s |'
          % ('%.3f' % rho4 if rho4 is not None else '-', '%.3f' % rho3 if rho3 is not None else '-', len(dd4),
             'nao avaliavel' if rho4 is None or rho3 is None else v(p112)),
          '| P14 Fabio "muitas que eu corrigi nem precisava" | >= metade das %d corrigidas com Dice(r3, r4) >= %.2f | %d de %d | %s |'
          % (len(corr), SEM_EFEITO, sem, len(dc), v(p14)),
          '| P13 Opus: borda falsa | >= 25 %% das imagens com artefato no campo (sem as 4 vistas) com >= %d %% do contorno colado no artefato | %d de %d | %s |'
          % (int(BF_LIMIAR * 100), nbf, len(com_art), v(p13)),
          '| P12.1 / P12.3 Fabio | contra os tracadores cegos | — | avaliadas com os tracadores |',
          '| P12.2 Fabio (pelo) | descritivo | %d PELO; r4 obtida em %d | sem veredito |'
          % (sum(1 for n in exc if r[n]['estado'] == 'PELO'), sum(1 for n in exc if r[n]['estado'] == 'PELO' and r[n]['obtida_r4'])),
          '', 'Curva do braco principal, r4 (dia: n, mediana mm2): ' +
          ' · '.join('%d: %d, %.1f' % (d, len(por4[d]), np.median(por4[d])) for d in sorted(por4))]

    # efeito da correcao, imagem por imagem
    T += ['', '## Efeito da correcao (as %d corrigidas)' % len(corr), '',
          '| imagem | estado | conta-gotas % campo | artefato % campo | area r3 | area r4 | Dice r3 x r4 | borda falsa |',
          '|---|---|---|---|---|---|---|---|']
    f = lambda x, k='%.2f': (k % x) if x is not None else '-'
    for n in sorted(corr, key=lambda n: (dia(n), n)):
        d = r[n]
        T.append('| %s | %s | %.1f | %.1f | %s | %s | %s | %s |' % (
            chave(n), 'filme' if cl[n] == 'S' else 'sem filme', 100 * d['frac_campo_conta_gotas'],
            100 * d['frac_campo_artefato'], f(d['area_r3']), f(d['area_r4']),
            f(d.get('dice_r3_r4'), '%.3f'), f(d.get('borda_falsa'))))
    T += ['', '## Cicatrizadas (resposta certa ~0)', '', '| imagem | estado | area r3 | area r4 |', '|---|---|---|---|']
    for n in cic:
        T.append('| %s | %s | %s | %s |' % (chave(n), r[n]['estado'], f(r[n]['area_r3']), f(r[n]['area_r4'])))
    open(os.path.join(saida, 'CAMUNDONGO_R4_RELATORIO.md'), 'w', encoding='utf-8').write('\n'.join(T) + '\n')
    print('\n'.join(T[:40]))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
