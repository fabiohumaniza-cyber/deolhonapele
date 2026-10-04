# ADENDO 41 · resultado do traçador cego Emílio — P12.1 e P12.3

**04/10/2026, Brasília, 11h04.** O `analisa_emilio.py` (`8c5f9233…`, publicado
no Adendo 40 antes de o arquivo ser aberto) rodou no PC do Fabio sobre o
arquivo lacrado (`afcbf928…`). As checagens de integridade passaram: versão
v2, declaração inicial marcada, 201 fotos fechadas e SHA de cada foto igual ao
do `_ORDEM`.

| arquivo | SHA-256 |
|---|---|
| `dados/tracado_camundongo_v2_emilio_2026-10-04.json` | `afcbf92870ffe5609bbc9be9e46f8f0cce089b5bb8949b3a69b50cd1499ff04a` |
| `dados/_ORDEM_v2_emilio.json` (agora público) | `e44ee2e7704ce4f418c483ec1404689e399ef2368bcdfdddc2bdfc47e0bc68be` |
| `dados/EMILIO_RELATORIO.md` | `66346e246a80ab2cfc3fea87758d304cc52f3f201544aac5b6d208a12b81db5c` |
| `dados/emilio_por_imagem.tsv` | `8f38658f0c7146f8f24a3080ee8565526836d0be7182559728f59b1a53327fac` |

## 1 · O PLACAR

| predição | critério | resultado | |
|---|---|---|---|
| **P12.1** Fabio, "traçados bons" | mediana Dice(r4, Emílio) ≥ 0,70 · braço principal e TRACADA (n = 48) | **0,899** | **confirmada** |
| **P12.3** Fabio, "quase todas certinhas" | ≥ 80 % com Dice ≥ 0,70 · mesmo conjunto | **90 %** (43 de 48) | **confirmada** |

## 2 · AO LADO, SEM VEREDITO

| conjunto | n | Dice r4 | Dice r3 (motor sozinho) | Dice nulo |
|---|---|---|---|---|
| principal + TRACADA | 48 | **0,899** | 0,895 | 0,602 |
| com filme + TRACADA | 23 | 0,941 | 0,935 | 0,856 |
| todas as traçadas, incluindo imaginadas (como o trabalho original) | 200 | 0,845 | 0,814 | 0,700 |
| só as IMAGINADAS | 45 | 0,511 | 0,475 | 0,496 |

## 3 · O QUE OS NÚMEROS DIZEM

1. **No braço principal, o motor fica muito acima do nulo** (0,90 contra 0,60).
   É a medida separando de verdade a ferida do círculo cego.
2. **A declaração do operador quase não mudou o acerto** nesse conjunto: 0,899
   com ela e 0,895 sem ela. Nas corrigidas, 0,888 contra 0,882. **O motor
   sozinho já acerta onde a borda é visível.** A correção mexeu onde a borda é
   ruim, e essas fotos o Emílio em geral não marcou como TRACADA.
3. **Com filme, o nulo já dá 0,86.** Ali o Dice alto do motor diz pouco. É o
   argumento do comparador nulo do primeiro artigo, repetido.
4. **Onde a borda foi imaginada, ninguém concorda com ninguém** (Dice ~0,5,
   igual ao nulo). Medir acerto contra borda imaginada não mede nada.
5. A razão de área r4/Emílio tem mediana de 1,06: o motor marca, em média, 6 %
   a mais.
6. **5 de 48 ficaram abaixo de 0,70:** `Day 14_A8-3-L` (0,25),
   `Day 6_Y8-2-R` (0,27), `Day 4_A8-5-R` (0,61), `Day 8_Y8-2-R` (0,64) e
   `Day 9_Y8-1-L` (0,70; sem a correção era 0,39).

## 4 · TRAÇABILIDADE: FABIO × EMÍLIO

| | Emílio TRACADA | Emílio não |
|---|---|---|
| Fabio mede (ok/nada) | 71 | 66 |
| Fabio exclui | **0** | 64 |

**Kappa 0,41.** As **64 que o Fabio excluiu, o Emílio também não marcou como
vistas**: nenhuma discordância nesse sentido. O Emílio foi **mais rigoroso**:
de 137 que o Fabio mediu, ele só disse "vejo a borda" em 71. Nas outras, marcou
PARCIAL (84 no total) ou IMAGINADA (45).

**Cicatrizadas:** das 5, o Emílio marcou 1 como FECHADA, 3 como IMAGINADA e
1 como PARCIAL. Nenhuma ele disse ver.

## 5 · TEMPO

Mediana de **35 s por foto** (p10 21 s, p90 59 s). Foram **145 min** do início
(08h36) ao salvo (11h01), **incluindo a pausa** das 09h46 às 10h03.

## 6 · O QUE DECLARAR, PORQUE PESA

- **O Emílio é irmão do Fabio.** Não viu as fotos antes, não viu o motor nem as
  marcas, e declarou isso no painel. Mas não é um leitor independente da
  família do projeto.
- **O Fabio acompanhou parte do traçado na tela.** Às 10h43 o Emílio pediu ao
  Fabio para mostrar uma foto ao Opus. O Opus respondeu que não podia comentar
  e não comentou (registrado na conversa).
- **É um traçador só, leigo** (ciência da computação, dois anos de
  veterinária). O acerto definitivo precisa de mais traçadores: Helga e as
  enfermeiras.
- **Não é comparável direto com o 0,96 do Carrión et al.** Lá, a rede foi
  **treinada** no mesmo anotador que a avaliou, e o conjunto de teste tinha ~32
  fotos. Aqui o motor **nunca viu** o Emílio. O mais próximo do desenho deles é
  a linha "todas as traçadas": **0,845**.

---

*Opus, 04/10/2026. Placar copiado do relatório gerado pelo `analisa_emilio.py`.*
