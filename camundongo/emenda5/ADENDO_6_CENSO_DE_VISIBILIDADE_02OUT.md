# ADENDO 6 · a ferida está na fotografia? O censo, e o desenho de três braços

**02/10/2026, Brasília, 15h40.** O motor **não rodou em imagem nenhuma** e a
etapa 3 **não foi iniciada**. Nenhum resultado do motor existe até esta linha.

Adendo aos Adendos 3, 4 e 5, que **não são alterados**.

---

## 1 · DE ONDE ISSO VEIO

Entre 15h15 e 15h30, medindo os anéis, o Fabio afirmou:

> *"TEM MUITAS que SÃO IMPOSSÍVEIS medir por humano, mais da metade"*

e abriu **três imagens ao acaso** — as três primeiras que escolheu — para
mostrar. Nas três, nenhum observador saberia dizer onde a ferida começa:
`A8-1 dia 15` (anel solto no cartão, dorso com marcas dispersas), `A8-1 dia 13`
(dois anéis, ferida sob filme enrugado e opaco), `Y8-3 dia 14` (pelo, régua,
nenhuma ferida visível).

Ele também observou, e isso é o que separa este adendo de um desabafo:

> *"tem algumas que são ótimas"*

Ou seja: o banco tem distribuição, não um veredito. **"Mais da metade" é
impressão, e impressão não é número.** Este adendo existe para transformá-la em
número — antes de o motor rodar, publicado imagem a imagem, para qualquer um
abrir a fotografia e discordar.

## 2 · O CENSO

**Todas as 255**, em ordem alfabética do nome do arquivo, **sem amostra e sem
seleção**. Censo é o que torna o número inatacável: não há como perguntar "por
que essas?".

### 2.1 · O vocabulário, fechado em quatro

| tecla | significa |
|---|---|
| `v` | vejo a ferida e daria para traçar |
| `c` | cicatrizada — fechou, não há ferida |
| `n` | há ferida, mas não dá para traçar |
| `d` | em dúvida |

mais, independente da classe:

| | |
|---|---|
| `p` | há plástico/filme sobre a **ferida** (não sobre o anel) |

e um **comentário livre**, que é descritivo, **não é categoria**, não entra em
contagem e não vira variável de análise.

### 2.2 · Por que `c` é separado de `n`

Distinção levantada pelo Fabio às 15h21, antes da primeira classificação. São
**opostos**: "não vejo porque o curativo tapa" é informação perdida; "não vejo
porque fechou" é **área zero**, que é uma medida. Se as duas virassem a mesma
resposta, a tabela ficaria ilegível.

### 2.3 · Por que `p` aqui, se já existe no `MEDIDAS.txt`

O `p` do `MEDIDAS.txt` diz "plástico sobre o **anel**". Este diz "sobre a
**ferida**". São coisas diferentes, e a diferença é justamente a que importa: o
Fabio observou às 15h30 que em algumas imagens com plástico um humano laudaria
tranquilo e em outras é impossível. A marca antiga é grossa demais para separar
isso.

### 2.4 · Quem declara, e o que isso vale

Declara o Fabio — enfermeiro, 12 anos de SUS —, com o nome dele, e **o
julgamento é auditável porque a fotografia é pública**.

Fica registrado que ele **não é cego**: mediu 172 anéis, conhece os dias, e nas
horas anteriores formou a expectativa de que o plástico derruba o motor. Em
contrapartida, e também registrado: durante a medição ele **olhava o anel, não a
lesão**.

A proteção não é a cegueira dele, que não existe. São estas quatro:

1. **Nenhuma imagem é excluída** da rodada pré-registrada por esta
   classificação. Ela é variável, nunca filtro. As 255 continuam 255.
2. **Feita antes de o motor rodar.** Ele não sabe em quais o motor falha.
3. **Publicada linha a linha**, com as fotografias públicas: qualquer um
   confere.
4. **Uma segunda avaliadora**, cega, repete 50 delas, e a **concordância entre
   os dois é reportada**. Se divergirem, o tamanho da divergência é o resultado.

### 2.5 · A ferramenta

`classifica_ferida.py`,
`ddbee3eaa44146be7e259783e8e2b04d81c1c0cf28c268fa0e6cc7fecbcc5f93`, 14.285 B.

**Não mede nada.** Não há clique sobre a imagem, não há distância, não há
escala. Zoom pela roda, arrasto pelo botão direito, lupa, e o recorte publicado
pelos autores do banco ao lado.

Grava em `CLASSIFICACAO.txt`, APPEND com `fsync` a cada declaração. **O arquivo
nunca é reescrito:** reclassificar entra como **linha nova**, vale a última, e as
anteriores ficam como histórico — e é assim que se audita quem mudou de ideia e
quando.

Ensaio antes de qualquer uso: vocabulário fechado em quatro; comentário sem
tabulação nem quebra de linha; leitura devolve a última linha de cada nome com o
histórico preservado no arquivo; censo só de `.tif`/`.tiff` em ordem alfabética;
ida e volta tela↔original exata nos 6 zooms e em qualquer posição de arrasto.

