# ADENDO 28 · PRÉ-REGISTRO DA RODADA 3 — o campo declarado

**03/10/2026, Brasília, 09h40.** Escrito **antes** de a rodada 3 rodar em
qualquer imagem do banco.

## 0 · OS ARQUIVOS

| arquivo | SHA-256 |
|---|---|
| `roda_rodada3.py` (driver) | `72cfb5cc420f1e1766954955b433948139e3fc2e93c9b09090ee25d66620f2c0` |
| `analisa_rodada3.py` (placar) | `fab878ef7474b837c8bfbd0e9f3f2b1271319a949ee3ace5eec40de254992b7b` |
| `dados/CAMPO.txt` (o campo, Adendo 15) | `91160713dc9b01686ec6b3d3426052eece1ed3cb1ef58342f67a731c5c36d7c1` |

O motor é o v0 congelado, **sem nenhuma constante alterada**. O driver importa
`roda_camundongo.py` (`8c1f6e4d…`), `motor_v0_funcoes.py` (`16028493…`) e
`roda_rodada2.py` (`420ff85b…`).

## 1 · O QUE O MOTOR ENXERGA

**Só o círculo amarelo** que o Fabio colocou à mão em 201 imagens, 0,3 mm para
dentro da borda visível do laranja. As 3 NAO_DA e as 51 SEM_ANEL **não rodam**.

## 2 · COMO O CAMPO ENTRA — E O QUE NÃO FUNCIONOU

O motor estima a **pele de referência** pela moldura de 8 % do quadro, menos o
`ar`. Foram testados dois desenhos, em 30 cenas sintéticas (semente 20260928,
mesma geometria do Adendo 24, operador encostando o verde em 4,3 mm):

| desenho | o que é | ferida achada | `None` |
|---|---|---|---|
| **A** | `ar` = tudo fora do círculo, no quadro de 700 | **0 / 30** | **30 / 30** |
| **B** | recorte **quadrado circunscrito** ao círculo, **mesma escala** (29,167 px/mm, sem reamostrar); `ar` = os 4 cantos fora do círculo | **30 / 30** | 0 / 30 |

O A falha **por construção**: a moldura inteira fica fora do campo, a mediana
da pele sai de um conjunto vazio e o motor não mede nada. **A rodada 3 usa o B.**
Com ele, a referência de pele é a faixa **dentro do campo, junto da borda**, a
pele que fica em volta da ferida.

**Consequência, declarada antes:** quando a ferida encosta na borda do campo,
ela contamina a referência de pele. Isso tende a acontecer nos primeiros dias,
com a ferida grande e descentrada.

## 3 · AS PREVISÕES

### P11 — do Fabio, verbatim, às 09h36

> *"agora vai mudar mais. ... porem tirandoartefato é q vai surpriender...."*

- **P11.1** "vai mudar mais": confirma se o número de imagens com **Dice > 0**
  contra o nulo, entre as 201, for **maior que 56**, que foi o da rodada 2.
- **P11.2** "tirando artefato é que vai surpreender": é previsão da **rodada 4**.
  Será traduzida em critério no pré-registro dela.

*Os critérios são do Opus. Se o Fabio ler diferente, a leitura dele vai em
arquivo novo e vale ao lado desta.*

### P10 — do Opus

- **P10.1 — a curva não cai, nas 201:** Spearman(dia, área mediana), nos dias
  com n ≥ 8 (o mesmo limiar da P2), **maior que −0,8**. É a P2 da rodada 1
  repetida, apostando que ela **continua falhando**.
  *Por quê:* com plástico e reflexo dentro do campo, o motor ainda vai pegar o
  que brilha mais, e não a ferida que fecha.
- **P10.2 — a curva não cai, nem nas limpas:** o mesmo, só nas `v` sem `p`, nos
  dias com n ≥ 3. **Maior que −0,8.**
  *Por quê:* nas limpas restam pelo no leito, sangue e ponto, e a ferida dos
  últimos dias é pequena e clara.
- **P10.3 — o motor pega o campo inteiro:** pelo menos **20 das 201** com
  máscara ≥ 80 % da área do campo.
  *Por quê:* sem nada fora para pegar, o contorno mais forte que sobra pode ser
  a própria borda do campo.

## 4 · O QUE A RODADA 3 NÃO MEDE

**Acerto.** Sem traçado humano, Dice > 0 contra o nulo quer dizer "a máscara
encosta no centro", e não "a máscara é a ferida". O que a rodada 3 pode
mostrar é **se a curva cai com os dias**, porque a ferida de verdade fecha (P2,
P10.1 e P10.2). O acerto vem com os traçadores (Adendo 19).

## 5 · ORDEM

1. Este arquivo, com hash, publicado.
2. O Fabio roda `roda_rodada3.py rodar` e depois `analisa_rodada3.py`.
3. O resultado vai num adendo próprio, com o placar copiado do relatório.

---

*Opus, 03/10/2026. Nenhum resultado da rodada 3 existe até esta linha.*
