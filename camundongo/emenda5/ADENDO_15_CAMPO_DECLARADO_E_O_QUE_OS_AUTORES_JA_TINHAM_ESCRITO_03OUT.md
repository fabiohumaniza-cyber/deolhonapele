# ADENDO 15 · o campo declarado, colocado à mão nas 204 — e o que os autores do banco já tinham escrito

**03/10/2026, Brasília, 07h50.** Registro de entrada. **Nenhum motor rodou sobre
este campo.** Este documento existe para que o campo tenha hash antes de
qualquer rodada que o use.

## 0 · OS ARQUIVOS

| arquivo | SHA-256 | bytes |
|---|---|---|
| `campo_disco.py` (a ferramenta) | `ccd9edff840ea539d2fa4312946e2fa6e06aac4dc91f92f90669cd08f3da4aef` | 11.987 |
| `dados/CAMPO.txt` (o campo) | `91160713dc9b01686ec6b3d3426052eece1ed3cb1ef58342f67a731c5c36d7c1` | 20.117 |

O `campo_disco.py` importa o `roda_camundongo.py` (`8c1f6e4d…`) e recorta com as
mesmas `abre_rgb8()` e `recorta()` da etapa 3. Não roda o motor, não lê máscara,
não escreve em nenhum arquivo anterior.

## 1 · POR QUE O CAMPO É COLOCADO À MÃO

Às 06h49 o Fabio apontou que um disco fixo de 4,5 mm no centro calculado "sai
fora" do buraco do splint — "e isso sempre acontece". O `ve_disco.py`
(`d1e1d3e9…`) confirmou: o buraco **visível** na foto é menor que os 5 mm do
splint, mesmo numa imagem limpa de dia 0. O Opus tinha proposto 0,5 mm de
folga; estava errado. O disco passou a ser colocado pelo operador, imagem a
imagem.

## 2 · A REGRA, COMO FOI APLICADA

- O operador arrasta e redimensiona um círculo **verde** até ele encostar na
  borda de dentro do laranja, **sem tocá-lo**.
- O **campo** é o círculo amarelo, **0,3 mm para dentro** do verde
  (`MARGEM_MM = 0.3`, fixada antes da primeira imagem e não alterada).
- A pergunta respondida é **só** "dá para ver onde o laranja termina?". **Não**
  é "dá para laudar a ferida" — essa já está respondida no `CLASSIFICACAO.txt` e
  não muda.
- Plástico, reflexo, pelo, sangue e anotação dos autores **ficam dentro do
  campo, de propósito**. São o que a rodada 3 testa; tirá-los é a rodada seguinte.
- `n` (NAO_DA) quando não dá para pôr um círculo que contenha o buraco sem tocar
  laranja.

Isto foi combinado durante a passada, por escrito, nas mensagens das 07h07,
07h25, 07h31 e 07h34. Na de 07h34 o operador perguntou se dava `n` numa imagem
com as linhas pretas e o texto "~6 manual" dos autores por cima. A resposta foi
não: o buraco estava visível, e dar `n` por artefato seria critério diferente
das outras. Ele deu Enter.

## 3 · O RESULTADO

Passada feita pelo Fabio entre **07h06:56 e 07h48:14**.

| | |
|---|---|
| imagens com escala | 204 |
| com campo (`ok`) | **201** |
| NAO_DA | **3** |
| faltando | 0 |
| linhas no arquivo | 206 (duas imagens gravadas duas vezes com o mesmo valor; vale a última) |

**As 3 NAO_DA são a mesma ferida**, `A8-1-R`, nos dias 1, 3 e 12. As três têm
"plástico deforma a ferida" ou "plástico na ferida" no comentário do operador.
Das três, duas estão classificadas como `n` e uma como `d`.

Raio do círculo encostado (`r_borda`) e do campo (`r_campo`), nas 201:

| | mín. | mediana | máx. |
|---|---|---|---|
| `r_borda` | 3,40 mm | 4,29 mm | 4,50 mm |
| `r_campo` | 3,10 mm | 3,99 mm | 4,20 mm |

- **Nenhum campo ficou menor que 3 mm**, que é o raio do punch.
- O círculo foi deslocado do centro dos cliques em mediana **0,37 mm**, com
  máximo de 1,43 mm. Em 39 imagens não foi deslocado.
