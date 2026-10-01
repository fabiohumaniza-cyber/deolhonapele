# EMENDA 3 · pré-registro do camundongo — o driver da rodada
### versão 2 · substitui a de 06h40, antes de confirmação e sem download

**01/10/2026, 07h00 (Brasília). Escrita ANTES de qualquer byte de imagem do banco
Dryad 10.25338/B84W8Q ser baixado ou aberto.**

> **Nota de substituição.** A versão anterior desta emenda, SHA-256
> `5c03d88f16011275ce84d974cc06134d524253ca57960a0df0068aa5ce9fdc11`, foi
> substituída **antes de ter hash confirmado pelo Fabio** e **sem nenhum
> download**, após revisão do Fable que achou seis defeitos no driver — dois
> deles bloqueantes. A versão anterior está no histórico do repositório, commit
> `20fae0d21e6ac5cbe6f7d5e9b48fc1b5d45a6ed4`. Nada do que ela dizia foi apagado:
> o que mudou está na seção 1.

Cadeia: `PRE_REGISTRO` `d0989cf7…` → `EMENDA_1` `161e1d78…` → `EMENDA_2`
**`5af2ca99d59d77b0757958c7138f4f0e78de7d515996f9b982e137ce9bebb8ca`**.
A Emenda 2 **não é alterada por esta**; seu hash segue de pé.

---

## 1 · OS SEIS DEFEITOS E O QUE MUDOU

**🔴 1. A trava da regra 3.2 tinha porta dos fundos.** `medir` processava só o
que estivesse em `MEDIDAS.txt`; e `rodar` só checava pendências **quando o
`_com_manual.json` não existia**. Logo, uma pendente sem linha passava: virava
"sem escala própria" **por omissão**, sem `SEM_ANEL` declarado. Escolha por
imagem, que é exatamente o que esta série de emendas existe para impedir.
→ `medir` **para** se qualquer pendente ficar sem linha; `rodar` **re-checa
pendências em qualquer JSON que carregar**, não só na ausência do manual.

**🔴 2. Profundidade de bits.** `Image.open(...).convert('RGB')` num TIFF de
16 bits **satura tudo em branco**; num TIFF em tons de cinza, R=G=B e o canal
`verm` do motor (`R − (G+B)/2`) **zera**. Os dois estragam em silêncio e a
rodada sairia com números que pareceriam válidos.
→ Função `abre_rgb8`: confere `im.mode` e o dtype, grava `modo_pil` no JSON e
**PARA** se não for RGB de 8 bits. *Formato inesperado não se converte no
improviso — é decisão do Fabio, com emenda datada, antes de qualquer medida.*

**3. "Mapa fixado antes da etapa 3" era promessa, não programa.** A etapa 4 só
conferia se o arquivo existia.
→ A **etapa 1 exige** o `MAPA_FERIDA_DIA.tsv` e grava o SHA-256 dele; a **etapa 4
recusa** se o hash tiver mudado. O mapa passa a ser anterior a qualquer detecção,
não só a qualquer medida.

**4. `teste_driver.py` tinha três caminhos fixos** (linhas 13, 16, 63) — não
rodava no PC do Fabio sem editar, e editar mataria o hash.
→ Tudo relativo a `AQUI`, como o próprio driver já fazia.

**5. `_meta` do JSON era incompleto.**
→ Passa a trazer os **SHA-256 dos três `.py` do caminho da medida**, o hash do
mapa e as **versões** de Python, numpy, scipy, skimage e Pillow, mais a
plataforma. O ambiente do executor fica registrado na saída.

**6. A docstring dizia "TRÊS ETAPAS" e listava quatro.** Corrigida.

**🔴 Um sétimo, achado ao corrigir o quinto: a etapa 3 vazava a resposta da P3.**
Ela imprimia área, nota e estrato por nome de arquivo no console — e o painel da
P3 pede que um revisor cego diga **qual das duas falhou**. Quem acompanhasse a
rodada pelo terminal já teria a resposta.
→ A etapa 3 agora imprime **só o contador** (`17/255`). Todo o detalhe vai para o
JSON. Isso não resolve sozinho a questão de quem é o revisor — ver a seção 4.

---

## 2 · O DRIVER

`roda_camundongo.py` — SHA-256 `0c7c7be2ef9948ad8f75c6b764778f7bf69aaf7d9a4c4624cc382b9838e2813e` (25675 bytes). Verbatim no anexo.

| etapa | o que faz | exige antes | saída |
|---|---|---|---|
| 1 `detectar` | detector da Emenda 2 em todas as imagens | `MAPA_FERIDA_DIA.tsv` · todas RGB 8 bits | `deteccao_camundongo.json` · `PENDENTES_ESCALA_MANUAL.txt` |
| 2 `medir` | diâmetro **e centro** das pendentes, ou `SEM_ANEL` | linha para **toda** pendente | `deteccao_camundongo_com_manual.json` |
| 3 `rodar` | recorte, motor congelado | zero pendência aberta | `camundongo_v0.json` |
| 4 `relatorio` | P1–P4, tabela por dia, IC, painel da P3 | hash do mapa inalterado | `CAMUNDONGO_V0_RELATORIO.md` · `PAINEL_P3.txt` · `CHAVE_P3_NAO_ABRIR.json` |

