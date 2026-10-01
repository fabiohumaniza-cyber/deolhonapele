# EMENDA 2 · pré-registro do camundongo — o detector do anel

**01/10/2026, 06h05 (Brasília). Escrita ANTES de qualquer byte de imagem do banco
Dryad 10.25338/B84W8Q ser baixado ou aberto.**

Pré-registro: `PRE_REGISTRO_CAMUNDONGO_30SET.md`, SHA-256
`d0989cf7a2ff8ad1185744f4afca4b3c3071119401f844b7cd52281ac9dac9a8` — conferido.
Emenda 1: `EMENDA_1_CAMUNDONGO_30SET.md`, SHA-256
`161e1d789d20509591935457df9dd28e5502346072dbb24fb24929af2b7d053d` — conferido.
Ambos lidos na íntegra; nada neles é alterado por esta emenda.

---

## 0 · OS CINCO ARQUIVOS DESTA EMENDA

| arquivo | bytes | SHA-256 | onde fica | o que e |
|---|---|---|---|---|
| `EMENDA_2_CAMUNDONGO_01OUT.md` | — | (o deste documento) | `07_PARA_O_FABLE\2026-10-01\` | esta emenda |
| `detecta_anel_camundongo.py` | 9425 | `56f1b4341d68d09e4398176f9da0fd8ce52dbe5fa5538fce0b70fded340d6ca7` | `06_MOTOR_DE_REGISTRO\` | **codigo novo**, escrito para esta rodada |
| `motor_v0_funcoes.py` | 2917 | `1602849373157ec849cef1ff3a39b75a797f85ad4f0b8adedfb810719ae4d224` | `06_MOTOR_DE_REGISTRO\` | **extracao verbatim** do motor congelado (ver abaixo) |
| `teste_sintetico.py` | 5842 | `16ff3d27a7d8045c3c0ef24767be4677ade0f9dece5603ca45b284593db6a864` | `06_MOTOR_DE_REGISTRO\` | **codigo novo**, prova do detector |
| `teste_cadeia.py` | 4277 | `d728933e1fd77be7838d42e1a4e4f5ea9b9b7d2a7655b34883b62fa940451e69` | `06_MOTOR_DE_REGISTRO\` | **codigo novo**, prova da cadeia |

⚠️ **Nenhum destes arquivos entra em `v0_congelado_2026-09-22\`.** A pasta
congelada nao recebe arquivo novo, nem o `motor_v0_funcoes.py`. Eles ficam um
nivel acima, em `06_MOTOR_DE_REGISTRO\`, como o `roda_v0.py` ja fica.

### `motor_v0_funcoes.py` — de onde saiu, exatamente

Nao e codigo novo e nao e reescrita. E **extracao mecanica, verbatim**, de
`06_MOTOR_DE_REGISTRO\v0_congelado_2026-09-22\rodar.py`, SHA-256
`78b193014577a45109771a2b15f3b7ff55663b0bb4312a23980c766fe7161732`.

O metodo da extracao: `ast.get_source_segment` sobre a arvore sintatica do
arquivo de origem, recortando os blocos `L`, `clareia`, `verm`, `lstar`,
`mapa_t`, `anel`, `dice`, `canais` e `grade`. **Nenhuma linha foi digitada,
reordenada ou alterada**; o cabecalho do arquivo gerado registra o hash da
origem. O arquivo de origem **nao foi tocado** — segue com o hash acima, dentro
do zip `MOTOR_v0_congelado.zip` registrado no INPI (`BR 51 2026 008413-0`).

Por que existe: o `rodar.py` congelado e, alem do motor, um *driver* do held-out
do dia 3, com `np.load` de caminhos daquela rodada no corpo do modulo. Importa-lo
inteiro executaria aquele driver. A extracao isola as funcoes **sem reescrever
nenhuma delas** — e e conferivel: reexecutar a extracao sobre o mesmo
`rodar.py` tem de devolver byte a byte o mesmo `motor_v0_funcoes.py`.

---

## POR QUE ESTA EMENDA EXISTE

A Emenda 1 fixa **o que** medir: *"círculo/elipse ajustado ao anel de 16 mm…
px/mm = diâmetro ajustado em px ÷ 16"*. Não fixa **como achar o anel**.

Achar o anel é código novo, no caminho da medida, que não existe no motor
congelado e não estava em nenhum arquivo com hash. Escrito depois de abrir a
primeira imagem do banco, ele deixa de ser cego: toda escolha — método de borda,
limiar, tolerância de excentricidade, critério de aceitação — passaria a ser
informada pelo que o executor viu. É o mesmo vazamento que a P4 de 29/09 expôs
no painel do porco, e que o item 5 do pré-registro proíbe.

Esta emenda fecha o buraco: o detector é escrito, testado e **hasheado antes do
download**, e passa a ser peça auditável como o resto da cadeia.

---

## 1 · O DETECTOR

Arquivo `detecta_anel_camundongo.py` — SHA-256 `56f1b4341d68d09e4398176f9da0fd8ce52dbe5fa5538fce0b70fded340d6ca7` (9425 bytes).
Código verbatim ao final desta emenda.

**Princípio.** O protocolo manda medir o **anel externo**. A cena tem até três
curvas concêntricas — o externo do splint (16 mm), a parede interna (10 mm) e a
ferida de punch (6 mm). O detector, portanto, não procura "um" anel: extrai
candidatas e escolhe, entre as concêntricas, **a de maior eixo com apoio
angular**. A regra "maior" vem do protocolo, não da inspeção.

**Passos, todos determinísticos e sem parâmetro por imagem:**

1. L\* da imagem — função copiada **verbatim** do motor congelado.
2. Bordas por Canny, com limiares dados por **quantil do gradiente da própria
   imagem** (0,980 e 0,995), não por valor absoluto — para não depender do brilho
   de cada foto.
3. Centro provisório = mediana dos pixels de borda. Histograma radial de 200 bins;
   picos acima de 25 % do maior pico = curvas concêntricas candidatas.
4. Para cada pico: ajuste algébrico direto de elipse (Halíř & Flusser, 1998),
   reajustado 3 vezes aparando os pontos fora da banda de ±10 % em raio
   normalizado. Ajuste fechado, sem otimização iterativa e sem semente — os
   mesmos pontos devolvem sempre a mesma elipse.
5. Entre as candidatas concêntricas (centros a ≤ 0,15·eixo), toma-se a de
   **maior eixo**.
6. **Aceitação**, fixada aqui: b/a ≥ 0,80 · ≥ 90 % dos 36 setores de 10° com
   apoio · mediana de |r_norm − 1| ≤ 0,02.
7. px/mm = eixo maior em px ÷ 16 mm.

As constantes são 17, todas no cabeçalho do arquivo, todas globais ao banco.

---

## 2 · A IDENTIDADE DA ESCALA — e o valor que o motor recebe

🔴 **Esta é a peça que faltava e que precisa estar escrita antes da rodada.**

O motor congelado calcula a área esperada do termo de tamanho como

```python
resp = np.pi*(diam/2 * 30 * L/1380)**2
```

com **30 px/mm fixo no quadro de 1380** — era a escala das normalizadas do porco.
Aqui o quadro de 1380 px cobre **24 mm**, logo s = 1380/24 = **57,5 px/mm**.
Passar `diam = 6` faria o motor procurar um objeto com quase metade do diâmetro
certo. Pela mesma identidade algébrica da reauditoria do dia 3:

> **diam_ef = DIAM_MM × s/30 = 6 × 57,5/30 = 11,5 mm**

**O motor recebe 11,5 e continua intocado.** 6 mm é o nominal físico; 11,5 mm é o
mesmo nominal expresso na escala que o código assume. Constante única para o
banco inteiro, porque o recorte é sempre 24 mm → 1380 px.

Área em mm² = `n · (1380/700)² / 57,5²`, com n em px do quadro de trabalho de 700.

⚠️ **O 11,5 mm é nominal, não medido.** Ele pressupõe que o campo recortado tem
mesmo 24 mm — o que vem do nominal de 16 mm do README, não do anel daquela foto.
Se o detector errar a escala numa imagem, o campo não é de 24 mm, e o motor
procura ali um objeto do tamanho errado: a medida daquela imagem cai **por
escala**, não por falha de transferência, e as duas coisas não podem ser
confundidas na leitura da P1.

Por isso ficam registrados **por imagem**, sem nenhum ajuste e sem nenhuma
exclusão: `diam_anel_px`, `px_mm`, e `razao_pxmm` = px/mm da imagem ÷ **mediana
do banco**. Imagem com `razao_pxmm` fora de [0,8; 1,25] entra no relatório numa
linha própria, **marcada e contada, nunca removida** — é o mesmo tratamento que a
§2.2 do artigo dá à régua discrepante no porco, menos o descarte, que aqui o
pré-registro proíbe.

---

## 3 · DESTINO DAS FALHAS, FIXADO ANTES (itens pedidos pelo Fable)

**3.1 · Detector não acha o anel → estrato "sem escala própria".** A imagem
**não é excluída** e **não é re-tentada com parâmetro novo** (regra 1 do
pré-registro). Roda assim: quadro inteiro recortado no maior quadrado central →
1380 px → 700 px, saída **em px²**, e com o critério **`sec`** do próprio motor
congelado — `(0,25·uni + 0,15·fino + 0,25·comp)/0,65`, que é o critério sem o
termo de tamanho, já existente no código congelado. É o que o item 3 do
pré-registro manda quando não há nominal utilizável.

**3.2 · Fallback manual pré-autorizado.** O operador pode medir o diâmetro do
anel à mão, em px, como **ato do operador**, declarado por imagem no JSON
(`escala_manual: true`, com o valor e a hora). Mesmo precedente da escala manual
da 1324·B no porco, que o artigo declara como ato do operador e não saída do
método. **Só o anel** — nenhuma outra intervenção, em nenhuma etapa.

**3.3 · Recorte que não cabe no quadro.** Se o quadrado de 24 mm centrado no
anel não couber inteiro dentro da imagem original, a imagem **não é excluída e o
recorte não é encolhido**: completa-se por replicação da borda, e ela entra no
estrato declarado **"recorte incompleto"**, com a fração de área replicada
registrada no JSON. Fica escrito aqui porque a moldura de 8 % do motor lê a
referência de pele exatamente nessa faixa: numa imagem com borda replicada, a
referência é em parte artificial, e isso precisa ser legível no resultado em vez
de descoberto depois. *(Este item não estava entre os três pedidos pelo Fable; é
acréscimo do executor, pela mesma razão que motivou a emenda — regra nova depois
da rodada começada contamina o pré-registro.)*

**3.4 · Teste só em imagem sintética.** O detector foi desenvolvido e calibrado
exclusivamente contra cenas **desenhadas por código**, com a geometria tirada dos
nominais do README (parede de 10→16 mm, coverslip de 16 mm, ferida de 6 mm).
**Zero contato com imagem real do banco** até esta emenda estar hasheada e
conferida pelo Fabio.

---

## 4 · O QUE O TESTE SINTÉTICO MOSTROU

`teste_sintetico.py` — SHA-256 `16ff3d27a7d8045c3c0ef24767be4677ade0f9dece5603ca45b284593db6a864`. 16 cenas, semente 20260928.

```
caso                         esperado    medido   erro %     b/a   setor  residuo  veredito
1 splint frontal                600.0     600.0    +0.00   1.000    1.00   0.0009  OK
2 inclinado b/a 0,85            600.0     600.0    -0.01   0.850    1.00   0.0010  OK
3 pelo escuro + ruido           580.0     579.9    -0.01   1.000    1.00   0.0010  OK
4 borda interna 10 mm           600.0     600.0    -0.00   1.000    1.00   0.0009  OK
5 reflexo especular             600.0     600.0    -0.01   1.000    1.00   0.0009  OK
6 ocluido 60 graus              600.0     606.2    +1.03   0.951    1.00   0.0124  OK
7 descentralizado               500.0     500.0    -0.01   1.000    1.00   0.0012  OK
8 com ferida de 6 mm            600.0     600.0    -0.00   1.000    1.00   0.0009  OK
9 b/a 0,70 (reprova)            600.0   recusou        -   0.700    1.00   0.0011  OK  [achatamento]
10 sem anel (reprova)               -   recusou        -   0.951    1.00   0.0431  OK  [residuo]
11 metade ausente (reprova)     600.0   recusou        -   0.528    0.33   0.0344  OK  [achatamento;setores;residuo]
12 textura de pelo              600.0     600.0    +0.00   1.000    1.00   0.0012  OK
13 anel pequeno no canto        360.0     359.9    -0.02   1.000    1.00   0.0016  OK
14 halo do coverslip            600.0     600.0    -0.01   1.000    1.00   0.0009  OK
15 desfocado                    600.0     599.4    -0.10   1.000    1.00   0.0011  OK
16 cortado pela moldura         600.0   recusou        -   0.771    0.72   0.0251  OK  [achatamento;setores;residuo]

