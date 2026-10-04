# ADENDO 59 · treino da rede interrompido três vezes; passa a ser retomável

**04/10/2026, Brasília, 16h55.** Nenhuma dobra terminou e nenhuma predição de
teste existe até esta linha.

## O que aconteceu

O ambiente de treino é reiniciado quando a conversa fica parada. A dobra 0 foi
interrompida três vezes:

| tentativa | parou na época | quando |
|---|---|---|
| 1 | 32 | 14h54 |
| 2 | 46 | ≈ 15h45 |
| 3 | 74 | ≈ 16h45 |

Os arquivos parciais de cada tentativa ficam guardados, não são apagados e não
são usados.

### Uma coisa vista sem querer, declarada

Às 14h58, ao checar por que o treino parou, apareceram na tela linhas do log
da tentativa 1 com o `dice` de **treino**. É o Dice achatado em três canais,
no conjunto de treino, não no de teste nem no de validação, e não diz nada
sobre a P19 e a P20. Nenhum `val_dice` e nenhuma predição foram vistos.

## O que muda: só a retomada

`rede/retoma_rede.py` (`d6566938a81ee5746447db2a50685161672fa83dd49f0987d81b594d824c4d6e`) importa do `treina_rede.py`
(`b767471e…`, que **não muda**) as dobras, a arquitetura, a métrica, a perda,
o otimizador, as 100 épocas, o lote, o aumento e o checkpoint pelo maior
`val_dice`. A saída é a mesma: `pred_dobra{k}.npz`.

O que ele acrescenta:
- ao fim de **cada época**, grava o modelo inteiro (pesos e estado do
  otimizador) e o melhor `val_dice` até ali;
- quando recomeça, segue da época seguinte;
- o checkpoint do melhor modelo continua de onde estava.

### Desvio declarado

O sorteio dos lotes depois de uma retomada usa a semente 20261004 + k + 1000 ×
época inicial. Por isso, a sequência de lotes não é idêntica à de um treino sem
interrupção. Os dados, as dobras e os hiperparâmetros não mudam.

O código foi testado com 1 e 2 épocas numa pasta temporária, que depois foi
apagada. Nenhuma métrica desse teste foi olhada.

---

*Opus, 04/10/2026.*
