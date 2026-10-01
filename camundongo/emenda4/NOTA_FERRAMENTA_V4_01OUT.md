# NOTA DE SUBSTITUIÇÃO · v4 da ferramenta — zoom, referência no lugar, lupa 4×

**01/10/2026, Brasília. Antes de qualquer medida.** `MEDIDAS.txt` não existe;
nenhuma imagem foi medida.

Ajuste de uso pedido pelo Fable depois de ver a ferramenta rodando na foto
grande. **Nada aqui entra em conta nenhuma.**

---

## O QUE MUDOU

| | antes | agora |
|---|---|---|
| referência do banco | canto **inferior esquerdo** — tapava o anel de baixo | canto **superior direito**, abaixo da lupa; tecla **`h`** esconde e mostra |
| zoom | não havia | tecla **`z`** liga/desliga 2× centrado em onde o mouse estava |
| lupa | 3× | **4×** |

## POR QUE ISSO NÃO É MUDANÇA DE MÉTODO

A v3 desenhava direto em coordenada de tela. A v4 passa a ter uma **vista**:
canto `(ox, oy)` **inteiro** na imagem original, escala efetiva `e = fator × zoom`.

Três funções, e são o único lugar onde tela e imagem se encontram — ficam **no
nível do módulo**, fora da janela, justamente para poderem ser testadas sem abrir
tela:

```
janela_de(W, H, larg, alt, fator, z, off)  ->  (ox, oy, ww, wh, e)
tela_para_orig(sx, sy, ox, oy, e)          ->  (x, y)  em px da ORIGINAL
orig_para_tela(x, y, ox, oy, e)            ->  (sx, sy)
```

Os cliques continuam guardados **em px da imagem original**, como sempre
estiveram. O zoom muda o que se vê, nunca o que se grava. Como `ox` e `oy` são
inteiros e `e` é conhecida, ida e volta são exatas.

### Medido, não afirmado

Imagem 3000 × 4000 numa tela de 1860 × 880 — fator 0,22, redução de 4,55×, que é
o caso real do Fabio:

```
pior erro de ida e volta, em 8 pontos, com zoom 1x e 2x:  0.00e+00 px
diametro medido com zoom 1x:  650.000000000 px
diametro medido com zoom 2x:  650.000000000 px
diferenca:                      0.00e+00 px
```

Zero, não "desprezível".

## E O PIXEL, JÁ QUE O ASSUNTO VEIO

O Fable tem razão e o número está no ensaio: um erro de **1 px num dos quatro
cliques**, num diâmetro de 2.000 px, dá **−0,025 %** no diâmetro e **−0,050 %**
em área. O que grava é a coordenada do cursor; o círculo verde é desenho.

Isso está escrito no cabeçalho do arquivo, para quem for usar não ficar mirando
no desenho.

## SUBSTITUIÇÃO

| arquivo | antes | agora | bytes |
|---|---|---|---|
| `mede_anel.py` | `5fc3f957d057163f0f42298c8787af72868c188e1674f6d5c48c18d8a858be22` | `259430d84b9bb2ea43e49271119707c4150bca13d895acc3cc17611252a1b3dd` | 17.951 |
| `teste_mede_anel.py` | `5c02a439ffc8cce893a61ab5268067e41e2c5d7f2d36119905c15bfedd3f28cc` | `adaf221d3cf250db93d61f95699f70d959356b423ac2d279e42fd1de53061d72` | 9.878 |

Substituídos no mesmo caminho, pela mesma razão da vez anterior: **nenhuma das
versões produziu medida**. Os bytes antigos ficam no commit `36a90896…` e estão
declarados aqui. O `ADENDO_2_QUAL_ANEL_01OUT.md` (`0867a9ec…`) cita o
`5fc3f957…` e **não é alterado**; esta nota é que diz que aquele hash foi
substituído.

## O QUE NÃO MUDOU

O formato do `MEDIDAS.txt` — quatro campos, e o ensaio confirma que o
`roda_camundongo.py medir` segue aceitando. A conta dos quatro cliques: média
das duas maiores entre as seis distâncias, centro pela média dos quatro, ordem
irrelevante, aviso da 3ª maior em 0,80. A tecla `d` e a coluna
`mais_de_um_anel` no log. A regra de qual anel, do Adendo 2. `append` com
`fsync` por imagem e a retomada pulando as feitas.

---

*Opus, 01/10/2026. Hashes colados do `sha256sum`. Nenhuma medida existe até esta
linha.*
