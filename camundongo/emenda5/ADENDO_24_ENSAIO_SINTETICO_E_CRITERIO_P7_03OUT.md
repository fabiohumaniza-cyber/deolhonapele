# ADENDO 24 · o ensaio sintético da rodada 2, o critério da P7 e o driver

**03/10/2026, Brasília, 08h37.** A rodada 2 **não rodou** sobre nenhuma imagem do
banco até esta linha.

## 0 · O DRIVER

| arquivo | SHA-256 |
|---|---|
| `roda_rodada2.py` | `420ff85baf520ba68fea6dcc8c019f16c4a2e278025208867cbd0f9821bf861f` |

Ele importa `roda_camundongo.py` (`8c1f6e4d…`) e `motor_v0_funcoes.py`
(`16028493…`) sem alterá-los. A função `roda_motor_ar` é a `roda_motor` da
etapa 3, linha a linha, com `ar = coroa` no lugar de `None`. A coroa vai de
145,83 a 233,33 px no quadro de 700. **Nenhuma constante do v0 muda.**

As 51 imagens SEM_ANEL não têm coroa e, pelo pré-registro, "rodam igual nas duas
rodadas". **Não são reexecutadas**: o resultado delas é copiado da rodada 1 e
marcado `copiada_da_rodada1`. A reexecução daria o mesmo resultado, porque a
reprodução das 204 do Adendo 23 mostrou que o motor é determinístico.

## 1 · O ENSAIO SINTÉTICO (pré-registro da rodada 2, §6)

São 30 cenas desenhadas por código, com semente 20260928, sem nenhuma imagem do
banco. Seguem a geometria do README: coroa de 5 a 8 mm e ferida de 2,4 a 3,0 mm
de raio, deslocada até 1 mm. Duas coisas foram acrescentadas, e ficam
declaradas:
- **o laranja visível começa entre 4,3 e 4,6 mm**, como o campo do operador
  mostrou (Adendo 15). Isso deixa a faixa que a coroa não cobre;
- achatamento de até 12 %, rotação qualquer e ruído.

| caso | n |
|---|---|
| 1 · o motor pega a ferida (Dice ≥ 0,5) | **29** |
| 2 · o fechamento atravessa a coroa | 0 |
| 3 · `anel()` devolve `None` | **0** |
| outro | 1 (Dice 0,475) |

Nas 29, o Dice contra a ferida desenhada ficou entre 0,960 e 0,985.

**A condição de parada não disparou.** A rodada 2 pode acontecer.

**Limite do ensaio, dito antes:** a cena sintética **não tem** pelo, luva,
régua, plástico nem reflexo. Ela prova só que a coroa excluída **não quebra a
topologia** do motor. **Não prova que ele vai achar a ferida nas fotos reais.**
Na rodada 1, 96 das 204 máscaras estavam fora do splint, e o ensaio não tem
nada fora do splint.

## 2 · O CRITÉRIO DA P7

A P7 do Fabio (Adendos 17, 18 e 20) não tinha número. O Fabio pediu para rodar
às 08h31, antes de responder às duas perguntas de 08h29. **Este critério é do
Opus**, escrito antes de rodar. Se o Fabio ler a P7 de outro jeito, a leitura
dele vai em arquivo novo e vale como segunda leitura, lado a lado, sem apagar
esta.

"Zona" é a mesma do `posicao_mascaras.py`: onde está mais da metade dos pixels
da máscara.

| | critério | confirma se |
|---|---|---|
| **P7.1** "vai mudar muito" | fração das 204 cuja máscara **muda de zona** da rodada 1 para a 2 | ≥ 50 % |
| **P7.2a** plástico = fracasso | entre as imagens com marca `p`, fração com máscara na zona **buraco** | < 50 % |
| **P7.2b** não laudável = fracasso | entre as imagens de classe `n`, fração com máscara no **buraco** | < 50 % |
| **P7.3** pelo | só existe em comentário livre | **não avaliável** |
| **P7.4** reflexo | só existe em comentário livre | **não avaliável** |

As limpas (`v` sem `p`) saem na mesma tabela, **só para comparação**, sem veredito.

A zona **buraco** quer dizer que o motor olhou para dentro do splint. **Não
quer dizer que ele achou a ferida.** Sem traçado humano, a rodada 2 não mede
acerto; mede **para onde o motor olha**.

## 3 · O QUE SAI

`camundongo_r2.json` e `CAMUNDONGO_R2_RELATORIO.md`, com P5a, P5b, as duas
assinaturas, a distribuição das áreas, a tabela de zonas, a P8 do Opus, a P7 do
Fabio e o pareado entre rodada 1 e rodada 2.

---

*Opus, 03/10/2026. Nenhum resultado da rodada 2 existe até esta linha.*
