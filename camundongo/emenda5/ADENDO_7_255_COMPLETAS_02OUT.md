# ADENDO 7 · as 255 medidas, e o erro da regra medido nos próprios cliques

**02/10/2026, Brasília, 17h55.** O motor **não rodou em imagem nenhuma** e a
etapa 3 **não foi iniciada**. Nenhum resultado do motor existe até esta linha.

Adendo aos Adendos 1 a 6, que **não são alterados**. A §3 deste documento
**corrige um número publicado no Adendo 3**; o Adendo 3 permanece como está, com
o hash que tem, e a correção vive aqui.

## 0 · OS ARQUIVOS

| arquivo | SHA-256 | bytes |
|---|---|---|
| `MEDIDAS.txt` | `034da5175c49eaee09a1c83f86f251775661df586f2f05aa8a54c5fc6c3d031b` | 11.865 |
| `MEDIDAS_LOG.tsv` | `b525d85785c943ed13875b2ac7ffef7f54bad58439103e57c38b01b0c4dc1c2d` | 32.479 |

Ferramenta: `mede_anel.py` v6
(`d4e4e81bfce1db89462ce9dd451620c7378c9db20a1f9116551d54fb959ed9f2`).

---

## 1 · A MEDIÇÃO ESTÁ COMPLETA

**255 de 255.** Nenhuma imagem pulada, nenhuma amostra, zero exclusão, como o
pré-registro manda. 203 com diâmetro medido, 52 `SEM_ANEL`.

Oito imagens seguem para reabertura, pelos motivos já registrados: as seis do dia
0 medidas antes de a marca `p` existir (`Day 0_A8-1-L/-R`, `Day 0_A8-3-L/-R`,
`Day 0_A8-4-R`, `Day 0_A8-5-L`), a `Day 10_A8-1-L`, e a `Day 1_A8-4-L` da §5.

## 2 · O ERRO DA REGRA DAS DUAS MAIORES, AGORA MEDIDO

O Adendo 4 registrou que a média das duas maiores de seis distâncias só é exata
para o círculo, e que o erro real seria medido e não suposto. Está medido.

### 2.1 · O que foi feito

Para cada uma das 203 imagens com medida, os **mesmos quatro cliques** gravados
no `MEDIDAS_LOG.tsv` foram lidos de duas maneiras: pela regra em uso (média das
duas maiores distâncias) e por um **círculo ajustado por mínimos quadrados**
(Kåsa) aos quatro pontos. Nenhuma imagem foi reaberta e nenhum clique novo
existe: é a mesma matéria-prima, lida duas vezes.

### 2.2 · O resultado

| | |
|---|---|
| mediana da diferença | **−0,187 %** |
| média | −0,307 % |
| Q1 · Q3 | −0,402 % · −0,100 % |
| mínimo · máximo | **−2,603 %** · −0,002 % |
| IC95 da mediana (bootstrap 10000, semente 20260928) | −0,226 % a −0,154 % |
| em área (dobro) | **−0,37 %** |

**Os 203 erros são negativos. Todos.** Isso não é achado empírico, é propriedade
aritmética: a média de duas cordas nunca supera o diâmetro. A regra em uso
**subestima por construção**, nunca superestima, e agora o tamanho disso tem
número e intervalo.

### 2.3 · O aviso da ferramenta, e o que ele separa

A v6 avisa na tela quando a 3ª maior distância passa de 80 % do diâmetro — sinal
de que os quatro pontos não estão em cruz. Nas 203:

| | |
|---|---|
| 3ª maior / diâmetro — mediana | 78,3 % |
| Q1 · Q3 | 74,8 % · 83,1 % |
| mínimo · máximo | 71,0 % · 95,8 % |
| acima do limite de 80 % | **81 de 203** |

O valor exato para quatro pontos em cruz é 70,7 %. A mediana observada é 78,3 %,
ou seja, o clique humano fica sistematicamente um pouco fora da cruz — o que é
esperado e não era conhecido em número.

O aviso **separa de verdade**, e separa pouco: mediana do erro de **−0,356 %**
nas 81 marcadas contra **−0,143 %** nas 122 não marcadas. Diferença real, ordem
de grandeza irrelevante diante da dispersão de 3,27 % que a medida pelo buraco
mostrou no Adendo 5.

**Nenhuma imagem é remedida por causa disto.** O pior caso isolado é a
`Day 5_Y8-4-R`, −2,603 %, com o anel comido e o par geométrico impossível de
fechar — situação declarada na hora e mantida deliberadamente.

### 2.4 · O que o círculo ajustado NÃO é

Não é verdade, é outro estimador. Um anel inclinado projeta-se como elipse, e
quatro pontos **não determinam uma elipse** — são precisos cinco. O que a §2.2
mede é a **discordância entre duas leituras dos mesmos cliques**, o que limita o
erro, não a distância até o valor verdadeiro.

A verificação independente disso continua sendo a do Adendo 5: dois objetos
físicos diferentes do mesmo splint, medidos em momentos diferentes, o segundo às
cegas, concordando com viés de −0,72 % e IIQ de 3,27 %. Os −0,187 % desta nota
cabem folgadamente dentro daquilo.

### 2.5 · Decisão

A regra das duas maiores **continua sendo a regra**, sem alteração, porque estava
pré-registrada e porque o erro medido é pequeno e de direção conhecida. O valor
do círculo ajustado **não substitui nenhum número** e entra no relatório apenas
como esta nota de sensibilidade.

## 3 · DESPRENDIMENTO DO SPLINT: O NÚMERO DO ADENDO 3 ESTAVA ERRADO

