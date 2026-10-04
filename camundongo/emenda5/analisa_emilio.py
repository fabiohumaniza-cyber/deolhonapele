"""
analisa_emilio.py — compara o tracado cego do Emilio (painel v2, Adendo 39) com
o motor (r3 e r4) e com a declaracao do Fabio. Escrito e publicado ANTES de o
JSON do Emilio ser aberto (o JSON foi lacrado com SHA-256 as 11h02 de 04/10).

So le. Escreve EMILIO_RELATORIO.md e emilio_por_imagem.tsv em <pasta_saida>.

O QUE CALCULA
  1. Integridade: versao v2, declaracao inicial marcada, 201 fotos fechadas,
     SHA de cada foto igual ao do _ORDEM. Se falhar, PARA.
  2. Rasterizacao: cada ilha do tracado (pontos com novo=true comecam ilha nova)
     vira um poligono preenchido; as ilhas se unem. Coordenada 0..1 da vista ->
     quadro de 700: (vx0 + x*vl, vy0 + y*vl).
  3. Dice no QUADRO INTEIRO de 700 (sem recortar pelo campo: se a ferida do
     tracador sai do campo, isso conta contra o motor).
  4. P12.1 e P12.3 (Adendo 36, como delimitadas no Adendo 39):
       conjunto = braco principal (Fabio ok/nada, sem filme) E Emilio TRACADA
       P12.1 confirma se mediana Dice(r4, Emilio) >= 0,70
       P12.3 confirma se >= 80 % das imagens com Dice(r4, Emilio) >= 0,70
  5. Ao lado, sem veredito: Dice(r3, Emilio), Dice(nulo, Emilio), e as mesmas
     contas em TODAS as fotos tracadas (incluindo imaginadas), que e o que o
     trabalho original fez.
  6. Concordancia de tracabilidade, Fabio x Emilio (kappa de Cohen):
       Fabio tracavel = ok/nada ; Emilio tracavel = TRACADA.
  7. Tempo por foto (t_fechou - t_abriu) e tempo total, com as pausas.

Uso:
    python analisa_emilio.py <pasta_saida> <tracado_emilio.json> <_ORDEM.json> <declaracao_r4.json>
"""
import os, sys, json, datetime
import numpy as np
from PIL import Image, ImageDraw

import roda_camundongo as R
import motor_v0_funcoes as M
import roda_rodada2 as R2

L = M.L
LIMIAR = 0.70
CICATRIZADAS = ['Day 10_Y8-2-R', 'Day 10_Y8-3-L', 'Day 10_Y8-4-L', 'Day 13_Y8-2-L', 'Day 15_A8-3-L']


def t(s):
    return datetime.datetime.fromisoformat(s.replace('Z', '+00:00'))


def ilhas(pts):
    out, cur = [], []
    for p in pts:
        if p.get('novo') and cur:
            out.append(cur); cur = []
        cur.append(p)
    if cur:
        out.append(cur)
    return [i for i in out if len(i) >= 3]


def rasteriza(pts, o):
    img = Image.new('L', (L, L), 0)
    d = ImageDraw.Draw(img)
    for il in ilhas(pts):
        d.polygon([(o['vx0'] + p['x'] * o['vl'], o['vy0'] + p['y'] * o['vl']) for p in il], fill=255)
    return np.asarray(img) > 0


def dice(a, b):
    s = a.sum() + b.sum()
    return float(2 * (a & b).sum() / s) if s else None


def kappa(a, b):
    a = np.asarray(a, bool); b = np.asarray(b, bool); n = len(a)
    po = (a == b).mean()
    pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    return float((po - pe) / (1 - pe)) if pe < 1 else None


