# ADENDO 70 · Resultado da sensibilidade: o motor contra redes mais fortes

**07/10/2026, Brasília, 01h00.** As 12 redes do Adendo 68 terminaram (conv, mnv2 e campo, 4 dobras cada). A análise rodou com `rede/sensibilidade_rede.py` (`1a6774fd…`, registrado no Adendo 68), sem nenhuma alteração. Ele usa o `analisa_rede.py` (`e3c5e9d0…`).

**Conferência do script.** Com as predições da rede original, ele reproduziu exatamente o Adendo 67: motor 0,919, rede 0,850, nulo 0,790; diferença +0,030, IC [−0,004; +0,223].

## 1 · Contra a Helga, nas 67 fotos TRACADA (primário)

Pós-processamento do confirmatório (`pos_rede`, Adendo 69 §1). Dice mediano por foto. Motor r4 = 0,919; nulo = 0,790.

| rede | Dice da rede | motor r4 − rede | IC 95 % (S1) | motor melhor em | rede vazia (de 201) |
|---|---|---|---|---|---|
| original (Adendo 52) | 0,850 | +0,030 | [−0,004; +0,223] | 44 de 67 | 33 |
| conv | 0,796 | +0,087 | [−0,009; +0,507] | 39 de 67 | 14 |
| **mnv2** | **0,961** | **−0,030** | **[−0,047; −0,021]** | **11 de 67** | 7 |
| campo | 0,896 | +0,008 | [−0,019; +0,103] | 36 de 67 | 5 |

**A rede mais forte (Adendo 69 §1) é a mnv2**, com 0,961. A seguinte é a campo, com 0,896. A distância entre as duas passa de 0,005, então o desempate não se aplica.

## 2 · Leitura contra a rede mais forte (Adendo 69 §3)

- **Limite inferior (LI) = −0,047.** Pela tabela registrada, −0,05 < LI ≤ 0 é **empate**: o motor não foi pior nem melhor que a rede mais forte.
- **Limite superior (LS) = −0,021 < 0.** Pela mesma regra, relata-se com estas palavras: **a rede foi superior, com o IC inteiro abaixo de zero.**
- **A margem do empate é de 0,003.** O LI ficou a 0,003 do limite de −0,05.
- **Estabilidade:**
  - nas 10 sementes (S2), o LI foi −0,047 em todas;
  - pelo BCa, IC [−0,047; −0,018];
  - ao nível da ferida (S3), −0,027, IC [−0,043; −0,011];
  - sem as fotos com máscara vazia (S4, n = 67, nenhuma vazia no primário), o resultado foi o mesmo;
  - sem o pós-processamento (S5, "bruta"), também o mesmo.
- **Com o motor r3, relatada ao lado (Adendo 69 §3):** −0,035, IC [−0,050; −0,024]. Pela tabela, LI ≤ −0,05 é **a rede ganha** (P19 falhou).
- **Contra o Emílio (secundário, 71 fotos):** mnv2 0,961 contra motor 0,915. Diferença −0,030, IC [−0,055; −0,025], P19 falhou: **a rede ganha.**

**O que vai para o artigo (Adendo 69 §4):**
1. O confirmatório do Adendo 67, contra a rede original: **empate.**
2. Contra a rede mais forte (MobileNetV2 pré-treinada): **empate pela regra registrada, com a rede superior e o IC inteiro abaixo de zero.** O empate depende de uma margem de 0,003 no LI e vira **"a rede ganha"** com o motor r3 e contra o segundo leitor.
3. **O subtítulo acompanha essa leitura.** A rede pré-treinada foi consistentemente melhor (56 de 67 fotos), por uma diferença pequena (~0,04 de Dice mediano). O título em forma de pergunta não muda.

## 3 · Outros números

