# RODADA 4 — campo declarado + declaracao do operador

imagens: 201 · medidas (ok + nada): 137 · principal 71 · com filme 66 · excluidas 64

## Trava

imagens sem correcao (nada): 81 · r4 identico a r3 em todas: True

## Bracos

| braco | n | com medida r4 | area mediana r3 | area mediana r4 |
|---|---|---|---|---|
| principal (sem filme) | 71 | 71 | 22.23 | 17.02 |
| com filme (exploratorio) | 66 | 66 | 26.71 | 25.15 |
| excluidas (descritivo) | 64 | 64 | 27.37 | 27.37 |
| cicatrizadas (exploratorio) | 5 | 5 | 28.29 | 28.29 |

## Placar (criterios do Adendo 36)

| | criterio | resultado | |
|---|---|---|---|
| P11.2 Fabio "tirando artefato vai surpreender" | principal: Spearman(dia, mediana r4) <= -0,8 (dias n >= 3) E mais negativo que r3 nas mesmas | r4 -0.881 · r3 -0.860 (12 dias) | confirmada |
| P14 Fabio "muitas que eu corrigi nem precisava" | >= metade das 56 corrigidas com Dice(r3, r4) >= 0.95 | 24 de 56 | FALHOU |
| P13 Opus: borda falsa | >= 25 % das imagens com artefato no campo (sem as 4 vistas) com >= 30 % do contorno colado no artefato | 3 de 43 | FALHOU |
| P12.1 / P12.3 Fabio | contra os tracadores cegos | — | avaliadas com os tracadores |
| P12.2 Fabio (pelo) | descritivo | 4 PELO; r4 obtida em 4 | sem veredito |

Curva do braco principal, r4 (dia: n, mediana mm2): 0: 16, 26.2 · 2: 6, 22.6 · 3: 4, 25.3 · 4: 4, 21.9 · 5: 7, 17.0 · 6: 6, 13.5 · 7: 5, 6.5 · 8: 4, 5.2 · 9: 5, 3.1 · 11: 4, 5.4 · 12: 4, 7.7 · 13: 3, 5.2 · 14: 2, 14.9 · 15: 1, 2.3

## Efeito da correcao (as 56 corrigidas)