A regra 3.2 **está na forma do programa**, não na disciplina de quem roda:

> Detector falha → medida manual do anel, **sempre**, antes de o motor rodar
> naquela imagem. Anel não visível → `SEM_ANEL`, estrato 3.1. Sem exceção.
> A medida manual exige **diâmetro em px e centro (x, y)** — a escala sozinha não
> define o recorte de 24 mm, e o centro do quadro não substitui o centro do anel.

**Recorte (3.3).** Fora do quadro → `numpy.pad(mode='edge')`, réplica de borda,
nunca preto, nunca encolhendo; `fracao_replicada` no JSON, estrato
`recorte incompleto`. **Sem escala (3.1).** Maior quadrado central → 1380 → 700,
saída em **px²**, critério **`sec`** do motor congelado. **`razao_pxmm`.** px/mm ÷
mediana do banco; fora de [0,80; 1,25] entra marcada — contada, nunca removida.

**Fixadas aqui, antes de ver o banco:** assinatura da P4 =
|área − 201,06 mm²|/201,06 ≤ **0,15**; "plausível" para o painel da P3 = obtida,
sem assinatura do splint e com razão dentro da faixa.

**Predição não avaliável não é predição falhada.** Se faltarem dias com n ≥ 8, a
P2 sai como **não avaliada**, não como falhada.

---

## 3 · O ENSAIO

`teste_driver.py` — SHA-256 `b49bbdc9bbf5cb14147621b728dc3567a7dfb0c61372f39d990893f7cad56202` (6103 bytes). Banco **sintético** de 24
imagens (3 dias × 8 feridas), desenhado por código, com ferida encolhendo, uma
sem anel e uma com o anel na beira. Semente 20260928.

```
banco sintetico: 24 imagens

=== etapa 1 detectar ===
pendentes de escala manual: 1 de 24


=== etapa 3 SEM a etapa 2 (tem de parar) ===
saiu com codigo 1 | Regra 3.2: medida manual do anel antes de o motor rodar nela.

=== etapa 2 com MEDIDAS.txt incompleto (tem de parar) ===
saiu com codigo 1 | Regra 3.2: TODA pendente recebe linha — diametro+centro ou SEM_ANEL. Omitir uma seria escolha p

=== etapa 2 medir ===
pendentes declarados SEM_ANEL: 1
medidas manuais: 0 | marcadas SEM_ANEL: 1 | pendencias abertas: 0

=== etapa 3 com pendencia reaberta no _com_manual (tem de parar) ===
saiu com codigo 1 | Regra 3.2: medida manual do anel antes de o motor rodar nela.

=== etapa 3 rodar ===
mediana de px/mm do banco: 40.3654

   1/24
…
  24/24

/home/claude/cam/ensaio/saida/camundongo_v0.json  SHA-256 34c7fb38d5c887a98ffa43bfff0a1d412449af4247beb1691d44e38e5b1bd669


=== TIFF de 16 bits (tem de parar) ===
saiu com codigo 1 | Formato inesperado nao se converte no improviso — e decisao do Fabio, com emenda datada, antes 

=== etapa 1 sem o mapa (tem de parar) ===
saiu com codigo 1 | Ele vem da convencao de nomes do README, e fixado ANTES da etapa 1 e nunca inferido do resultad

=== etapa 4 relatorio ===
# CAMUNDONGO · motor v0 congelado · relatório da rodada

Banco Dryad 10.25338/B84W8Q · 24 imagens · motor intocado (origem SHA-256 78b193014577a451…)

Diâmetro nominal 6 mm · efetivo passado ao motor **11.5 mm** (s = 57.5 px/mm no quadro de 1380) · semente 20260928 · bootstrap 10000

## PREDIÇÕES

| | predição | resultado | |
|---|---|---|---|
| **P1** | medida obtida em ≥ 50 % das imagens com anel visível | **100.0 %** (23 de 23) · IC95 [100.0; 100.0] | ✅ **confirmada** |
| **P2** | Spearman(dia, área mediana) ≤ −0,8 | **não avaliável** — só 2 dia(s) com n ≥ 8, e o coeficiente exige 3 | ⏳ **não avaliada** |
| **P3** | revisor cego acerta ≥ 75 % dos pares | painel de 0 pares emitido; a preencher | ⏳ pendente |
| **P4** | falha dominante = referência de pele contaminada | assinatura "anel do splint" em **78.3 %** das obtidas | ver modos abaixo |

## TABELA POR DIA

| dia | n medidas | área mediana | mínimo | máximo |
|---|---|---|---|---|
| 0 | 8 | 189.35 | 29.39 | 195.69 |

/home/claude/cam/ensaio/saida/CAMUNDONGO_V0_RELATORIO.md


--- conferencias do driver ---
imagens com recorte replicado : 1  (fracao max 0.150)
imagens no estrato sem escala : 1  (unidade px2, criterio sec)
imagens com medida obtida     : 24 de 24
painel P3 emitido             : True
```

