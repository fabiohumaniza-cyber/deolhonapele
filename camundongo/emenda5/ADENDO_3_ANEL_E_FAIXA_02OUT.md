# ADENDO 3 · o anel na vida real, e o método da faixa

**02/10/2026, Brasília, 11h50.** Escrito durante a medição manual, com o motor
**não executado em imagem nenhuma** e a **etapa 3 não iniciada**. Nenhum resultado
do motor existe até esta linha.

Adendo à `EMENDA_3`, à `NOTA_MEDIDA_MANUAL_01OUT.md` (`0f851530…`) e ao
`ADENDO_2_QUAL_ANEL_01OUT.md` (`0867a9ec…`), que **não são alterados**.

## 0 · ESTADO CONGELADO NESTE INSTANTE

| arquivo | SHA-256 | bytes |
|---|---|---|
| `MEDIDAS.txt` | `9a035e9dedbcc2e517067e311007b406c579cb12b954115ce08e7463fcbec227` | 4.395 |
| `MEDIDAS_LOG.tsv` | `01d81d985c5d47b7b5de75a20c41e5b8a41d70a7dc5e15360fd2ce9b9582ac1c` | 13.085 |

**92 linhas de medida: 64 com diâmetro, 28 `SEM_ANEL`.** Última medida:
`Day 14_Y8-2-R`. Ferramenta em uso: `mede_anel.py` v6,
`d4e4e81bfce1db89462ce9dd451620c7378c9db20a1f9116551d54fb959ed9f2`.

---

## 1 · AS TRÊS REGRAS DO ANEL

O `ADENDO_2` resolveu **qual** anel medir quando há mais de um. Não resolveu o
que fazer quando o anel existe mas não está em condição de ser escala. Essas
situações apareceram na medição, nesta ordem, e a regra foi fixada **antes** da
contagem da seção 3.

1. **Anel mordido, com pedaço faltando e o resto no lugar** → **mede**. O arco
   que sobrou continua em cima do círculo original de 16 mm; clicam-se os 4
   pontos no trecho íntegro. Isto é **procedimento**, não exceção: vale desde a
   primeira imagem do banco, e foi o que o operador já vinha fazendo.
   **O juiz é o aviso da própria ferramenta** — se a 3ª maior distância passar de
   0,80·D, os pontos estão amontoados e a imagem vai para `SEM_ANEL`. O aviso não
   sabe de que animal é a foto, e é por isso que ele decide.
2. **Anel fora do plano da ferida** (solto, caído no cartão ou na maca) →
   **`SEM_ANEL`**. Objeto em outra profundidade e outro ângulo não é escala.
3. **Anel dobrado, enrolado ou deslocado**, com o material fora do círculo
   original → **`SEM_ANEL`**. Material faltando é diferente de material fora do
   lugar: o primeiro preserva o círculo, o segundo o destrói.

Primeiras imagens registradas por 2 e 3: **`Day 11_Y8-1-L`** (anel solto no
cartão) e **`Day 14_A8-5-L`** (anel deformado).

## 2 · NENHUMA MARCA NOVA, E POR QUÊ

A `EMENDA_5` deixou escrito que uma quarta marca seria emenda nova com hash.
Chegou-se a cogitar `s` (splint solto) e `m` (mordido). **Não se cria nenhuma.**

Motivo: a marca entraria na imagem 48 de 255. O resultado seria uma coluna
preenchida pela metade, que não serve nem para contar nem para explicar — pior
que marca nenhuma. O vocabulário `p;d;f` segue fechado e inalterado.

**A informação não se perde.** O `MEDIDAS_LOG.tsv` grava os 4 cliques brutos de
cada imagem. Num anel íntegro os cliques se espalham pela volta; num anel mordido
o operador é obrigado a espremê-los no arco que sobrou. A distribuição angular
dos cliques, calculada depois, identifica os mordidos **sem reabrir uma imagem
sequer** e sem depender da memória de ninguém. Fica declarado aqui que esse
cálculo será feito e reportado.

## 3 · O ACHADO: A FALTA DE ANEL NÃO É ALEATÓRIA

Contagem feita sobre as 92 linhas acima, **antes de o motor rodar**:

| grupo | medidas | `SEM_ANEL` | |
|---|---|---|---|
| **A8-x (idosos)** | 46 | 4 | **9 %** |
| **Y8-x (jovens)** | 40 | 21 | **52 %** |

Por animal: `Y8-1`, `Y8-3` e `Y8-4` com **7 de 10** cada; `Y8-2` com **0 de 10**;
nos idosos só `A8-5`, com 3.

Por dia: **dia 0 sem nenhuma falta nos dois grupos**; a partir do dia 10 os
jovens perdem o anel e os idosos não.

