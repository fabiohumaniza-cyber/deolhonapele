# ADENDO 37 · resultado da rodada 4 — campo declarado mais a declaração do operador

**04/10/2026, Brasília.** A rodada 4 rodou no PC do Fabio e terminou às
**08h21:11**. Os hashes de código e de entrada, gravados pelo próprio driver,
**batem com o pré-registro** (Adendo 36, commit `689c129`). As três travas
passaram: o r3 refeito bateu com o `camundongo_r3.json` nas 201, e o r4 saiu
idêntico ao r3 nas 81 imagens `nada`.

| arquivo | SHA-256 |
|---|---|
| `dados/camundongo_r4.json` | `f113165112e63704d07f241375ae50ccc345a3eb1961821b618c746770d7b940` |
| `dados/CAMUNDONGO_R4_RELATORIO.md` | `bef307f74f1e6b451cda24776a6eb6c959f057bba79ad5eddcbdff3d46a3a90c` |

## 1 · O PLACAR

| predição | de quem | critério | resultado | |
|---|---|---|---|---|
| **P11.2** "tirando artefato vai surpreender" | Fabio | principal: Spearman ≤ −0,8 **e** mais negativo que o r3 | **−0,881** contra −0,860 | **confirmada** |
| **P14** "muitas que eu corrigi nem precisava" | Fabio | ≥ metade das 56 com Dice(r3, r4) ≥ 0,95 | **24 de 56** | **FALHOU** |
| **P13** borda falsa | Opus | ≥ 25 % das imagens com artefato (sem as 4 vistas) com ≥ 30 % do contorno colado no artefato | **3 de 43** | **FALHOU** |
| P12.1 / P12.3 | Fabio | contra os traçadores cegos | — | pendente |
| P12.2 (pelo) | Fabio | descritivo | 4 PELO, o motor deu área nas 4 | sem veredito |

**A P11.2 confirmada é por pouco** (−0,881 contra −0,860), e isso fica dito. A
curva do braço principal já caía na rodada 3. A declaração a deixou mais
inclinada, mas não a criou.

## 2 · A CURVA DO BRAÇO PRINCIPAL (71 imagens, sem filme)

Área mediana r4, em mm². O punch nominal é 28,27 mm².

| dia | 0 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| n | 16 | 6 | 4 | 4 | 7 | 6 | 5 | 4 | 5 | 4 | 4 | 3 | 2 | 1 |
| mm² | **26,2** | 22,6 | 25,3 | 21,9 | 17,0 | 13,5 | 6,5 | 5,2 | **3,1** | 5,4 | 7,7 | 5,2 | 14,9 | 2,3 |

No braço **com filme** (66, exploratório), a mediana caiu pouco: de 26,7 para
25,2 mm².

## 3 · O EFEITO DA CORREÇÃO (as 56 corrigidas)

- **24 de 56** saíram praticamente iguais (Dice r3×r4 ≥ 0,95). A mediana do
  Dice r3×r4 foi **0,91**.
- **7 de 56** mudaram muito (Dice < 0,5). Todas são imagens com artefato, como
  `Day 4_A8-4-L`, `Day 8_Y8-4-L`, `Day 9_Y8-1-L` e `Day 11_A8-1-L`.
- O **conta-gotas** sozinho mudou pouco: nas imagens do dia 0, o Dice ficou
  entre 0,80 e 0,999.
- A mediana da fração do campo marcada como artefato foi de **8,9 %**.

**A P14 falhou por pouco** (24 de 56 é 43 %, e o critério era 50 %). Quase
metade das correções não mudou a máscara. Isso é dado do trabalho: mostra
quanto o operador intervém sem necessidade.

## 4 · A BORDA FALSA NÃO APARECEU

Só **3 de 43** imagens tiveram ≥ 30 % do contorno colado no artefato. O Opus
esperava pelo menos 11. Os casos altos foram `Day 7_Y8-2-L` (0,50),
`Day 9_A8-1-R` (0,49) e `Day 0_Y8-4-R` (0,32). A `Day 8_Y8-2-L` (0,82) é uma
das 4 vistas antes do registro e não conta.

## 5 · O ACHADO NEGATIVO: AS CICATRIZADAS

Nas 5 cicatrizadas, a resposta certa é área ≈ 0. **O motor deu de 25,7 a
28,6 mm²** em todas, praticamente o tamanho do punch. **O motor v0 não sabe
dizer "não há ferida".** Diante de pele fechada, ele acha um contorno do
tamanho que espera achar.

Isso vai para o artigo com o mesmo peso do resto, e para a lista do v1.

## 6 · O QUE ISTO É E O QUE NÃO É

**É:** a medida assistida (motor com o operador), no braço sem filme,
seguindo uma ferida que fecha: de 26 mm² no dia 0 para 3 a 8 mm² nos dias 7 a
13.

**Não é acerto.** Sem traçado humano, a curva cair não prova que a máscara é a
ferida. O acerto vem com a Helga, o Emílio e as enfermeiras (P12.1 e P12.3).

---

*Opus, 04/10/2026. Placar copiado do relatório gerado pelo `analisa_rodada4.py`.*
