# EMENDA 5 · as marcas da foto, e a extensão do driver para o 5º campo

**02/10/2026, Brasília. Antes das 228.** O motor não rodou em nenhuma imagem; a
etapa 3 não foi executada.

Decisão do Fable em 02/10, de madrugada, sobre a pergunta deixada em aberto na
véspera: **marcar, não pular.**

---

## 1 · POR QUE MARCAR E NÃO PULAR

Pular adia e não acrescenta nada. Marcar **registra antes do motor** e transforma
três fatos sobre a fotografia em variáveis explicativas legítimas do relatório.

A diferença é inteira: *"das que falharam, tantas tinham reflexo no plástico"*
dito **antes** da rodada é análise; dito **depois** de ver quais falharam é
história contada para encaixar no resultado. É a mesma razão de tudo o mais
neste projeto estar hasheado com hora.

## 2 · O VOCABULÁRIO, FECHADO

| tecla | significa |
|---|---|
| `p` | plástico/reflexo sobre o anel |
| `d` | dois anéis no quadro |
| `f` | pelo dentro do anel |

**Fechado de propósito.** Marca é fato declarado sobre a foto, não texto livre.
Letra fora dessas três **para a etapa 2** com mensagem nomeando a marca inválida.
Se amanhã fizer falta uma quarta, isso é emenda nova com hash — não uma letra
inventada no meio da medição.

O `d`, que na v3–v5 já existia e ia só para o log, **vira marca** e passa a
viajar com a medida.

## 3 · O FORMATO

A linha mantém os quatro campos de sempre e ganha o quinto:

```
Day 3_A8-1-L.tiff   612.600    1500.000   2000.000   p;f
Day 9_Y8-2-L.tiff   SEM_ANEL   -          -          d
Day 4_Y8-1-R.tiff   598.100    1402.500   1988.000   -
```

Ordem canônica **`p;d;f`**, sempre — a linha não depende da ordem em que o
operador apertou as teclas. `-` quando não há nenhuma. Marca combina tanto com
medida quanto com `SEM_ANEL`. As colunas 3 e 4 do `SEM_ANEL` levam `-` para que
o campo de marcas fique **sempre na quinta posição**.

As teclas são alternadas (aperta de novo e tira) e aparecem na barra antes de
gravar. Tudo vai também para o `MEDIDAS_LOG.tsv`, em coluna própria.

**Marca não é medida.** Não muda diâmetro, centro nem escala. Nenhuma imagem é
excluída por marca, e nenhuma marca entra em predição.

## 4 · A EXTENSÃO DO DRIVER — E POR QUE ELA FOI NECESSÁRIA

Conferido no código antes de escrever: a `etapa_medir` do
`3b787ef95a344ddba94fa5520feadb54e20afaffd1d399816a085947e9a35a55` exige
`len(partes) != 4 → PARADO` para linha medida. Uma linha de cinco campos **para
a etapa 2**. Não havia como ter o quinto campo sem estender o driver.

Como o Fable mandou: **extensão com nota, não edição.** O `3b787ef9…` fica
intocado em `camundongo/emenda4/`, com o hash dele; o novo entra em
`camundongo/emenda5/`.

| | hash |
|---|---|
| antes | `3b787ef95a344ddba94fa5520feadb54e20afaffd1d399816a085947e9a35a55` |
| agora | `8c1f6e4d1bc9c937caa4345ed7f11c038cfc75863739f1afc9e1e6fc53a0ee51` (33.671 B) |

O que mudou, e **só isso**:

1. `le_marcas()`, função nova: lê o 5º campo contra o vocabulário fechado e
   **para** se achar letra de fora.
2. `etapa_medir` aceita 4 **ou** 5 campos e grava `marcas` no registro. Linha de
   quatro campos continua válida — o `teste_driver.py` escreve assim e segue
   passando.
3. A linha da etapa 3 carrega `marcas` para o `camundongo_v0.json`.
4. A etapa 4 ganha uma seção descritiva: por marca, quantas imagens, quantas com
   medida e quantas sem.

**Nada mais.** Nenhuma constante do v0, nenhum limiar, nenhuma predição, nenhuma
regra de escala, de recorte ou de nulo.

### O que a etapa 1 já produzida continua valendo