**Não se afirma a causa.** O que está registrado é o que se observa na
fotografia: o anel não está utilizável como escala. Se caiu, foi retirado, ou o
enquadramento mudou, este adendo não decide.

### 3.1 · A consequência, declarada antes

Sem anel não há escala, e sem escala não há mm². Logo **o subconjunto com medida
em milímetro não está balanceado entre os grupos**. Fica estabelecido, antes de
qualquer resultado:

- toda comparação idoso × jovem em mm² reporta, **ao lado**, o n por grupo e a
  fração `SEM_ANEL` de cada um;
- as imagens sem escala vão para o estrato **px²**, como o pré-registro já manda,
  e não são excluídas de contagem nenhuma;
- a tabela final de `SEM_ANEL` por grupo, por animal e por dia é publicada
  **inteira**, qualquer que seja ela, inclusive se o desequilíbrio aumentar
  quando as 163 restantes forem medidas.

Os números desta seção são de 92 imagens e **vão mudar**. São registrados agora
porque foram vistos agora.

## 4 · O DEGRAU: A BORDA DO ANEL É DUPLA

Observação do Fabio na lupa, 11h34, registrada com a descrição dele.

O splint tem **1,6 mm de espessura**: é um cilindro baixo, não um desenho. Como
quase nenhuma foto do banco foi tirada perpendicular à ferida, **de um lado
enxerga-se só o topo do silicone e do outro enxerga-se topo e parede**. A borda
externa, nesse segundo lado, aparece dupla — o "degrau". O reflexo do Tegaderm e
do coverslip por cima lava ainda mais a transição.

Geometria: para um anel de 16 mm com 1,6 mm de altura visto com inclinação θ, a
projeção mede `16·cos θ + 1,6·sen θ` na direção da inclinação e **16 mm limpos**
na direção perpendicular. A conta da ferramenta usa as **duas maiores** das seis
distâncias, que são justamente as da direção perpendicular — ou seja, o método
descarta sozinho a direção contaminada. Isto não é correção nova: é a propriedade
do método que já estava escrita na `NOTA_REPARO_ORDEM_CLIQUE_01OUT.md`.

**Por que fica registrado:** o detector congelado reprovou 255 de 255 na etapa 1.
Uma borda externa dupla é mecanismo plausível para isso. Escrito **antes** da
etapa 3, pelo mesmo motivo da moldura de pele contaminada do `ADENDO_2`: depois
do resultado, qualquer explicação é suspeita.

## 5 · A MEDIÇÃO PELO DIÂMETRO ESTÁ PAUSADA, NÃO ABANDONADA

Por decisão do Fabio, 11h44, a medição pelo diâmetro **pausa em 92 de 255**. As
92 ficam como estão, com os hashes da seção 0. As 163 restantes serão medidas
pelo mesmo `mede_anel.py` v6, sem alteração, quando ele retomar.

**Nenhuma troca de método ocorreu.** Este ponto importa: a contagem da seção 3
foi vista **antes** desta pausa, e um método diferente aplicado às imagens
restantes depois dela resgataria preferencialmente um dos grupos. É exatamente
por isso que a faixa da seção 6 **não substitui nada** e é medida nas imagens que
**já estão** medidas.

## 6 · O MÉTODO DA FAIXA — IDEIA DO FABIO, 02/10, 11h25–11h41

### 6.1 · O argumento dele

Medir a **largura da faixa de silicone** (3 mm nominais) em vez do diâmetro
(16 mm), num trecho onde não há degrau.

O argumento a favor é geométrico e é dele: medindo a borda externa e a interna
**no mesmo lado**, as duas estão deslocadas pela mesma espessura, na mesma
direção, e o deslocamento **se cancela na subtração**. O método do diâmetro
atravessa o anel, onde os dois lados têm geometria oposta. A faixa também é
local, e portanto quase imune à curvatura do dorso, que encurta a corda do
diâmetro.

### 6.2 · O que pesa contra, declarado antes

- **Erro 5,33× maior.** O mesmo erro de clique dividido por 3 mm em vez de
  16 mm. A repetibilidade intra-observador medida no diâmetro foi **0,62 %**
  (mediana, 17 feridas do dia 0, v3 contra v6).
- **A borda interna é ambígua.** Sobre o splint há um **coverslip de 16 mm** mais
  Tegaderm, tapando o buraco de 10 mm. Na borda externa a ambiguidade é inócua —
  splint e coverslip têm o mesmo nominal, e isso já estava declarado na
  `EMENDA_1`. Na borda interna, não: pode-se estar clicando no silicone, no
  plástico ou na pele por baixo.
- **O nominal de 3 mm** sai de 10 mm interno / 16 mm externo, lidos do README e
  registrados na `EMENDA_1_CAMUNDONGO_30SET.md`, anterior a qualquer medida.

