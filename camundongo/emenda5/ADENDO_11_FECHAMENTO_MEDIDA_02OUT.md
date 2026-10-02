# ADENDO 11 · fechamento da medida manual — os hashes sobre os quais o motor vai rodar

**02/10/2026, Brasília, 20h10.** O motor **não rodou em imagem nenhuma** e a
etapa 3 **não foi iniciada**. Nenhum resultado do motor existe até esta linha.

Este é o último adendo antes de o motor rodar. Ele existe para uma coisa: fixar,
com hash publicado, **exatamente os arquivos sobre os quais a rodada
pré-registrada vai ser executada**. Nada aqui altera os Adendos 1 a 10.

## 0 · OS ARQUIVOS DA RODADA

| arquivo | SHA-256 | bytes |
|---|---|---|
| `MEDIDAS.txt` | `7aaebccef0ec8875b07feb5ef82e0b0eaa6c6d5fe2c2f0941e9eee2005c773c4` | 11.876 |
| `MEDIDAS_LOG.tsv` | `9783dbd43d9dedad705259a638f452a67850592276d766cd7bddc8d2d7808456` | 33.241 |
| `CLASSIFICACAO.txt` | `3f10f490e964fc5beef5b459845c564ee74872cc18e75bab84f6882fac35d704` | 18.389 |

E os dois arquivos que a reabertura das 19h52 produziu, que tornam a operação
reversível por qualquer um:

| arquivo | SHA-256 |
|---|---|
| `MEDIDAS_ATE_20261002_195253.txt` | `034da5175c49eaee09a1c83f86f251775661df586f2f05aa8a54c5fc6c3d031b` |
| `REABERTURA_20261002_195253.tsv` | `6aecda8bb084e9768c13e4eaf29c21fb1d20152bd59b3570110535d4f3d609fa` |

**A cópia de segurança saiu com o hash `034da517…`, que é exatamente o registrado
na §0 do Adendo 7.** O arquivo não foi tocado entre o registro e a reabertura, e
isso é verificável sem acreditar em ninguém.

## 1 · AS SEIS REABERTURAS, E O QUE ELAS MOSTRARAM

Reabertas às 19h52 pelo critério da §1 abaixo e remedidas até 19h58:

| imagem | antes | agora | diferença |
|---|---|---|---|
| `Day 0_A8-1-L` | 604,912 | 599,793 | **−0,85 %** |
| `Day 0_A8-1-R` | 603,580 | 595,231 | **−1,38 %** |
| `Day 0_A8-3-L` | 595,313 | 598,989 | **+0,62 %** |
| `Day 0_A8-3-R` | 593,124 | 591,885 | **−0,21 %** |
| `Day 10_A8-1-L` | 610,006 | 598,247 | **−1,93 %** |
| `Day 1_A8-4-L` | `SEM_ANEL` | **594,477** | — |

**O critério da reabertura.** As quatro primeiras foram medidas antes das
**06h18 de 02/10**, hora em que a marca `p` aparece pela primeira vez em todo o
`MEDIDAS_LOG.tsv`. As duas outras imagens do dia 0 sem `p` — `Day 0_A8-4-R`
(06h20) e `Day 0_A8-5-L` (06h22) — foram medidas **depois** desse marco, entre
imagens em que o `p` foi aplicado, e portanto são declarações e não omissões.
Não foram reabertas. O corte é temporal, verificável no log, e foi decidido
antes de qualquer remedição.

### 1.1 · Repetibilidade intra-observador, um dado que apareceu de graça

As cinco imagens que tinham medida foram medidas **duas vezes pelo mesmo
operador, em dias diferentes, sem ver o valor anterior**, pela mesma regra
escrita. A diferença entre as duas leituras ficou entre **−1,93 % e +0,62 %**.

Isto é repetibilidade intra-observador de medida de escala manual, e praticamente
não se reporta esse número na literatura de ferida. São cinco imagens — descritivo,
não teste. Fica registrado como tal.

### 1.2 · O `n` acidental: confirmado

A `Day 1_A8-4-L` tinha anel o tempo todo, e agora mede 594,477 px. O engano foi
relatado pelo operador no momento em que ocorreu, apareceu sozinho na tabela como
anomalia (§5 do Adendo 7), e está desfeito. `SEM_ANEL` cai de 52 para **51**.

## 2 · A MARCA `d` NÃO É REPRODUTÍVEL, E NÃO SERÁ REPORTADA COMO CONTAGEM

As seis reaberturas voltaram todas com marca `-`, inclusive três que antes tinham
`d` ou `p;d`. Perguntado, o operador explicou às 20h00:

> *"eu mudo a posição, cara... é isso"*

Ou seja: `d` ("dois anéis no quadro") depende do **enquadramento na hora de
medir** — zoom e arrasto —, não da fotografia. Quem aproxima até sobrar um anel
só na tela não vê dois anéis, e não marca.

Consequência, declarada antes de o motor rodar:

1. **O `d` foi aplicado de forma inconsistente nas 255.** As 103 imagens que o
   têm não são "as imagens do banco com dois anéis no quadro".