O Adendo 3 registrou, com 92 e depois 144 medidas, que o `SEM_ANEL` não era
aleatório: **9 % nos velhos contra 52 % nos jovens**. Era amostra parcial e
enviesada para os dias finais. Com as 255 completas:

| | |
|---|---|
| velhos | **11 de 128 = 8,6 %** |
| jovens | **41 de 127 = 32,3 %** |
| total | 52 de 255 = 20,4 % |

A direção do achado se mantém — o jovem perde o splint quase **quatro vezes
mais** —, mas **a magnitude cai de 52 % para 32,3 %**, e quem citar os 52 % estará
citando número errado. Fica aqui, com o Adendo 3 intacto, como a regra de
imutabilidade manda.

E não é o grupo inteiro: são **três dos quatro animais jovens**.

| animal | sem anel |
|---|---|
| A8-1 | 2/32 |
| A8-3 | **0/32** |
| A8-4 | 3/32 |
| A8-5 | 6/32 |
| Y8-1 | **14/32** |
| Y8-2 | 2/31 |
| Y8-3 | **11/32** |
| Y8-4 | **14/32** |

O `A8-3` não perdeu o splint uma única vez em 32 fotografias. O `Y8-2` perdeu
duas vezes em 31 — menos que dois dos quatro velhos.

## 4 · O PADRÃO POR DIA É MAIS FORTE QUE A PORCENTAGEM

| dia | velhos | jovens |
|---|---|---|
| 0 a 6 | **0/56** (exceto a §5) | **0/56** |
| 7 | 0/8 | 2/8 |
| 8 | 0/8 | 2/8 |
| 9 | 0/8 | 2/7 |
| 10 | 0/8 | 3/8 |
| 11 | 1/8 | 6/8 |
| 12 | 1/8 | 6/8 |
| 13 | 1/8 | 6/8 |
| 14 | 2/8 | 6/8 |
| 15 | 5/8 | **8/8** |

A frase que isto autoriza é mais precisa que qualquer percentual único:

> **O splint segura igual nos dois grupos durante a primeira semana. O jovem
> começa a perdê-lo no dia 7; o velho, no dia 11 — quatro dias depois.**

E o dia 15 desaba nos dois grupos porque é o dia da coleta: o cartão da própria
fotografia diz *"Collect Day 15"*. Ali o splint é retirado, não perdido.

## 5 · O `n` ACIDENTAL: OS DADOS O ACUSARAM SOZINHOS

A linha

```
Day 1_A8-4-L.tiff	SEM_ANEL	-	-	p
```

é a **única** perda em animal velho antes do dia 11, isolada no meio de oitenta
imagens consecutivas com anel medido. E está marcada `p` — plástico **sobre o
anel** —, marca que só pode existir se houve anel escolhido.

O operador relatou o engano no momento em que ocorreu, antes de qualquer análise.
Fica registrado que a tabela o revela de forma independente do relato, e que a
imagem entra no lote de reabertura.

## 6 · O CENSO DAS MARCAS

| marca | imagens | fração das 255 |
|---|---|---|
| `p` plástico/reflexo sobre o anel | **153** | **60,0 %** |
| `d` dois anéis no quadro | 105 | 41,2 % |
| `f` pelo dentro do anel | 12 | 4,7 % |

**Seis em cada dez fotografias do banco têm filme ou reflexo sobre o objeto de
escala.** Este é o número que sustenta, com dado em vez de impressão, a discussão
do Adendo 6 sobre fotografia de ferida com curativo por cima. Ele não é usado
como filtro em lugar nenhum da rodada pré-registrada.

## 7 · UM LIMITE FÍSICO QUE DISPENSA TRAÇADOR

Declarado aqui, antes de o motor rodar, e verificável por qualquer um:

A ferida é feita com **punch de 6 mm**, área **28,2743 mm²**, e ferida de
excisão **só encolhe** depois do dia 0. Portanto, em qualquer dia ≥ 1, **área
devolvida pelo motor acima de 28,2743 mm² é impossível** — não é discordância
com um traçador, é violação do padrão físico do próprio experimento.

Isto não é critério de exclusão nem ajuste: é uma **conferência**, que será
reportada como contagem de quantas imagens a violam, qualquer que seja o número.
Vale para as 255, inclusive as 52 sem escala, onde o limite se aplica depois da
conversão de px² quando houver.

## 8 · O QUE NÃO MUDA

A rodada das 255, uma só, **zero exclusão**; a escala pela borda externa de 16 mm
e `px_mm = D/16`; a regra das duas maiores; recorte de 24 mm → 1380 → 700;
`diam_ef` 11,5 mm; a grade de 144; a coroa da rodada 2 entre 145,83 e 233,33 px;
semente 20260928; **nenhuma constante do v0**; o detector congelado, reprovado
nas 255 e intocado; o `roda_camundongo.py` da Emenda 5 (`8c1f6e4d…`); o
vocabulário `p;d;f`; a **P5** do pré-registro da rodada 2 (`3a27e63c…`) e o
Adendo 1 com o texto do Fabio inalterado; e tudo dos Adendos 3, 4, 5 e 6 —
ressalvado apenas o número corrigido na §3.

---

*Opus, 02/10/2026. Hashes colados do `sha256sum`. Todos os números desta nota
foram calculados sobre o `MEDIDAS.txt` de hash `034da517…` e o `MEDIDAS_LOG.tsv`
de hash `b525d857…`, trazidos do PC do Fabio neste instante. O motor não rodou em
nenhuma imagem até esta linha.*
