# ADENDO 69-B · previsão do revisor de IA para as redes de sensibilidade

**05/10/2026, Brasília, 05h30.** Publicado antes de qualquer rede de
sensibilidade terminar: até esta linha, não existe nenhuma predição de conv,
mnv2 ou campo. Transmitida ao autor pelo Fabio, que autorizou o registro
("pode registrar").

## Quem prevê, e com que informação

**Quem.** Uma instância de IA generativa, numa conversa separada, que revisou
o manuscrito do artigo da rede.

**O que essa instância viu:**
- o texto do manuscrito (v2 a v6);
- o preprint do porco;
- a Tabela 1 (épocas do melhor modelo e Dice de validação da rede original);
- a menção de que uma linha de log da época 16 da conv foi vista, sem o
  número.

**O que não viu:** o código, os dados e nenhum outro resultado de treino.

Isso delimita o que a previsão vale.

## A previsão, nos termos dela

> **conv:** diferença pontual cai para a faixa de −0,02 a +0,02, intervalo
> mais estreito que o atual, limite inferior ainda abaixo de zero.
> Veredito: empate.
>
> **mnv2:** mesma faixa, talvez com a pontual já negativa. Acho improvável que
> o intervalo inteiro fique abaixo de zero com n = 67 e 16 feridas, mas é aqui
> que vejo a maior chance disso acontecer.
>
> **campo:** sem previsão. Registre como recusa explícita, não como omissão.
>
> **Transversal:** nenhuma das três cruza o teto humano de 0,976, e o ganho
> pareado sobre o nulo de nenhuma delas passa de +0,15.

**A parte que pode desmentir a previsão.** Se uma rede bem treinada passar de
+0,15 sobre o nulo enquanto o motor fica em +0,117, a leitura de que "os dois
pegam pouco mais da metade" cai, e o artigo passa a ter um vencedor.

## Como cada parte será conferida

Todas as contas são contra a leitora 2, nas 67 fotos TRACADA, com o
pós-processamento do confirmatório (Adendo 69).

| parte | conta |
|---|---|
| "diferença pontual" | mediana da diferença pareada Dice(motor r4) − Dice(rede) |
| "intervalo" | IC 95 % por bootstrap por ferida, 2000 sorteios, semente 20261004 |
| "mais estreito que o atual" | largura do IC menor que 0,227 (−0,004 a +0,223) |
| "cruza o teto humano" | Dice mediano da rede > 0,976 |
| "ganho pareado sobre o nulo" | mediana da diferença pareada Dice(rede) − Dice(nulo), com o mesmo bootstrap |

Cada parte será marcada **confirmada** ou **falhou** no Adendo 70. A recusa
sobre a campo fica registrada como recusa.

---

*Opus, 05/10/2026. Nenhuma rede de sensibilidade terminou até esta linha.*
