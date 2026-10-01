"""
roda_camundongo.py — driver da rodada do motor v0 congelado no banco de
camundongo (Dryad 10.25338/B84W8Q).

CONGELADO PELA EMENDA 3 do pré-registro (01/10/2026). Escrito, testado em cena
sintética e hasheado ANTES de qualquer byte de imagem do banco ser baixado.

Não contém nenhuma constante do motor v0 e não altera nenhuma. O motor entra
por motor_v0_funcoes.py, extração verbatim de v0_congelado_2026-09-22/rodar.py.

QUATRO ETAPAS, NESTA ORDEM, SEM EXCEÇÃO
  1  detectar  — detector do anel em todas as imagens; grava deteccao.json e,
                 se houver falha, PENDENTES_ESCALA_MANUAL.txt.
  2  medir     — o operador informa o diâmetro do anel em px das pendentes.
                 Obrigatória sempre que a etapa 1 deixar pendência (regra 3.2
                 da Emenda 3). O motor ainda NÃO rodou em imagem nenhuma: o
                 operador não pode ter visto resultado algum.
  3  rodar     — recorte, motor; grava camundongo_v0.json.
  4  relatorio — P1-P4, tabela por dia, IC bootstrap e painel cego da P3;
                 grava CAMUNDONGO_V0_RELATORIO.md. Exige MAPA_FERIDA_DIA.tsv,
                 que vem da convenção de nomes do README e é fixado ANTES da
                 etapa 3 — nunca inferido do resultado.

Uso:
    python roda_camundongo.py detectar <pasta_tiffs> <pasta_saida>
    python roda_camundongo.py medir    <pasta_saida> MEDIDAS.txt
    python roda_camundongo.py rodar     <pasta_tiffs> <pasta_saida>
    python roda_camundongo.py relatorio <pasta_saida>

MEDIDAS.txt: uma linha por imagem,
    nome <TAB> diametro_px <TAB> centro_x_px <TAB> centro_y_px
O centro é obrigatório: a escala sozinha não define o recorte de 24 mm, e o
centro do quadro NÃO serve de substituto. Imagem sem anel visível: escrever
"SEM_ANEL" no lugar dos três números (estrato 3.1).
"""
import os, sys, json, hashlib, datetime
import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from detecta_anel_camundongo import detecta, px_por_mm, ANEL_MM
import motor_v0_funcoes as M

# ---------------------------------------------------------------- constantes
RECORTE_MM = 24.0                      # Emenda 1, item 3
LADO_1380  = 1380                      # quadro de referência
DIAM_MM    = 6.0                       # nominal do punch (Emenda 1, item 4)
S_1380     = LADO_1380 / RECORTE_MM     # 57,5 px/mm por construção
DIAM_EF    = DIAM_MM * S_1380 / 30.0    # 11,5 mm — identidade da reauditoria d3
SEMENTE    = 20260928
BOOT       = 10000
RAZAO_LO, RAZAO_HI = 0.80, 1.25         # faixa de razao_pxmm que não vira linha própria
AREA_SPLINT_MM2 = np.pi * (ANEL_MM / 2) ** 2          # 201,06 mm²
TOL_SPLINT = 0.15                       # |área − 201,06|/201,06 ≤ 0,15 = assinatura P4
EXT = ('.tif', '.tiff')


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def lista(pasta):
    return sorted(f for f in os.listdir(pasta) if f.lower().endswith(EXT))