vereditos corretos: 16 de 16
erro absoluto de diametro: mediana 0.006 % | maximo 1.032 %
```

Os três casos de recusa são controles: inclinação além do tolerado, quadro sem
anel nenhum, e anel cortado pela moldura. Nenhum deles passou.

**Durante o desenvolvimento, o sintético derrubou três versões do detector** —
está registrado porque é o que dá sentido ao teste:

| versão | o que quebrou |
|---|---|
| 1 · Hough circular + elipse | enviesava em anel inclinado; erro de −21 % em b/a 0,85 |
| 2 · + resíduo | o resíduo media a **espessura do traço desenhado**, não o ajuste; o sintético era infiel à parede real do splint |
| 3 · geometria fiel (10→16 mm) | expôs o erro de fundo: `use_quantiles` calibrava o Canny contra o **ruído do fundo liso**, e a Hough circular escolhia a ferida de 6 mm em vez do anel |

A versão congelada troca a Hough por histograma radial + ajuste algébrico, e
torna "anel externo" uma regra explícita do código.

---

## 5 · O QUE A CADEIA INTEIRA MOSTROU

`teste_cadeia.py` — SHA-256 `d728933e1fd77be7838d42e1a4e4f5ea9b9b7d2a7655b34883b62fa940451e69`. Motor congelado extraído verbatim em
`motor_v0_funcoes.py` — SHA-256 `1602849373157ec849cef1ff3a39b75a797f85ad4f0b8adedfb810719ae4d224`, origem
`v0_congelado_2026-09-22/rodar.py` SHA-256
`78b193014577a45109771a2b15f3b7ff55663b0bb4312a23980c766fe7161732`.

```
s no quadro de 1380 = 57.5000 px/mm  |  diam_ef = 11.5000 mm

