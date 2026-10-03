# ADENDO 29 · resultado da rodada 3 — o campo declarado

**03/10/2026, Brasília, 09h55.** A rodada 3 rodou no PC do Fabio e terminou às
**09h50:14**, com o driver `roda_rodada3.py` (`72cfb5cc…`) e os módulos
congelados. Os hashes dos arquivos de código e de entrada, conferidos pelo
próprio driver, batem com o pré-registro (Adendo 28, `bea34c81…`).

O placar foi gerado pelo `analisa_rodada3.py` (`fab878ef…`), escrito e publicado
antes da rodada.

| arquivo | SHA-256 |
|---|---|
| `dados/camundongo_r3.json` | `ab82d594f88665ac6f760d30b43c651cedf3a4e2ca3416ddf72cda8ac2a44041` |
| `dados/CAMUNDONGO_R3_RELATORIO.md` | (abaixo, colado do `sha256sum`) |

## 1 · O PLACAR

| predição | de quem | critério | resultado | |
|---|---|---|---|---|
| **P11.1** "vai mudar mais" | Fabio | Dice > 0 nas 201 > 56 | **201** | **confirmada** |
| P11.2 "tirando artefato vai surpreender" | Fabio | — | — | rodada 4 |
| **P10.1** a curva não cai, nas 201 | Opus | Spearman > −0,8 (n ≥ 8) | **−0,625** | **confirmada** |
| **P10.2** a curva não cai, nem nas limpas | Opus | Spearman > −0,8 (n ≥ 3) | **−0,860** | **FALHOU** |
| **P10.3** o motor pega o campo inteiro | Opus | ≥ 20 com máscara ≥ 80 % do campo | **0** | **FALHOU** |

**A P11.1 confirmada é quase automática**, e isso fica dito. Com o motor vendo
só um círculo de ~4 mm de raio no centro, uma máscara dentro dele dificilmente
deixa de encostar no nulo de 3 mm. O Dice > 0 aqui diz pouco.

## 2 · O ACHADO: A CURVA DAS LIMPAS CAI

Área mediana (mm²) por dia. O punch nominal é **28,27 mm²**.

| dia | 0 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **limpas** (n) | 16 | 6 | 4 | 4 | 7 | 6 | 5 | 4 | 5 | 4 | 3 | 3 | 2 | 1 |
| **limpas** (mm²) | **27,2** | 22,6 | 26,0 | 21,9 | 17,0 | 26,1 | **6,5** | 15,1 | **5,8** | **6,4** | **7,2** | **5,2** | 14,9 | 2,3 |
| **com plástico** (mm²) | — | 26,6 | 27,1 | 28,6 | 26,2 | 26,6 | 27,8 | 26,5 | 25,8 | 27,4 | 25,5 | 24,1 | 19,4 | 27,3 |

*(a linha do plástico vai do dia 1 ao 14; os dias estão alinhados pela tabela
completa no relatório)*

- **Nas limpas**, o motor dá **27,2 mm² no dia 0**, 96 % do punch, e cai para
  **~5 a 7 mm²** a partir do dia 7. **Spearman −0,860.** É o critério da P2 da
  rodada 1 (≤ −0,8), que **na rodada 1 tinha falhado com −0,16**.
- **Com plástico**, a curva é **reta em ~26 mm²**, do primeiro ao último dia,
  igual à da rodada 1 inteira. **O plástico trava o número.**
- **Todas juntas:** −0,625, porque o plástico, que é mais da metade, puxa a
  curva para a reta.

Isso bate com a P7.2a do Fabio, da rodada 2 ("plástico = fracasso"), e com a
P11.2, que ainda vai ser testada.

## 3 · O QUE ISTO É E O QUE NÃO É

**É:** a primeira vez, no camundongo, que o número do motor **se comporta como
uma ferida que fecha**. Ele aparece no subconjunto que o operador classificou
como limpo **antes** de o motor rodar.

**Não é:**
- **acerto medido.** Não há traçado humano ainda (Adendo 19). Uma curva que cai
  pode cair pelo motivo errado;
- **validação.** O campo foi colocado à mão pelo operador, que já tinha visto as
  imagens. É uma condição de uso, não o motor sozinho;
- **resultado das 255.** São 70 imagens limpas, com n por dia entre 1 e 16, e os
  dias finais têm poucas imagens.

A P10.3 falhou: **nenhuma** máscara pegou o campo inteiro. A maior pegou 76 %, e
a mediana foi de 50 %.

## 4 · A HISTÓRIA DAS TRÊS RODADAS, NAS LIMPAS

| | onde o motor foi | a curva cai? |
|---|---|---|
| rodada 1 (sem barreira) | anel e pelo de fora; **0 de 70 no buraco** | não (todas: −0,16) |
| rodada 2 (sem o anel) | pelo, luva e régua; **26 de 70 no buraco** | — |
| rodada 3 (campo do Fabio) | **70 de 70 no campo** | **sim: −0,86** |

---

*Opus, 03/10/2026. Placar copiado do relatório gerado pelo `analisa_rodada3.py`.
A linha do plástico na tabela da §2 foi calculada sobre o mesmo
`camundongo_r3.json` e o `CLASSIFICACAO.txt` (`3f10f490…`).*
