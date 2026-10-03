"""
roda_rodada2.py — RODADA 2: o motor v0 congelado com a COROA do splint declarada
como artefato (PRE_REGISTRO_RODADA2_01OUT.md 3a27e63c..., Adendo 1 08715c08... nao;
Adendo 1 da rodada 2 = a segunda assinatura, anel interno).

NENHUMA LINHA DO MOTOR MUDA. Importa roda_camundongo.py (8c1f6e4d...) e
motor_v0_funcoes.py (16028493...). A unica diferenca para a etapa 3 da rodada 1
e o argumento `ar` — o mecanismo que ja existe em mapa_t() e anel() — que na
rodada 1 era None e aqui e a coroa:

    coroa = { p : 145,83 <= |p - centro do quadro| <= 233,33 px }   (L = 700)

As 51 imagens SEM_ANEL nao tem coroa: o pre-registro diz que "rodam igual nas
duas rodadas". Elas NAO sao reexecutadas: o resultado delas e copiado do
camundongo_v0.json, com a marca 'copiada_da_rodada1'. Ficam fora do pareamento.

Le: deteccao/camundongo_v0.json, CAMPO.txt (so para descrever posicao).
Escreve: <saida>/camundongo_r2.json e <saida>/CAMUNDONGO_R2_RELATORIO.md

Uso:
    python roda_rodada2.py sintetico                    (ensaio da secao 6)
    python roda_rodada2.py rodar <pasta_tiffs> <pasta_saida>
"""
import os, sys, json, time, hashlib
import numpy as np

import roda_camundongo as R
import motor_v0_funcoes as M

L = M.L
C0 = (L - 1) / 2.0
PXMM = R.S_1380 * L / R.LADO_1380             # 29,1667
R_IN, R_OUT = 5.0 * PXMM, 8.0 * PXMM          # 145,83 e 233,33
AREA_INTERNO = 78.5398
TOL = 0.15
_yy, _xx = np.mgrid[0:L, 0:L]
RR = np.hypot(_xx - C0, _yy - C0)
COROA = (RR >= R_IN) & (RR <= R_OUT)


def roda_motor_ar(rgb, diam, criterio, ar):
    """IGUAL a roda_camundongo.roda_motor, linha a linha, com `ar` no lugar de None."""
    cache, mel = {}, (-1, None, None)
    k = 1 if criterio == 'prim' else 2
    for gama, can, g, dsl, al, (lo, hi) in M.grade:
        ka = (gama, can)
        if ka not in cache:
            cache[ka] = M.canais[can](M.clareia(rgb, gama))
        kt = (gama, can, g, dsl, al)
        if kt not in cache:
            cache[kt] = M.mapa_t(cache[ka], g, dsl, al, 4, ar)
        r = M.anel(cache[kt], lo, hi, 3, ar, diam)
        if r is None:
            continue
        if r[k] > mel[0]:
            mel = (r[k], r[0], (gama, can, g, dsl, al, lo, hi))
    return mel


def zonas(m, campo=None):
    n = float(m.sum())
    fb = (m & (RR < R_IN)).sum() / n
    fc = (m & COROA).sum() / n
    ff = (m & (RR > R_OUT)).sum() / n
    z = max((fb, 'buraco'), (fc, 'coroa'), (ff, 'fora'))[1] if max(fb, fc, ff) > 0.5 else 'misto'
    d = {'f_buraco': fb, 'f_coroa': fc, 'f_fora': ff, 'zona': z}
    if campo is not None:
        cx, cy, rb, rc = campo
        rcam = np.hypot(_xx - cx, _yy - cy)
        d['f_campo'] = (m & (rcam <= rc)).sum() / n
        d['f_faixa'] = (m & (rcam > rb) & (RR < R_IN)).sum() / n
    return d


# ------------------------------------------------------------ ensaio sintetico
def cena(rng):
    """Geometria do README no quadro de 700: coroa 5 a 8 mm, ferida de 6 mm.
    Acrescentado o que o campo do operador mostrou (Adendo 15): laranja visivel
    comecando entre 4,3 e 4,6 mm, nao em 5. Inclinacao, deslocamento e ruido."""
    pele = np.array([205, 170, 160]) + rng.normal(0, 8, 3)
    lar = np.array([215, 90, 40]) + rng.normal(0, 8, 3)
    fer = np.array([165, 75, 70]) + rng.normal(0, 8, 3)
    im = np.empty((L, L, 3)); im[:] = pele
    a = 1.0 + rng.uniform(0, 0.12); th = rng.uniform(0, np.pi)
    X = (_xx - C0) * np.cos(th) + (_yy - C0) * np.sin(th)
    Y = -(_xx - C0) * np.sin(th) + (_yy - C0) * np.cos(th)
    rs = np.hypot(X / a, Y)
    r_int = rng.uniform(4.3, 4.6) * PXMM
    im[(rs >= r_int) & (rs <= R_OUT)] = lar
    dx, dy = rng.uniform(-1.0, 1.0, 2) * PXMM
    rf = rng.uniform(2.4, 3.0) * PXMM
    ferida = np.hypot(_xx - C0 - dx, _yy - C0 - dy) <= rf
    im[ferida] = fer
    im += rng.normal(0, 6, im.shape)
    return np.clip(im, 0, 255).astype(np.uint8), ferida


