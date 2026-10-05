# ADENDO 67 · Resultado: motor × rede neural (P19 e P20)

**04/10/2026, Brasília, 21h01.** As quatro dobras terminaram. A análise rodou
com `rede/analisa_rede.py` (`e3c5e9d0…`), sem mudança de código, exatamente
como registrada no Adendo 52 (`9f5e18c`) e no Adendo 53 (`2978f19`).

## Placar

| contra | conjunto | n | motor r4 | rede | nulo | mediana motor − rede | IC 95 % | veredito |
|---|---|---|---|---|---|---|---|---|
| **Helga** (primário, a rede nunca viu) | TRACADA | 67 | **0,919** | 0,850 | 0,790 | **+0,030** | [−0,004; +0,223] | P19 **confirmada** · P20 **falhou** |
| Emílio (secundário, viés a favor da rede) | TRACADA | 71 | **0,915** | 0,817 | 0,798 | +0,059 | [+0,004; +0,203] | sem veredito (Adendo 53) |

Valores de Dice: mediana por foto.

**Leitura registrada (Adendo 53): EMPATE.** O motor não perde para a rede
(P19), mas a superioridade (P20: limite inferior > 0) não se confirmou contra
a Helga. O limite inferior ficou em −0,004. Isso é empate pela regra, e é
isso que vai para o artigo. A previsão do Fabio, "o motor ganha", **não foi
confirmada** pelo critério que ele mesmo aceitou antes do resultado.

## Outros números da saída

- **Todas as traçadas, inclusive as imaginadas:**
  - contra a Helga (n = 194): motor 0,834, rede 0,781;
  - contra o Emílio (n = 200): motor 0,845, rede 0,736.
- **Só as 30 impossíveis:**
  - contra a Helga (n = 24): motor 0,479, rede 0,198, nulo 0,502;
  - contra o Emílio (n = 30): motor 0,372, rede 0,066, nulo 0,351.
  - Nenhum dos dois métodos supera o nulo nessas fotos.
- **Cicatrizadas (5):** a rede deixou a máscara vazia em 3 e marcou ferida em 2.
- **Rede vazia no total:** 33 de 201 fotos.
- **Dice da rede no estilo Semantic-Shapes** (3 canais achatados, contra o
  rótulo do Emílio): mediana 0,946.
  - Esta é a métrica que infla o número, porque o fundo conta como acerto.
  - Não é comparável ao Dice da ferida.

## Desvio de execução, declarado

Na primeira tentativa, `mascara_nula` não foi encontrada. A cópia preparada
do `roda_camundongo.py` em `hs/motor` era anterior à que tem a função.

A correção foi só a ordem do `PYTHONPATH`: `.` (a pasta `emenda5`, cujo
`roda_camundongo.py` define `mascara_nula`) antes de `hs/motor`. Nenhuma
linha de código e nenhuma constante mudou.

## Hashes (sha256sum)

```
5804b57b5b46099b767cbe365b67b1984346d838484cd7994b632a1f9d42f159  pred_dobra0.npz
67e1227e1edfd23279ae138f658532513c5adda7fe8b04bd1dca3d6c7f3eea2b  pred_dobra1.npz
1008676a19746fbe53d4d836f24318ed59b2789df656293b8090977f2b600e38  pred_dobra2.npz
cea66b11855d3b8abbb4a13cba41e47eaf5403b7e2933b07dbeace50311ca160  pred_dobra3.npz
e21bf0b8ccfdad692f18eec39b5099dda46edc57c5389a2d5bde5ccc0900831f  modelo_dobra0.keras
1f7fcc0b5ca8147b94a722759800165a5a9e24e91f3278f7cc444aa6d1a73e7f  modelo_dobra1.keras
a928025a439d64a6c36ed4b8a08392743a644d1888cb3e52bb62b1fc062c1adf  modelo_dobra2.keras
a38f507bcfe66b03b4ed3fb17c9e28a934c1add4d7e4d6396e60d2007b993cc5  modelo_dobra3.keras
0c8670a69444d40e4832dca19e9a157991446ca859e43fc598a2738a598384ae  log_dobra0.csv
f9ece87eb73063aa8cf872ea3da71bc358e47312254d7539c9fb0195a7f6f533  log_dobra1.csv
66569cdcfa93db700ac38fb984bc69b4c6be22bd4643d5b0171cefcb651b533e  log_dobra2.csv
fc38b151de4ed9e29d4797f6b538868be6ded4ba30eb57f2bb4f3268e08bd290  log_dobra3.csv
663d3e144613adfd76bec595b8132d48c7f45895cf35a2b31ed49f3800bb1c62  DOBRAS.json
88640f6d272b31e5e9aef1ae9b6b701e02cf14a69cd3db209df76873327aa99c  REDE_x_MOTOR_Emilio.md
6166d9587f9218efa342cda8872c364b8c4ad234bbf11951ef90f2bda5ca87ba  REDE_x_MOTOR_Helga.md
cc4343c690e412574d90aa764351227b85227a8211cdd8bb85eaea1287c9b9c3  rede_por_imagem_Emilio.tsv
295d9b0daeab1273f63e4c6fdcf47b4c1ce4c08662d4ddcf8d2e2d412a68110a  rede_por_imagem_Helga.tsv
a6f6db31dd7f1f3e9d15c6c163b2b6ecebfba14579ba93ad0a211e5d7ba794c1  treino.log
88072f494beb92354e556dea86ad06f5db7401962e3817c80ff2618e667633db  rede_dados.npz
```

- **No repositório, em `dados/rede_resultado/`:** predições, logs por época,
  dobras, relatórios e tabelas por imagem.
- **Fora do repositório (pesos `.keras`):** só o hash fica
  aqui. Os arquivos ficam guardados com o autor.

---

*Opus, 04/10/2026. Análise autorizada antecipadamente pelo Fabio ("qndo chegar
pode rodar tudo sem eu autorizar").*