def abre_rgb8(p):
    """Abre a imagem e PARA se nao for RGB de 8 bits, ou RGBA de 8 bits com
    alfa igual a 255 em TODO pixel (EMENDA 4, 01/10/2026).

    Regra fixada antes do download: formato inesperado -> parado, nunca
    conversao improvisada. `Image.convert('RGB')` num TIFF de 16 bits satura em
    branco, e num TIFF em tons de cinza zera o canal 'verm' (R-(G+B)/2 = 0).
    Os dois estragam em silencio. O modo lido vai para o JSON.

    EMENDA 4: o banco do camundongo e 254 RGBA + 1 RGB, com alfa = 255 em todo
    pixel das 254. Alfa constante em 255 nao carrega informacao: os tres canais
    de cor sao byte a byte os mesmos com ou sem ele. A fatia [:,:,:3] e
    explicita de proposito — `convert('RGB')` do PIL descarta o alfa SEM compor,
    inclusive quando o alfa e diferente de 255, entao ele nao e trava nenhuma.
    Esta funcao e o UNICO ponto do projeto onde o alfa e conferido: na etapa 1 o
    detector recebe o ARRAY daqui e nunca abre arquivo."""
    im = Image.open(p)
    modo = im.mode
    if modo not in ('RGB', 'RGBA'):
        sys.exit('PARADO: %s tem modo PIL %r, esperado RGB ou RGBA de 8 bits.\n'
                 'Formato inesperado nao se converte no improviso — e decisao do '
                 'Fabio, com emenda datada, antes de qualquer medida.' % (os.path.basename(p), modo))
    a = np.asarray(im)
    n_canais = 4 if modo == 'RGBA' else 3
    if a.dtype != np.uint8 or a.ndim != 3 or a.shape[2] != n_canais:
        sys.exit('PARADO: %s tem modo %r, dtype %s e forma %s, esperado uint8 HxWx%d.'
                 % (os.path.basename(p), modo, a.dtype, a.shape, n_canais))
    if modo == 'RGBA':
        alfa = a[:, :, 3]
        amin, amax = int(alfa.min()), int(alfa.max())
        if amin != 255 or amax != 255:
            sys.exit('PARADO: %s e RGBA com alfa entre %d e %d, esperado 255 em todo pixel.\n'
                     'Alfa que nao e constante em 255 carrega informacao, e descarta-lo '
                     'seria alterar a imagem. Decisao do Fabio, com emenda datada.'
                     % (os.path.basename(p), amin, amax))
        a = np.ascontiguousarray(a[:, :, :3])
    return a, modo


def exige_mapa(saida):
    """O mapa ferida-dia vem da convencao de nomes do README e e fixado ANTES
    de qualquer deteccao. A etapa 1 exige o arquivo e grava o SHA-256 dele; a
    etapa 4 recusa se o hash tiver mudado."""
    pm = os.path.join(saida, 'MAPA_FERIDA_DIA.tsv')
    if not os.path.isfile(pm):
        sys.exit('PARADO: falta %s.\nEle vem da convencao de nomes do README, e '
                 'fixado ANTES da etapa 1 e nunca inferido do resultado.' % pm)
    return sha256(pm)


# ------------------------------------------------------------------ etapa 1
def etapa_detectar(pasta, saida):
    os.makedirs(saida, exist_ok=True)
    h_mapa = exige_mapa(saida)
    arqs = lista(pasta)
    print('%d imagens | SHA-256 do mapa %s' % (len(arqs), h_mapa[:16] + '…'))
    reg = {'_meta': {'sha256_mapa_ferida_dia': h_mapa,
                     'quando': datetime.datetime.now().astimezone()
                     .isoformat(timespec='seconds')}}
    for i, a in enumerate(arqs, 1):
        p = os.path.join(pasta, a)
        arr, modo = abre_rgb8(p)
        r = detecta(arr)
        reg[a] = {'arquivo': a, 'sha256': sha256(p), 'modo_pil': modo,
                  'deteccao': r,
                  'px_mm': (px_por_mm(r) if r['ok'] else None),
                  'escala_manual': False}
        print('%4d/%d  %-40s %s' % (i, len(arqs), a,
              ('px/mm %.3f' % px_por_mm(r)) if r['ok'] else 'PENDENTE [%s]' % r['motivo']))
    json.dump(reg, open(os.path.join(saida, 'deteccao_camundongo.json'), 'w'), indent=1)
    pend = [a for a in arqs if not reg[a]['deteccao']['ok']]
    with open(os.path.join(saida, 'PENDENTES_ESCALA_MANUAL.txt'), 'w') as f:
        f.write('# Regra 3.2 da Emenda 3: toda imagem desta lista recebe medida\n'
                '# manual do anel, OBRIGATORIAMENTE, antes de o motor rodar nela.\n'
                '# nome <TAB> diametro_px <TAB> centro_x_px <TAB> centro_y_px   (ou SEM_ANEL)\n')
        for a in pend:
            f.write('%s\t\t\t\n' % a)
    print('\npendentes de escala manual: %d de %d' % (len(pend), len(arqs)))
    return len(pend)