A `deteccao_camundongo.json` (mapa `87c4d45a…`, 01/10 13:21:53 −03) foi escrita
pelo `3b787ef9…`. O que mudou no driver **não toca na detecção**: nem o detector,
nem `abre_rgb8`, nem o critério de reprovação. Os 255 de 255 reprovados continuam
sendo o resultado da etapa 1, pelo código que a rodou.

## 5 · AS 27 JÁ MEDIDAS: REABRIR TODAS

Decisão do Fable, e concordo: reabrir **as 27**, não só as 10.

O motivo é que o banco inteiro passa a sair de **uma única versão da
ferramenta**, sem uma coluna de marcas vazia nas primeiras 27 que depois teria de
ser explicada em nota de rodapé. Custa uns 15 minutos do Fabio.

```
python reabre_pendentes.py "...\saida" "medidas na v3 sem campo de marcas" --todas
```

O `MEDIDAS_ATE_<data-hora>.txt` guarda as 27 antigas, byte a byte, com hash
conferido.

### O teste de repetibilidade que cai no colo

As **17 feridas do dia 0** terão sido medidas duas vezes, por **operadores
diferentes do mesmo operador**: ele na v3, ontem, sem saber que remediria; e ele
hoje na v6, com zoom e com a referência fora do caminho.

Comparar as duas séries dá, de graça, uma **repetibilidade intra-observador** —
coisa que normalmente exige desenhar um estudo para obter. Fica declarado aqui,
**antes** de as segundas medidas existirem, que essa comparação será feita e
reportada **seja qual for o resultado**, inclusive se a dispersão for feia.

Os dados ficam nos dois arquivos: `MEDIDAS_ATE_<data-hora>.txt` (v3) e
`MEDIDAS.txt` (v6).

## 6 · HASHES

| arquivo | SHA-256 | bytes |
|---|---|---|
| `mede_anel.py` (v6) | `d4e4e81bfce1db89462ce9dd451620c7378c9db20a1f9116551d54fb959ed9f2` | 20.366 |
| `roda_camundongo.py` (emenda 5) | `8c1f6e4d1bc9c937caa4345ed7f11c038cfc75863739f1afc9e1e6fc53a0ee51` | 33.671 |
| `reabre_pendentes.py` (com `--todas`) | `c4c5bf334718299f20f198f28bd805fb080cca778f1cb02bd6df4fbaf0ec2976` | 5.267 |
| `teste_mede_anel.py` | `5735d6448dcde53a65117ad56d6834d061beb1b229b4d9b3c811a5643f7d7b26` | 11.125 |

Colados do `sha256sum`. Substituem `ba018034…` (v5), `3b787ef9…` (driver) e
`3e31fcb4…` (reabertura), que ficam onde estão, intocados.

### Duas coisas que o `--todas` obrigou

O `reabre_pendentes.py` ganhou a forma `--todas`, que reabre **todas** as linhas
de medida do arquivo — não existia; só havia nomes avulsos e `--sem-anel-do-dia`.

E, com o arquivo reaberto inteiro, o `MEDIDAS.txt` ficaria com o **cabeçalho
antigo de quatro colunas** sobre linhas de cinco. O `mede_anel.py` passa a
escrever o cabeçalho também quando o arquivo existe mas está **sem linha de
medida**. O cabeçalho velho fica, como comentário: ele registra que o arquivo
mudou de versão de ferramenta, o que é informação, não sujeira.

## 7 · ENSAIO

- **Ordem canônica**: `{f,p}` → `p;f`; `{f,d,p}` → `p;d;f`; vazio → `-`.
- **As marcas chegam ao JSON** pela etapa 2: `['f','p']`, `[]`, `['d']` nas três
  linhas de teste, com `px_mm` e estrato inalterados.
- **Marca inventada para a rodada**: um `x;p` numa linha faz a etapa 2 sair com
  código 1 nomeando a marca inválida.
- **Zoom 1× contra 2×**: diferença `0.00e+00` no diâmetro, as 24 ordens de clique
  dando um valor só — tudo o que já passava continua passando.
- **`teste_driver.py`** (`b49bbdc9…`) re-executado inteiro: quatro etapas correm,
  cinco paradas de protocolo param, e linha de quatro campos segue aceita.

---

*Opus, 02/10/2026, a pedido do Fabio, com a especificação do Fable e o ponto da
`etapa_medir` conferido no código, não de memória. O motor não rodou em nenhuma
imagem até esta linha.*