cena                                  px/mm px/mm med    erro % area mm2    nota
A frontal, 40 px/mm                   40.00     40.00    -0.007   201.84   0.435
B frontal, 25 px/mm                   25.00     25.00    -0.006    31.85   0.542
C inclinada b/a 0,88                  38.00     37.99    -0.018   177.25   0.491
D alta resolucao 70 px/mm             70.00     70.00    -0.004   196.85   0.470
E quadro retangular                   45.00     45.00    -0.010   193.24   0.471

alvo da ferida de 6 mm: 28.27 mm2
erro de escala: mediana 0.007 % | maximo 0.018 %
area recuperada: mediana 193.24 mm2 | de 31.85 a 201.84 (desvio do alvo: +583.5 %)
```

**Dois achados, declarados antes do download:**

1. **A escala fecha.** Erro mediano de 0,007 % na recuperação de px/mm, em cinco
   cenas com escalas de 25 a 70 px/mm, quadro quadrado e retangular, frontal e
   inclinada.

2. 🔴 **O motor congelado escolhe o anel do splint, não a ferida, em 4 das 5
   cenas sintéticas** — área recuperada ≈ 195 mm², que é π·8² = 201 mm², o disco
   de 16 mm. É **exatamente o modo de falha previsto** no item 5 da Emenda 1
   ("a borda interna do splint como anel concorrente — o modo 'dois anéis' da
   §3.7") e na P4 do pré-registro.

   **Nada é alterado por causa disso.** Nem constante do motor, nem máscara, nem
   recorte. Fica escrito aqui, antes de ver o banco, que esta é a assinatura
   esperada — para que, se ela aparecer no real, ninguém possa dizer que foi
   descoberta depois, e para que, se **não** aparecer, a surpresa também esteja
   registrada.

   Cena sintética não é evidência sobre o banco. É evidência de que a cadeia está
   ligada e de que a predição estava escrita antes.

---

## 6 · ORDEM DE EXECUÇÃO A PARTIR DAQUI

1. Esta emenda gravada e hasheada. ✅
2. **Fabio confere o hash.** ← aqui
3. PC conectado (abrir a conversa no app do Claude no PC).
4. Download dos 4,48 GB na máquina do Fabio.
5. README conferido contra o SHA-256 já registrado na Emenda 1
   (`1c41430786690cfea4e7246b3c9d1cf5eb0e3a23bab8a749ed678d2db22f542f`).
6. Uma rodada, 255 TIFFs, zero exclusão.
7. `saida\camundongo_v0.json` + `CAMUNDONGO_V0_RELATORIO.md`, com P1–P4
   marcadas confirmada/FALHOU e os hashes das duas saídas dentro do relatório.

## 7 · O QUE CONTINUA VALENDO

Tudo do pré-registro e da Emenda 1: uma rodada · nenhuma exclusão por resultado ·
nenhuma constante do v0 tocada · P1–P4 como escritas · estratos de idade e lado
só descritivos · IC bootstrap 10 000, semente 20260928 · dia 7/16/19 do porco
fechados · CWDB intocado · v2 do Zenodo não se publica aqui.

---

## ANEXO · `detecta_anel_camundongo.py`, verbatim

```python
"""
detecta_anel_camundongo.py — detector do anel de contencao de 16 mm.

CONGELADO PELA EMENDA 2 do pre-registro do camundongo (01/10/2026).
Escrito e calibrado ANTES de qualquer imagem do banco Dryad 10.25338/B84W8Q
ser aberta. Testado somente em imagens sinteticas desenhadas por codigo, com a
geometria dos NOMINAIS DO README (EMENDA 1): parede do splint de 10 mm (interna)
a 16 mm (externa), coverslip de 16 mm, ferida de punch de 6 mm.

Nao contem nenhuma constante do motor v0 e nao altera nenhuma.
Devolve apenas: centro do anel e diametro do eixo maior, em px da imagem original.

O protocolo manda medir o ANEL EXTERNO. Como a cena tem ate tres curvas
concentricas (16 mm, 10 mm e a ferida de 6 mm), o detector extrai varias elipses
e escolhe, entre as concentricas, a de MAIOR eixo com apoio angular.
"""
import numpy as np
from PIL import Image
from skimage.feature import canny

