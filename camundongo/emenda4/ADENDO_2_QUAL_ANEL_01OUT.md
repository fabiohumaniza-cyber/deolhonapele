# ADENDO 2 · qual anel é o desta imagem

**01/10/2026, Brasília. Antes de qualquer medida.** `MEDIDAS.txt` não existe no
PC do Fabio até esta linha; nenhuma imagem foi medida.

Adendo à `EMENDA_3_CAMUNDONGO_01OUT.md` (`299c9181…`) e à
`NOTA_MEDIDA_MANUAL_01OUT.md` (`0f851530…`), que **não são alteradas**.

**Declaração de ato do operador:** para escrever este adendo, o Opus abriu duas
imagens do banco — `Day 0_A8-1-L.tiff` (`a638c881d0b2d78078fd9bb6dc9e4fc68f0de18e57b56029ef288641c7cf2b80`)
e `Day 0_A8-1-R.tiff` (`3dca964340739e7c4d09fa561d6ebbf5fec3cc36e1b220b35e02a15ffe33d913`).
Olhar foto não é medir, e nada do que está congelado mudou por isso; fica
registrado porque o registro é a regra.

---

## 1 · O ACHADO

**O enquadramento não é constante no banco.** Nas duas imagens abertas:

- `Day 0_A8-1-L.tiff` — **retrato, 3000 × 4000**. Mostra o animal inteiro, em
  decúbito, cabeça à esquerda, **com os dois splints no quadro**, mais um cartão
  de identificação escrito "A8-1 / Day", a caixa de acrílico e o campo azul.
- `Day 0_A8-1-R.tiff` — **paisagem, 4000 × 3000**. É um **close de um único
  anel**, com uma mão enluvada segurando o animal. O outro splint **não aparece**.

Os dois arquivos têm hashes distintos: são fotos diferentes, não uma copiada
duas vezes. O pré-registro fica de pé — são 255 fotografias.

Mas a consequência é operacional e precisa de regra: **em parte das imagens há
mais de um anel no quadro, e o operador precisa saber qual medir.** Medir o anel
errado não estraga a escala (os dois splints são de 16 mm), mas **troca a ferida**:
a série temporal daquela ferida passa a misturar dois sítios diferentes, e o
estrato L × R da Emenda 3 fica invertido para aquela imagem. É erro silencioso,
que é a classe que este projeto existe para não cometer.

## 2 · A REGRA

Por ordem; a primeira que se aplicar decide.

1. **Um único anel no quadro** → é esse. Não há escolha a fazer.
2. **Mais de um anel** → é o que aparece no recorte publicado pelos próprios
   autores do banco, `Cropped images/Day N_<animal>-<L|R>.png`, para esta mesma
   ferida-dia. O operador compara e mede o correspondente.
3. **Não determinável** (o recorte de referência não resolve, ou não há recorte)
   → **`SEM_ANEL`**, pela regra 1 do pré-registro: a imagem vai para o estrato
   *sem escala própria* e roda em px². **Nunca chute.**

A regra 2 **não é critério inventado aqui**. É a rotulagem dos próprios autores:
a pasta `Cropped images` traz 255 PNGs, um por ferida-dia, com o nome completo
`Day N_<animal>-<L|R>.png` — a mesma convenção que o `achata_banco.py`
(`efe5081d…`) usou para nomear a pasta plana, e com a mesma ausência declarada
(`Day 9_Y8-2-R`). A correspondência é 1 para 1.

**Por que não por anatomia.** Decidir "esquerda" e "direita" pela posição da
cabeça e das patas exige saber se a vista é dorsal ou ventral e aplicar a
convenção anatômica certa. Errar isso **inverte os 255 de uma vez**, de forma
sistemática e invisível. O recorte dos autores não tem esse risco: ele já é a
resposta deles.

## 3 · O OUTRO ANEL DENTRO DO RECORTE

