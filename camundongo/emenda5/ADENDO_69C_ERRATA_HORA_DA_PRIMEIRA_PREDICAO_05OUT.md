# ADENDO 69-C · errata do Adendo 69-B: a primeira predição saiu 3 segundos antes

**05/10/2026, Brasília, 05h31.** Corrige o Adendo 69-B (`4348373`), que **não
se edita**.

## O que estava errado

O Adendo 69-B diz que, quando foi publicado, não existia nenhuma predição de
conv, mnv2 ou campo. **Isso estava errado por 3 segundos.**

| evento | hora (Brasília) |
|---|---|
| a mensagem com a previsão chega ao Opus (o texto foi escrito antes) | 05h29 |
| gravado `sens_conv/pred_dobra0.npz` (dobra 0 da conv) | 05h29m31s |
| commit do Adendo 69-B | 05h29m34s |

## O que não foi afetado

- **Ninguém abriu a predição.** O Opus viu só a contagem de arquivos (1),
  num comando que conferia que não havia nenhum. Nada do conteúdo foi lido.
- **A previsão foi escrita antes de o arquivo existir.** Quem previu não tem
  acesso a nenhum arquivo do treino.

## Declarado junto

Na mesma conferência, o estado do treino da dobra 0 da conv mostrou:
- parada na época 43;
- melhor modelo na época 13.

É informação de treino (época e critério de parada pré-registrado), não de
teste. Nenhuma decisão dependeu dela.

---

*Opus, 05/10/2026.*
