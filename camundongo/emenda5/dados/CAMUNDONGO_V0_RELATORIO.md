# CAMUNDONGO · motor v0 congelado · relatório da rodada

Banco Dryad 10.25338/B84W8Q · 255 imagens · motor intocado (origem SHA-256 78b193014577a451…)

Diâmetro nominal 6 mm · efetivo passado ao motor **11.5 mm** (s = 57.5 px/mm no quadro de 1380) · semente 20260928 · bootstrap 10000

> **Executor declarado:** o pré-registro dizia "executor Opus, no PC do Fabio". Na prática a rodada é executada pelo **Fabio, no cmd do seu PC**, com scripts escritos e hasheados pelo Opus e revisados pelo Fable. Declarado antes do download.

## PREDIÇÕES

| | predição | resultado | |
|---|---|---|---|
| **P1** | medida obtida em ≥ 50 % das imagens com anel visível | **100.0 %** (204 de 204) · IC95 [100.0; 100.0] | ✅ **confirmada** |
| **P2** | Spearman(dia, área mediana) ≤ −0,8 | **-0.1607** (15 dias com n ≥ 8) | ❌ **FALHOU** |
| **P3** | revisor cego acerta ≥ 75 % dos pares | nenhum par possível — não houve falha para parear (n = 0) | ⏳ **não avaliável** |
| **P4** | falha dominante = referência de pele contaminada | assinatura "anel do splint" em **19.6 %** das obtidas | 📋 **descritiva** |

> Três estados, fixados antes do banco: **confirmada** · **FALHOU** · **não avaliável**, este sempre com o motivo e os números. "Não avaliável" é resultado publicável: não entra no placar como confirmação nem como falha. A **P4 é descritiva** e não tem veredito automático.


## COMPARADOR NULO GEOMÉTRICO (regra 4 do pré-registro)

Círculo de 6 mm no centro do anel, pareado por imagem. Área do nulo: **28.27 mm²** (constante por construção).

| | mediana | mínimo | máximo |
|---|---|---|---|
| área do motor | 28.99 | 6.32 | 210.92 |
| área do nulo | 28.24 | 28.24 | 28.24 |
| diferença (motor − nulo) | 0.74 | -21.92 | 182.68 |
| Dice motor × nulo | 0.0000 | 0.0000 | 0.8385 |

IC95 da diferença mediana: [0.25; 2.02] · Wilcoxon pareado p = 4.022e-05 · n = 204


## ESTRATOS DESCRITIVOS (Emenda 1, item 6)

Pré-declarados como **descritivos**: nenhum teste confirmatório entre estratos nesta rodada.

### Idade (A × Y)

| estrato | n | área mediana | mínimo | máximo |
|---|---|---|---|---|
| A (idoso) | 118 | 28.65 | 7.17 | 205.73 |
| Y (jovem) | 86 | 30.32 | 6.32 | 210.92 |

### Lado (L × R)

| estrato | n | área mediana | mínimo | máximo |
|---|---|---|---|---|
| L | 108 | 28.86 | 6.32 | 206.77 |
| R | 96 | 30.03 | 17.08 | 210.92 |

## TABELA POR DIA

| dia | n medidas | área mediana | mínimo | máximo |
|---|---|---|---|---|
| 0 | 16 | 34.28 | 20.43 | 201.52 |
| 1 | 16 | 32.22 | 20.96 | 210.92 |
| 2 | 16 | 28.51 | 7.17 | 206.77 |
| 3 | 16 | 28.03 | 23.37 | 189.81 |
| 4 | 16 | 29.73 | 19.94 | 195.95 |
| 5 | 16 | 30.33 | 22.71 | 199.66 |
| 6 | 16 | 28.83 | 16.26 | 201.70 |
| 7 | 14 | 28.01 | 8.13 | 192.47 |
| 8 | 14 | 28.36 | 18.64 | 199.46 |
| 9 | 13 | 29.17 | 15.13 | 199.65 |
| 10 | 13 | 28.40 | 6.32 | 192.96 |
| 11 | 9 | 30.08 | 14.67 | 188.79 |
| 12 | 9 | 29.96 | 27.27 | 195.61 |
| 13 | 9 | 29.00 | 19.99 | 192.49 |
| 14 | 8 | 29.38 | 26.81 | 205.73 |
| 15 | 3 | 26.20 | 20.89 | 190.10 |

## MODOS DE FALHA


## MARCAS DA FOTO (declaradas na etapa 2, antes do motor)

Fatos sobre a FOTOGRAFIA, anotados pelo operador **antes** de o motor rodar. Descritivos: nenhuma imagem foi excluída por marca, e nenhuma marca entra em predição. Vocabulário fechado.

| marca | o que é | imagens | com medida | sem medida |
|---|---|---|---|---|
| `d` | dois aneis no quadro | 103 | 103 | 0 |
| `f` | pelo dentro do anel | 12 | 12 | 0 |
| `p` | plastico/reflexo sobre o anel | 158 | 158 | 0 |
| `-` | nenhuma marca | 69 | 69 | 0 |

*Uma imagem pode ter mais de uma marca; as linhas não somam 255.*


## ESTRATOS

- normal — 203
- recorte incompleto — 1
- sem escala propria — 51
- escala manual (ato do operador) — 204
- razao_pxmm fora de [0.80; 1.25] — 0

*Nenhuma imagem foi excluída. Nenhuma constante do motor foi tocada.*

## HASHES DAS SAÍDAS

- `camundongo_v0.json` — baf4671f67e8098923c327c3eeac7329801231c677282692bef8836cba64d82c
- `CAMUNDONGO_V0_RELATORIO.md` — calculado após esta linha, registrado pelo executor no log.