# ------------------------------------------------------------------ etapa 2
def etapa_medir(saida, medidas):
    pj = os.path.join(saida, 'deteccao_camundongo.json')
    reg = json.load(open(pj))
    quando = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
    n_ok = n_sem = 0
    for linha in open(medidas, encoding='utf-8'):
        linha = linha.strip()
        if not linha or linha.startswith('#'):
            continue
        partes = [x.strip() for x in (linha.split('\t') if '\t' in linha
                                      else linha.split())]
        if len(partes) < 2:
            continue
        nome = partes[0]
        if nome not in reg:
            print('ignorado (nao esta na deteccao): %s' % nome); continue
        if partes[1].upper() == 'SEM_ANEL':
            reg[nome]['estrato'] = 'sem escala propria'
            reg[nome]['px_mm'] = None
            reg[nome]['quando_medido'] = quando
            n_sem += 1
        else:
            if len(partes) != 4:
                sys.exit('PARADO: %s precisa de diametro_px, centro_x e centro_y '
                         '(ou SEM_ANEL). Linha: %r' % (nome, linha))
            d, cx, cy = (float(x.replace(',', '.')) for x in partes[1:4])
            reg[nome]['escala_manual'] = True
            reg[nome]['diam_anel_px_manual'] = d
            reg[nome]['centro_manual'] = [cx, cy]
            reg[nome]['px_mm'] = d / ANEL_MM
            reg[nome]['quando_medido'] = quando
            n_ok += 1
    faltam = [a for a, v in reg.items()
              if not a.startswith('_') and not v['deteccao']['ok']
              and not v.get('escala_manual') and v.get('estrato') != 'sem escala propria']
    if faltam:
        sys.exit('PARADO: %d pendencia(s) sem linha em MEDIDAS.txt: %s\n'
                 'Regra 3.2: TODA pendente recebe linha — diametro+centro ou '
                 'SEM_ANEL. Omitir uma seria escolha por imagem.'
                 % (len(faltam), ', '.join(faltam[:5]) + ('…' if len(faltam) > 5 else '')))
    json.dump(reg, open(os.path.join(saida, 'deteccao_camundongo_com_manual.json'), 'w'),
              indent=1)
    print('medidas manuais: %d | marcadas SEM_ANEL: %d | pendencias abertas: 0'
          % (n_ok, n_sem))


# --------------------------------------------------------- recorte (item 3.3)
def recorta(im, cx, cy, pxmm):
    """24 mm centrado no anel -> 1380 -> 700. Se o quadrado nao couber no quadro,
    completa por REPLICACAO DA BORDA (nunca preto, nunca encolhendo o recorte) e
    devolve a fracao de area replicada. Regra 3.3 da Emenda 2."""
    H, W = im.shape[:2]
    lado = int(round(RECORTE_MM * pxmm))
    x0 = int(round(cx - lado / 2)); y0 = int(round(cy - lado / 2))
    esq = max(0, -x0); cima = max(0, -y0)
    dir_ = max(0, (x0 + lado) - W); baixo = max(0, (y0 + lado) - H)
    frac = 1.0 - (max(0, min(W, x0 + lado) - max(0, x0)) *
                  max(0, min(H, y0 + lado) - max(0, y0))) / float(lado * lado)
    if esq or dir_ or cima or baixo:
        im = np.pad(im, ((cima, baixo), (esq, dir_), (0, 0)), mode='edge')
        x0 += esq; y0 += cima
    rec = Image.fromarray(im[y0:y0 + lado, x0:x0 + lado])
    q1380 = rec.resize((LADO_1380, LADO_1380), Image.LANCZOS)
    q700 = q1380.resize((M.L, M.L), Image.LANCZOS)
    return np.asarray(q700.convert('RGB')), float(frac)


def mascara_nula(lado_px):
    """Nulo geometrico da REGRA 4 do pre-registro: circulo do diametro declarado
    (6 mm) no CENTRO DO ANEL. No recorte de 24 mm o centro do anel e o centro do
    quadro por construcao. Devolve a mascara no quadro de trabalho de 700."""
    r_px = (DIAM_MM / 2) * S_1380 * (lado_px / LADO_1380)
    yy, xx = np.mgrid[0:lado_px, 0:lado_px]
    c = (lado_px - 1) / 2.0
    return np.hypot(xx - c, yy - c) <= r_px


def quadrado_central(im):
    """estrato 'sem escala propria': maior quadrado central -> 1380 -> 700"""
    H, W = im.shape[:2]
    lado = min(H, W)
    y0, x0 = (H - lado) // 2, (W - lado) // 2
    q = Image.fromarray(im[y0:y0 + lado, x0:x0 + lado])
    return np.asarray(q.resize((LADO_1380, LADO_1380), Image.LANCZOS)
                       .resize((M.L, M.L), Image.LANCZOS).convert('RGB'))