# ----------------------------------------------------------------------
# CONSTANTES DO DETECTOR — fixadas pela Emenda 2, nenhuma por imagem
# ----------------------------------------------------------------------
SIGMA        = 2.0       # suavizacao gaussiana do Canny
Q_BAIXO      = 0.98      # quantil do gradiente -> limiar baixo do Canny
Q_ALTO       = 0.995     # quantil do gradiente -> limiar alto do Canny
MAX_PTS      = 40000     # teto de pixels de borda usados (subamostragem por passo)
N_BINS       = 200       # bins do histograma radial que acha as curvas concentricas
PICO_FRAC    = 0.25      # altura minima de um pico, fracao do maior pico
BANDA_H      = 0.25      # banda do pico radial; cobre b/a ate MIN_ACHATA
N_TRIM       = 3         # reajustes com corte dos pontos fora da banda (fixo)
MIN_PTS_FIT  = 60        # pontos minimos para ajustar uma elipse
CONCENT      = 0.15      # centros a <=0,15*eixo maior sao concentricos
R_MIN_FRAC   = 0.08      # eixo maior minimo, fracao do menor lado do quadro
R_MAX_FRAC   = 0.95      # eixo maior maximo, fracao do menor lado do quadro
MIN_ACHATA   = 0.80      # b/a minimo aceito (tolera inclinacao da camera)
N_SETORES    = 36        # setores angulares de 10 graus
MIN_SETORES  = 0.90      # fracao minima de setores com pixel de apoio
BANDA        = 0.10      # banda em r_norm para contar apoio e residuo
MAX_RESID    = 0.02      # mediana de |r_norm - 1| aceita
ANEL_MM      = 16.0      # nominal externo do splint (EMENDA 1)


