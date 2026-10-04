# ADENDO 65 · segunda rodada de reanálises do revisor, especificadas antes de rodar (EXPLORATÓRIAS)

**04/10/2026, Brasília, 18h20.** A tréplica do revisor pediu mais cinco
análises. Todas usam só o `dados/REANALISE_REVISOR.json` do Adendo 64, que
já está publicado. Nenhum dado novo entra.

## As análises

- **R9 · Bland-Altman completo** (S_r, motor r4 − leitor, em mm²)
  - viés com IC e DP;
  - limites de concordância;
  - viés proporcional: inclinação da diferença sobre a média, com IC agrupado
    por animal;
  - limites em razão geométrica (escala log);
  - gráfico de diferença contra média: Figura 4.
- **R10 · distância de borda por faixa de dia** (0–4, 5–9, 10–15)
  - HD95 e ASSD em mm;
  - a mesma distância dividida pelo raio equivalente da ferida do leitor
    (√(área/π));
  - também leitor × leitor.
- **R11 · área × dia por ferida**
  - a distribuição do ρ de Spearman por ferida (feridas com ≥ 4 imagens);
  - um modelo misto: área ~ dia, com intercepto e inclinação aleatórios por
    ferida (REML).
- **A diferença pareada motor − nulo** com IC agrupado por animal já saiu no
  Adendo 64 (R1). Não é refeita.

## O código

`reanalise_revisor2.py`, SHA-256 `5f42010c10659973765c2b864a3a5e632fd0880c67512a3f2544b67da2935cca`.

---

*Opus, 04/10/2026. Nada destas contas foi calculado até esta linha.*