## 3 · O QUE A LITERATURA DIZ, E O QUE ELA NÃO DIZ

Procurado em 02/10 a pedido do Fabio, que duvidava que traçar ferida com
artefato por cima fosse aceitável.

**Não existe regra explícita.** Não se achou documento afirmando que fotografia
com curativo sobre a ferida seja inelegível para traçado. Isso é, em si, um
achado: **o campo não tem critério declarado de elegibilidade** para o que conta
como fotografia de ferida avaliável.

**Mas o método de referência é de contato**, e portanto não executável aqui. O
traçado padrão consiste em *"applying a two-layer transparent acetate over the
wound and tracing the perimeter with a permanent pen"*, com a advertência de que
*"Leaning too heavily on the wound border can distort the wound shape"*
(Gethin, Wounds UK). Planimetria idem: *"may be taken either directly on the
wound or indirectly from a tracing"*. Com splint, coverslip e Tegaderm por cima,
**o método de referência não pode ser realizado** — não por proibição, por
impossibilidade física.

A fotografia aparece na literatura exatamente como a alternativa que *"avoids...
direct contact with the wound"* (Phlebolymphology/Servier) — ela existe para
fotografar a ferida, não o curativo.

**E a literatura já afirma o que este projeto vem sustentando**: o perímetro é
*"an entirely subjective estimate that depends on the observer"*, com
dificuldade maior na *"difficult delineation of the epidermis edge, owing to its
thinness and translucency"* (idem). Fonte independente, com a palavra
*translucency* dentro.

As **IMI National Guidelines** (Institute of Medical Illustrators, *Wound
Management*) tratam a retirada do curativo como parte do preparo — *"especially
if dressings are being removed in preparation for photography"* — e exigem que
*"The wound and the surrounding area... should be cleaned before photography."*
Ressalva declarada: a IMI é de fotografia **clínica humana**; a aplicação a um
banco pré-clínico de camundongo é por **analogia**.

## 4 · O DESENHO DE TRÊS BRAÇOS, PARA O ESTUDO NOVO

A rodada pré-registrada das 255 **não muda e não exclui nada**. O que segue é um
**estudo novo**, com pré-registro próprio, usando a classificação da §2 como
critério — declarado antes de o motor rodar em qualquer imagem.

| braço | imagens | o que mede |
|---|---|---|
| **principal** | ferida visível (`v`), sem plástico | acerto |
| **controle negativo** | cicatrizadas (`c`) | **falso positivo** |
| **excluídas, mas contadas** | com plástico | o tamanho do problema do banco |

### 4.1 · Por que as cicatrizadas NÃO são excluídas

O Fabio propôs às 15h37 tirar as cicatrizadas junto com as de plástico. **Não.**

Numa ferida fechada a resposta certa do motor é **não achar nada**. Se ele pintar
área ali, é **falso positivo** — e taxa de falso positivo em medida de ferida
quase nunca é reportada: o campo mede acerto onde a ferida existe e raramente
mede quantas vezes o método inventa ferida onde não há. O banco traz esse
controle de graça, na mesma rodada, sem gastar imagem. Excluí-las seria jogar
fora o único dado de especificidade disponível.

### 4.2 · A terceira linha é a honestidade

As excluídas **aparecem no artigo com número**. Não somem. A frase é
*"restringimos às fotografias que atendem à condição aceita para fotografia de
ferida — leito exposto — e eram N de 255"*, não *"excluímos as difíceis"*.

## 5 · DECLARAÇÃO DE IMAGENS ABERTAS

Pela mesma regra do Adendo 2 — olhar foto não é medir, mas o registro é a regra.

O Opus abriu diretamente **três** imagens do banco, às 13h58, para verificar se a
régua da cena era utilizável: `Day 10_Y8-1-R`, `Day 11_Y8-3-L`, `Day 13_Y8-4-R`.
Além dessas, recebeu do operador, ao longo do dia, **capturas de tela** de
imagens que ele estava medindo. Nada do que está congelado mudou por isso, e
nenhuma medida foi feita a partir dessas visualizações.

## 6 · O QUE NÃO MUDA

A rodada das 255, uma só, **zero exclusão**; escala pelo anel externo de 16 mm;
`px_mm = D/16`; recorte de 24 mm → 1380 → 700; `diam_ef` 11,5 mm; a grade de
144; a coroa da rodada 2 entre 145,83 e 233,33 px; semente 20260928; **nenhuma
constante do v0**; o detector congelado, reprovado nas 255 e intocado; o
`roda_camundongo.py` da Emenda 5 (`8c1f6e4d…`); o vocabulário `p;d;f` do
`MEDIDAS.txt`; a **P5** do pré-registro da rodada 2 (`3a27e63c…`) e o Adendo 1,
com o texto do Fabio inalterado; e tudo dos Adendos 3, 4 e 5.

---

*Opus, 02/10/2026, a pedido do Fabio. Hash colado do `sha256sum`. O motor não
rodou em nenhuma imagem até esta linha.*
