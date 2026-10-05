# ADENDO 69-D · nota do revisor de IA e a curva de validação da rede original

**05/10/2026, Brasília, 05h33.** Publicado antes de qualquer resultado de teste
das redes de sensibilidade. Até esta linha, existe uma predição (dobra 0 da
conv), que ninguém abriu.

## 1 · O revisor diz onde a própria previsão deve errar primeiro

Depois de saber só que a dobra 0 da conv parou na época 43, com o melhor
modelo na 13 (Adendo 69-C), o revisor escreveu, verbatim:

> "Se a conv converge cedo e é essencialmente a mesma rede do confirmatório,
> ela deve chegar perto de 0,850, e a diferença pontual deve ficar perto de
> +0,030 em vez de cair para a faixa de −0,02 a +0,02 que eu registrei. […]
> A previsão continua valendo como está escrita no 69-B."

A previsão do Adendo 69-B não muda. Esta nota só fixa, antes do número, onde
o revisor espera errar.

## 2 · A curva de validação da rede original, dobra 0

**A fonte.** `dados/rede_resultado/log_dobra0.csv`, já publicado no Adendo 67.
Não é resultado de teste.

| época (contando de 1) | Dice de validação (3 classes) |
|---|---|
| 5 | 0,797 |
| 10 | 0,868 |
| 13 | 0,887 |
| 20 | 0,870 |
| 27 | 0,905 (o melhor até a época 43) |
| 40 | 0,894 |
| 60 | 0,887 |
| 81 | **0,911 (o máximo)** |
| 100 | 0,904 |

**Leitura descritiva.**
- Do dia 13 ao 81, o Dice de validação subiu devagar, cerca de +0,02, com
  oscilação.
- Não é só ruído num platô, nem uma curva que ainda sobe forte.
- Na rede original, a melhor época até a 43 foi a 27. Na conv, foi a 13. Os
  dois treinos, que partem da mesma semente, divergem cedo. O treino em CPU
  não é determinístico, e a rede original foi retomada com outra semente
  depois da época 32.
- **Consequência possível:** numa curva que sobe devagar, a paciência de 30
  épocas pode parar a conv antes do ponto que a rede original alcançou. Isso
  não foi previsto no Adendo 68 e será relatado com o resultado.

## 3 · Correção de unidade na Tabela 1 do manuscrito

As épocas do melhor modelo da rede original (80, 91, 99 e 95) foram lidas da
coluna `epoch` do log, que conta a partir de 0. Contando a partir de 1, como a
conv, elas são **81, 92, 100 e 96**. O manuscrito passa a usar a contagem a
partir de 1.

---

*Opus, 05/10/2026.*
