# ADENDO 64 · resultado das reanálises do revisor (Adendo 63), EXPLORATÓRIAS

**04/10/2026, Brasília, 18h05.** O `reanalise_revisor.py` rodou sem
alteração depois do commit `59cb910`.

| arquivo | SHA-256 |
|---|---|
| `dados/REANALISE_REVISOR.md` | `3431712e39801764…` |
| `dados/REANALISE_REVISOR.json` | `6c01002fbbc85588…` |

## O que muda a leitura

1. **O filtro do operador não seleciona o conjunto.** O braço definido só
   pelos leitores (L_r: leitor TRACADA e sem filme, sem o filtro do operador)
   é **idêntico** ao do placar (S_r), com n = 48 e n = 44. Nenhuma imagem sem
   filme que um leitor marcou TRACADA tinha sido excluída pelo operador. O
   número principal não depende do juízo do operador.

2. **ρ do Adendo 37 é sobre medianas diárias.** O −0,881 foi calculado entre o
   dia e a **mediana diária** da área, como manda a P2 do pré-registro. Calculado
   **por imagem**, com IC agrupado por animal, dá:

   | conjunto | n | ρ por imagem | IC 95 % |
   |---|---|---|---|
   | braço principal, r4 | 71 | −0,71 | −0,84 a −0,57 |
   | limpas, r3 | 70 | −0,63 | −0,73 a −0,42 |

   O artigo passa a dizer qual ρ é qual.

3. **Erro de área contra os leitores (Bland-Altman, S_r).**

   | leitor | viés do motor | IC 95 % | limites de 95 % | viés relativo mediano |
   |---|---|---|---|---|
   | 1 | +1,9 mm² | +0,5 a +3,7 | −9,5 a +13,3 mm² | +6 % |
   | 2 | +1,7 mm² | +0,6 a +3,2 | −7,6 a +11,1 mm² | +7 % |

   O motor marca um pouco a mais. Os limites são largos para feridas de
   mediana ~15 mm².

4. **Distância de borda (HD95).**

   | comparação | HD95 mediano |
   |---|---|
   | motor × leitores | 0,37 mm |
   | leitor × leitor (C) | 0,14 mm |

   O motor fica a cerca de 0,2 mm a mais da borda humana do que um leitor fica
   do outro.

5. **Segundo nulo, o campo inteiro:** Dice 0,42 e 0,44, contra 0,90 do motor.
   O motor não está só desenhando o campo.

6. **Com e sem filme (C).**

   | conjunto | n | Dice motor | Dice nulo | leitor × leitor |
   |---|---|---|---|---|
   | com filme | 17 | 0,95 | 0,86 | 0,98 |
   | sem filme | 38 | 0,91 a 0,92 | 0,65 | 0,97 |

   Sem filme, o motor tira 0,19 a 0,20 acima do nulo, com IC acima de zero.

7. **κ com IC.**

   | par | κ | IC 95 % |
   |---|---|---|
   | leitores entre si | 0,69 | 0,52–0,83 |
   | operador × leitor 1 | 0,41 | 0,32–0,49 |
   | operador × leitora 2 | 0,36 | 0,29–0,43 |

8. **Subgrupos.**

   | recorte | o que aparece |
   |---|---|
   | dias 5–9 | Dice mais baixo (0,78 a 0,84); só cerca de 20 % das imagens traçáveis |
   | dias 0–4 | 0,93 a 0,94 |
   | feridas jovens (Y) | traçáveis com mais frequência (42 a 50 %) que as idosas (A, 24 a 27 %) |
   | animal Y8-2 | o de menor Dice (0,78 a 0,86) |

---

*Opus, 04/10/2026. Números copiados do relatório gerado pelo script.*
