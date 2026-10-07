# ADENDO 70-A · exploratório: rede, motor e humanos onde os humanos discordam

**07/10/2026, Brasília, 02h28.** Escrito **antes** de calcular qualquer número desta análise. É posterior ao Adendo 70 e motivado por ele: é **exploratório** e não muda nenhuma leitura registrada.

## Pergunta

Nas fotos em que os dois traçadores humanos menos concordam entre si, como se comportam a rede (mnv2) e o motor?

## O que já se sabe e não muda

- A rede treinou com os traçados do **Emílio** (Adendo 52).
- A **Helga** nunca foi vista pela rede e é a referência limpa.
- O resultado principal (Adendo 70) é contra a Helga e não é reescrito.

## A régua (fixada agora)

- **Conjunto:** as 67 fotos TRACADA pela Helga. Entram as que o Emílio também traçou; as demais saem, e são contadas.
- **Concordância humana:** Dice(Helga, Emílio) por foto, no quadro de 700 px. Os traçados são rasterizados como no `analisa_rede.py`.
- **Grupo de baixa concordância:** o **quartil inferior** desse Dice. Fotos empatadas no corte entram.
- **Grupo de referência:** os outros três quartis.

## O que se relata, nos dois grupos

Medianas por foto de:
- Dice(Helga, Emílio);
- Dice(rede, Helga);
- Dice(rede, Emílio);
- Dice(motor r4, Helga);
- Dice(motor r4, Emílio).

Ao lado, a diferença pareada **Dice(rede, Helga) − Dice(Helga, Emílio)**, com IC 95 % por bootstrap das fotos (2000 sorteios, semente 20261007).

## Leitura (neutra, fixada agora)

- **Se a rede ficar mais perto da Helga do que o Emílio fica da Helga, no quartil inferior:** escreve-se que, onde os humanos discordam, a rede produz um contorno mais próximo de cada traçador do que eles ficam um do outro.
  - Isso é compatível com um **contorno médio**.
  - **Não é evidência de borda recuperada.** Nessas fotos, Dice alto significa concordância com uma convenção humana.
- **Se ficar igual ou mais longe:** escreve-se isso.
- **Rede × Emílio** está ao lado porque o Emílio é o "professor" da rede. Se ela ficar tão perto da Helga quanto do Emílio, o contorno médio fica reforçado.
- **O motor não conhece traçado nenhum.** A queda dele no quartil inferior é relatada como tal.

Nada aqui muda o veredito, o resumo ou o subtítulo definidos pelo Adendo 69 e aplicados no Adendo 70.

---

*Opus, 07/10/2026, 02h28. Proposta do Fable, com a correção do Opus (a rede treinou com o Emílio) e o acréscimo da linha rede × Emílio. Nenhum número desta análise foi calculado até esta linha.*