def ensaio(n=30):
    rng = np.random.default_rng(20260928)
    caso = {'1_ferida': 0, '2_atravessa_coroa': 0, '3_None': 0, 'outro': 0}
    linhas = []
    t0 = time.time()
    for i in range(n):
        rgb, fer = cena(rng)
        _, m, _ = roda_motor_ar(rgb, R.DIAM_EF, 'prim', COROA)
        if m is None:
            c, dc, fc = '3_None', None, None
        else:
            dc = float(M.dice(m, fer)); fc = float((m & COROA).sum() / m.sum())
            c = '1_ferida' if dc >= 0.5 else ('2_atravessa_coroa' if fc > 0.2 else 'outro')
        caso[c] += 1
        linhas.append((i, c, dc, fc))
        print('\r%2d/%d  %.0f s' % (i + 1, n, time.time() - t0), end='', flush=True)
    print()
    for l in linhas:
        print('cena %2d  %-18s dice_ferida %s  frac_coroa %s' % (
            l[0], l[1], '-' if l[2] is None else '%.3f' % l[2],
            '-' if l[3] is None else '%.3f' % l[3]))
    print('RESUMO', json.dumps(caso))
    para = caso['3_None'] > n / 2
    print('CONDICAO DE PARADA (caso 3 domina): %s' % ('SIM — A RODADA 2 NAO ACONTECE' if para else 'nao'))
    return caso, para


# ------------------------------------------------------------------ rodada 2
def le_campo(p):
    c = {}
    if os.path.isfile(p):
        for l in open(p, encoding='utf-8'):
            if l.startswith('#') or not l.strip():
                continue
            x = l.rstrip('\n').split('\t')
            if len(x) >= 9 and x[8] == 'ok':
                c[x[0]] = tuple(map(float, x[1:5]))
    return c


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def rodar(pasta, saida):
    pj = os.path.join(saida, 'camundongo_v0.json')
    v0 = json.load(open(pj, encoding='utf-8'))
    r1 = v0['imagens']
    campo = le_campo(os.path.join(saida, 'CAMPO.txt'))
    res = {}
    nomes = sorted(r1)
    t0 = time.time()
    for i, nome in enumerate(nomes, 1):
        v = r1[nome]
        if not v.get('px_mm'):
            d = dict(v); d['copiada_da_rodada1'] = True
            res[nome] = d
            continue
        im, _ = R.abre_rgb8(os.path.join(pasta, nome))
        cx, cy = v['centro_px']
        rgb, frac = R.recorta(im, cx, cy, v['px_mm'])
        nota, m, aj = roda_motor_ar(rgb, R.DIAM_EF, 'prim', COROA)
        d = {'arquivo': nome, 'estrato': v.get('estrato'), 'unidade': 'mm2',
             'px_mm': v['px_mm'], 'centro_px': v['centro_px'], 'criterio': 'prim'}
        if m is None:
            d.update({'obtida': False, 'area': None})
        else:
            area = float(m.sum() * (R.LADO_1380 / L) ** 2 / (R.S_1380 ** 2))
            d.update({'obtida': True, 'area': area, 'nota': float(nota),
                      'ajuste': list(aj),
                      'dice_motor_vs_nulo': float(M.dice(m, R.mascara_nula(L))),
                      'parece_anel_do_splint': bool(abs(area - R.AREA_SPLINT_MM2)
                                                    / R.AREA_SPLINT_MM2 <= TOL),
                      'parece_anel_interno': bool(abs(area - AREA_INTERNO)
                                                  / AREA_INTERNO <= TOL)})
            d.update({k: (float(x) if not isinstance(x, str) else x)
                      for k, x in zonas(m, campo.get(nome)).items()})
        res[nome] = d
        feitas = sum(1 for x in res.values() if not x.get('copiada_da_rodada1'))
        dt = time.time() - t0
        print('\r%4d/204  %4.0f min restantes' % (feitas, dt / feitas * (204 - feitas) / 60),
              end='', flush=True)
    print()
    meta = {'rodada': 2, 'artefato': 'coroa 145.83 a 233.33 px, L=700',
            'quando': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'sha_codigo': {'roda_rodada2.py': sha(__file__),
                           'roda_camundongo.py': sha(R.__file__),
                           'motor_v0_funcoes.py': sha(M.__file__)},
            'sha_entrada': {'camundongo_v0.json': sha(pj)}}
    json.dump({'_meta': meta, 'imagens': res},
              open(os.path.join(saida, 'camundongo_r2.json'), 'w', encoding='utf-8'),
              indent=1, ensure_ascii=False)
    relatorio(saida, r1, res, meta)


