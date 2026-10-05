# ADENDO 69-F · dois exploratórios pedidos pela literatura de métricas, especificados antes de calcular

**05/10/2026, Brasília, 05h45.** Especificado antes de qualquer conta. Usa
só as predições já publicadas no Adendo 67 (rede original) e as máscaras do
motor. Não toca nas redes de sensibilidade. É **exploratório**.

## Por quê

- **Dice e tamanho.** O Dice cai com o tamanho da estrutura, mesmo com a
  segmentação igualmente boa. Reinke et al. (*Common limitations of image
  processing metrics*, §6) recomendam estratificar por tamanho; o
  USE-Evaluator documenta o mesmo efeito. Aqui, as feridas vão de 28,3 mm²
  (dia 0) a 3–8 mm² nos dias finais.
- **Referência vazia ou incerta.** O USE-Evaluator recomenda, nesses casos,
  trocar o Dice por métricas de classificação.

## E1 · Estratificação por tamanho e por dia

**Conjunto.** As 67 fotos que a leitora 2 marcou TRACADA.

**Estratos.**
- **Tamanho:** tercis da área do traçado da leitora 2, em mm² no quadro de
  700 px (29,1667 px/mm), com os cortes calculados nessas 67.
- **Dia:** 0–4, 5–9 e 10–15.

**Em cada estrato:**
- n e número de feridas;
- Dice mediano do motor r4, da rede e do nulo;
- mediana da diferença pareada motor − rede, com IC 95 % (bootstrap por
  ferida, 2000 sorteios, semente 20261004), quando houver ao menos 4 feridas.

## E2 · Classificação: o método diz quando não há o que medir?

**Três grupos.**
- As 67 TRACADA da leitora 2 (há ferida visível);
- as 30 fotos em que nenhum observador viu a borda;
- as 5 com suspeita de fechamento.

**A conta.** Em cada grupo, a fração em que cada método devolve máscara
vazia ("sem ferida / não medido").
- Para a rede, é a máscara vazia depois do pós-processamento.
- Para o motor, é a máscara r4 vazia.

**A leitura, descritiva.**
- Nas 67, devolver vazio é **erro** (falso negativo).
- Nas 5 com suspeita de fechamento, devolver vazio é o comportamento
  esperado se a ferida fechou. A referência é incerta, e isso é dito.
- Nas 30 sem borda visível, devolver vazio é **recusa**: não há referência
  confiável para medir. Não se chama de acerto nem de erro.

**Nada disso tem veredito.**

---

*Opus, 05/10/2026. Nenhuma das contas acima foi feita até esta linha.*
