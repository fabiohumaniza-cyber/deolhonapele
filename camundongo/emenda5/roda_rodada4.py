"""
roda_rodada4.py — RODADA 4: o motor v0 congelado vendo o campo declarado
(CAMPO.txt, Adendo 15) MAIS a declaracao do operador (conta-gotas e artefato),
gravada na declaracao_camundongo_v8.html e salva em declaracao_camundongo_r4.json.

NENHUMA LINHA DO MOTOR MUDA. Importa roda_rodada3.py (72cfb5cc...), que importa
roda_camundongo.py, motor_v0_funcoes.py e roda_rodada2.py, todos congelados.

O QUE A DECLARACAO FAZ — e so isso
  coordenadas: pixel da VISTA; ponto no quadro de 700 = (vx0 + x, vy0 + y)
  (conferido por confere_declaracao.py, 41fad00b..., nas 56 com correcao:
   todas cairam no mesmo lugar, dif media 1,37 a 2,23 de 4,0 aceitos).
  conta-gotas ('corr'): PINTA os pixels do traco com a cor escolhida, como a
      pagina desenha (linha de largura 2r, ponta e juncao redondas; 1 ponto =
      disco de raio r). A imagem que o motor recebe muda so ali.
  artefato ('art'): cada toque e um disco (x, y, r). A uniao dos discos entra
      no `ar` do recorte circunscrito, junto com os 4 cantos fora do campo.
      O motor nao usa esses pixels nem para a pele de referencia nem para a
      banda candidata (mesmo mecanismo da rodada 3).
  setas e nota: o driver NAO usa.

CADA IMAGEM RODA DUAS VEZES, na mesma execucao:
  r3: sem a declaracao (identico a rodada 3);
  r4: com a declaracao.
Isso mede o EFEITO DA CORRECAO imagem por imagem (Dice entre as duas mascaras,
diferenca de area) e serve de trava: nas imagens sem correcao, r4 tem de ser
IGUAL a r3, e a area r3 tem de bater com camundongo_r3.json. Se nao bater, PARA.

Roda as 201 com campo, em TODOS os estados (ok, nada, NAO_TRACAVEL, PELO,
BORDA_PARCIAL). Quem entra em qual braco e decidido no analisa_rodada4.py.

BORDA FALSA: para cada imagem com artefato, fracao dos pixels de contorno da
mascara r4 que ficam a <= 2 px de um pixel de artefato (dentro do campo).
E a medida de quanto o motor seguiu a beirada da pintura em vez da ferida.

Uso:
    python roda_rodada4.py sintetico
    python roda_rodada4.py rodar <pasta_tiffs> <pasta_saida> <declaracao_r4.json>
"""
import os, sys, json, time, hashlib, warnings
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

import roda_camundongo as R
import motor_v0_funcoes as M
import roda_rodada2 as R2
import roda_rodada3 as R3

L = M.L
TOL_CAMPO = 0.05      # px: campo do JSON (vista) + (vx0, vy0) contra CAMPO.txt
TOL_AREA = 1e-6       # mm2: r3 refeito contra camundongo_r3.json
VIZ_BF = 2            # px: vizinhanca da borda falsa


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


# ------------------------------------------------------------ declaracao -> quadro de 700
def pinta_corr(rgb700, corr, vx0, vy0):
    """conta-gotas: pinta no quadro de 700, como a pagina e como o confere_declaracao."""
    if not corr:
        return rgb700
    img = Image.fromarray(rgb700)
    d = ImageDraw.Draw(img)
    for k in corr:
        r = float(k['r']); cor = tuple(int(c) for c in k['cor'])
        pts = [(x + vx0, y + vy0) for x, y in k['pts']]
        if len(pts) > 1:
            d.line(pts, fill=cor, width=max(1, int(round(2 * r))), joint='curve')
        for x, y in pts:
            d.ellipse([x - r, y - r, x + r, y + r], fill=cor)
    return np.asarray(img).copy()


def mascara_art(art, vx0, vy0):
    """artefato: uniao dos discos, no quadro de 700."""
    m = np.zeros((L, L), bool)
    if not art:
        return m
    img = Image.new('L', (L, L), 0)
    d = ImageDraw.Draw(img)
    for t in art:
        x, y, r = t['x'] + vx0, t['y'] + vy0, t['r']
        d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    return np.asarray(img) > 0


def roda_campo_art(rgb700, campo, art700):
    """igual a roda_rodada3.roda_campo, com o artefato somado ao `ar`."""
    cx, cy, rb, rc = campo
    sub, ar, (x0, y0) = R3.recorte_campo(rgb700, cx, cy, rc)
    if art700.any():
        lado = sub.shape[0]
        pad = max(0, -x0, -y0, x0 + lado - L, y0 + lado - L)
        a = np.pad(art700, pad) if pad else art700
        ar = ar | a[y0 + pad:y0 + pad + lado, x0 + pad:x0 + pad + lado]
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        nota, m, aj = R2.roda_motor_ar(sub, R.DIAM_EF, 'prim', ar)
    if m is None:
        return None, None, None
    return nota, R3.volta_ao_700(m, x0, y0), aj


