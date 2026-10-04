# ADENDO 51 · o erro de método da rodada 1, assumido, e a área de análise fixada

**04/10/2026, Brasília, 12h47.** Pedido do Fabio, às 12h44:

> *"a gente tem q assumir o erro de metedologia e fixar a area, justificando no
> trabalho deles"*

Nada aqui altera os Adendos 14 e 15, nem qualquer arquivo com hash.

## 1 · O ERRO, ASSUMIDO

Na **rodada 1** (Adendo 14), o motor v0 rodou **sem limite de área**: buscou a
ferida na foto, e não só dentro do anel (splint). Isso foi **erro de método
nosso**, não do motor nem do banco.

- O banco foi feito com um anel em volta de cada ferida, para delimitar onde
  ela está. O estudo original mede **só dentro do anel** (§3).
- Nós não lemos o artigo de origem antes de rodar. Isso já está declarado no
  Adendo 15, §6.
- **Consequência:** o motor mediu o anel e a pele junto com a ferida. Por isso
  a curva não caiu com os dias: Spearman −0,16, contra os −0,8 previstos.

A rodada 1 **continua publicada**, como resultado negativo. Ela não é apagada
nem refeita.

## 2 · A ÁREA, FIXADA

Desta data em diante, toda análise do braço camundongo usa como área de busca
o **interior do anel**. Isso vale para o motor, para os traçadores e para os
enfermeiros.

- **O campo** é o de `dados/CAMPO.txt`
  (`91160713dc9b01686ec6b3d3426052eece1ed3cb1ef58342f67a731c5c36d7c1`). Foi
  colocado à mão, foto a foto, antes de qualquer rodada que o usasse
  (Adendo 15).
- O recorte é o **circunscrito** das rodadas 3 e 4 (Adendos 28 e 36).
- O campo não muda. Se precisar de outro, ele vai para arquivo novo, com
  pré-registro.
- As rodadas 3 e 4 já usavam esse campo. A partir daqui, ele deixa de ser "uma
  rodada" e passa a ser **o método**.

## 3 · A JUSTIFICATIVA, NO TRABALHO DELES

Carrión et al. 2022 (PLoS Comput Biol 18(3):e1009852), código público em
github.com/Gomez-Lab/WoundSizeEstimation (commit `45fb2d2`),
`Wound_Segmentation_Inference_and_Results_(external).ipynb`:

| o que fazem | onde |
|---|---|
| uma rede acha o anel; a foto é girada e recortada num quadrado de 352 px **com o anel no centro** | `Wound_Cropper.ipynb` (`angle_key.csv`); pastas `consistent_crops_full` |
| a segmentação tem duas classes, **interior do anel** (verde) e **ferida** (vermelho) | células 13 e 225 |
| ferida = a mancha vermelha **mais perto do centro do anel** (172, 172) | célula 15, `single_mask_size_wound` |
| área = pixels da ferida ÷ pixels do interior do anel × **π·5² mm²** (anel de 10 mm de diâmetro interno) | célula 230, `get_manual_size` |
| a referência humana são dois polígonos por foto, **`Ring_inner`** e ferida, e a área manual sai pela mesma conta | células 225 e 232 |

O estudo original **nunca** analisa fora do anel. Ao fixar a área no interior
do anel, este projeto passa a medir **no mesmo espaço** que o estudo
original.

## 4 · O QUE CONTINUA DIFERENTE, E FICA DECLARADO

| | Carrión et al. | este projeto |
|---|---|---|
| quem define a área | uma rede, sozinha | uma pessoa (o Fabio), com hash antes de rodar |
| escala | relativa ao anel (π·5²) | fixa no quadro: 29,1667 px/mm |
| Dice | no recorte | no **quadro inteiro de 700 px**, o que é conservador para o motor |

## 5 · NO ARTIGO

*"Na primeira execução, o motor foi aplicado sem restrição de área e falhou
(ρ = −0,16). Isso foi erro de método nosso: o estudo de origem restringe a
análise ao interior do anel. A área de análise foi então fixada no interior do
anel, colocada manualmente e registrada antes das execuções seguintes. A
primeira execução é relatada como resultado negativo."*

---

*Opus, 04/10/2026.*