- **Nenhum `r_borda` passou de 4,50 mm.**

## 4 · UMA RESSALVA SOBRE O 4,50

A ferramenta **começa** com o verde em 4,50 mm. Em **68 das 201** o operador não
mudou o tamanho, e o teto do banco inteiro é exatamente esse valor de partida.

Há duas leituras, e este registro não escolhe entre elas:
1. o buraco visível nunca passa de ~4,5 mm (o `ve_disco` já indicava isso); ou
2. **ancoragem**: o valor inicial puxou o operador, que só diminuiu.

A ferramenta não tinha teto em 4,5 mm (o limite do código é a metade do quadro).
Mas o valor de partida não era neutro, e isso fica declarado.

## 5 · A PREVISÃO DO FABIO SOBRE O CAMPO

Em 02/10, à noite, antes de qualquer círculo: *"acho que todas vão dar certo"*,
e *"só nas que estiverem ovais e não couberem a gente declara"*.

**201 de 204 couberam.** As 3 que não couberam são a mesma ferida, e pelo
plástico deformado, não pelo formato do buraco.

## 6 · O QUE OS AUTORES DO BANCO JÁ TINHAM ESCRITO

Às 07h41 o Fabio pediu para ver se os donos do banco tinham notado que o filme
atrapalha a imagem. **Tinham.** O artigo é:

> Carrión H, Jafari M, Bagood MD, Yang HY, Isseroff RR, Gomez M. *Automatic
> wound detection and size estimation using deep learning algorithms.* PLoS
> Comput Biol. 2022;18(3):e1009852. Preprint em bioRxiv,
> doi:10.1101/2020.11.13.275917.

Na lista de dificuldades das imagens, os autores citam, entre outras:
- o leito da ferida **ocluído por coberturas plásticas, reflexos e sujeira**;
- **borrão**, por foco errado ou porque o Tegaderm ainda estava em cima;
- iluminação direta por luz de tom quente;
- **pelo que cresce de volta** antes de a ferida fechar e a encobre;
- ângulo de câmera desconhecido em relação à ferida.

O padrão de referência deles foi traçado manual de polígono, em volta da ferida
e em volta do splint, no programa Labelme. O artigo **não** declara imagens
excluídas: mais de 25 % das imagens tinham o splint faltando ou muito danificado,
e foram mantidas e tratadas por pós-processamento.

### O que isto muda no nosso registro

**Este projeto não leu o artigo de origem antes de rodar.** O pré-registro de
30/09 diz que a fonte de tudo era a página do Dryad e o README. O reflexo do
Tegaderm já estava previsto como modo de falha na Emenda 1. Mas a extensão do
problema — plástico **ocluindo** o leito, pelo crescendo de volta — estava
publicada desde 2022.

Daí três consequências:

1. **Frases como "a gente não imaginava o plástico" valem para este projeto e
   não para o campo.** Os artefatos que derrubaram a rodada 1 eram conhecidos e
   publicados pelos autores do banco.
2. **O que o operador viu nas 255 bate com o que os autores descreveram**, de
   forma independente. O censo de visibilidade (Adendos 6 e 10) não foi
   impressão de um observador só.
3. **Daqui em diante, antes de rodar qualquer banco, o artigo de origem é
   lido** e os obstáculos que ele declara entram no pré-registro.

## 7 · O QUE NÃO MUDA

- Rodada 1: encerrada, Adendo 14.
- Ordem do Adendo 14, §11: previsão da rodada 2, ensaio sintético, rodada 2,
  **pré-registro da rodada 3 antes de ela rodar**. Este campo é a **entrada** da
  rodada 3, não o pré-registro dela.
- `CLASSIFICACAO.txt`, `MEDIDAS.txt`, `camundongo_v0.json`: intocados.
- **Nenhuma constante do v0.**

---

*Opus, 03/10/2026. Hashes colados do `sha256sum`. As citações do §6 foram
conferidas no texto do preprint do bioRxiv; os autores e o número da PLoS Comput
Biol vêm do registro bibliográfico (RePEc) e devem ser conferidos contra a
página da revista antes de entrarem em manuscrito.*