### 6.3 · A ferramenta, e por que são três cliques

`mede_faixa.py`, `df8d779f56686a78c6f986e3f45c1379aa9c53d28cc2bf84a20d00bf02e1e29d`,
17.032 B.

**Dois cliques na borda externa, afastados, e um na interna.** A largura é a
distância **perpendicular** do terceiro ponto à reta dos dois primeiros.

Com apenas dois cliques, atravessar a faixa de esguelha daria largura maior que a
real **sem nenhum sinal de que isso aconteceu**. A perpendicular elimina esse
erro e não depende de onde, ao longo da borda interna, o terceiro ponto caiu. A
ferramenta avisa quando os pontos 1 e 2 ficam a menos de 12 px um do outro, caso
em que a reta — e portanto a perpendicular — fica instável.

A ferramenta **não mostra o diâmetro já medido da mesma imagem, nem px/mm
nenhum**. Se mostrasse, a mão do operador seguiria o número e a comparação
perderia o valor. Ela não lê nenhum campo do `MEDIDAS.txt` além do nome, não
toca nesse arquivo, e grava em `FAIXAS.txt` e `FAIXAS_LOG.tsv`, novos.

Ensaio da aritmética, antes de qualquer uso: perpendicular exata; independente de
onde o ponto 3 cai na borda interna; invariante a rotação (diferença 0,00e+00);
indiferente à ordem de 1 e 2; separação 1–2 devolvida junto; pontos coincidentes
não estouram; ida e volta tela↔original exata com e sem zoom.

### 6.4 · Em quais imagens, e por quê

Nas **mesmas 92** da seção 0, na ordem em que estão no `MEDIDAS.txt` — incluindo
as 28 `SEM_ANEL`.

Motivo: nessas 92 **não há escolha a fazer**. Elas foram definidas pelo operador
antes desta conversa e antes da contagem da seção 3. Qualquer conjunto novo
exigiria uma regra de seleção, e toda regra de seleção escrita depois de um
achado é suspeita. Daí saem as duas respostas de uma vez: **64 pares** diâmetro ×
faixa, e **28 imagens** em que se vê se a faixa alcança o que o diâmetro perdeu.

### 6.5 · O critério, escrito antes de a primeira faixa ser medida

Comparação: `px/mm` pela faixa (`largura_px / 3`) contra `px/mm` pelo diâmetro
(`diâmetro_px / 16`), par a par, nas imagens que tiverem os dois.

Estatística: **diferença relativa mediana** e o **intervalo interquartil** dessa
diferença, mais bootstrap de 10000 com semente 20260928 para o intervalo de 95 %
da mediana.

A faixa passa a ser admitida como escala **secundária** — e **só** para imagens
em que o diâmetro é impossível — se, e somente se:

- `|mediana da diferença relativa| ≤ 2 %` **e**
- `intervalo interquartil ≤ 5 %`.

Os números saem da repetibilidade: 2 % é cerca de três vezes os 0,62 % medidos no
diâmetro, e corresponde a ~4 % em área. Acima disso a faixa acrescentaria mais
ruído do que imagem recuperada.

**O resultado é publicado seja qual for**, inclusive se reprovar, inclusive se a
divergência for grande — caso em que o tamanho dela mede o efeito combinado da
curvatura e do degrau, e isso é achado, não defeito.

Se a faixa reprovar, as `SEM_ANEL` continuam `SEM_ANEL` e vão para px². Se
passar, qualquer imagem resgatada por ela entra **marcada como escala por
faixa**, e todas as análises são reportadas nas duas formas: só com escala por
diâmetro, e com as duas escalas.

## 7 · O QUE NÃO MUDA

Escala pelo anel **externo** de 16 mm como método primário; `px_mm = D/16`;
recorte de 24 mm → 1380 → 700; `diam_ef` 11,5 mm; a grade de 144; a coroa da
rodada 2 entre 145,83 e 233,33 px; semente 20260928; as 255; uma rodada; zero
exclusão; **nenhuma constante do v0**; o detector congelado, reprovado nas 255 e
intocado; o `roda_camundongo.py` da Emenda 5 (`8c1f6e4d…`); o vocabulário de
marcas `p;d;f`; a P5 do pré-registro da rodada 2 (`3a27e63c…`) e o Adendo 1, com
o texto do Fabio inalterado.

---

*Opus, 02/10/2026, a pedido do Fabio. Hashes colados do `sha256sum`. As contagens
da seção 3 foram calculadas sobre o `MEDIDAS.txt` de hash `9a035e9d…`, trazido do
PC do Fabio neste instante. O motor não rodou em nenhuma imagem até esta linha.*
