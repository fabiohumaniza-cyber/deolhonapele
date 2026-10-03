# ADENDO 27 · resultado da rodada 2 — a coroa excluída

**03/10/2026, Brasília, 09h20.** A rodada 2 rodou no PC do Fabio entre ~08h43 e
09h15:38, com o driver `roda_rodada2.py` (`420ff85b…`) e os módulos congelados
lidos de `06_MOTOR_DE_REGISTRO\`. Os hashes conferidos pelo próprio driver estão
no relatório.

| arquivo | SHA-256 |
|---|---|
| `dados/camundongo_r2.json` | `62b5ce501389eb7fd5009ceaabc380e44af559af2bd6a854f2ba5e931a5dfe5a` |
| `dados/CAMUNDONGO_R2_RELATORIO.md` | `4ce2a33b4ba87f02a82318059beb3148057d2f262a952a6c95774b5da2b6f8bc` |

## 1 · O PLACAR

| predição | de quem | critério | resultado | |
|---|---|---|---|---|
| P5a | Fabio, 01/10 | ≥ 55 % das 255 fora das duas assinaturas | 252 / 255 = 98,8 % | **confirmada** |
| P5b | Fabio, 01/10 | mediana do dia 0 entre 20 e 40 mm² | 26,53 mm² (n = 16) | **confirmada** |
| P7.1 | Fabio, 08h05 | ≥ 50 % mudam de zona | 122 / 204 = 59,8 % | **confirmada** |
| P7.2a | Fabio, 08h05 | < 50 % das `p` no buraco | 25,5 % | **confirmada** |
| P7.2b | Fabio, 08h05 | < 50 % das `n` no buraco | 8,6 % | **confirmada** |
| P7.3 / P7.4 | Fabio | pelo / reflexo | — | não avaliáveis |
| P8.1 | Opus | ≥ 80 com Dice zero | 148 | **confirmada** |
| P8.2 | Opus | ≥ 25 das limpas com Dice zero | 44 | **confirmada** |
| P8.3 | Opus | ≥ 20 máscaras > 50 % na faixa laranja | **0** | **FALHOU** |
| **P9** | Fabio, 08h40 | < 21 das 204 no buraco ("nunca a ferida") | **56** | **FALHOU** |

**A P5a e a P5b confirmadas não são acerto.** Isso foi escrito antes: no
pré-registro, §7.3, e no Adendo 23, §2. **148 das 204 máscaras estão fora do
splint, com área de ferida.** A P5a conta essas máscaras como "mede a ferida",
e a mediana do dia 0 cai em 26,5 mm² porque o pelo da beira tem esse tamanho.

## 2 · ONDE A MÁSCARA FOI

| rodada 1 → rodada 2 | n |
|---|---|
| coroa → **buraco** | **36** |
| coroa → fora | 68 |
| fora → **buraco** | **17** |
| fora → fora | 79 |
| buraco → buraco | 3 |
| buraco → fora | 1 |

| grupo | n | buraco | coroa | fora |
|---|---|---|---|---|
| todas com escala | 204 | **56** (27 %) | 0 | 148 |
| limpas (`v` sem `p`) | 70 | **26** (37 %) | 0 | 44 |
| com plástico (`p`) | 110 | 28 (25 %) | 0 | 82 |
| classe `n` | 35 | 3 (9 %) | 0 | 32 |

- **A coroa sumiu inteira**: nenhuma máscara ficou nela.
- **Das 104 que estavam na coroa, 68 foram para fora do splint** (pelo, luva,
  régua) e 36 foram para dentro do buraco.
- **O buraco foi de 4 para 56.** Nessas 56, o Dice contra o nulo teve mediana
  de 0,73, e a máscara ficou inteira dentro do campo amarelo do Fabio (mediana
  `f_campo` = 1,00).
- **As 56 se concentram nos primeiros dias**: 35 delas são dos dias 0 a 2.
  Do dia 3 em diante, quando a ferida diminui, o buraco quase não aparece.
- Ordem esperada entre os grupos, sem veredito: limpas 37 % > plástico 25 % > `n` 9 %.

**A faixa laranja não virou armadilha** (P8.3 falhou, 0 máscaras). A previsão
do Opus estava errada: sem a coroa, o motor foi para **fora**, e não para a
borda que sobrou.

## 3 · RODADA 1 × RODADA 2

| | rodada 1 | rodada 2 | Wilcoxon |
|---|---|---|---|
| área mediana (mm²) | 28,99 | 27,45 | p = 1,5 × 10⁻¹¹ |
| Dice × nulo, mediana | 0,000 | 0,000 | p = 5,0 × 10⁻⁸ |
| Dice zero | 158 | 148 | — |

## 4 · O QUE ISTO DIZ

1. **Tirar o anel não basta.** Na maioria das imagens, o que o motor pegava no
   lugar do anel não era a ferida: era o que está **fora** do splint.
2. **Quando não há nada fora para pegar, ele vai para a ferida.** Isso
   aconteceu em 56 imagens, quase todas dos primeiros dias.
3. **É exatamente o que o campo declarado (rodada 3) remove.** O Adendo 23, §3,
   escrito antes desta rodada, já dizia isso.

**Sem traçado humano, "buraco" quer dizer que o motor olhou para dentro do
splint, não que acertou a ferida** (Adendo 24, §2).

---

*Opus, 03/10/2026. Hashes colados do `sha256sum`. Placar copiado do relatório
gerado pelo driver. A P9 e a tabela de transição foram calculadas sobre o
`camundongo_r2.json` de hash `62b5ce50…` e o `POSICAO_MASCARAS.tsv` de hash
`f7baa788…`.*