def borda_falsa(m, art700, campo):
    cx, cy, rb, rc = campo
    yy, xx = np.mgrid[0:L, 0:L]
    dentro = np.hypot(xx - cx, yy - cy) <= rc
    a = art700 & dentro
    if m is None or not a.any():
        return None
    cont = m & ~ndimage.binary_erosion(m)
    n = int(cont.sum())
    if n == 0:
        return None
    perto = ndimage.binary_dilation(a, iterations=VIZ_BF)
    return float((cont & perto).sum() / n)


def area_mm2(m):
    return float(m.sum() * (R.LADO_1380 / L) ** 2 / (R.S_1380 ** 2))


# ------------------------------------------------------------ ensaio sintetico
def ensaio(n=30):
    """Trava 1: sem declaracao, a rodada 4 tem de dar EXATAMENTE a rodada 3.
    Trava 2: um disco de artefato declarado num quadrante. Quando ele cai FORA
    da ferida, a mascara nao pode entrar nele. Quando cai EM CIMA da ferida, o
    motor fecha a mascara por cima (preenchimento) e a ferida continua achada:
    o artefato nao abre buraco na ferida. As duas contagens saem separadas."""
    rng = np.random.default_rng(20260928)
    iguais = 0; fora_do_art = 0; art_fora_da_ferida = 0; art_na_ferida = 0
    ferida_ok_com_art_em_cima = 0; t0 = time.time()
    for i in range(n):
        rgb, fer = R2.cena(rng)
        rb = 4.3 * R2.PXMM; rc = rb - 0.3 * R2.PXMM
        campo = (R2.C0, R2.C0, rb, rc)
        _, m3, _ = R3.roda_campo(rgb, campo)
        _, m4, _ = roda_campo_art(rgb, campo, np.zeros((L, L), bool))
        if (m3 is None and m4 is None) or (m3 is not None and m4 is not None and np.array_equal(m3, m4)):
            iguais += 1
        # artefato declarado num quadrante: o motor nao pode por mascara la
        art = np.zeros((L, L), bool)
        yy, xx = np.mgrid[0:L, 0:L]
        art[(np.hypot(xx - (R2.C0 + 60), yy - (R2.C0 - 60)) < 25)] = True
        _, ma, _ = roda_campo_art(rgb, campo, art)
        sobre_ferida = (art & fer).any()
        if sobre_ferida:
            art_na_ferida += 1
            if ma is not None and M.dice(ma, fer) >= 0.5:
                ferida_ok_com_art_em_cima += 1
        else:
            art_fora_da_ferida += 1
            if ma is None or not (ma & art).any():
                fora_do_art += 1
        print('\r%2d/%d  %.0f s  iguais %d' % (i + 1, n, time.time() - t0, iguais), end='', flush=True)
    print()
    print('RESUMO', json.dumps({'n': n, 'sem_declaracao_igual_a_r3': iguais,
                               'artefato_fora_da_ferida': art_fora_da_ferida,
                               'nesses_mascara_nao_entra_no_artefato': fora_do_art,
                               'artefato_em_cima_da_ferida': art_na_ferida,
                               'nesses_ferida_achada_dice_ge_0_5': ferida_ok_com_art_em_cima}))


# ------------------------------------------------------------ rodada
def uma(pasta, nome, v, campo_n, ref_area, e):
    """Uma imagem: r3 (sem declaracao) e r4 (com declaracao). PARA nas travas."""
    im, _ = R.abre_rgb8(os.path.join(pasta, nome))
    rgb, _ = R.recorta(im, v['centro_px'][0], v['centro_px'][1], v['px_mm'])
    cx, cy, rb, rc = campo_n
    area_campo = np.pi * rc * rc * (R.LADO_1380 / L) ** 2 / (R.S_1380 ** 2)
    # r3: sem declaracao
    _, m3, _ = R3.roda_campo(rgb, campo_n)
    a3 = area_mm2(m3) if m3 is not None else None
    if (a3 is None) != (ref_area is None) or (a3 is not None and abs(a3 - ref_area) > TOL_AREA):
        sys.exit('PARADO: %s — r3 refeito (%s) difere de camundongo_r3.json (%s)' % (nome, a3, ref_area))
    # r4: com declaracao
    rgb4 = pinta_corr(rgb, e.get('corr', []), e['vx0'], e['vy0'])
    art = mascara_art(e.get('art', []), e['vx0'], e['vy0'])
    n4, m4, aj4 = roda_campo_art(rgb4, campo_n, art)
    sem_decl = not e.get('corr') and not e.get('art')
    if sem_decl and not ((m3 is None and m4 is None) or
                         (m3 is not None and m4 is not None and np.array_equal(m3, m4))):
        sys.exit('PARADO: %s — sem declaracao, r4 difere de r3' % nome)
    yy, xx = np.mgrid[0:L, 0:L]
    dentro = np.hypot(xx - cx, yy - cy) <= rc
    pint = np.any(rgb4 != rgb, axis=2)
    d = {'arquivo': nome, 'estado': e['estado'], 'unidade': 'mm2',
         'area_r3': a3, 'area_r4': area_mm2(m4) if m4 is not None else None,
         'obtida_r3': m3 is not None, 'obtida_r4': m4 is not None,
         'area_campo_mm2': float(area_campo),
         'frac_campo_conta_gotas': float((pint & dentro).sum() / dentro.sum()),
         'frac_campo_artefato': float((art & dentro).sum() / dentro.sum()),
         'n_corr': len(e.get('corr', [])), 'n_art': len(e.get('art', []))}
    if m3 is not None and m4 is not None:
        d['dice_r3_r4'] = float(M.dice(m3, m4))
    if m4 is not None:
        d['nota_r4'] = float(n4); d['ajuste_r4'] = list(aj4)
        d['frac_do_campo_r4'] = float(d['area_r4'] / area_campo)
        d['dice_r4_vs_nulo'] = float(M.dice(m4, R.mascara_nula(L)))
        d['borda_falsa'] = borda_falsa(m4, art, campo_n)
    return d, m3, m4, art


