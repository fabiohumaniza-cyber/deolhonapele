# ADENDO 63 · reanálises pedidas pelo revisor, especificadas antes de rodar (EXPLORATÓRIAS)

**04/10/2026, Brasília, 17h55.** Uma revisão independente do rascunho v2 (o
texto da revisão fica com o autor) pediu reanálises. Elas estão especificadas
aqui **antes** de serem calculadas.

**São todas pós-hoc e exploratórias.** Os vereditos já registrados (P12, P15)
continuam valendo como estão. As coletas novas pedidas — operador
independente, terceiro leitor, repetição pelos mesmos leitores, remedição da
escala — exigem pré-registro próprio e não estão aqui.

## Unidade de reamostragem

**Animal** (8). Todo intervalo de confiança é IC 95 % por bootstrap agrupado
por animal: 5000 sorteios, semente 20261004, percentil. Ao lado de cada
mediana sai o IQR.

## Conjuntos

| nome | definição |
|---|---|
| **S_r** | braço principal (operador ok/nada, sem filme) ∩ leitor r TRACADA. É o conjunto do placar |
| **L_r** | leitor r TRACADA e sem filme, **sem o filtro do operador**. É o braço definido pelos leitores |
| **C** | os dois leitores TRACADA (55), estratificado em sem filme / com filme |

## Análises

| | o que se calcula | onde |
|---|---|---|
| R1 | Dice do motor (r4 e r3) e do nulo contra cada leitor, a diferença motor − nulo, e o Dice escalonado (D − Dnulo) / (1 − Dnulo) | S_r, L_r e C |
| R2 | segundo nulo, o **campo inteiro** (círculo `r_campo` do `CAMPO.txt`), contra cada leitor | S_r |
| R3 | **Bland-Altman da área** em mm², motor r4 − leitor: viés, limites de 95 % e viés relativo em % | S_r e L_r |
| R4 | **HD95 e ASSD em mm**, motor × leitor e leitor × leitor (escala do quadro: 700 px = 24 mm, 29,17 px/mm) | S_r e C |
| R5 | κ com IC agrupado: leitor × leitor e operador × cada leitor | 201 imagens |
| R6 | ρ de Spearman (dia, área r4) com IC agrupado | braço principal (71) e limpas da exec. 3 |
| R7 | subgrupos: idade (A × Y), animal e faixa de dia (0–4, 5–9, 10–15), com n, mediana de Dice e fração TRACADA de cada leitor | — |
| R8 | fluxo das imagens: 255 → escala → campo → declaração → braço → TRACADA | — |

**Código:** `reanalise_revisor.py`. O hash vai no commit deste adendo, antes
de rodar.

---

*Opus, 04/10/2026. Nenhuma destas contas foi feita até esta linha.*

`reanalise_revisor.py` SHA-256 `ccb94676b4970531f5523ff21d33177434fdb4bc006199b3700016674fe1db2e`.