def _lstar(im):
    """L* exatamente como no motor congelado v0_congelado_2026-09-22/rodar.py.
    Copiado verbatim; nenhuma constante alterada."""
    q = im.astype(np.float64) / 255.
    def lin(c): return np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    R, G, B = [lin(q[:, :, i]) for i in range(3)]
    Y = R * .2126 + G * .7152 + B * .0722
    f = np.where(Y > 0.008856, np.cbrt(Y), 7.787 * Y + 16 / 116)
    return (116 * f - 16) * 2.55


def _bordas(cinza):
    """Canny com limiares por quantil do proprio gradiente da imagem — quantil,
    e nao valor absoluto, para nao depender do brilho de cada foto."""
    return canny(cinza / 255.0, sigma=SIGMA, low_threshold=Q_BAIXO,
                 high_threshold=Q_ALTO, use_quantiles=True)


def _ajusta_elipse(pts):
    """Ajuste algebrico direto de elipse (Halir & Flusser, 1998), vetorizado.
    Devolve (xc, yc, a, b, theta) ou None. Sem iteracao de otimizacao, sem
    semente: dado o mesmo conjunto de pontos, devolve sempre o mesmo resultado."""
    if len(pts) < 5:
        return None
    m = pts.mean(0)
    e = max(1e-9, float(np.abs(pts - m).max()))
    x = (pts[:, 0] - m[0]) / e
    y = (pts[:, 1] - m[1]) / e
    D1 = np.column_stack([x * x, x * y, y * y])
    D2 = np.column_stack([x, y, np.ones_like(x)])
    S1, S2, S3 = D1.T @ D1, D1.T @ D2, D2.T @ D2
    try:
        T = -np.linalg.solve(S3, S2.T)
    except np.linalg.LinAlgError:
        return None
    M = S1 + S2 @ T
    M = np.array([M[2] / 2.0, -M[1], M[0] / 2.0])
    try:
        val, vec = np.linalg.eig(M)
    except np.linalg.LinAlgError:
        return None
    cond = 4 * vec[0] * vec[2] - vec[1] ** 2
    k = np.nonzero(cond > 0)[0]
    if len(k) == 0:
        return None
    a1 = np.real(vec[:, k[0]])
    A, B, C = a1
    D, E, F = np.real(T @ a1)
    den = B * B - 4 * A * C
    if den >= -1e-12:          # B^2-4AC < 0 e a condicao de elipse
        return None
    xc = (2 * C * D - B * E) / den
    yc = (2 * A * E - B * D) / den
    # conica centrada: autovalores da forma quadratica dao as direcoes dos eixos
    F0 = F + (D * xc + E * yc) / 2.0
    W = np.array([[A, B / 2.0], [B / 2.0, C]])
    w, v = np.linalg.eigh(W)
    if np.any(np.abs(w) < 1e-15) or np.any(-F0 / w <= 0):
        return None
    semi = np.sqrt(-F0 / w)
    k = int(np.argmax(semi))
    ax1, ax2 = float(semi[k]), float(semi[1 - k])
    th = float(np.arctan2(v[1, k], v[0, k]))
    return (float(xc * e + m[0]), float(yc * e + m[1]),
            float(ax1 * e), float(ax2 * e), float(th))