**Cinco tentativas de furar o protocolo, cinco bloqueios com código 1:** etapa 3
sem a etapa 2 · `MEDIDAS.txt` incompleto · pendência reaberta no JSON manual ·
TIFF de 16 bits · etapa 1 sem o mapa.

🔴 A assinatura do anel do splint aparece em **78,3 %** das imagens do ensaio —
o mesmo que a Emenda 2 viu em 4 de 5 cenas. Continua sendo cena sintética, e
continua não autorizando mexer em nada.

---

## 4 · DECISÃO QUE É DO FABIO, ANTES DO DOWNLOAD

**Quem é o revisor cego da P3?** A etapa 3 não imprime mais nada que vaze a
resposta, mas isso não basta se o revisor for a mesma pessoa que roda. Duas
saídas, e o pré-registro não escolhe entre elas:

- **outra pessoa** preenche o `PAINEL_P3.txt` — o Emílio foi observador 2 no
  porco e já fez esse papel; ou
- **o Fabio preenche o painel ANTES de abrir `camundongo_v0.json` e o
  relatório**, e declara a ordem no log.

Fica registrado que a escolha foi feita antes de qualquer imagem ser vista.

---

## 5 · O QUE CONTINUA VALENDO

Tudo do pré-registro, da Emenda 1 e da Emenda 2: uma rodada · nenhuma exclusão
por resultado · nenhuma constante do v0 tocada · P1–P4 como escritas · estratos
de idade e lado só descritivos · IC bootstrap 10 000, semente 20260928 · diâmetro
efetivo **11,5 mm** pela identidade da reauditoria d3 · dias 7/16/19 do porco
fechados · CWDB intocado · v2 do Zenodo não se publica aqui.

---

## ANEXO · `roda_camundongo.py`, verbatim

```python
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
    """Abre a imagem e PARA se nao for RGB de 8 bits.

    Regra fixada antes do download: formato inesperado -> parado, nunca
    conversao improvisada. `Image.convert('RGB')` num TIFF de 16 bits satura em
    branco, e num TIFF em tons de cinza zera o canal 'verm' (R-(G+B)/2 = 0).
    Os dois estragam em silencio. O modo lido vai para o JSON."""
    im = Image.open(p)
    modo = im.mode
    if modo != 'RGB':
        sys.exit('PARADO: %s tem modo PIL %r, esperado RGB de 8 bits.\n'
                 'Formato inesperado nao se converte no improviso — e decisao do '
                 'Fabio, com emenda datada, antes de qualquer medida.' % (os.path.basename(p), modo))
    a = np.asarray(im)
    if a.dtype != np.uint8 or a.ndim != 3 or a.shape[2] != 3:
        sys.exit('PARADO: %s tem dtype %s e forma %s, esperado uint8 HxWx3.'
                 % (os.path.basename(p), a.dtype, a.shape))
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
                linha.update({'obtida': True, 'area': area, 'nota': float(nota),
                              'ajuste': list(aj), 'canal': aj[1],
                              'componentes': int(_comp(m)),
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
    rel.append('## PREDIÇÕES\n')
    rel.append('| | predição | resultado | |')
    rel.append('|---|---|---|---|')
    if not p1_aval:
        rel.append('| **P1** | medida obtida em ≥ 50 %% das imagens com anel visível | '
                   '**não avaliável** — nenhuma imagem com anel visível | '
                   '⏳ **não avaliada** |')
    else:
        rel.append('| **P1** | medida obtida em ≥ 50 %% das imagens com anel visível | '
                   '**%.1f %%** (%d de %d) · IC95 [%.1f; %.1f] | %s |'
                   % (100 * p1, len(obtidas), len(com_anel), 100 * p1_lo, 100 * p1_hi,
                      '✅ **confirmada**' if p1 >= 0.5 else '❌ **FALHOU**'))
    if len(dias) < 3 or not np.isfinite(p2):
        rel.append('| **P2** | Spearman(dia, área mediana) ≤ −0,8 | '
                   '**não avaliável** — só %d dia(s) com n ≥ 8, e o coeficiente '
                   'exige 3 | ⏳ **não avaliada** |' % len(dias))
    else:
        rel.append('| **P2** | Spearman(dia, área mediana) ≤ −0,8 | **%.4f** '
                   '(%d dias com n ≥ 8) | %s |'
                   % (p2, len(dias), '✅ **confirmada**' if p2 <= -0.8 else '❌ **FALHOU**'))
    rel.append('| **P3** | revisor cego acerta ≥ 75 %% dos pares | '
               'painel de %d pares emitido; a preencher | ⏳ pendente |' % len(painel))
    rel.append('| **P4** | falha dominante = referência de pele contaminada | '
               'assinatura "anel do splint" em **%s** das obtidas | ver modos abaixo |'
               % ('%.1f %%' % (100 * p4_assin) if obtidas else 'não avaliável'))
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
```

---

*Escrita pelo Opus em 01/10/2026, sobre a segunda revisão do Fable. Nenhuma
imagem do banco foi baixada, aberta ou inspecionada até esta linha.*
