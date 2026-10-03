# ADENDO 23 · onde estavam as máscaras da rodada 1 — e a previsão do Opus para a rodada 2

**03/10/2026, Brasília, 08h30.** Cumpre o item 1 da §11 do Adendo 14. **A
rodada 2 não rodou**, e o driver dela não existe.

## 0 · OS ARQUIVOS

| arquivo | SHA-256 |
|---|---|
| `posicao_mascaras.py` | `8296bc06101c05027c3c3bd86defeb80e10c72aa986d59610ef4366866e75c44` |
| `dados/POSICAO_MASCARAS.tsv` | `f7baa78898af47093ab7036b860ccbe3f01eefc75c49ef8ecb0ec65e43cee62c` |
| `dados/POSICAO_MASCARAS_RESUMO.txt` | `5d600308eb6038d084cb5e7eb3c03c276865eaf400e894a8795e4e96de5ff7bc` |

Rodado pelo Fabio no PC, das 07h56 às 08h26, com os módulos congelados lidos de
`06_MOTOR_DE_REGISTRO\` por `PYTHONPATH`.

**As 204 máscaras foram reproduzidas exatamente:** a área de cada uma bateu com
a do `camundongo_v0.json` (`baf4671f…`), com tolerância de 10⁻⁶ mm². O script
para na primeira diferença, e não parou.

## 1 · O RESULTADO

"Zona" é onde está **mais da metade** dos pixels da máscara, no quadro de 700:
buraco (< 5 mm), coroa (5 a 8 mm), fora (> 8 mm).

| | n | buraco | coroa | fora |
|---|---|---|---|---|
| Dice zero contra o nulo | 158 | **0** | 63 | **95** |
| Dice > 0 | 46 | 4 | 41 | 1 |
| **todas** | **204** | **4** | **104** | **96** |
| as 70 limpas (`v`, sem `p`) | 70 | **0** | 41 | **29** |

Nenhuma máscara caiu em "misto".

- **Só 4 das 204 máscaras estão majoritariamente dentro do buraco**, e as 4
  estão majoritariamente dentro do campo amarelo do Fabio.
- **Nas 70 limpas, nenhuma.**
- **96 estão fora do splint**: pelo, pele, campo. Na rodada 1, o pelo do canto
  não foi exceção, foi quase metade.

### A faixa laranja que a coroa não cobre

Pelo `CAMPO.txt`, o laranja visível começa antes dos 5 mm. A faixa entre o
verde do operador e os 5 mm tem largura mínima de **0,50 mm**, mediana de
**0,71 mm** e máxima de **1,60 mm**. **A coroa da rodada 2 não a exclui.**

Na rodada 1, **99 máscaras tocam essa faixa**, mas **em nenhuma ela é mais da
metade** da máscara, e só em 3 passa de 20 %.

## 2 · A PREVISÃO — DO OPUS, NÃO DO FABIO

Separada da P7 do Fabio (Adendos 17, 18 e 20), que continua valendo como está.

**O mecanismo:** a rodada 2 exclui a coroa de três lugares: da banda candidata,
da moldura que estima a pele e do percentil que normaliza. As **104** máscaras
da coroa perdem o candidato. As **96** de fora **não** perdem o candidato, mas
podem mudar mesmo assim, porque a pele e o percentil mudam.

**P8.1 —** Na rodada 2, **pelo menos 80 das 204** imagens com escala continuam
com **Dice zero** contra o nulo.
*Por quê 80:* são 95 com Dice zero fora do splint, menos uma folga de ~15 % para
as que se movem pela mudança de normalização. É estimativa, não cálculo.

**P8.2 —** Nas **70 limpas**, **pelo menos 25** continuam com Dice zero.
*Por quê:* 29 estão fora do splint, com a mesma folga.

**P8.3 —** **A faixa laranja vira armadilha.** Sem a coroa, o anel mais forte
que sobra perto do centro é a borda laranja entre ~4,3 e 5 mm. Previsão: **pelo
menos 20 das 204** máscaras da rodada 2 terão **mais da metade** dos pixels
nessa faixa. Na rodada 1 foram **zero**.
*Medida com a mesma regra* do `posicao_mascaras.py` (`f_faixa > 0,5`), aplicada
às máscaras da rodada 2.

### Uma fraqueza da P5a, apontada antes

A P5a do pré-registro da rodada 2 conta como "mede a ferida" qualquer máscara
que não tenha área de anel. **Uma máscara de pelo no canto, com área de ferida,
conta como acerto.** Se a P8.1 se confirmar, a P5a pode confirmar e o motor
continuar errando de lugar. Por isso a P5a sai **sempre ao lado** do Dice contra
o nulo e da zona da máscara. A ressalva 7.3 do pré-registro já dizia isso da
P5b; aqui vale também para a P5a.

## 3 · O QUE ISTO DIZ SOBRE A RODADA 3

A rodada 3 usa o campo amarelo. Pela tabela da §1, **ela remove as 96 de fora e
as 104 da coroa** de uma vez, e a faixa laranja também, porque o campo fica
0,3 mm para dentro do verde. Fica registrado **antes**: se a rodada 3 não
melhorar, a culpa não vai ser do splint nem do pelo do canto. Vai ser do que
está **dentro** do buraco: plástico, reflexo, pelo no leito, sangue e ponto.

---

*Opus, 03/10/2026. Hashes colados do `sha256sum`. Nenhum resultado da rodada 2
existe até esta linha.*