| imagem | estado | conta-gotas % campo | artefato % campo | area r3 | area r4 | Dice r3 x r4 | borda falsa |
|---|---|---|---|---|---|---|---|
| Day 0_A8-1-R | sem filme | 5.6 | 0.0 | 28.94 | 28.92 | 0.999 | - |
| Day 0_A8-3-L | sem filme | 1.3 | 0.0 | 28.15 | 26.29 | 0.965 | - |
| Day 0_A8-3-R | sem filme | 8.6 | 0.0 | 31.74 | 29.25 | 0.954 | - |
| Day 0_A8-4-L | sem filme | 3.0 | 0.0 | 28.48 | 28.46 | 0.999 | - |
| Day 0_A8-4-R | sem filme | 0.6 | 0.0 | 26.59 | 26.71 | 0.998 | - |
| Day 0_A8-5-L | sem filme | 17.1 | 0.0 | 27.03 | 28.38 | 0.933 | - |
| Day 0_A8-5-R | sem filme | 4.5 | 0.0 | 27.92 | 27.96 | 0.999 | - |
| Day 0_Y8-1-R | sem filme | 10.4 | 0.0 | 29.28 | 19.43 | 0.796 | - |
| Day 0_Y8-2-L | sem filme | 0.4 | 0.0 | 27.36 | 27.40 | 0.999 | - |
| Day 0_Y8-2-R | sem filme | 2.6 | 0.0 | 19.47 | 16.41 | 0.881 | - |
| Day 0_Y8-3-L | sem filme | 1.6 | 17.3 | 32.36 | 17.51 | 0.683 | 0.06 |
| Day 0_Y8-4-R | sem filme | 1.1 | 6.2 | 22.97 | 23.82 | 0.941 | 0.32 |
| Day 1_A8-3-L | filme | 0.0 | 1.9 | 25.51 | 25.70 | 0.993 | 0.03 |
| Day 1_A8-3-R | filme | 4.9 | 0.0 | 29.96 | 28.56 | 0.976 | - |
| Day 1_A8-4-L | filme | 0.0 | 1.7 | 21.36 | 20.98 | 0.991 | 0.05 |
| Day 1_Y8-2-L | filme | 0.0 | 11.4 | 29.76 | 29.51 | 0.993 | 0.03 |
| Day 1_Y8-3-R | filme | 0.0 | 13.3 | 26.79 | 26.81 | 0.987 | 0.18 |
| Day 2_A8-4-L | filme | 0.0 | 21.3 | 28.21 | 27.68 | 0.767 | 0.12 |
| Day 2_Y8-2-L | filme | 0.0 | 9.1 | 21.98 | 21.52 | 0.990 | 0.04 |
| Day 2_Y8-3-L | sem filme | 17.5 | 3.4 | 27.85 | 29.13 | 0.800 | 0.10 |
| Day 3_A8-4-L | filme | 0.0 | 5.2 | 28.79 | 23.05 | 0.450 | 0.00 |
| Day 3_A8-4-R | filme | 0.0 | 11.6 | 30.91 | 24.05 | 0.875 | 0.20 |
| Day 3_A8-5-R | filme | 0.9 | 8.8 | 27.19 | 21.42 | 0.875 | 0.21 |
| Day 3_Y8-1-L | filme | 0.0 | 3.8 | 22.05 | 22.62 | 0.987 | 0.00 |
| Day 3_Y8-3-L | sem filme | 1.3 | 5.4 | 30.01 | 27.53 | 0.648 | 0.06 |
| Day 4_A8-4-L | filme | 0.0 | 21.9 | 26.58 | 0.66 | 0.048 | 0.00 |
| Day 4_Y8-2-L | filme | 0.0 | 6.1 | 28.13 | 27.27 | 0.965 | 0.20 |
| Day 4_Y8-3-L | filme | 0.0 | 5.3 | 28.14 | 26.75 | 0.975 | 0.20 |
| Day 4_Y8-4-L | filme | 1.3 | 0.8 | 24.90 | 20.64 | 0.906 | 0.01 |
| Day 5_A8-4-L | filme | 0.0 | 19.0 | 26.40 | 19.81 | 0.662 | 0.02 |
| Day 5_A8-5-R | sem filme | 0.0 | 13.2 | 26.38 | 25.71 | 0.915 | 0.03 |
| Day 6_Y8-1-L | filme | 0.0 | 11.4 | 17.44 | 23.85 | 0.690 | 0.09 |
| Day 6_Y8-3-R | sem filme | 0.0 | 12.4 | 21.38 | 7.33 | 0.511 | 0.07 |
| Day 6_Y8-4-L | sem filme | 0.0 | 8.9 | 27.89 | 6.82 | 0.393 | 0.11 |
| Day 6_Y8-4-R | sem filme | 0.0 | 15.6 | 24.38 | 11.62 | 0.646 | 0.05 |
| Day 7_A8-5-R | sem filme | 0.0 | 20.9 | 11.73 | 12.89 | 0.953 | 0.00 |
| Day 7_Y8-1-L | filme | 0.0 | 3.3 | 11.19 | 11.12 | 0.997 | 0.00 |
| Day 7_Y8-2-L | filme | 0.0 | 17.8 | 27.87 | 16.68 | 0.749 | 0.50 |
| Day 7_Y8-2-R | sem filme | 0.0 | 7.6 | 3.19 | 3.10 | 0.985 | 0.00 |
| Day 8_A8-3-R | filme | 0.0 | 1.2 | 24.34 | 24.09 | 0.995 | 0.06 |
| Day 8_A8-4-L | filme | 0.0 | 11.9 | 24.64 | 23.10 | 0.963 | 0.14 |
| Day 8_A8-5-L | filme | 0.0 | 4.5 | 25.40 | 19.84 | 0.857 | 0.04 |
| Day 8_A8-5-R | sem filme | 0.0 | 51.8 | 5.90 | 4.93 | 0.910 | 0.00 |
| Day 8_Y8-1-L | filme | 0.0 | 15.7 | 16.33 | 14.01 | 0.884 | 0.21 |
| Day 8_Y8-2-L | sem filme | 0.0 | 67.7 | 24.41 | 12.11 | 0.663 | 0.82 |
| Day 8_Y8-3-R | filme | 0.0 | 20.1 | 28.02 | 24.89 | 0.810 | 0.13 |
| Day 8_Y8-4-L | sem filme | 0.0 | 49.0 | 24.31 | 5.49 | 0.270 | 0.00 |
| Day 9_A8-1-L | filme | 0.0 | 22.2 | 26.97 | 6.73 | 0.399 | 0.10 |
| Day 9_A8-1-R | filme | 0.0 | 36.1 | 27.89 | 16.84 | 0.753 | 0.49 |
| Day 9_Y8-1-L | sem filme | 0.0 | 23.1 | 24.11 | 3.12 | 0.229 | 0.00 |
| Day 9_Y8-2-L | sem filme | 0.0 | 61.3 | 20.55 | 8.68 | 0.594 | 0.11 |
| Day 9_Y8-3-L | sem filme | 0.0 | 1.2 | 5.83 | 5.81 | 0.998 | 0.00 |
| Day 9_Y8-3-R | sem filme | 0.0 | 14.2 | 2.59 | 3.02 | 0.925 | 0.00 |
| Day 9_Y8-4-L | sem filme | 0.0 | 17.8 | 3.23 | 3.04 | 0.970 | 0.00 |
| Day 11_A8-1-L | sem filme | 0.0 | 25.0 | 29.91 | 3.70 | 0.220 | 0.00 |
| Day 11_A8-1-R | sem filme | 0.0 | 2.6 | 5.23 | 5.25 | 0.997 | 0.00 |

## Cicatrizadas (resposta certa ~0)

| imagem | estado | area r3 | area r4 |
|---|---|---|---|
| Day 10_Y8-2-R | NAO_TRACAVEL | 25.71 | 25.71 |
| Day 10_Y8-3-L | NAO_TRACAVEL | 28.60 | 28.60 |
| Day 10_Y8-4-L | NAO_TRACAVEL | 28.45 | 28.45 |
| Day 13_Y8-2-L | NAO_TRACAVEL | 28.29 | 28.29 |
| Day 15_A8-3-L | NAO_TRACAVEL | 26.72 | 26.72 |
