# ADENDO 69-K · previsões do Fabio e do Claude para as redes de sensibilidade

**05/10/2026, Brasília, 17h57.** Publicado antes de a análise de sensibilidade
rodar. Até esta linha, nenhuma predição das redes conv, mnv2 e campo foi aberta
ou comparada com traçado, e o `sensibilidade_rede.py` não rodou.

## Estado do treino nesta hora

- **conv:** dobras 0, 1 e 2 terminadas (melhor época 13, 294 e 219); dobra 3 em
  andamento.
- **mnv2 e campo:** não começaram.

## O que os dois viram antes de prever

- **A sondagem do Adendo 69-E.** É a rede original, dobra 3, só o log de Dice de
  validação. Resultado: ainda subindo, +0,035 contra desvio de 0,014.
- **As épocas de parada da conv**, listadas acima.
- **Uma linha de métrica de treino da fila.** Na checagem das 16h03, o fim do
  `sens_treino.log` mostrou o Dice de treino e de validação de uma época. É
  validação interna da rede, não é o teste contra a Helga.
- **Nenhum Dice contra traçado** de rede nova.

## Fabio (17h57), nas palavras dele

> "novo empate"

**Como se confere.** Contra a rede mais forte, isto é, a de maior Dice mediano
contra a Helga (Adendo 68, §4, regra 2), nas 67 fotos TRACADA, o resultado tem
de ser:
- P19 confirmada;
- P20 não confirmada.

## Claude (17h56)

| parte | previsão |
|---|---|
| conv | quase igual à rede original, porque a paciência de 30 a para cedo (dobra 0 na época 43) |
| mnv2 | a mais forte das três e a mais perto do motor |
| campo | sem previsão; fica registrado como recusa explícita |
| veredito contra a rede mais forte | **empate** (P19 confirmada, P20 não confirmada) |
| mediana motor − rede mais forte | **menor que +0,030** (a original deu +0,030) |
| chance de o motor falhar a P19 | cerca de **30 %** |

**Como se confere.** Pelas contas do Adendo 69-B: mediana da diferença pareada e
IC por bootstrap por ferida, 2000 sorteios, semente 20261004, com o
pós-processamento do confirmatório.

Cada parte será marcada **confirmada** ou **falhou** no Adendo 70.

## Correção de uma fala desta tarde

Às 17h53, o Claude disse ao Fabio que o artigo do camundongo ainda não tinha
título. Estava errado. O título em forma de pergunta já está registrado no
Adendo 68, §4, regra 5: *"É preciso treinar uma rede para medir uma ferida na
fotografia?"*. O que depende do resultado é o subtítulo.

---

*Opus, 05/10/2026, 17h57. A análise de sensibilidade não rodou até esta linha.*