def rodar(pasta, saida, pdec):
    v0 = json.load(open(os.path.join(saida, 'camundongo_v0.json'), encoding='utf-8'))['imagens']
    campo = R2.le_campo(os.path.join(saida, 'CAMPO.txt'))
    r3j = json.load(open(os.path.join(saida, 'camundongo_r3.json'), encoding='utf-8'))['imagens']
    E = json.load(open(pdec, encoding='utf-8'))['E']
    nomes = sorted(n for n in v0 if v0[n].get('px_mm') and n in campo)
    chave = lambda arq: os.path.splitext(arq)[0]
    falta = [n for n in nomes if chave(n) not in E]
    if falta or len(E) != len(nomes):
        sys.exit('PARADO: declaracao com %d imagens, campo com %d; faltam %s' % (len(E), len(nomes), falta[:5]))
    # trava: campo do JSON (coordenada da vista) + vista = CAMPO.txt
    for n in nomes:
        e = E[chave(n)]
        cx, cy, rb, rc = campo[n]
        jx, jy, jr = e['campo']
        if abs(jx + e['vx0'] - cx) > TOL_CAMPO or abs(jy + e['vy0'] - cy) > TOL_CAMPO or abs(jr - rc) > TOL_CAMPO:
            sys.exit('PARADO: %s — campo da declaracao nao bate com CAMPO.txt' % n)
    pmasc = os.path.join(saida, 'mascaras_r4')
    if os.path.exists(pmasc):
        sys.exit('PARADO: %s ja existe. Rodada nova vai para pasta nova.' % pmasc)
    os.makedirs(pmasc)
    vazio = np.zeros((0, 0), bool)
    res = {}; t0 = time.time()
    for i, nome in enumerate(nomes, 1):
        d, m3, m4, art = uma(pasta, nome, v0[nome], campo[nome], r3j[nome].get('area'), E[chave(nome)])
        res[nome] = d
        np.savez_compressed(os.path.join(pmasc, chave(nome) + '.npz'),
                            m3=m3 if m3 is not None else vazio, m4=m4 if m4 is not None else vazio, art=art)
        dt = time.time() - t0
        print('\r%4d/%d  %4.0f min restantes' % (i, len(nomes), dt / i * (len(nomes) - i) / 60), end='', flush=True)
    print()
    meta = {'rodada': 4, 'campo': 'CAMPO.txt, recorte circunscrito + ar = cantos + artefato; conta-gotas pintado',
            'quando': time.strftime('%Y-%m-%dT%H:%M:%S%z'),
            'sha_codigo': {'roda_rodada4.py': sha(__file__), 'roda_rodada3.py': sha(R3.__file__),
                           'roda_rodada2.py': sha(R2.__file__), 'roda_camundongo.py': sha(R.__file__),
                           'motor_v0_funcoes.py': sha(M.__file__)},
            'sha_entrada': {'CAMPO.txt': sha(os.path.join(saida, 'CAMPO.txt')),
                            'camundongo_v0.json': sha(os.path.join(saida, 'camundongo_v0.json')),
                            'camundongo_r3.json': sha(os.path.join(saida, 'camundongo_r3.json')),
                            os.path.basename(pdec): sha(pdec)}}
    json.dump({'_meta': meta, 'imagens': res},
              open(os.path.join(saida, 'camundongo_r4.json'), 'w', encoding='utf-8'),
              indent=1, ensure_ascii=False)
    print('gravado: camundongo_r4.json  (%d imagens)' % len(res))


if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == 'sintetico':
        ensaio()
    elif len(sys.argv) == 5 and sys.argv[1] == 'rodar':
        rodar(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        sys.exit(__doc__)