O recorte da etapa 3 tem 24 mm de lado centrado no anel medido: meia-largura
12 mm. O outro anel tem raio 8 mm. Logo **ele toca o recorte se os centros
estiverem a menos de 20 mm** — e, nesse caso, um segundo anel de 16 mm entra no
quadro de trabalho, onde a coroa da rodada 2 não o cobre.

Isso é **modo de falha a registrar, não a corrigir**: nada se recorta diferente,
nada se pinta. Para que ele seja contado em vez de suposto, o operador passa a
marcar, por imagem, se há **mais de um anel no quadro** — tecla `d`, item 4.

Não estimo aqui a distância típica entre os centros: minha tentativa de medi-la
por limiar de cor não foi confiável, porque **o anel vem quebrado pelas suturas e
pelos reflexos do silicone**. Número que eu não medi direito não entra em
registro hasheado. Depois da etapa 2, com D e centro de cada imagem conhecidos, a
distância sai por conta.

## 4 · A FERRAMENTA, v3

`mede_anel.py` passa de
`7bee9991f28740c4ded02f9fe0a0c1a3591113d4d3463dd60e3c677cc7a9861b` para
`5fc3f957d057163f0f42298c8787af72868c188e1674f6d5c48c18d8a858be22` (14.774 B).
Duas adições, **nenhuma delas mede coisa alguma**:

- **Terceiro argumento opcional**: a pasta `Cropped images`. Quando dada, o
  recorte dos autores para a ferida-dia corrente aparece num canto, com a
  legenda *"referência do banco — é ESTA ferida"*. É figura: não é clicável, não
  entra em conta, e se o PNG não existir a ferramenta segue sem ele.
- **Tecla `d`**: marca/desmarca "há mais de um anel neste quadro". Vai para o
  **`MEDIDAS_LOG.tsv`**, em coluna nova, **não** para o `MEDIDAS.txt` — o
  formato que a etapa 2 exige continua com exatamente quatro campos, e o ensaio
  confirma que o `medir` segue aceitando as linhas.

O `MEDIDAS_LOG.tsv` ganha a coluna `mais_de_um_anel`. Como nenhuma medida existe,
nenhum log precisa ser migrado.

## 5 · UM SEGUNDO ACHADO, REGISTRADO ANTES DA RODADA

Nas duas imagens abertas, **a moldura de 8 % do quadro — que é exatamente o que
`mapa_t` usa para estimar a pele — está contaminada**:

| imagem | quadro | quase preto na moldura de 8 % | no quadro inteiro |
|---|---|---|---|
| `Day 0_A8-1-L` | 3000 × 4000 | **24,8 %** | 23,3 % |
| `Day 0_A8-1-R` | 4000 × 3000 | **12,2 %** | 7,0 % |

*(critério: soma dos três canais < 40; contagem simples de intensidade, sem
modelo de cor.)*

A causa é visível: a foto é montada num quadro maior, com um **retângulo preto**
num dos cantos superiores e um **cartão de identificação branco** no outro, mais
campo azul, acrílico e luva verde. Um quarto da moldura de referência de pele da
imagem L não é pele — não é pele coisa nenhuma.

**A P4 do pré-registro prevê que a falha dominante será a referência de pele
contaminada.** Este adendo registra que o **mecanismo foi visto antes de o motor
rodar**, em duas imagens, com números. Isso **não altera a P4**, não altera
limiar nenhum e não autoriza recorte novo. Fica escrito agora precisamente para
que, depois, não possa ser confundido com explicação inventada após o resultado.

## 6 · O QUE NÃO MUDA

Escala pelo anel **externo** de 16 mm; `px_mm = D/16`; recorte de 24 mm → 1380 →
700; `diam_ef` 11,5 mm; a grade de 144; semente 20260928; as 255; uma rodada;
zero exclusão; **nenhuma constante do v0**; o detector congelado, que continua
reprovado nas 255 e não será tocado; e todo o pré-registro da rodada 2 com o
Adendo 1.

---

*Opus, 01/10/2026. Hashes colados do `sha256sum`. Duas imagens do banco foram
abertas e estão declaradas na seção 0. Nenhuma medida existe até esta linha.*
