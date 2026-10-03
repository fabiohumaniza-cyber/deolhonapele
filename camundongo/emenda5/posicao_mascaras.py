"""
posicao_mascaras.py — ONDE estao as mascaras da rodada 1, em relacao a coroa
da rodada 2 e ao campo declarado da rodada 3.

POR QUE EXISTE
Adendo 14, secao 11, item 1: antes da rodada 2, registrar uma previsao numerica
de quanto ela corrige. A rodada 2 exclui a coroa de 145,83 a 233,33 px (5 a
8 mm) no quadro de 700. Se a mascara da rodada 1 estava na coroa, a rodada 2
tira o candidato do motor; se estava fora (pelo no canto), nao tira.

NAO MEDE NADA NOVO E NAO ALTERA NADA. Importa o roda_camundongo.py (8c1f6e4d...)
e chama recorta() e roda_motor() exatamente como a etapa 3 chamou. Antes de
usar cada mascara, CONFERE que a area dela e a area gravada no
camundongo_v0.json (baf4671f...). Se uma so diferir, PARA: nao seria a mascara
da rodada 1.

So le: camundongo_v0.json e CAMPO.txt (91160713...). So escreve:
<saida>/POSICAO_MASCARAS.tsv e <saida>/POSICAO_MASCARAS_RESUMO.txt.

ZONAS (raio a partir do centro do quadro, 349,5 px)
  buraco   r < 145,83 px     (dentro de 5 mm)
  coroa    145,83 <= r <= 233,33   (5 a 8 mm) — o que a rodada 2 exclui
  fora     r > 233,33 px     (alem do splint: pelo, pele, campo)
E, com o CAMPO.txt (centro e raio do operador, por imagem):
  campo    dentro do amarelo — o que a rodada 3 deixa o motor ver
  faixa    entre o verde do operador e os 5 mm — laranja visivel que a
           coroa da rodada 2 NAO cobre

Uso:
    python posicao_mascaras.py <pasta_tiffs> <pasta_saida>
"""
import os, sys, json, time
import numpy as np

import roda_camundongo as R
import motor_v0_funcoes as M

L = M.L
C0 = (L - 1) / 2.0
PXMM = R.S_1380 * L / R.LADO_1380            # 29,1667 px/mm no quadro de 700
R_IN = 5.0 * PXMM                             # 145,83
R_OUT = 8.0 * PXMM                            # 233,33
TOL = 1e-6


def le_campo(p):
    c = {}
    for l in open(p, encoding='utf-8'):
        if l.startswith('#') or not l.strip():
            continue
        x = l.rstrip('\n').split('\t')
        if len(x) >= 9:
            c[x[0]] = x                       # vale a ultima linha
    return c