def roda_motor(rgb, diam, criterio):
    """percorre a grade de 144 do motor congelado; criterio 'prim' ou 'sec'"""
    cache, mel = {}, (-1, None, None)
    k = 1 if criterio == 'prim' else 2
    for gama, can, g, dsl, al, (lo, hi) in M.grade:
        ka = (gama, can)
        if ka not in cache:
            cache[ka] = M.canais[can](M.clareia(rgb, gama))
        kt = (gama, can, g, dsl, al)
        if kt not in cache:
            cache[kt] = M.mapa_t(cache[ka], g, dsl, al, 4, None)
        r = M.anel(cache[kt], lo, hi, 3, None, diam)
        if r is None:
            continue
        if r[k] > mel[0]:
            mel = (r[k], r[0], (gama, can, g, dsl, al, lo, hi))
    return mel


# ------------------------------------------------------------------ etapa 3
def etapa_rodar(pasta, saida):
    pj = os.path.join(saida, 'deteccao_camundongo_com_manual.json')
    if not os.path.isfile(pj):
        pj = os.path.join(saida, 'deteccao_camundongo.json')
    reg = json.load(open(pj))
    # a checagem roda em QUALQUER json carregado, nao so quando falta o manual
    abertas = [a for a, v in reg.items()
               if not a.startswith('_') and not v['deteccao']['ok']
               and not v.get('escala_manual') and v.get('estrato') != 'sem escala propria']
    if abertas:
        sys.exit('PARADO: %d pendencia(s) de escala sem resposta: %s\n'
                 'Regra 3.2: medida manual do anel antes de o motor rodar nela.'
                 % (len(abertas), ', '.join(abertas[:5]) + ('…' if len(abertas) > 5 else '')))

    # razao_pxmm contra a MEDIANA DO BANCO: precisa de todas as escalas antes
    itens = {a: v for a, v in reg.items() if not a.startswith('_')}
    escalas = [v['px_mm'] for v in itens.values() if v['px_mm']]
    med = float(np.median(escalas)) if escalas else None
    print('mediana de px/mm do banco: %s' % ('%.4f' % med if med else '—'))

    res = {}
    for i, (a, v) in enumerate(sorted(itens.items()), 1):
        p = os.path.join(pasta, a)
        im, modo = abre_rgb8(p)
        linha = {'arquivo': a, 'sha256': v['sha256'], 'modo_pil': modo,
                 'escala_manual': bool(v.get('escala_manual')),
                 'diam_anel_px': (v.get('diam_anel_px_manual')
                                  or (v['deteccao'].get('diam_px') if v['deteccao']['ok'] else None)),
                 'px_mm': v['px_mm'], 'motivo_deteccao': v['deteccao'].get('motivo', ''),
                 'centro_px': (v.get('centro_manual') if v.get('escala_manual')
                               else ([v['deteccao']['cx'], v['deteccao']['cy']]
                                     if v['deteccao']['ok'] else None))}
        if v['px_mm'] is None:
            rgb = quadrado_central(im)
            nota, m, aj = roda_motor(rgb, DIAM_EF, 'sec')
            linha.update({'estrato': 'sem escala propria', 'criterio': 'sec',
                          'unidade': 'px2', 'fracao_replicada': 0.0,
                          'razao_pxmm': None})
            if m is None:
                linha.update({'obtida': False, 'area': None, 'nota': None})
            else:
                linha.update({'obtida': True,
                              'area': float(m.sum() * (LADO_1380 / M.L) ** 2),
                              'nota': float(nota), 'ajuste': list(aj),
                              'canal': aj[1], 'componentes': int(_comp(m))})
        else:
            if v.get('escala_manual'):
                cx, cy = v['centro_manual']
            else:
                cx, cy = v['deteccao']['cx'], v['deteccao']['cy']
            rgb, frac = recorta(im, cx, cy, v['px_mm'])
            nota, m, aj = roda_motor(rgb, DIAM_EF, 'prim')
            razao = v['px_mm'] / med if med else None
            linha.update({'estrato': ('recorte incompleto' if frac > 0 else 'normal'),
                          'criterio': 'prim', 'unidade': 'mm2',
                          'fracao_replicada': frac, 'razao_pxmm': razao,
                          'razao_fora_da_faixa': bool(razao is not None and
                                                      not (RAZAO_LO <= razao <= RAZAO_HI))})
            if m is None:
                linha.update({'obtida': False, 'area': None, 'nota': None,
                              'parece_anel_do_splint': None})
            else:
                area = float(m.sum() * (LADO_1380 / M.L) ** 2 / (S_1380 ** 2))
                nulo = mascara_nula(M.L)
                area_nulo = float(nulo.sum() * (LADO_1380 / M.L) ** 2 / (S_1380 ** 2))
                linha.update({'obtida': True, 'area': area, 'nota': float(nota),
                              'ajuste': list(aj), 'canal': aj[1],
                              'componentes': int(_comp(m)),
                              'area_nulo_mm2': area_nulo,
                              'dice_motor_vs_nulo': float(M.dice(m, nulo)),
                              'parece_anel_do_splint':
                                  bool(abs(area - AREA_SPLINT_MM2) / AREA_SPLINT_MM2
                                       <= TOL_SPLINT)})
        res[a] = linha
        # NAO se imprime area, nota, px/mm nem se a medida saiu: isso e a
        # resposta da P3. So o contador. O detalhe vai para o JSON.
        print('\r%4d/%d' % (i, len(itens)), end='', flush=True)

    print()
    saidas = {'_meta': {'quando': datetime.datetime.now().astimezone()
                        .isoformat(timespec='seconds'),
                        'recorte_mm': RECORTE_MM, 'lado_1380': LADO_1380,
                        'diam_nominal_mm': DIAM_MM, 'diam_efetivo_mm': DIAM_EF,
                        's_1380_px_mm': S_1380, 'semente': SEMENTE,
                        'bootstrap': BOOT, 'mediana_pxmm_banco': med,
                        'sha256_motor_origem':
                            '78b193014577a45109771a2b15f3b7ff55663b0bb4312a23980c766fe7161732',
                        'sha256_codigo': _hashes_codigo(),
                        'sha256_mapa_ferida_dia': reg.get('_meta', {})
                            .get('sha256_mapa_ferida_dia'),
                        'versoes': _versoes()},
              'imagens': res}
    pout = os.path.join(saida, 'camundongo_v0.json')
    json.dump(saidas, open(pout, 'w'), indent=1)
    print('\n%s  SHA-256 %s' % (pout, sha256(pout)))
    return saidas


