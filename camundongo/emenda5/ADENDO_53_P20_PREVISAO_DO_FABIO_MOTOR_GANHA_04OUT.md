# ADENDO 53 · P20, a previsão do Fabio: o motor ganha da rede

**04/10/2026, Brasília, 13h07.** O treino começou às 13h03 (Adendo 52,
`9f5e18c`). Este adendo foi publicado antes de **qualquer** dobra terminar e
antes de alguém olhar o log do treino.

## A previsão, verbatim (13h06)

> *"nao posso falar uma coisa q nao sei, posso falar diante de observacao,
> nosso motor que nao usa rede neural ganha"*

Ele declara que a previsão vem do que observou: as rodadas 3 e 4 e o traçado
do Emílio. **Não** vem de nenhum resultado da rede, que ainda não existe.

## Como se mede

**P20** (superioridade, mais forte que a P19):
- **Conta:** Dice(motor r4) − Dice(rede), pareado foto a foto, e a mediana
  dessa diferença.
- **Conjunto:** as fotos que a **Helga** marcar TRACADA.
- **Critério:** o motor ganha se o **limite inferior do IC 95 %** dessa mediana
  for **> 0**. O IC é o mesmo da P19: bootstrap por ferida, 2000 sorteios,
  semente 20261004.

Ao lado, **sem veredito**, sai a mesma conta contra o Emílio, que tem viés a
favor da rede.

| resultado | leitura |
|---|---|
| P19 confirmada e P20 falhou | **empate**: o motor não perde, mas também não ganha |
| P19 falhou | **a rede ganha** |

O que estiver no placar é o que vai para o artigo.

---

*Opus, 04/10/2026. Nenhuma dobra terminou até esta linha.*
