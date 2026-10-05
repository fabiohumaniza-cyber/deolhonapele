# ADENDO 69 · emenda ao Adendo 68: o que é "a rede mais forte" e como se lê

**05/10/2026, Brasília, 05h24.** Emenda ao Adendo 68 (`6fad75e`), que **não
se edita**. Publicada antes de qualquer rede de sensibilidade terminar: até
esta linha, não existe nenhuma predição (`pred_dobra*.npz`) de conv, mnv2 ou
campo.

O resultado das sensibilidades, antes previsto como Adendo 69, passa a ser o
**Adendo 70**.

## Por quê

O Adendo 68, §4, diz que o resumo do artigo refletirá o resultado contra "a
rede mais forte", mas não fixa o pós-processamento, o desempate nem a leitura.
Com três redes novas e vários cortes, haveria mais de uma candidata. A
revisão de IA do manuscrito apontou que escolher depois de ver os números é o
que o resto do estudo não faz.

## 1 · A métrica que define a rede mais forte

**A medida.** O Dice mediano por foto contra a **leitora 2 (Helga)**, no
conjunto primário: as **67 fotos** que ela marcou TRACADA.

**O pós-processamento.** O do confirmatório (`pos_rede` do `analisa_rede.py`,
`e3c5e9d0…`): a mancha de ferida ≥ 50 px de centro mais perto do centro da
vista.
- Na rede campo, a predição já sai com a ferida zerada fora do campo
  (Adendo 68); o mesmo `pos_rede` é aplicado depois.

**As candidatas.** A original (Adendo 52), conv, mnv2 e campo.

## 2 · O desempate

Se duas candidatas ficarem a até **0,005** uma da outra nesse Dice mediano, a
mais forte é a que dá o **menor limite inferior** do IC 95 % de Dice(motor r4)
− Dice(rede). Ou seja, a que é **pior para o motor**.

O limite é calculado como no Adendo 52: bootstrap por ferida, 2000 sorteios,
semente 20261004.

## 3 · A leitura contra a rede mais forte

Mesma conta e mesma tabela do Adendo 53, aplicadas à rede mais forte: LI e LS
são os limites inferior e superior do IC 95 % da mediana da diferença pareada
Dice(motor r4) − Dice(rede).

| resultado | leitura | o que o resumo diz |
|---|---|---|
| LI > 0 | **o motor ganha** | o motor foi superior à rede mais forte |
| −0,05 < LI ≤ 0 | **empate** | o motor não foi pior nem melhor que a rede mais forte |
| LI ≤ −0,05 | **a rede ganha** | o motor não demonstrou não ser pior que a rede mais forte |

Ao lado, sem mudar a leitura:
- **LS < 0:** a rede foi superior com IC inteiro abaixo de zero. Isso é
  relatado com essas palavras.
- **A mesma conta com a r3,** relatada ao lado.

## 4 · O que vai para o artigo

1. **O veredito confirmatório** (Adendo 67, rede original: empate) continua no
   resumo, como o resultado pré-registrado.
2. **O veredito contra a rede mais forte**, lido pela tabela acima, entra no
   resumo e na conclusão, logo depois, com o nome da rede.
3. **Se os dois divergirem**, o resumo diz os dois, nessa ordem, e a
   conclusão segue o da rede mais forte.
4. **O subtítulo do artigo acompanha a leitura contra a rede mais forte.**
   - Se for "a rede ganha", o subtítulo diz isso.
   - O título em forma de pergunta não muda.
5. **Se a mais forte for a campo,** isso é dito: ela recebeu a mesma entrada
   manual do motor.

## 5 · Declarado

**Uma métrica de treino foi vista.** Em 05/10, às 05h05, ao conferir a
retomada do treino da conv, a última linha do log mostrou o Dice de validação
da época 16 da dobra 0.
- É uma métrica de treino, não de teste.
- Nenhuma decisão dependeu dela: o critério de parada (paciência 30) e o
  limite de épocas estão fixados no Adendo 68.

---

*Opus, 05/10/2026. Nenhuma rede de sensibilidade terminou até esta linha.*