def _hashes_codigo():
    """SHA-256 dos tres .py do caminho da medida, gravados na propria saida"""
    d = {}
    for f in ('detecta_anel_camundongo.py', 'motor_v0_funcoes.py', 'roda_camundongo.py'):
        q = os.path.join(AQUI, f)
        d[f] = sha256(q) if os.path.isfile(q) else None
    return d


def _versoes():
    import platform, numpy, scipy, skimage, PIL
    return {'python': platform.python_version(), 'numpy': numpy.__version__,
            'scipy': scipy.__version__, 'skimage': skimage.__version__,
            'Pillow': PIL.__version__, 'plataforma': platform.platform()}


def _comp(m):
    from scipy import ndimage as ndi
    return ndi.label(m)[1]


def _resumo(l):
    if not l.get('obtida'):
        return 'SEM MEDIDA'
    u = l['unidade']
    s = '%9.2f %s  nota %.3f  %s' % (l['area'], u, l['nota'], l['estrato'])
    if l.get('parece_anel_do_splint'):
        s += '  [assinatura P4: anel do splint]'
    if l.get('razao_fora_da_faixa'):
        s += '  [razao_pxmm fora da faixa]'
    return s


# ------------------------------------------------------------------ etapa 4
def _spearman(x, y):
    """rho de Spearman, sem dependencia externa"""
    def posto(v):
        o = np.argsort(np.argsort(v, kind='stable'), kind='stable').astype(float)
        v = np.asarray(v, float)
        for u in np.unique(v):
            k = v == u
            if k.sum() > 1:
                o[k] = o[k].mean()
        return o
    a, b = posto(x), posto(y)
    a = a - a.mean(); b = b - b.mean()
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d else float('nan')


