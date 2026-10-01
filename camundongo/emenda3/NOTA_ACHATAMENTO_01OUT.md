# NOTA · por que existe o `achata_banco.py`

**01/10/2026, 07h54 (Brasília). Escrita e hasheada ANTES de qualquer TIFF do banco
Dryad 10.25338/B84W8Q ser aberto.** Anexa à `EMENDA_3_CAMUNDONGO_01OUT.md`
(SHA-256 `299c91818ef9db680d6b2bbdaa1e4bf5bf4eed9a7c097a63a5a8544ffeab68ce`).
A Emenda 3 **não é alterada por este arquivo**.

---

## O FATO QUE OBRIGA

O README do banco (SHA-256 `1c414307…`, 24.611 bytes, o mesmo citado na Emenda 1)
descreve os TIFFs brutos assim:

```
<animal>\Left wound\Day N.tiff
<animal>\Right wound\Day N.tiff
```

O animal e o lado estão **no caminho da pasta**, não no nome do arquivo.
`Day 0.tiff` existe 16 vezes no banco — uma por ferida. Os PNGs **recortados**, que
não entram na rodada primária, é que têm nome completo: `Day 0_A8-1-L.png`.

O `roda_camundongo.py` (SHA-256 `2e926368283b56b396bdad532c715cbc7d41e8fc001fe684d917e705ffc5481a`)
lista **uma** pasta e usa o nome do arquivo como chave do JSON, do
`MAPA_FERIDA_DIA.tsv` e do painel da P3. Apontado para a árvore como ela vem, ele
tem três destinos, todos ruins:

1. apontado na raiz, acha **0** imagens;
2. apontado numa subpasta, acha **16** e chama a rodada de completa;
3. tornado recursivo às pressas, **sobrescreve chave em silêncio** — 16 imagens
   ocupando a mesma entrada, 239 perdidas sem erro.

O terceiro é a classe de erro que este projeto existe para não cometer. Já
aconteceu dez vezes aqui com arquivo hasheado fora do lugar citado, e uma vez
comigo mesmo, em hash inventado num commit público (errata `34cbf4c0…`).

---

## O QUE O SCRIPT FAZ, E O QUE NÃO FAZ

`achata_banco.py` — SHA-256 `efe5081d4cbb6e91f046f71dd51cb2fda2f63e97b81d5ab424c0833b39609e1a`,
5.902 bytes.

**Faz:** copia cada TIFF para uma pasta plana com nome único
`Day N_<animal>-<L|R>.tiff`; grava `MANIFESTO_ACHATAMENTO.tsv` com origem,
destino e o SHA-256 dos dois; gera `MAPA_FERIDA_DIA.tsv` a partir da **árvore de
pastas**.

**Não faz:** não move, não renomeia o original, não apaga nada, não decodifica
imagem, não reamostra, não converte, não corrige, não escolhe. Ele lê bytes e
escreve os mesmos bytes. `from PIL import Image` não aparece no arquivo.

Por isso ele **não é motor novo nem pré-processamento novo**: a medida que o
motor v0 vai ler é byte a byte a mesma que o Dryad entregou, e o manifesto prova
isso com hash de origem e de destino em cada uma das 255 linhas. É operação de
nome de arquivo, e nada mais.

E por isso **nenhuma linha do `roda_camundongo.py` muda**. O driver continua
congelado no hash acima. É o banco que passa a ter a forma que o driver
congelado já esperava.

### Convenção: por que *esta* e não outra

`Day 9_A8-1-L.tiff` é a convenção do **próprio README**, nos PNGs recortados.
Não foi inventada aqui. Se fosse inventada, seria regra nova entrando depois do
pré-registro.

---

## AS QUATRO PARADAS

O script sai com código 1, **sem ter copiado nada**, se:

1. existir `.tif`/`.tiff` fora de `<animal>\<Left|Right> wound\Day N.tiff` —
   com o animal casando `[AY]8-<n>`;
2. o total não for **255**;
3. o conjunto ferida×dia não for exatamente o do README: 8 animais × 2 lados ×
   dias 0–15, **menos** `Y8-2 Right Day 9`, a única ausência que o README declara
   (duas vezes: na Folder 7 e na nota das imagens recortadas);
4. um nome de destino repetir, ou o SHA-256 da cópia divergir do da origem.

A parada 3 é o ponto que o Fable marcou: **o mapa não se dobra para fechar a
conta.** Ele é conferido contra o README antes de a primeira cópia sair, e se não
bater, a rodada não começa — não se ajusta a lista para dar 255.

---

## ENSAIO, ANTES DO BANCO REAL

`teste_achata.py` — SHA-256 `4d9e3b7866890c57d432f20dcd220e839ef35cdc33701591dac111d883351c44`,
4.653 bytes. Monta árvores sintéticas com a estrutura do README e bytes
aleatórios de semente 20260928. Nenhum arquivo do banco é tocado.

| caso | esperado | obtido |
|---|---|---|
| árvore completa, 255 | copia 255, nomes únicos | 255 copiados, 255 nomes únicos, 0 divergência de hash, 255 linhas no mapa, código 0 |
| 254: falta não declarada | para, nada copiado | código 1, 0 arquivos na pasta de destino |
| 255 mas conjunto errado (`Day 7` de A8-1-L trocado por `Day 16`) | para, dizendo o que falta e o que sobra | código 1, `faltam: [('A8-1','L',7)]  sobram: [('A8-1','L',16)]` |
| `.tiff` fora da convenção | para, nada copiado | código 1 |
| rodar duas vezes | mesmo manifesto, mesmo mapa | hashes iguais nas duas passadas |

---

## ORDEM DE USO, NESTA SEQUÊNCIA

```
python achata_banco.py "<raiz do banco descompactado>" "D:\...\10_CAMUNDONGO\plano"
copy "D:\...\10_CAMUNDONGO\plano\MAPA_FERIDA_DIA.tsv" "D:\...\10_CAMUNDONGO\saida\"
python roda_camundongo.py detectar "D:\...\10_CAMUNDONGO\plano" "D:\...\10_CAMUNDONGO\saida"
```

O mapa tem de estar na pasta de **saída**: é lá que a etapa 1 o exige e grava o
SHA-256 dele, e é contra esse hash que a etapa 4 recusa um mapa alterado. O
`copy` acima é cópia, não edição — o mapa que a etapa 1 hasheia é byte a byte o
que o `achata_banco.py` gerou da árvore.

O `MANIFESTO_ACHATAMENTO.tsv` **não** tem hash declarado aqui, de propósito: ele
contém caminhos absolutos do PC do Fabio, então o hash dele é diferente em cada
máquina. O que está congelado é o script que o gera. O que o manifesto prova é
interno a ele: cada linha traz os dois SHA-256, e eles são iguais.

---

*Escrita pelo Opus em 01/10/2026 às 07h54, a pedido do Fabio, com o diagnóstico
do nome repetido conferido pelo Fable no README `1c414307…`. Nenhuma imagem do
banco foi baixada, aberta ou inspecionada até esta linha.*
