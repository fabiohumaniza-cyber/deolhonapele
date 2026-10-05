# ADENDO 68 · pré-registro das análises de sensibilidade: motor × rede

**05/10/2026, Brasília, 04h56.** Este adendo é publicado **antes** de rodar
qualquer uma das análises abaixo. Até esta linha, só rodou um teste de fumaça
de uma época da rede pré-treinada, para medir o tempo; ninguém olhou métrica
nem predição desse teste, e a saída foi apagada.

## 1 · Por quê

Uma revisão externa independente leu o rascunho do artigo motor × rede e
apontou quatro problemas no resultado do Adendo 67 (`1d8495b`):

1. **A rede pode não ter convergido.** O melhor modelo apareceu nas épocas
   80, 91, 99 e 95, perto do teto de 100.
2. **A comparação é assimétrica.** O motor recebe o campo de busca colocado à
   mão; a rede não.
3. **Uma U-Net treinada do zero, em 201 fotos, não representa as redes
   atuais**, que usam codificador pré-treinado.
4. **O veredito depende de 0,004** no limite inferior. É preciso saber se ele
   muda com outra semente ou outro método de IC.

O revisor também pediu que a rede fosse avaliada sem o filtro de
pós-processamento, que gerou 33 máscaras vazias.

## 2 · O que NÃO muda

- **O veredito do Adendo 67 é o confirmatório e não será reescrito:** P19
  confirmada, P20 não confirmada, leitura registrada **empate**.
- Tudo abaixo é **sensibilidade**, decidida depois de ver o resultado do
  Adendo 67, e assim será rotulado no artigo.
- O motor não muda: as mesmas máscaras r3 e r4, sem nenhuma constante nova.

## 3 · As análises

### Sobre as predições que já existem (minutos)

| | análise | o que responde |
|---|---|---|
| S1 | o veredito do jeito registrado (2000 sorteios, semente 20261004) | referência para as outras |
| S2 | 10 sementes (20261004 a 20261013) × 10 000 sorteios por ferida; BCa com jackknife por ferida | o veredito é estável? |
| S3 | mediana das medianas por ferida, IC por bootstrap das feridas | o resultado depende de feridas com muitas fotos? |
| S4 | sem as fotos em que a rede deixou a máscara vazia, diferença pareada com IC | quanto da vantagem vem das vazias? |
| S5 | a rede sem pós-processamento: ferida = todo pixel classificado como ferida | o filtro prejudicou a rede? |

### Três redes novas (horas)

Mesmas fotos, rótulos (traçado inteiro do leitor 1), dobras, perda, otimizador,
lote e aumento do Adendo 52. Predição fora da dobra, como antes.

| rede | o que muda | responde ao item |
|---|---|---|
| **conv** | a mesma U-Net, treinada até convergir: até 300 épocas, para após 30 épocas sem melhorar o Dice de validação | 1 |
| **mnv2** | U-Net com codificador **MobileNetV2 pré-treinado na ImageNet**, todas as camadas treináveis; até 150 épocas, mesma paciência | 3 |
| **campo** | a U-Net conv, mas a foto fora do **mesmo campo de busca que o motor recebe** vira preta, e a ferida predita fora dele é zerada | 2 |

- **Ordem:** conv, depois mnv2, depois campo.
- **Por que MobileNetV2:** é a rede de codificador pré-treinado usada por
  Wang et al. (2020, Sci Rep) para segmentar feridas, e cabe em CPU.
- **Os pesos ImageNet** vêm do repositório público
  `JonathanCMitchell/mobilenet_v2_keras` (release v1.1, a origem dos pesos
  oficiais do Keras): `mobilenet_v2_weights_tf_dim_ordering_tf_kernels_1.0_224_no_top.h5`,
  SHA-256 `f8aff69536bd77a692c594f559c798c19bf7f3f36668fc9fa00b21c6aab4797c`.
  O endereço oficial do Keras está bloqueado neste ambiente.

### O motor sem o campo manual

**O motor v0 não detecta o anel sozinho;** a escala sempre vem dos cliques do
operador. A execução sem campo de busca (execução 1, Adendo 14) já
falhou e está relatada. Não há execução nova do motor.

### Leitura (sem computação)

**A reimplementação reproduz o original?** Carrión et al. relatam Dice de
teste de 0,8665 (Adendo 49). A comparação vai para o texto, com a ressalva de
que a métrica e o conjunto de teste deles não são idênticos aos daqui.

## 4 · Regras de leitura, fixadas agora

1. **Para cada rede nova**, contra a leitora 2 (Helga), nas fotos que ela
   marcou TRACADA:
   - P19 e P20 calculadas exatamente como no Adendo 52/53 (S1);
   - S2 a S5 ao lado.
2. **No resumo e na conclusão do artigo entra o resultado contra a rede mais
   forte:** a de maior Dice mediano contra a Helga nesse conjunto, entre a
   original, conv, mnv2 e campo.
   - Se o motor falhar a P19 contra qualquer uma delas, o resumo diz que ele
     foi pior que aquela rede.
3. **Instabilidade não vira vitória.** Se a P20 passar em alguma semente do S2
   mas não na registrada, a leitura continua empate, e a instabilidade é
   relatada.
4. **Tudo é relatado,** inclusive o que for contra o motor.
5. **O título em forma de pergunta** ("É preciso treinar uma rede para medir
   uma ferida na fotografia?") serve a qualquer resultado; o subtítulo e o
   resumo acompanham o que sair.

## 5 · Arquivos (o código não muda depois deste commit)

| arquivo | SHA-256 |
|---|---|
| `rede/treina_rede2.py` | `286a478ea1f96e23078279ad9bc30ca8c43f975016df8a367cd549df5212cf06` |
| `rede/sensibilidade_rede.py` | `1a6774fde74ead6dc205b6e48d34c3291b46ef1aff1dbe38d06819c2e9ff73b3` |
| `rede/treina_rede.py` (importado, sem mudança) | `b767471e8ec8cb5f3cd5aa5d1319c3fdfb235a0203de31b216e25d8d828bfd8d` |
| `rede/analisa_rede.py` (importado, sem mudança) | `e3c5e9d0b8f35558a2e8f3a040679a60c6ce4b191e2e23b5cb37bf4827c6f725` |
| `dados/CAMPO.txt` | `91160713dc9b01686ec6b3d3426052eece1ed3cb1ef58342f67a731c5c36d7c1` |
| `rede_dados.npz` | `88072f494beb92354e556dea86ad06f5db7401962e3817c80ff2618e667633db` |

Treino em CPU (2 núcleos), estimativa total de 20 a 30 horas, retomável.

---

*Opus, 05/10/2026. Nenhuma das análises acima rodou até esta linha.*
