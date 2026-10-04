# ADENDO 36 · PRÉ-REGISTRO DA RODADA 4 — o campo declarado mais a declaração do operador

**04/10/2026, Brasília, 08h03.** Escrito **antes** de a rodada 4 rodar no banco.
A exceção são 4 imagens que o Opus rodou para testar o driver. Elas estão
declaradas na §1 e saem da P13.

## 0 · OS ARQUIVOS

| arquivo | SHA-256 |
|---|---|
| `roda_rodada4.py` (driver) | `602a6013bec4f3fe3f2ccf7bb889c8490828575110a7c10c1484baabe1459d9d` |
| `analisa_rodada4.py` (placar) | `0c6a82cf0dd790fc7710912b62dfa985b9c866b26c2d55455379c17a05ccc7b7` |
| `dados/declaracao_camundongo_r4.json` (a declaração) | `eeaa5d8f725472a1d251390cce956e52757bfe462230e6a9db639dbada83b9e9` |
| `declaracao_camundongo_v8.html` (a página, montada no PC) | `43e0b7ab3e773d05629b7299a6d3e3adc1c0246f1ab8651222ed274deadb08a9` |
| `declaracao_camundongo_modelo_v8.html` / `monta_declaracao_v8.py` | `1ad997da…` / `553c80e0…` |
| `confere_declaracao.py` | `41fad00bcbcb0a53125590064059ebac032f2a99cc029b38fcd403b267b88bb0` |
| `dados/CAMPO.txt` · `dados/camundongo_v0.json` · `dados/camundongo_r3.json` | `91160713…` · `baf4671f…` · `ab82d594…` |

O motor é o v0 congelado, **sem nenhuma constante alterada**. O driver importa
`roda_rodada3.py` (`72cfb5cc…`), `roda_rodada2.py` (`420ff85b…`),
`roda_camundongo.py` (`8c1f6e4d…`) e `motor_v0_funcoes.py` (`16028493…`).

## 1 · O QUE JÁ FOI VISTO ANTES DESTE REGISTRO

- **Fabio:** marcou as 201 imagens na v8 entre 03/10 13h23 e 04/10 07h45, **sem
  o traçado do motor na tela**. Antes disso já tinha visto as máscaras da
  rodada 3 nas 201 (Adendos 33 e 34). Da rodada 4 não viu nenhum número.
- **Opus:** às 08h00 rodou o driver em **4 imagens reais**, para conferir que
  ele funciona: `Day 0_A8-1-L` (nada), `Day 0_A8-1-R`, `Day 0_Y8-3-L` e
  `Day 8_Y8-2-L` (ok). Viu os números dessas 4. **Por isso as 4 saem da P13**,
  que é a previsão do Opus. Elas continuam em todo o resto do relatório.

## 2 · A DECLARAÇÃO

**201 imagens**, cada uma com um estado:

| estado | n | o que é |
|---|---|---|
| `nada` | 81 | nada a tirar |
| `ok` | 56 | com conta-gotas e/ou artefato |
| `NAO_TRACAVEL` | 49 | a borda não pode ser seguida com confiança |
| `BORDA_PARCIAL` | 11 | só parte da borda é visível |
| `PELO` | 4 | pelo sobre o leito (Adendo 32) |

**Regra de traçabilidade**, aplicada pelo operador e escrita agora como foi
usada: *a borda pode ser seguida com confiança na maior parte da volta.* Abaixo
disso a imagem sai, com o motivo escrito na nota.

**Cicatrizadas:** 5 imagens têm "cicatrizada" ou "fechada" na nota e estão como
`NAO_TRACAVEL`: `Day 10_Y8-2-R`, `Day 10_Y8-3-L`, `Day 10_Y8-4-L`,
`Day 13_Y8-2-L` e `Day 15_A8-3-L`. Elas ficam **fora da medida** e formam um
braço **exploratório**, em que a resposta certa é área ≈ 0.

**Revisão antes do registro, declarada:** entre 07h18 e 07h45 de 04/10, o Opus
cruzou estado e nota e apontou 8 desacordos. O Fabio corrigiu os 8 na própria
página: 1 imagem marcada como não traçável por um clique duplo, 1 nota faltando,
3 PELO sem nota, 1 "não traçável" escrito na nota mas não marcado, 1 "borda
parcial" escrito mas não marcado, e 1 cicatrizada para uniformizar. Nenhuma
correção foi feita depois de ver resultado do motor.

**O motivo do artefato.** O botão de motivo ficou em "reflexo" nas imagens até o
dia 5 e em "sangue" do dia 6 em diante, mesmo onde a marca é filme ou pelo. O
motor não usa o motivo, então isso não muda nenhuma medida. **A contagem por
motivo no artigo sai das notas**, e não do botão.

**Definição de borda usada nas duas bordas** (anel claro e leito vermelho), dita
pelo Fabio em 04/10, às 06h19, na `Day 7_A8-4-R` e seguintes: **a borda é o
limite do vermelho.** O protocolo dos traçadores vai repetir essa definição.

## 3 · COMO A DECLARAÇÃO ENTRA NO MOTOR

