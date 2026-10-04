# ADENDO 52 · pré-registro: motor (regra escrita) × rede neural (U-Net), no mesmo banco

**04/10/2026, Brasília, 13h05.** Publicado **antes de qualquer treino**. Até
esta linha, só rodou um teste de fumaça de uma época, para ver se o código
funcionava. Ninguém olhou métrica nem máscara desse teste, e a saída foi
apagada.

> Fabio, 12h56: *"eu quero fazer o teste redeneural vs nosso motor"*

## 1 · A PERGUNTA

Na mesma tarefa, nas mesmas fotos e contra o mesmo traçador independente, a
**regra escrita e congelada** (motor v0, rodadas r3 e r4) é pior que uma **rede
neural treinada** com traçado humano?

## 2 · A REDE: A MESMA ARQUITETURA DO TRABALHO ORIGINAL

O Carrión et al. 2022 não publicou os pesos da rede. Publicou o caderno de
treino, que chama `train.py` do **Semantic-Shapes** (github.com/seth814/Semantic-Shapes,
commit `00289c010f35f9d3f3f069b2fb78b83f8a08bc93`).

| | escolha | origem |
|---|---|---|
| arquitetura | `unet(base=4)`, camada a camada | Semantic-Shapes `models.py` |
| classes | fundo, interior do anel, ferida (softmax) | caderno deles: `hues = {'Wound', 'Ring_inner'}` |
| entrada | 352 × 352 | tamanho dos recortes deles |
| otimizador, perda | Adam 1e-4, entropia cruzada categórica | Semantic-Shapes |
| épocas, modelo guardado | 100; o de maior `val_dice` | log deles: `Epoch 100/100 … saving model to UWound_v9` |
| lote | 5 | Semantic-Shapes `train.py` |
| aumento | espelho horizontal (p = 0,5) e rotação de 90° (k ∈ {0, 1, 2, 3}) | **desvio declarado:** o original usa `imgaug` com rotação contínua de ±90° |
| pós-processamento | ferida = mancha ≥ 50 px de centro mais perto do centro; nenhuma = "sem ferida" | `single_mask_size_wound` deles |

## 3 · OS DADOS

- **Fotos:** as 201 vistas do painel do Emílio (`008f863d…`), as mesmas que o
  traçador viu, redimensionadas para 352.
- **Rótulo da ferida:** o traçado do **Emílio** (`afcbf928…`), **inteiro**,
  incluindo PARCIAL e IMAGINADA, como o anotador do original, que traçou
  todas as fotos. FECHADA = sem ferida.
- **Rótulo do anel:** o círculo `r_borda` do `CAMPO.txt` (`91160713…`, Adendo 51).
- `rede_dados.npz` gerado por `prepara_rede.py`: SHA-256
  `88072f494beb92354e556dea86ad06f5db7401962e3817c80ff2618e667633db`.

## 4 · A DIVISÃO: POR FERIDA, COM PREDIÇÃO FORA DA DOBRA

As 16 feridas são divididas em **4 dobras de 4 feridas** (2 A + 2 Y), por
sorteio com `random.Random(20261004)`. Toda foto recebe **uma** predição, feita
por um modelo que **nunca viu a ferida dela**.

| dobra | teste (fotos) | validação (fotos) | treino (fotos) |
|---|---|---|---|
| 0 | A8-1-R, A8-5-L, Y8-3-R, Y8-3-L (49) | A8-4-L, Y8-1-L (26) | 10 feridas (126) |
| 1 | A8-4-L, A8-4-R, Y8-1-L, Y8-4-R (48) | A8-3-R, Y8-4-L (27) | 10 feridas (126) |
| 2 | A8-3-R, A8-5-R, Y8-4-L, Y8-1-R (45) | A8-1-L, Y8-2-R (28) | 10 feridas (128) |
| 3 | A8-1-L, A8-3-L, Y8-2-R, Y8-2-L (59) | A8-1-R, Y8-3-R (23) | 10 feridas (119) |

O original usou 12 feridas de treino, 2 de validação e 2 de teste, e **uma**
divisão só. Aqui a divisão é em 10, 2 e 4, e as quatro dobras cobrem as 16
feridas.

## 5 · A REFERÊNCIA E O VEREDITO

### Primário: a Helga, que a rede nunca viu

- **Conjunto:** as fotos que a **Helga** marcar TRACADA.
- **P19** (o motor não é pior que a rede): o limite inferior do IC 95 % da
  mediana da diferença pareada **Dice(motor r4) − Dice(rede)** é **> −0,05**.
  - O IC sai de um bootstrap **por ferida**, com 2000 sorteios e semente
    20261004.
  - Dice no quadro inteiro de 700 px.
- Se a Helga não traçar, a P19 fica **não avaliável**. Nesse caso, o que sai é
  só o secundário.

### Secundário: o Emílio

- É a mesma conta, contra o Emílio, nas fotos que ele marcou TRACADA.
- **Viés declarado a favor da rede:** ela aprendeu o estilo do Emílio nas
  outras feridas. O motor nunca viu o Emílio.

### Ao lado, sem veredito

- motor r3;
- nulo;
- todas as traçadas, incluindo as imaginadas;
- as 30 impossíveis;
- as 5 cicatrizadas: a rede diz "sem ferida"? O motor v0 não sabe dizer;
- o Dice da rede no estilo do Semantic-Shapes (três canais achatados, com o
  fundo dentro), para mostrar o quanto esse jeito de contar infla o número.

## 6 · OS ARQUIVOS (o código não muda depois deste commit)

| arquivo | SHA-256 |
|---|---|
| `rede/prepara_rede.py` | `e0350432167c76dc5ecf9be903449942338d75ce10b36060fa966a257bae213d` |
| `rede/treina_rede.py` | `b767471e8ec8cb5f3cd5aa5d1319c3fdfb235a0203de31b216e25d8d828bfd8d` |
| `rede/analisa_rede.py` | `e3c5e9d0b8f35558a2e8f3a040679a60c6ce4b191e2e23b5cb37bf4827c6f725` |

- O treino roda em CPU, no ambiente de trabalho do Opus (TensorFlow 2.21),
  as 4 dobras em sequência, com estimativa de 4 a 5 horas.
- Os pesos, os logs e as predições serão publicados com hash.

## 7 · CUIDADOS

- **A Helga não pode ver este adendo nem nenhum resultado antes de traçar.**
- A previsão do Fabio entra num adendo próprio, **antes** de o primeiro modelo
  terminar de treinar.

---

*Opus, 04/10/2026. Nenhuma rede foi treinada até esta linha.*
