# ADENDO 66 · resultado da rodada 2 (Adendo 65) e o levantamento da literatura

**04/10/2026, Brasília, 18h35.**

| arquivo | SHA-256 |
|---|---|
| `dados/REANALISE_REVISOR2.md` | `f066542ba53a4e2d…` |
| `artigo/FIGURA_4_BLAND_ALTMAN.png` | `85b2d81438af2819…` |
| `dados/LEVANTAMENTO_LITERATURA_S2.md` | `3bdbccf2c9a599ee…` |

## 1 · Bland-Altman

**Viés:** constante, sem componente proporcional.

| leitor | inclinação da diferença sobre a média | IC 95 % |
|---|---|---|
| 1 | +0,03 | −0,04 a +0,11 |
| 2 | +0,01 | −0,06 a +0,08 |

**Viés absoluto:**

| leitor | viés | limites de 95 % |
|---|---|---|
| 1 | +1,9 mm² | −9,5 a +13,3 mm² |
| 2 | +1,7 mm² | −7,6 a +11,1 mm² |

**Em razão, os limites são muito largos.**

| leitor | razão motor/leitor | limites de 95 % |
|---|---|---|
| 1 | 1,16 | 0,47 a 2,85 |
| 2 | 1,22 | 0,56 a 2,66 |

Um erro absoluto de alguns mm² pesa muito em feridas pequenas. **Imagem a
imagem, a área do motor não é intercambiável com a do leitor.** Isso vai para
o artigo como achado negativo.

**De onde vem o viés.** A escala subestima a área em ~0,4 %. Logo, o viés
positivo vem da regra de borda, que fecha um pouco por fora.

## 2 · Distância de borda por faixa de dia

**HD95, em mm:**

| dias | motor × leitores | leitor × leitor |
|---|---|---|
| 0–4 | 0,38 a 0,48 | 0,14 |
| 5–9 | 0,34 a 0,52 | 0,20 |
| 10–15 | 0,26 a 0,29 | 0,21 |

**HD95 relativo ao raio equivalente da ferida:**

| dias | motor × leitores | leitor × leitor |
|---|---|---|
| 0–4 | 0,13 a 0,18 | 0,05 |
| 5–9 | **0,41 a 0,48** | 0,18 |
| 10–15 | 0,26 a 0,27 | 0,19 |

O erro relativo do motor cresce quando a ferida encolhe, sobretudo nos dias
5–9. Nos dias 10–15, a distância entre motor e leitores se aproxima da
distância entre os próprios leitores.

## 3 · Área × dia por ferida

- **ρ por ferida** (10 feridas com ≥ 4 imagens): mediana −0,72, IQR −0,88 a
  −0,70.
- **Modelo misto** (16 feridas, 71 imagens): inclinação de −1,76 mm²/dia (IC
  95 % −2,22 a −1,30). O ajuste emitiu aviso de convergência, declarado aqui.

## 4 · Levantamento da literatura (Tabela S2)

Um agente de busca separado levantou 35 estudos de 2015 a 2026. Cada item foi
codificado só a partir do resumo ou do texto completo efetivamente lido.

| relato de quantas imagens podiam ser avaliadas | n | % |
|---|---|---|
| sim, com contagem (por qualidade da foto, não pela borda) | 2 | 5,7 % |
| parcial | 12 | 34,3 % |
| não | 20 | 57,1 % |
| não verificado | 1 | 2,9 % |

**Nenhum estudo trata como desfecho a proporção de imagens com borda
traçável.** Limitações do levantamento: 11 dos 20 "não" se basearam só no
resumo, e 10 itens estão sem DOI verificado.

---

*Opus, 04/10/2026.*