def main(pasta, saida):
    js = json.load(open(os.path.join(saida, 'camundongo_v0.json'), encoding='utf-8'))
    reg = js['imagens']
    campo = le_campo(os.path.join(saida, 'CAMPO.txt'))
    nomes = sorted(n for n, v in reg.items() if v.get('px_mm'))
    yy, xx = np.mgrid[0:L, 0:L]
    rr = np.hypot(xx - C0, yy - C0)
    z_bur, z_cor, z_for = rr < R_IN, (rr >= R_IN) & (rr <= R_OUT), rr > R_OUT

    cab = ['nome', 'obtida', 'area_mm2', 'dice_nulo', 'px_mask',
           'f_buraco', 'f_coroa', 'f_fora', 'zona', 'f_campo', 'f_faixa',
           'estado_campo', 'r_borda_mm', 'faixa_mm']
    out = open(os.path.join(saida, 'POSICAO_MASCARAS.tsv'), 'w', encoding='utf-8')
    out.write('\t'.join(cab) + '\n')
    t0 = time.time()
    linhas = []
    for i, nome in enumerate(nomes, 1):
        v = reg[nome]
        im, _ = R.abre_rgb8(os.path.join(pasta, nome))
        cx, cy = v['centro_px']
        rgb, _ = R.recorta(im, cx, cy, v['px_mm'])
        _, m, _ = R.roda_motor(rgb, R.DIAM_EF, v.get('criterio', 'prim'))

        if m is None:
            if v.get('obtida'):
                sys.exit('PARADO: %s — o JSON diz obtida, a reexecucao nao' % nome)
            d = {'nome': nome, 'obtida': 'N'}
        else:
            area = float(m.sum() * (R.LADO_1380 / L) ** 2 / (R.S_1380 ** 2))
            if v.get('area') is None or abs(area - v['area']) > TOL:
                sys.exit('PARADO: %s — area reexecutada %.6f, JSON %s. Nao e a '
                         'mascara da rodada 1.' % (nome, area, v.get('area')))
            n = float(m.sum())
            fb, fc, ff = (m & z_bur).sum() / n, (m & z_cor).sum() / n, (m & z_for).sum() / n
            zona = max((fb, 'buraco'), (fc, 'coroa'), (ff, 'fora'))[1] \
                if max(fb, fc, ff) > 0.5 else 'misto'
            d = {'nome': nome, 'obtida': 'S', 'area_mm2': '%.4f' % area,
                 'dice_nulo': '%.4f' % v.get('dice_motor_vs_nulo', float('nan')),
                 'px_mask': '%d' % n, 'f_buraco': '%.4f' % fb,
                 'f_coroa': '%.4f' % fc, 'f_fora': '%.4f' % ff, 'zona': zona}
            c = campo.get(nome)
            if c is not None:
                d['estado_campo'] = c[8]
                if c[8] == 'ok':
                    ccx, ccy, rb, rc = map(float, c[1:5])
                    rcam = np.hypot(xx - ccx, yy - ccy)
                    em_campo = rcam <= rc
                    faixa = (rcam > rb) & (rr < R_IN)
                    d.update({'f_campo': '%.4f' % ((m & em_campo).sum() / n),
                              'f_faixa': '%.4f' % ((m & faixa).sum() / n),
                              'r_borda_mm': '%.3f' % (rb / PXMM),
                              'faixa_mm': '%.3f' % ((R_IN - rb) / PXMM)})
        out.write('\t'.join(str(d.get(k, '')) for k in cab) + '\n')
        out.flush()
        linhas.append(d)
        dt = time.time() - t0
        print('\r%4d/%d  %4.0f min restantes' % (i, len(nomes), dt / i * (len(nomes) - i) / 60),
              end='', flush=True)
    out.close()
    print()

    # ---------------------------------------------------------------- resumo
    def conta(sub, rot):
        z = [d.get('zona', 'sem_mascara') for d in sub]
        s = '%s (n=%d): ' % (rot, len(sub))
        return s + '  '.join('%s %d' % (k, z.count(k))
                             for k in ('buraco', 'coroa', 'fora', 'misto', 'sem_mascara'))

    ob = [d for d in linhas if d['obtida'] == 'S']
    dz = [d for d in ob if float(d['dice_nulo']) == 0.0]
    dp = [d for d in ob if float(d['dice_nulo']) > 0.0]
    fc = [d for d in ob if d.get('f_campo')]
    mais_campo = sum(float(d['f_campo']) > 0.5 for d in fc)
    tocou_faixa = sum(float(d['f_faixa']) > 0.0 for d in fc)
    fx = sorted(float(d['faixa_mm']) for d in fc)
    res = ['POSICAO DAS MASCARAS DA RODADA 1 — gerado por posicao_mascaras.py',
           'imagens com escala: %d   com mascara: %d   todas reproduzidas (area = JSON)'
           % (len(linhas), len(ob)),
           'zona = onde esta MAIS DA METADE dos pixels da mascara; "misto" se nenhuma passa de 50 %',
           '', conta(dz, 'Dice zero'), conta(dp, 'Dice > 0'), conta(ob, 'todas'),
           '', 'com campo declarado (ok): %d' % len(fc),
           '  mascara com mais da metade DENTRO do campo amarelo: %d' % mais_campo,
           '  mascara que toca a faixa laranja entre o verde e os 5 mm: %d' % tocou_faixa]
    if fx:
        res.append('  largura dessa faixa (5 mm - r_borda): min %.2f  mediana %.2f  max %.2f mm'
                   % (fx[0], fx[len(fx) // 2], fx[-1]))
    t = '\n'.join(res) + '\n'
    open(os.path.join(saida, 'POSICAO_MASCARAS_RESUMO.txt'), 'w', encoding='utf-8').write(t)
    print(t)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