- **Coordenadas:** um ponto da vista vale (vx0 + x, vy0 + y) no quadro de 700.
  O `confere_declaracao.py` conferiu as 56 imagens com correção no PC do Fabio,
  em 04/10 às 07h49: **todas caíram no mesmo lugar**, com diferença média por
  pixel de 1,37 a 2,23, abaixo do limite de 4,0.
- **Conta-gotas:** pinta os pixels do traço com a cor escolhida, exatamente
  como a página desenha.
- **Artefato:** a união dos discos entra no `ar` do recorte circunscrito da
  rodada 3, junto com os cantos fora do campo.
- **Setas e notas:** o driver não usa.
- **Toda imagem roda duas vezes:** r3, sem a declaração, e r4, com ela.

**Travas do driver**, que param tudo se falharem:
1. o r3 refeito tem de bater com o `camundongo_r3.json`, com tolerância de
   10⁻⁶ mm²;
2. nas imagens `nada`, o r4 tem de ser idêntico ao r3;
3. o campo da declaração tem de bater com o `CAMPO.txt`, com tolerância de
   0,05 px.

**Ensaio sintético** (30 cenas, semente 20260928):
- sem declaração, o r4 saiu **igual ao r3 em 30 de 30**;
- com um disco de artefato **fora** da ferida (4 cenas), a máscara **não
  entrou nele em 4 de 4**;
- com o disco **em cima** da ferida (26 cenas), a ferida foi achada (Dice ≥ 0,5)
  em 25 de 26: o motor fecha a máscara por cima e o artefato não abre buraco
  na ferida.

## 4 · OS BRAÇOS (Adendo 35, nunca somados)

| braço | estados | filme | n | estatuto |
|---|---|---|---|---|
| **principal** | ok + nada | não | **71** | confirmatório |
| com filme | ok + nada | sim | 66 | exploratório |
| excluídas | NAO_TRACAVEL, PELO, BORDA_PARCIAL | — | 64 | descritivo |
| cicatrizadas | as 5 da §2 | — | 5 | exploratório, resposta certa ≈ 0 |

## 5 · AS PREVISÕES

### P11.2 — do Fabio, Adendo 28: *"tirando artefato é que vai surpreender"*

Confirma se, **no braço principal**, as duas condições valem:
- Spearman(dia, área mediana r4), nos dias com n ≥ 3, **≤ −0,8**; e
- esse valor é **mais negativo** que o do r3 nas mesmas imagens.

### P12.1 e P12.3 — do Fabio, Adendos 31 e 34: *"traçados bons"*, *"quase todas certinhas"*

São avaliadas **contra os traçadores cegos** (Helga, Emílio e as enfermeiras),
no braço principal, com cada traçador separado:
- **P12.1** confirma se a **mediana do Dice** entre a máscara r4 e o traçado
  for **≥ 0,70**;
- **P12.3** confirma se **pelo menos 80 %** das imagens tiverem **Dice ≥ 0,70**.

### P12.2 — do Fabio: pelo

Fica **descritiva**. O relatório mostra, nas 4 PELO, se o motor devolveu área ou
`None`, que é a pergunta do Adendo 31.

### P14 — do Fabio, 04/10, 07h56, verbatim

> *"tem muitas, mas muito q eu corrigi q nem precisava corrigir... entauma gente
> vai ter q fazer tbm um levantamento pro trabalho o efeito dacorrecao"*

Confirma se **pelo menos metade** das 56 imagens corrigidas tiver
**Dice(r3, r4) ≥ 0,95**, ou seja, a correção não mudou a máscara.
*O critério é do Opus. Se o Fabio ler diferente, a leitura dele vai em arquivo
novo e vale ao lado desta.*

### P13 — do Opus: borda falsa

Confirma se **pelo menos 25 %** das imagens medidas com artefato dentro do
campo, **sem as 4 da §1**, tiverem **≥ 30 % do contorno da máscara r4 a até
2 px de um pixel de artefato**.

*Por quê:* nas pranchas do `confere` há imagens em que o artefato contorna a
ferida rente à borda. Lá, o contorno mais forte que sobra pode ser a beirada da
pintura, e não a ferida.

## 6 · O QUE O RELATÓRIO MOSTRA ALÉM DO PLACAR

- **Efeito da correção, imagem por imagem**, nas 56: fração do campo pintada
  com conta-gotas e com artefato, área r3, área r4, Dice r3×r4 e borda falsa.
- A curva do braço principal, a do braço com filme, as cicatrizadas e as 64
  excluídas, cada uma separada.
- **A medida é assistida.** Quem declarou o artefato já tinha visto onde o motor
  errou na rodada 3. O r4 é **o motor com o operador**, e não o motor sozinho,
  e é reportado assim, como a medida assistida da bancada humana. O motor
  sozinho é o r3.

## 7 · ORDEM

1. Este arquivo, com hash, publicado.
2. O Fabio roda `roda_rodada4.py rodar`, depois `analisa_rodada4.py`.
3. O resultado vai num adendo próprio, com o placar copiado do relatório.

---

*Opus, 04/10/2026. Fora as 4 imagens da §1, nenhum resultado da rodada 4 existe
até esta linha.*