def etapa_relatorio(saida):
    """P1-P4, tabela por dia, IC bootstrap e painel cego da P3."""
    dados = json.load(open(os.path.join(saida, 'camundongo_v0.json')))
    imgs = dados['imagens']
    pmapa = os.path.join(saida, 'MAPA_FERIDA_DIA.tsv')
    if not os.path.isfile(pmapa):
        sys.exit('PARADO: falta MAPA_FERIDA_DIA.tsv (nome<TAB>dia<TAB>animal<TAB>lado).\n'
                 'Ele vem da convencao de nomes do README e e fixado ANTES da etapa 3.')
    h_agora = sha256(pmapa)
    h_etapa1 = dados['_meta'].get('sha256_mapa_ferida_dia')
    if h_etapa1 and h_agora != h_etapa1:
        sys.exit('PARADO: MAPA_FERIDA_DIA.tsv mudou depois da etapa 1.\n'
                 '  etapa 1: %s\n  agora  : %s\n'
                 'O mapa e fixado antes de qualquer medida e nao se altera depois.'
                 % (h_etapa1, h_agora))
    mapa = {}
    for linha in open(pmapa, encoding='utf-8'):
        if linha.startswith('#') or not linha.strip():
            continue
        c = [x.strip() for x in linha.rstrip('\n').split('\t')]
        if len(c) >= 4:
            mapa[c[0]] = {'dia': int(c[1]), 'animal': c[2], 'lado': c[3]}
    faltam = [a for a in imgs if a not in mapa]
    if faltam:
        sys.exit('PARADO: %d imagens sem linha no mapa (ex.: %s)' % (len(faltam), faltam[:3]))

    rng = np.random.default_rng(SEMENTE)
    def ic(v, f):
        v = np.asarray(v, float)
        if len(v) == 0:
            return (float('nan'), float('nan'))
        b = [f(v[rng.integers(0, len(v), len(v))]) for _ in range(BOOT)]
        return float(np.percentile(b, 2.5)), float(np.percentile(b, 97.5))

    com_anel = [a for a, l in imgs.items() if l['estrato'] != 'sem escala propria']
    obtidas = [a for a in com_anel if imgs[a]['obtida']]
    p1 = len(obtidas) / len(com_anel) if com_anel else float('nan')
    p1_aval = bool(com_anel)
    p1_lo, p1_hi = ic([1.0 if imgs[a]['obtida'] else 0.0 for a in com_anel], np.mean)

    por_dia = {}
    for a in obtidas:
        por_dia.setdefault(mapa[a]['dia'], []).append(imgs[a]['area'])
    dias = sorted(d for d, v in por_dia.items() if len(v) >= 8)
    med_dia = [float(np.median(por_dia[d])) for d in dias]
    p2 = _spearman(dias, med_dia) if len(dias) >= 3 else float('nan')

    modos = {}
    for a, l in imgs.items():
        if not l['obtida']:
            modos[l.get('motivo_deteccao') or 'motor nao devolveu medida'] = \
                modos.get(l.get('motivo_deteccao') or 'motor nao devolveu medida', 0) + 1
    n_splint = sum(1 for a in obtidas if imgs[a].get('parece_anel_do_splint'))
    p4_assin = n_splint / len(obtidas) if obtidas else float('nan')

    # painel cego da P3: pares do mesmo dia, uma plausivel e uma falhada
    plaus = [a for a in obtidas if not imgs[a].get('parece_anel_do_splint')
             and not imgs[a].get('razao_fora_da_faixa')]
    falhou = [a for a, l in imgs.items() if not l['obtida']]
    pares = []
    for a in falhou:
        d = mapa[a]['dia']
        cand = [b for b in plaus if mapa[b]['dia'] == d and b not in [p[1] for p in pares]]
        if cand:
            pares.append((a, cand[int(rng.integers(0, len(cand)))]))
    ordem = rng.permutation(len(pares))
    painel = []
    for i in ordem:
        a, b = pares[i]
        ab = [a, b] if rng.integers(0, 2) == 0 else [b, a]
        painel.append({'par': int(i) + 1, 'A': ab[0], 'B': ab[1],
                       'qual_falhou': 'A' if ab[0] == a else 'B'})
    json.dump({'semente': SEMENTE, 'n_pares': len(painel), 'pares': painel},
              open(os.path.join(saida, 'CHAVE_P3_NAO_ABRIR.json'), 'w'), indent=1)
    with open(os.path.join(saida, 'PAINEL_P3.txt'), 'w', encoding='utf-8') as f:
        f.write('# Painel cego da P3. Para cada par, dizer qual das duas FALHOU e por que.\n'
                '# O revisor nao ve area, nota, px/mm nem estrato.\n')
        for p_ in painel:
            f.write('par %d\tA = %s\tB = %s\tresposta: \tcausa: \n'
                    % (p_['par'], p_['A'], p_['B']))

    linhas = ['| dia | n medidas | área mediana | mínimo | máximo |', '|---|---|---|---|---|']
    for d in sorted(por_dia):
        v = por_dia[d]
        linhas.append('| %d | %d | %.2f | %.2f | %.2f |'
                      % (d, len(v), np.median(v), min(v), max(v)))
    rel = []
    rel.append('# CAMUNDONGO · motor v0 congelado · relatório da rodada\n')
    rel.append('Banco Dryad 10.25338/B84W8Q · %d imagens · motor intocado '
               '(origem SHA-256 %s)\n' % (len(imgs), dados['_meta']['sha256_motor_origem'][:16] + '…'))
    rel.append('Diâmetro nominal %.0f mm · efetivo passado ao motor **%.1f mm** '
               '(s = %.1f px/mm no quadro de 1380) · semente %d · bootstrap %d\n'
               % (DIAM_MM, DIAM_EF, S_1380, SEMENTE, BOOT))
    rel.append('> **Executor declarado:** o pré-registro dizia "executor Opus, no PC '
               'do Fabio". Na prática a rodada é executada pelo **Fabio, no cmd do '
               'seu PC**, com scripts escritos e hasheados pelo Opus e revisados pelo '
               'Fable. Declarado antes do download.\n')
    rel.append('## PREDIÇÕES\n')
    rel.append('| | predição | resultado | |')
    rel.append('|---|---|---|---|')
    if not p1_aval:
        rel.append('| **P1** | medida obtida em ≥ 50 %% das imagens com anel visível | '
                   '**não avaliável** — nenhuma imagem com anel visível (n = 0) | '
                   '⏳ **não avaliável** |')
    else:
        rel.append('| **P1** | medida obtida em ≥ 50 %% das imagens com anel visível | '
                   '**%.1f %%** (%d de %d) · IC95 [%.1f; %.1f] | %s |'
                   % (100 * p1, len(obtidas), len(com_anel), 100 * p1_lo, 100 * p1_hi,
                      '✅ **confirmada**' if p1 >= 0.5 else '❌ **FALHOU**'))
    if len(dias) < 3 or not np.isfinite(p2):
        rel.append('| **P2** | Spearman(dia, área mediana) ≤ −0,8 | '
                   '**não avaliável** — %d dia(s) com n ≥ 8; o coeficiente exige '
                   '≥ 3 | ⏳ **não avaliável** |' % len(dias))
    else:
        rel.append('| **P2** | Spearman(dia, área mediana) ≤ −0,8 | **%.4f** '
                   '(%d dias com n ≥ 8) | %s |'
                   % (p2, len(dias), '✅ **confirmada**' if p2 <= -0.8 else '❌ **FALHOU**'))
    rel.append('| **P3** | revisor cego acerta ≥ 75 %% dos pares | '
               '%s | ⏳ **%s** |'
               % (('painel de %d pares emitido; a preencher' % len(painel)) if painel
                  else 'nenhum par possível — não houve falha para parear (n = 0)',
                  'pendente' if painel else 'não avaliável'))
    rel.append('| **P4** | falha dominante = referência de pele contaminada | '
               'assinatura "anel do splint" em **%s** das obtidas | 📋 **descritiva** |'
               % ('%.1f %%' % (100 * p4_assin) if obtidas else 'não avaliável (n = 0)'))
    rel.append('\n> Três estados, fixados antes do banco: **confirmada** · '
               '**FALHOU** · **não avaliável**, este sempre com o motivo e os '
               'números. "Não avaliável" é resultado publicável: não entra no '
               'placar como confirmação nem como falha. A **P4 é descritiva** e '
               'não tem veredito automático.\n')
    # ---- comparador nulo geometrico, pareado (regra 4 do pre-registro) ----
    par = [(imgs[a]['area'], imgs[a]['area_nulo_mm2']) for a in obtidas
           if imgs[a].get('area_nulo_mm2') is not None]
    rel.append('\n## COMPARADOR NULO GEOMÉTRICO (regra 4 do pré-registro)\n')
    rel.append('Círculo de %.0f mm no centro do anel, pareado por imagem. '
               'Área do nulo: **%.2f mm²** (constante por construção).\n'
               % (DIAM_MM, np.pi * (DIAM_MM / 2) ** 2))
    if len(par) >= 3:
        am = np.array([x[0] for x in par]); an_ = np.array([x[1] for x in par])
        dif = am - an_
        dices = np.array([imgs[a]['dice_motor_vs_nulo'] for a in obtidas
                          if imgs[a].get('dice_motor_vs_nulo') is not None])
        lo, hi = ic(dif, np.median)
        try:
            from scipy.stats import wilcoxon
            pw = float(wilcoxon(am, an_).pvalue)
            spw = '%.4g' % pw
        except Exception:
            spw = 'não calculado'
        rel.append('| | mediana | mínimo | máximo |')
        rel.append('|---|---|---|---|')
        rel.append('| área do motor | %.2f | %.2f | %.2f |' % (np.median(am), am.min(), am.max()))
        rel.append('| área do nulo | %.2f | %.2f | %.2f |' % (np.median(an_), an_.min(), an_.max()))
        rel.append('| diferença (motor − nulo) | %.2f | %.2f | %.2f |'
                   % (np.median(dif), dif.min(), dif.max()))
        rel.append('| Dice motor × nulo | %.4f | %.4f | %.4f |'
                   % (np.median(dices), dices.min(), dices.max()))
        rel.append('\nIC95 da diferença mediana: [%.2f; %.2f] · Wilcoxon pareado p = %s · n = %d\n'
                   % (lo, hi, spw, len(par)))
    else:
        rel.append('**não avaliável** — %d imagem(ns) com nulo pareável; exige ≥ 3.\n' % len(par))

    # ---- estratos descritivos (Emenda 1, item 6) ----
    def tabela(chave, titulo, rot):
        gr = {}
        for a in obtidas:
            gr.setdefault(rot(mapa[a]), []).append(imgs[a]['area'])
        out = ['\n### %s\n' % titulo, '| estrato | n | área mediana | mínimo | máximo |',
               '|---|---|---|---|---|']
        for k in sorted(gr):
            v = gr[k]
            out.append('| %s | %d | %.2f | %.2f | %.2f |'
                       % (k, len(v), np.median(v), min(v), max(v)))
        return out
    rel.append('\n## ESTRATOS DESCRITIVOS (Emenda 1, item 6)\n')
    rel.append('Pré-declarados como **descritivos**: nenhum teste confirmatório '
               'entre estratos nesta rodada.')
    rel.extend(tabela('idade', 'Idade (A × Y)', lambda m_:
                      'A (idoso)' if m_['animal'].upper().startswith('A') else 'Y (jovem)'))
    rel.extend(tabela('lado', 'Lado (L × R)', lambda m_: m_['lado'].upper()))

    rel.append('\n## TABELA POR DIA\n')
    rel.extend(linhas)
    rel.append('\n## MODOS DE FALHA\n')
    for k, v in sorted(modos.items(), key=lambda z: -z[1]):
        rel.append('- %s — %d' % (k or '(sem motivo)', v))
    rel.append('\n## ESTRATOS\n')
    for e in sorted(set(l['estrato'] for l in imgs.values())):
        n = sum(1 for l in imgs.values() if l['estrato'] == e)
        rel.append('- %s — %d' % (e, n))
    n_man = sum(1 for l in imgs.values() if l['escala_manual'])
    n_raz = sum(1 for l in imgs.values() if l.get('razao_fora_da_faixa'))
    rel.append('- escala manual (ato do operador) — %d' % n_man)
    rel.append('- razao_pxmm fora de [%.2f; %.2f] — %d' % (RAZAO_LO, RAZAO_HI, n_raz))
    rel.append('\n*Nenhuma imagem foi excluída. Nenhuma constante do motor foi tocada.*\n')
    prel = os.path.join(saida, 'CAMUNDONGO_V0_RELATORIO.md')
    open(prel, 'w', encoding='utf-8').write('\n'.join(rel))
    pj = os.path.join(saida, 'camundongo_v0.json')
    with open(prel, 'a', encoding='utf-8') as f:
        f.write('\n## HASHES DAS SAÍDAS\n\n')
        f.write('- `camundongo_v0.json` — %s\n' % sha256(pj))
        f.write('- `CAMUNDONGO_V0_RELATORIO.md` — calculado após esta linha, '
                'registrado pelo executor no log.\n')
    print('\n'.join(rel[:14]))
    print('\n%s' % prel)


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    etapa = sys.argv[1]
    if etapa == 'detectar':
        etapa_detectar(sys.argv[2], sys.argv[3])
    elif etapa == 'medir':
        etapa_medir(sys.argv[2], sys.argv[3])
    elif etapa == 'rodar':
        etapa_rodar(sys.argv[2], sys.argv[3])
    elif etapa == 'relatorio':
        etapa_relatorio(sys.argv[2])
    else:
        sys.exit(__doc__)