- **Nas 30 impossíveis (Helga, n = 24):** mnv2 0,852; motor 0,479; nulo 0,502. A mnv2 supera o nulo nessas fotos; o motor, não.
- **Em todas as traçadas (Helga, n = 194):** mnv2 0,931; motor 0,834.
- **A conv parou cedo em duas dobras** (épocas 43 e 68) e ficou **pior** que a original (0,796 contra 0,850). É coerente com a limitação do 69-E: a paciência de 30 é curta para esta curva.
- **A campo,** que recebe a mesma entrada manual do motor, ficou atrás dele (0,896 contra 0,919), em empate pela regra.

## 4 · As previsões registradas

**Fabio (Adendo 69-K): "novo empate".** **Confirmada pela regra** (P19 confirmada, P20 não). Registra-se ao lado que a rede foi superior, com o IC inteiro abaixo de zero.

**Claude (Adendo 69-K):**

| parte | resultado |
|---|---|
| conv quase igual à original | **falhou**: 0,796 contra 0,850 |
| mnv2 a mais forte e a mais perto do motor | **confirmada** como a mais forte; passou do motor |
| veredito contra a mais forte: empate | **confirmada pela regra**, por 0,003 |
| mediana motor − rede mais forte < +0,030 | **confirmada**: −0,030 |
| campo | recusa registrada |

O Claude estimou em cerca de 30 % a chance de o motor falhar a P19. A rede passou o motor na mediana, embora a P19 tenha se mantido para o r4.

**Revisor de IA (Adendo 69-B):**

| parte | resultado |
|---|---|
| conv na faixa −0,02 a +0,02, IC mais estreito que 0,227 | **falhou**: +0,087, IC de largura 0,516 |
| mnv2 na mesma faixa; "improvável o intervalo inteiro abaixo de zero" | **falhou**: −0,030, com o intervalo inteiro abaixo de zero |
| campo | recusa registrada |
| nenhuma rede cruza o teto humano de 0,976 | **confirmada**: a maior é 0,961 |
| ganho pareado de nenhuma rede sobre o nulo passa de +0,15 | **não calculado** pelo script registrado; fica pendente, num adendo próprio |

## 5 · Declarado

- **Duas métricas de treino foram vistas antes deste adendo.** Nenhuma é teste contra traçado, e nenhuma decisão dependeu delas:
  - o Dice de validação de uma época, no log da fila, em 05/10, 16h03;
  - o `melhor_val_dice` de validação interna da campo, dobra 2, visto ao fazer o backup em 06/10, 06h02.
- **O treino foi interrompido várias vezes** por reinícios do ambiente. Foi retomado sempre do estado salvo por época, como o `treina_rede2.py` prevê, sem mudar nenhum parâmetro.
- As predições ficam num repositório privado até a publicação. Aqui ficam só os hashes.

## 6 · Hashes (SHA-256, 16 primeiros)

**Predições:**
- conv: `7fdd02a724d5aea7` · `8240e0d24da298f4` · `87cf8806ed8e68db` · `56d3cb3215b19909`
- mnv2: `c91202b5daf5f411` · `4b9a00e0d70fd75d` · `1af6ae10f947c713` · `ddab099838a68023`
- campo: `214ebc78b4ec3c44` · `54b876f76d959911` · `15796b93e2a55fd3` · `384d3e511453b836`

**Saídas** (`SENS_<rede>_<pos>_<ref>.md`):
- mnv2 orig Helga `4c891c745c3b85ff` · campo orig Helga `b1b5b63f3bdd7d91` · conv orig Helga `73ee52bcdb09785f` · original orig Helga `7dc27cd5940fe61b`
- mnv2 orig Emílio `c8e79e28a7cdcce1` · campo orig Emílio `8f71ef558943eced` · conv orig Emílio `c71e354b7ca4423c` · original orig Emílio `f06cc7170d930fca`
- as 8 versões "bruta" estão listadas em `SHA256_RESULTADOS.txt`, no repositório privado.

---

*Opus, 07/10/2026. Análise executada exatamente como registrada nos Adendos 68 e 69.*
