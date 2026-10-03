# ADENDO 14 · resultado da rodada 1 — o motor v0 congelado nas 255

**03/10/2026, Brasília, 07h00.** A rodada 1 foi executada em **02/10/2026, entre
20h15 e 20h52**, depois de registrados os Adendos 1 a 12. Este documento
registra o resultado. Nada nele altera os documentos anteriores.

## 0 · OS ARQUIVOS

| arquivo | SHA-256 | bytes |
|---|---|---|
| `camundongo_v0.json` (saída do motor) | `baf4671f67e8098923c327c3eeac7329801231c677282692bef8836cba64d82c` | 219.573 |
| `CAMUNDONGO_V0_RELATORIO.md` (relatório pré-registrado) | `92605a5d1e78654a03edbf9b8142edf6287f32946eb0fb50dad84403e1839c5b` | 4.257 |
| `ve_mascara.py` (visualizador, §6) | `91e27e2d4e478928445d6dcc49651083c52c1417fcc2d17be403c97a55c05b54` | 4.688 |

Entradas: as da §0 do Adendo 11 (`MEDIDAS.txt` `7aaebcce…`, `MEDIDAS_LOG.tsv`
`9783dbd4…`, `CLASSIFICACAO.txt` `3f10f490…`).

Execução: pelo Fabio, no cmd do seu PC, com `roda_camundongo.py` (`8c1f6e4d…`,
conferido byte a byte antes de rodar). Os dois módulos congelados foram lidos
**do lugar onde foram congelados** — `06_MOTOR_DE_REGISTRO\` —, apontados por
`PYTHONPATH`, sem cópia: `detecta_anel_camundongo.py` `56f1b434…` e
`motor_v0_funcoes.py` `16028493…`, hashes conferidos contra a Emenda 2 antes da
execução.

## 1 · O PLACAR PRÉ-REGISTRADO

Transcrito do relatório gerado pelo próprio `roda_camundongo.py`:

| | predição | resultado | |
|---|---|---|---|
| **P1** | medida obtida em ≥ 50 % das imagens com anel visível | **100,0 %** (204 de 204) | **confirmada** |
| **P2** | Spearman(dia, área mediana) ≤ −0,8 | **−0,1607** | **FALHOU** |
| **P3** | revisor cego acerta ≥ 75 % dos pares | nenhum par possível (n = 0) | **não avaliável** |
| **P4** | falha dominante = referência de pele contaminada | assinatura "anel do splint" em **19,6 %** | **descritiva** |

## 2 · A P1 CONFIRMADA É A PIOR NOTÍCIA DA RODADA

A P1 está confirmada pelo critério escrito, e fica confirmada. Mas o que ela
mede precisa estar dito ao lado:

**O motor devolveu medida em 255 de 255 imagens. Não recusou nenhuma.**

Isso inclui as **62** que o operador classificou como `n` (não dá para laudar) e
as **9** classificadas `c` (cicatrizadas, sem ferida). O motor tem mecanismo de
recusa — `anel()` devolve `None` quando não acha estrutura — e ele não disparou
uma única vez neste banco.

Responder sempre não é robustez: é a incapacidade de dizer "não sei".

## 3 · A P2 FALHOU, E A CURVA MOSTRA POR QUÊ

Área mediana por dia, **só as 204 com escala, em mm²**:

| dia | n | mm² | % do punch | | dia | n | mm² | % do punch |
|---|---|---|---|---|---|---|---|---|
| 0 | 16 | 34,28 | 121 % | | 8 | 14 | 28,36 | 100 % |
| 1 | 16 | 32,22 | 114 % | | 9 | 13 | 29,17 | 103 % |
| 2 | 16 | 28,51 | 101 % | | 10 | 13 | 28,40 | 100 % |
| 3 | 16 | 28,03 | 99 % | | 11 | 9 | 30,08 | 106 % |
| 4 | 16 | 29,73 | 105 % | | 12 | 9 | 29,96 | 106 % |
| 5 | 16 | 30,33 | 107 % | | 13 | 9 | 29,00 | 103 % |
| 6 | 16 | 28,83 | 102 % | | 14 | 8 | 29,38 | 104 % |
| 7 | 14 | 28,01 | 99 % | | 15 | 3 | 26,20 | 93 % |

Uma reta em torno de 100 % do punch de 6 mm (28,2743 mm²) do primeiro ao
último dia. A ferida fecha — no dia 15 o operador declarou 7 de 16 cicatrizadas
— e o número do motor não muda.

## 4 · O COMPARADOR NULO

Círculo de 6 mm no centro do anel, desenhado sem olhar a imagem.

| | |
|---|---|
| diferença mediana de área, motor − nulo | **+0,74 mm²** (IC95 0,25 a 2,02) |
| Wilcoxon pareado | p = 4,02 × 10⁻⁵, n = 204 |
| Dice motor × nulo, mediana | **0,000** |
| imagens com Dice **zero** | **158 de 204** |

A área do motor é quase a do nulo; o lugar não é. Em 158 das 204 imagens a
máscara do motor e o círculo central **não têm um pixel em comum**.

Pela geometria do splint — buraco de 10 mm, ferida de 6 mm suturada dentro dele
—, uma ferida pode estar descentrada no máximo 2 mm, e o círculo nulo tem 3 mm
de raio. **Uma ferida dentro do buraco sempre encosta no nulo.** Dice zero
significa que o motor pintou fora do buraco.

## 5 · O BRAÇO PRINCIPAL: AS 70 LIMPAS

`v`, sem plástico sobre a ferida, com escala (Adendo 10, §6).

| | n | |
|---|---|---|
| área entre 0,5× e 1,5× o punch **e** Dice > 0 | **1** | Dice 0,010 |
| área entre 0,5× e 1,5× o punch, Dice **zero** | **47** | tamanho de ferida, fora do lugar |
| área fora da faixa, Dice > 0 | **22** | todas marcadas "anel do splint" |
| área fora da faixa, Dice zero | 0 | |

As 22 do terceiro grupo encostam no nulo porque pintaram o **disco inteiro do
splint**, de ~201 mm², que contém o círculo central.

**Em nenhuma das 70 o motor encontrou a ferida.**

Acima do punch, dia ≥ 1: **37 de 54 (68,5 %)** nas limpas, contra **106 de 188
(56,4 %)** nas 204. O subconjunto limpo foi **pior**, não melhor.

## 6 · O QUE AS MÁSCARAS MOSTRAM

O `roda_camundongo.py` grava números, não imagens. O `ve_mascara.py` (§0)
**importa** o `roda_camundongo.py` e chama as mesmas funções da etapa 3 —
`recorta`, `quadrado_central`, `roda_motor`, `mascara_nula` —, de modo que o
que se desenha é o que o motor fez, não uma reconstrução. Não escreve em nenhum
arquivo do motor; só cria PNG.

Foram desenhadas as 158 de Dice zero. As inspecionadas mostram duas coisas
diferentes:

- **Pelo escuro no canto do recorte** (`Day 0_A8-1-L`, 20,43 mm²;
  `Day 10_Y8-1-L`, 6,32 mm²) — numa delas, uma imagem de dia 0 com a ferida
  nítida e o círculo nulo sobre ela.
- **A faixa laranja do splint** (`Day 11_A8-1-L`, 28,49 mm²) — a máscara
  acompanha a borda interna da faixa, exatamente na coroa de 5 a 8 mm de raio
  que a rodada 2 vai declarar como artefato.

Dice zero por classe do operador: `v` 99 · `n` 32 · `d` 27.

## 7 · O CONTROLE NEGATIVO

As 9 cicatrizadas estão **todas** entre as 51 sem escala, então o motor as
mediu em **px²**, como o pré-registro manda. Convertidas **só para leitura**
pela mediana do banco (38,1806 px/mm) — conversão que não é a análise
pré-registrada —, **8 das 9** passam do punch, de 2× a 22×. Uma
(`Day 15_Y8-3-R`) dá 17,9 mm².

Numa ferida fechada a resposta certa é área zero. O motor não deu zero em
nenhuma.

## 8 · A P6, DO FABIO

Registrada no Adendo 12 às 20h10:59, antes da execução.

- **P6.1 — "a rodada principal vai mal": confirmada.**
- **P6.2 — "melhora sem plástico e tirando artefato": a parte "sem plástico"
  falhou.** As 70 limpas foram piores que as 204 (§5). A parte "tirando
  artefato" ainda não foi testada: é a rodada 2.

## 9 · UMA OBSERVAÇÃO, SEM INTERPRETAÇÃO

As duas imagens com maior Dice contra o nulo em todo o banco:

| imagem | Dice | área | classe do operador | `p` |
|---|---|---|---|---|
| `Day 2_A8-3-L` | **0,838** | 25,91 | `d` | S |
| `Day 2_A8-1-R` | **0,755** | 20,50 | `n` | S |

São as duas imagens em que o motor mais coincidiu com o círculo central — e
são, ambas, imagens que o operador **não** conseguiu laudar com confiança, ambas
com plástico sobre a ferida.

Isto é registrado porque o Fabio levantou, em 02/10 às 20h50, a hipótese de que
o motor poderia achar borda onde o olho não vê. **Duas imagens não testam essa
hipótese**, e coincidir com o círculo nulo não é achar a ferida. Ficam
anotadas como candidatas a uma conferência futura, a ser desenhada e
registrada antes.

## 10 · O MECANISMO, COMO DESCRIÇÃO

A função `anel()` procura uma **estrutura fechada em anel** e devolve o que está
dentro dela. No suíno, o anel mais forte da imagem era a borda da ferida. No
camundongo, sem o `ar` ligado (Adendo 13, §1), o anel mais forte é o **splint
de silicone laranja**, presente em todas as imagens com escala; e, quando ele
não vence, vence uma mancha de **pelo escuro** que fecha contorno contra a pele
clara.

A formulação do Fabio, em 02/10 às 21h14, que este registro adota:

> No suíno o campo era pele, e o artefato era exceção — subtraí-lo bastava. No
> camundongo o artefato é a maioria do campo — splint, filme, pelo, campo
> cirúrgico, régua —, e subtrair não termina. É preciso **declarar o campo**.

Isto é descrição do que se viu. A rodada 2 e a rodada 3 é que testam.

## 11 · O QUE VEM, NESTA ORDEM

1. Previsão numérica de quanto a rodada 2 corrige: posição das 158 máscaras de
   Dice zero em relação à coroa — registrada **antes** da rodada 2.
2. O ensaio sintético da §6 do pré-registro da rodada 2, com a sua condição de
   parada.
3. A rodada 2.
4. O pré-registro da rodada 3 — o campo declarado — **antes** de ela rodar.

## 12 · O QUE NÃO MUDA

A rodada 1 está encerrada e o seu resultado é este, publicado inteiro. O motor
v0 continua congelado e intocado, e o seu registro em três bancos é: acertou no
suíno, não transferiu para ferida humana, falhou no camundongo. **Nenhuma
constante do v0.**

---

*Opus, 03/10/2026. Hashes colados do `sha256sum`. Os números das §§1, 3 e 4 são
os do relatório gerado pelo `roda_camundongo.py`; os das §§5 a 9 foram
calculados sobre o `camundongo_v0.json` de hash `baf4671f…` e o
`CLASSIFICACAO.txt` de hash `3f10f490…`. Uma leitura preliminar feita pelo Opus
fora do relatório, na noite de 02/10, misturou as áreas em px² das 51 sem escala
com as em mm² das outras 204; foi corrigida na mesma noite, antes de qualquer
registro, e nenhum número dela entrou aqui. O relatório oficial nunca misturou
as unidades.*