# ---------------------------------------------------------------- relatorio
def relatorio(saida, r1, r2, meta):
    from scipy.stats import wilcoxon
    cl = {}
    pc = os.path.join(saida, 'CLASSIFICACAO.txt')
    for l in open(pc, encoding='utf-8'):
        if l.startswith('#') or not l.strip():
            continue
        x = l.rstrip('\n').split('\t')
        cl[x[0]] = (x[1], (x[2] if len(x) > 2 else ''))     # ultima linha vale
    pos1 = {}
    p1 = os.path.join(saida, 'POSICAO_MASCARAS.tsv')
    for l in list(open(p1, encoding='utf-8'))[1:]:
        x = l.rstrip('\n').split('\t')
        pos1[x[0]] = x[8]
    com = [n for n in r2 if not r2[n].get('copiada_da_rodada1')]
    T = ['# RODADA 2 — coroa declarada como artefato', '',
         'Gerado por roda_rodada2.py em %s.' % meta['quando'], '',
         '| arquivo | sha256 |', '|---|---|']
    T += ['| %s | `%s` |' % kv for kv in list(meta['sha_codigo'].items()) + list(meta['sha_entrada'].items())]

    # P5a
    ok = [n for n in r2 if r2[n].get('obtida')]
    def mede(n):
        d = r2[n]
        return d.get('obtida') and not d.get('parece_anel_do_splint') and not d.get('parece_anel_interno')
    n5a = sum(1 for n in r2 if mede(n))
    ext = sum(1 for n in com if r2[n].get('parece_anel_do_splint'))
    inn = sum(1 for n in com if r2[n].get('parece_anel_interno'))
    T += ['', '## P5a — mede a ferida em >= 55 % das 255', '',
          'obtida e fora das duas assinaturas: **%d de 255 = %.1f %%** -> **%s**'
          % (n5a, 100 * n5a / 255, 'confirmada' if n5a / 255 >= 0.55 else 'FALHOU'),
          '', 'assinatura anel externo (170,9-231,2 mm2): %d · anel interno (66,8-90,3 mm2): %d · nenhuma das duas: %d'
          % (ext, inn, sum(1 for n in com if r2[n].get('obtida')) - ext - inn),
          '', '**Ressalva escrita antes (Adendo 23 §2):** a P5a conta mascara de pelo ou luva com area de ferida.'
          ' Ler sempre ao lado do Dice e da zona.']
    # P5b
    d0 = [r2[n]['area'] for n in com if n.startswith('Day 0_') and r2[n].get('obtida')]
    if len(d0) >= 8:
        med = float(np.median(d0))
        v5b = 'confirmada' if 20 <= med <= 40 else 'FALHOU'
        T += ['', '## P5b — mediana do dia 0 entre 20 e 40 mm2', '',
              'n = %d, mediana **%.2f mm2** -> **%s**' % (len(d0), med, v5b)]
    else:
        T += ['', '## P5b', '', 'nao avaliavel: %d imagens do dia 0 com medida (< 8)' % len(d0)]
    dz = [r2[n]['dice_motor_vs_nulo'] for n in com if r2[n].get('obtida')]
    T += ['', 'Dice motor x nulo, mediana: **%.3f** · Dice zero: **%d de %d**'
          % (float(np.median(dz)), sum(1 for x in dz if x == 0), len(dz))]

    # distribuicao
    a = sorted(r2[n]['area'] for n in com if r2[n].get('obtida'))
    if a:
        q = np.percentile(a, [0, 25, 50, 75, 100])
        T += ['', 'Areas (mm2) min / Q1 / mediana / Q3 / max: ' + ' / '.join('%.2f' % x for x in q)]

    # zonas
    def tab(sub, rot):
        z = [r2[n].get('zona', 'sem_mascara') for n in sub]
        return '| %s | %d | %s |' % (rot, len(sub), ' | '.join(str(z.count(k)) for k in
                                                               ('buraco', 'coroa', 'fora', 'misto', 'sem_mascara')))
    limpas = [n for n in com if cl.get(n, ('', ''))[0] == 'v' and cl[n][1] != 'S']
    comp = [n for n in com if cl.get(n, ('', ''))[1] == 'S']
    cn = [n for n in com if cl.get(n, ('', ''))[0] == 'n']
    T += ['', '## Onde caiu a mascara', '',
          '| grupo | n | buraco | coroa | fora | misto | sem mascara |', '|---|---|---|---|---|---|---|',
          tab(com, 'todas com escala'), tab(limpas, 'limpas (v sem p)'),
          tab(comp, 'com plastico (p)'), tab(cn, 'classe n')]

    # P8 (Opus)
    z0 = lambda sub: sum(1 for n in sub if r2[n].get('obtida') and r2[n]['dice_motor_vs_nulo'] == 0)
    p81 = z0(com); p82 = z0(limpas)
    p83 = sum(1 for n in com if r2[n].get('f_faixa', 0) > 0.5)
    T += ['', '## P8 — previsao do Opus (Adendo 23)', '',
          '| | previsto | resultado | |', '|---|---|---|---|',
          '| P8.1 Dice zero nas 204 | >= 80 | %d | %s |' % (p81, 'confirmada' if p81 >= 80 else 'FALHOU'),
          '| P8.2 Dice zero nas 70 limpas | >= 25 | %d | %s |' % (p82, 'confirmada' if p82 >= 25 else 'FALHOU'),
          '| P8.3 mascara > 50 %% na faixa laranja | >= 20 | %d | %s |' % (p83, 'confirmada' if p83 >= 20 else 'FALHOU')]

    # P7 (Fabio) — criterio do Adendo 24
    mud = sum(1 for n in com if pos1.get(n) and r2[n].get('zona', 'sem_mascara') != pos1[n])
    def frac_bur(sub):
        return sum(1 for n in sub if r2[n].get('zona') == 'buraco') / max(1, len(sub))
    T += ['', '## P7 — previsao do Fabio (Adendos 17, 18, 20; criterio no Adendo 24)', '',
          '| | criterio | resultado | |', '|---|---|---|---|',
          '| P7.1 "vai mudar muito" | >= 50 %% das 204 mudam de zona | %d de %d = %.1f %% | %s |'
          % (mud, len(com), 100 * mud / len(com), 'confirmada' if mud / len(com) >= 0.5 else 'FALHOU'),
          '| P7.2a plastico = fracasso | < 50 %% das `p` no buraco | %.1f %% | %s |'
          % (100 * frac_bur(comp), 'confirmada' if frac_bur(comp) < 0.5 else 'FALHOU'),
          '| P7.2b nao laudaveis = fracasso | < 50 %% das `n` no buraco | %.1f %% | %s |'
          % (100 * frac_bur(cn), 'confirmada' if frac_bur(cn) < 0.5 else 'FALHOU'),
          '| (comparacao) limpas | — | %.1f %% no buraco | — |' % (100 * frac_bur(limpas)),
          '| P7.3 pelo | so comentario livre | — | nao avaliavel |',
          '| P7.4 reflexo | so comentario livre | — | nao avaliavel |']

    # rodada 1 x rodada 2 pareado
    par = [n for n in com if r1[n].get('obtida') and r2[n].get('obtida')]
    if len(par) > 10:
        x = np.array([r1[n]['area'] for n in par]); y = np.array([r2[n]['area'] for n in par])
        dx = np.array([r1[n]['dice_motor_vs_nulo'] for n in par]); dy = np.array([r2[n]['dice_motor_vs_nulo'] for n in par])
        pa = wilcoxon(x, y).pvalue if np.any(x != y) else 1.0
        pd = wilcoxon(dx, dy).pvalue if np.any(dx != dy) else 1.0
        T += ['', '## Rodada 1 x rodada 2, pareado (n = %d)' % len(par), '',
              'area mediana r1 %.2f · r2 %.2f mm2 · Wilcoxon p = %.3g' % (np.median(x), np.median(y), pa),
              '', 'Dice x nulo mediana r1 %.3f · r2 %.3f · Wilcoxon p = %.3g' % (np.median(dx), np.median(dy), pd),
              '', 'Dice zero r1 %d · r2 %d' % ((dx == 0).sum(), (dy == 0).sum())]
    T += ['', 'Imagens SEM_ANEL (sem coroa, copiadas da rodada 1): %d' % (255 - len(com)), '']
    open(os.path.join(saida, 'CAMUNDONGO_R2_RELATORIO.md'), 'w', encoding='utf-8').write('\n'.join(T))
    print('\n'.join(T))


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'sintetico':
        ensaio()
    elif len(sys.argv) == 4 and sys.argv[1] == 'rodar':
        rodar(sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