def main(saida, ptr, pord, pdec):
    T = json.load(open(ptr, encoding='utf-8'))
    O = {o['id']: o for o in json.load(open(pord, encoding='utf-8'))['ordem']}
    D = json.load(open(pdec, encoding='utf-8'))['E']
    r4 = json.load(open(os.path.join(saida, 'camundongo_r4.json'), encoding='utf-8'))['imagens']
    cl = {}
    for l in open(os.path.join(saida, 'CLASSIFICACAO.txt'), encoding='utf-8'):
        if not l.startswith('#') and l.strip():
            x = l.rstrip('\n').split('\t'); cl[x[0]] = x[2] if len(x) > 2 else ''
    # 1 · integridade
    erros = []
    if T.get('versao') != 'tracador_camundongo_v2': erros.append('versao %s' % T.get('versao'))
    if not (T.get('declaracao') or {}).get('declarou_nao_ter_visto'): erros.append('sem declaracao inicial')
    if T.get('n_fechadas') != len(O): erros.append('fechadas %s de %d' % (T.get('n_fechadas'), len(O)))
    for k, e in T['E'].items():
        if e.get('sha256_imagem') != O[k]['sha256_imagem']: erros.append('sha %s' % k)
    if erros:
        sys.exit('PARADO: ' + '; '.join(erros[:10]))
    nula = R.mascara_nula(L)
    linhas = []; res = {}
    for k, e in sorted(T['E'].items()):
        o = O[k]; nome = o['nome']; arq = o['arquivo']
        mz = np.load(os.path.join(saida, 'mascaras_r4', nome + '.npz'))
        m3 = mz['m3'] if mz['m3'].size else None
        m4 = mz['m4'] if mz['m4'].size else None
        em = rasteriza(e['t'], o) if e['estado'] != 'FECHADA' else np.zeros((L, L), bool)
        dur = (t(e['t_fechou']) - t(e['t_abriu'])).total_seconds() if e.get('t_fechou') else None
        r = {'id': k, 'nome': nome, 'emilio': e['estado'], 'fabio': D[nome]['estado'],
             'filme': cl.get(arq) == 'S', 'cicatrizada': nome in CICATRIZADAS,
             'area_emilio_mm2': float(em.sum() * (R.LADO_1380 / L) ** 2 / R.S_1380 ** 2),
             'area_r4': r4[arq]['area_r4'], 'area_r3': r4[arq]['area_r3'],
             'dice_r4': dice(m4, em) if m4 is not None and em.any() else None,
             'dice_r3': dice(m3, em) if m3 is not None and em.any() else None,
             'dice_nulo': dice(nula, em) if em.any() else None,
             'segundos': dur, 'nota': (e.get('nota') or '').replace('\t', ' ').replace('\n', ' ')}
        res[k] = r; linhas.append(r)
    # 4 · P12.1 e P12.3
    conj = [r for r in linhas if r['fabio'] in ('ok', 'nada') and not r['filme'] and r['emilio'] == 'TRACADA']
    d4 = [r['dice_r4'] for r in conj if r['dice_r4'] is not None]
    med = float(np.median(d4)) if d4 else None
    frac = float(np.mean([x >= LIMIAR for x in d4])) if d4 else None
    v = lambda ok: 'confirmada' if ok else 'FALHOU'
    md = lambda xs: '%.3f' % np.median(xs) if xs else '-'
    S = ['# EMILIO — tracador cego, painel v2', '',
         'tracador: %s · inicio %s · salvo %s · 201 fotos fechadas · declaracao inicial: sim'
         % (T['tracador'], T['inicio'], T['salvo']), '',
         '## Estados do Emilio', '',
         ' · '.join('%s %d' % (s, sum(1 for r in linhas if r['emilio'] == s))
                    for s in ('TRACADA', 'PARCIAL', 'IMAGINADA', 'FECHADA')), '',
         '## Placar (Adendos 36 e 39)', '', '| | criterio | resultado | |', '|---|---|---|---|',
         '| P12.1 Fabio "tracados bons" | mediana Dice(r4, Emilio) >= 0,70 · principal e TRACADA (n = %d) | %s | %s |'
         % (len(d4), '%.3f' % med if med is not None else '-', 'nao avaliavel' if med is None else v(med >= LIMIAR)),
         '| P12.3 Fabio "quase todas certinhas" | >= 80 %% com Dice(r4, Emilio) >= 0,70 · mesmo conjunto | %s | %s |'
         % ('%.0f %%' % (100 * frac) if frac is not None else '-', 'nao avaliavel' if frac is None else v(frac >= 0.80)),
         '', '## Ao lado, sem veredito', '',
         '| conjunto | n | Dice r4 mediano | Dice r3 mediano | Dice nulo mediano |', '|---|---|---|---|---|']
    def bloco(rot, s):
        S.append('| %s | %d | %s | %s | %s |' % (rot, len(s), md([r['dice_r4'] for r in s if r['dice_r4'] is not None]),
                                                md([r['dice_r3'] for r in s if r['dice_r3'] is not None]),
                                                md([r['dice_nulo'] for r in s if r['dice_nulo'] is not None])))
    bloco('principal + TRACADA (o do placar)', conj)
    bloco('com filme + TRACADA', [r for r in linhas if r['fabio'] in ('ok', 'nada') and r['filme'] and r['emilio'] == 'TRACADA'])
    bloco('TODAS as tracadas, incluindo imaginadas (como o trabalho original)', [r for r in linhas if r['emilio'] != 'FECHADA'])
    bloco('so as IMAGINADAS', [r for r in linhas if r['emilio'] == 'IMAGINADA'])
    # 6 · concordancia
    fa = [r['fabio'] in ('ok', 'nada') for r in linhas]; em_ = [r['emilio'] == 'TRACADA' for r in linhas]
    tab = {(a, b): sum(1 for x, y in zip(fa, em_) if x == a and y == b) for a in (True, False) for b in (True, False)}
    S += ['', '## Concordancia de tracabilidade (Fabio x Emilio)', '',
          '| | Emilio TRACADA | Emilio nao |', '|---|---|---|',
          '| Fabio mede (ok/nada) | %d | %d |' % (tab[(True, True)], tab[(True, False)]),
          '| Fabio exclui | %d | %d |' % (tab[(False, True)], tab[(False, False)]),
          '', 'kappa de Cohen: %s' % ('%.3f' % kappa(fa, em_) if kappa(fa, em_) is not None else '-'),
          '', 'Cicatrizadas (Fabio) -> Emilio: ' + ', '.join('%s %s' % (r['nome'], r['emilio']) for r in linhas if r['cicatrizada'])]
    # 7 · tempo
    seg = [r['segundos'] for r in linhas if r['segundos'] is not None]
    tot = (t(T['salvo']) - t(T['inicio'])).total_seconds()
    S += ['', '## Tempo', '',
          'mediana por foto %.1f s · p10 %.1f s · p90 %.1f s · soma das fotos %.1f min · do inicio ao salvo %.1f min'
          % (np.median(seg), np.percentile(seg, 10), np.percentile(seg, 90), sum(seg) / 60, tot / 60)]
    open(os.path.join(saida, 'EMILIO_RELATORIO.md'), 'w', encoding='utf-8').write('\n'.join(S) + '\n')
    cols = ['id', 'nome', 'emilio', 'fabio', 'filme', 'cicatrizada', 'area_emilio_mm2', 'area_r3', 'area_r4',
            'dice_r3', 'dice_r4', 'dice_nulo', 'segundos', 'nota']
    with open(os.path.join(saida, 'emilio_por_imagem.tsv'), 'w', encoding='utf-8') as f:
        f.write('\t'.join(cols) + '\n')
        for r in sorted(linhas, key=lambda r: r['nome']):
            f.write('\t'.join('' if r[c] is None else (('%.4f' % r[c]) if isinstance(r[c], float) else str(r[c])) for c in cols) + '\n')
    print('\n'.join(S))


if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    main(*sys.argv[1:])