2. **O `d` não será reportado como contagem**, nem usado como variável em
   análise nenhuma. Quem quiser saber em quantas fotografias aparecem dois anéis
   abre as fotografias, que são públicas, e conta.
3. **Nada do que importa depende dele.** O `d` nunca entrou na escala, no
   `px_mm`, nem em conta alguma. O risco que ele existia para sinalizar — medir o
   anel da ferida errada — continua tratado pelo recorte de referência do banco,
   que fica na tela ao lado durante toda a medição.
4. O `p` e o `f` **não** têm esse problema: filme sobre o anel e pelo dentro do
   anel são propriedades da fotografia, não do enquadramento.

Isto corrige, na prática, o uso do vocabulário `p;d;f` fixado na Emenda 5. A
Emenda 5 permanece com o hash que tem.

## 3 · OS NÚMEROS FINAIS DA MEDIDA MANUAL

**255 imagens · 204 com diâmetro medido · 51 `SEM_ANEL` · zero exclusão.**

Marcas: `p` 158 · `d` 103 (não reportado, §2) · `f` 12.

### 3.1 · Desprendimento do splint

| | |
|---|---|
| velhos | **10 de 128 = 7,8 %** |
| jovens | **41 de 127 = 32,3 %** |
| total | 51 de 255 = 20,0 % |

Substitui o 8,6 % × 32,3 % da §3 do Adendo 7, que por sua vez já substituía o
9 % × 52 % do Adendo 3. A mudança é a correção do `n` acidental, uma imagem.

Por animal: A8-1 2/32 · **A8-3 0/32** · A8-4 2/32 · A8-5 6/32 · Y8-1 14/32 ·
Y8-2 2/31 · Y8-3 11/32 · Y8-4 14/32.

### 3.2 · E o bloco inicial ficou limpo

Com o `n` acidental desfeito, **os dias 0 a 6 têm zero perdas nos dois grupos** —
112 fotografias consecutivas, sem uma exceção. O jovem começa a perder o splint
no **dia 7**; o velho, no **dia 11**. O dia 15 desaba nos dois porque é o dia da
coleta.

A frase do Adendo 7 fica mais forte, não mais fraca.

### 3.3 · O erro da regra das duas maiores, recalculado

| | |
|---|---|
| mediana | **−0,197 %** |
| IC95 (bootstrap 10000, semente 20260928) | −0,231 % a −0,158 % |
| pior caso | −2,603 % (`Day 5_Y8-4-R`) |
| em área | **−0,39 %** |
| 3ª maior ≥ 80 % do diâmetro | 81 de 204 (mediana 78,3 %) |

Todos os 204 erros continuam negativos. A regra subestima por construção. Sem
alteração de conclusão em relação à §2 do Adendo 7.

## 4 · O CRUZAMENTO, E O CONJUNTO LIMPO

| | `v` | `c` | `n` | `d` | % `v` |
|---|---|---|---|---|---|
| **51 `SEM_ANEL`** | **0** | 9 | 27 | 15 | **0,0 %** |
| 204 com anel | 132 | 0 | 35 | 37 | 64,7 % |

**Nenhuma das 51 imagens sem splint tem ferida legível.** Inalterado.

**Braço principal: 70 imagens** — `v`, sem plástico sobre a ferida, com escala
pelo anel. **27,5 % das 255.** Controle negativo: 9 cicatrizadas, nenhuma com
escala, o que não o invalida.

## 5 · A PARTIR DAQUI O MOTOR PODE RODAR

Tudo o que o pré-registro exigia estar escrito antes está escrito e com hash
publicado: a rodada das 255 e as suas constantes (Adendo 1 e pré-registro da
rodada 2, `3a27e63c…`), a escala e o seu erro medido (Adendos 4, 5 e 7), o censo
de legibilidade e os três braços (Adendos 6, 9 e 10), a redação da exclusão e as
rodadas secundárias (Adendo 8), e os arquivos de entrada desta §0.

O que o motor devolver será publicado inteiro, qualquer que seja — incluindo a
contagem de imagens que violarem o limite físico de **28,2743 mm²** da §7 do
Adendo 7.

A **P6** não foi dada e não será inventada. O relatório dirá que não houve P6.

## 6 · O QUE NÃO MUDA

A rodada das **255, uma só, zero exclusão**; a escala pela borda externa de 16 mm
e `px_mm = D/16`; a regra das duas maiores; recorte de 24 mm → 1380 → 700;
`diam_ef` 11,5 mm; a grade de 144; a coroa entre 145,83 e 233,33 px; semente
20260928; **nenhuma constante do v0**; o detector congelado, reprovado nas 255 e
intocado; o `roda_camundongo.py` da Emenda 5 (`8c1f6e4d…`); o limite físico de
28,2743 mm²; e tudo dos Adendos 3 a 10, ressalvados os números corrigidos em cada
um deles.

---

*Opus, 02/10/2026. Hashes colados do `sha256sum`. Todos os números deste adendo
foram calculados sobre os três arquivos da §0, trazidos do PC do Fabio neste
instante. O motor não rodou em nenhuma imagem até esta linha.*