def _norm(pts, par):
    """raio normalizado e angulo de cada ponto na elipse par=(xc,yc,a,b,theta)"""
    xc, yc, a, b, th = par
    X = (pts[:, 0] - xc) * np.cos(th) + (pts[:, 1] - yc) * np.sin(th)
    Y = -(pts[:, 0] - xc) * np.sin(th) + (pts[:, 1] - yc) * np.cos(th)
    return np.hypot(X / a, Y / b), np.arctan2(Y, X)


def _ordena(par):
    xc, yc, a, b, th = par
    return (xc, yc, b, a, th + np.pi / 2) if a < b else (xc, yc, a, b, th)


def detecta(caminho_ou_array):
    """Devolve dict com cx, cy (px da original), diam_px (eixo maior), b/a,
    setores apoiados, residuo e 'ok'. Se nao achar anel: {'ok': False, ...}."""
    if isinstance(caminho_ou_array, (str, bytes)):
        im = np.asarray(Image.open(caminho_ou_array).convert('RGB'))
    else:
        im = np.asarray(caminho_ou_array)[:, :, :3]
    H, W = im.shape[:2]
    menor = min(H, W)

    eo = _bordas(_lstar(im))
    ys, xs = np.nonzero(eo)
    if len(xs) < MIN_PTS_FIT:
        return {'ok': False, 'motivo': 'bordas insuficientes'}
    passo = max(1, int(np.ceil(len(xs) / MAX_PTS)))
    pts0 = np.column_stack([xs[::passo], ys[::passo]]).astype(float)

    # --- 1. curvas concentricas pelo histograma radial a partir do centro
    #        provisorio (mediana das bordas). Os picos sao as curvas candidatas:
    #        anel de 16 mm, parede de 10 mm e ferida de 6 mm.
    c0 = np.median(pts0, axis=0)
    r = np.hypot(pts0[:, 0] - c0[0], pts0[:, 1] - c0[1])
    rmin, rmax = R_MIN_FRAC * menor / 2, R_MAX_FRAC * menor / 2
    dentro = (r >= rmin) & (r <= rmax)
    if int(np.sum(dentro)) < MIN_PTS_FIT:
        return {'ok': False, 'motivo': 'bordas fora da faixa de raio'}
    hist, bordas_bin = np.histogram(r[dentro], bins=N_BINS, range=(rmin, rmax))
    centros = (bordas_bin[:-1] + bordas_bin[1:]) / 2
    alto = hist.max()
    picos = [i for i in range(N_BINS)
             if hist[i] >= PICO_FRAC * alto
             and hist[i] >= hist[max(0, i - 1)] and hist[i] >= hist[min(N_BINS - 1, i + 1)]]
    if not picos:
        return {'ok': False, 'motivo': 'sem pico radial'}

    # --- 2. para cada pico, elipse ajustada e aparada N_TRIM vezes
    cands = []
    for i in picos:
        rp = centros[i]
        sel = np.abs(r - rp) <= BANDA_H * rp
        if int(np.sum(sel)) < MIN_PTS_FIT:
            continue
        par = _ajusta_elipse(pts0[sel])
        for _ in range(N_TRIM):
            if par is None:
                break
            rn, _a = _norm(pts0, par)
            sel = np.abs(rn - 1.0) <= BANDA
            if int(np.sum(sel)) < MIN_PTS_FIT:
                break
            par = _ajusta_elipse(pts0[sel])
        if par is None or par[2] <= 0:
            continue
        if not (R_MIN_FRAC * menor <= 2 * par[2] <= R_MAX_FRAC * menor):
            continue
        rn, _a = _norm(pts0, par)
        cands.append((par, int(np.sum(np.abs(rn - 1.0) <= BANDA))))
    if not cands:
        return {'ok': False, 'motivo': 'nenhuma elipse ajustada'}

    # --- 3. entre as concentricas a mais apoiada, a de MAIOR eixo (anel externo)
    base = max(cands, key=lambda c: c[1])[0]
    grupo = [c for c in cands
             if np.hypot(c[0][0] - base[0], c[0][1] - base[1]) <= CONCENT * base[2]]
    par = max(grupo, key=lambda c: c[0][2])[0] if grupo else base

    xc, yc, a, b, th = par
    rn, ang = _norm(pts0, par)
    sel = np.abs(rn - 1.0) <= BANDA
    n_ap = int(np.sum(sel))
    if n_ap < N_SETORES:
        return {'ok': False, 'motivo': 'apoio insuficiente'}
    resid = float(np.median(np.abs(rn[sel] - 1.0)))
    setores = len(np.unique(((ang[sel] + np.pi) / (2 * np.pi) * N_SETORES)
                            .astype(int) % N_SETORES))
    frac_set = setores / N_SETORES
    achata = b / a

    ok = (achata >= MIN_ACHATA and frac_set >= MIN_SETORES and resid <= MAX_RESID)
    motivo = '' if ok else ';'.join(m for m, c in [
        ('achatamento', achata < MIN_ACHATA),
        ('setores', frac_set < MIN_SETORES),
        ('residuo', resid > MAX_RESID)] if c)
    return {'ok': bool(ok), 'cx': float(xc), 'cy': float(yc),
            'diam_px': float(2 * a), 'eixo_menor_px': float(2 * b),
            'theta': float(th), 'achatamento': float(achata),
            'setores_apoiados': int(setores), 'fracao_setores': float(frac_set),
            'residuo': resid, 'n_apoio': n_ap, 'n_candidatas': len(cands),
            'motivo': motivo}


def px_por_mm(res):
    """px/mm = diametro ajustado em px / 16 mm (EMENDA 1, item 2)."""
    return res['diam_px'] / ANEL_MM
```

---

*Escrita pelo Opus em 01/10/2026, no pedido do Fabio e com os três acréscimos do
Fable. Nenhuma imagem do banco foi baixada, aberta ou inspecionada até esta
linha.*
