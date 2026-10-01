# EMENDA 4 · alfa constante em 255 no `abre_rgb8`

**01/10/2026, Brasília. Escrita DEPOIS do achatamento e ANTES de qualquer medida.**
Nenhuma imagem do banco passou pelo motor até esta linha.

Emenda à `EMENDA_3_CAMUNDONGO_01OUT.md`, SHA-256
`299c91818ef9db680d6b2bbdaa1e4bf5bf4eed9a7c097a63a5a8544ffeab68ce`, que **não é
alterada por este arquivo**.

---

## 1 · O QUE O BANCO TEM

Conferido no banco já achatado, antes de rodar:

- **254 imagens RGBA + 1 RGB** (`Day 0_Y8-3-L.tiff`, 36.000.586 bytes — exatamente
  3000 × 4000 × 3).
- Nas 254 RGBA: **alfa mínimo = alfa máximo = 255**, em todo pixel.
- `uint8` em todas; 3000 × 4000 e 4000 × 3000 (retrato e paisagem).

O driver `2e926368…`, como estava escrito, **para na primeira imagem**: ele exigia
modo PIL `RGB` e recusava `RGBA`. Essa trava foi escrita de propósito, antes do
download, para que formato inesperado nunca fosse convertido no improviso. Ela
fez o trabalho dela: parou, e a decisão vem por escrito, datada, antes da medida.

---

## 2 · A REGRA

> `RGBA` com alfa **≡ 255 em todo pixel** → usa `[:, :, :3]`, grava o `modo_pil`
> **original** no JSON.
> `RGB` de 8 bits → segue como estava.
> Qualquer alfa ≠ 255, ou qualquer outro modo → **PARADO**.

Alfa constante em 255 não carrega informação: os três canais de cor são byte a
byte os mesmos com ou sem ele. **Nenhum número muda por causa desta emenda.**

A fatia `[:, :, :3]` é explícita de propósito, e `np.ascontiguousarray` só
garante o layout — nenhum dos dois toca em valor.

---

## 3 · CORREÇÃO DE UM MECANISMO, REGISTRADA

Estava em circulação a ideia de que o detector congelado já descartaria o alfa
sozinho, pelo `convert('RGB')` dele. **Duas coisas erradas nisso**, as duas
conferidas no código e em teste:

1. `Image.convert('RGB')` do PIL descarta o alfa **sem compor, inclusive quando o
   alfa é diferente de 255**. Testado: com alfa 200, o resultado de
   `convert('RGB')` é idêntico ao RGB original. Ele não é trava nenhuma — aceita
   em silêncio exatamente o caso que a gente quer barrar.
2. No caminho real, o detector **nunca abre arquivo**. A etapa 1 chama
   `abre_rgb8(p)` e passa o **array** para `detecta(arr)`; a linha
   `Image.open(...).convert('RGB')` do detector só roda quando ele recebe um
   caminho, o que não acontece aqui.

Portanto `abre_rgb8` é o **único** ponto do projeto onde o alfa é conferido. Está
escrito assim no docstring da função.

---

## 4 · O QUE MUDA E O QUE NÃO MUDA

**Muda:** uma função do driver, `abre_rgb8`.

| arquivo | antes | agora |
|---|---|---|
| `roda_camundongo.py` | `2e926368283b56b396bdad532c715cbc7d41e8fc001fe684d917e705ffc5481a` | `3b787ef95a344ddba94fa5520feadb54e20afaffd1d399816a085947e9a35a55` (31.309 B) |

O `2e926368…` fica **substituído**, e fica recuperável no commit `863939b` do
branch. Substituí-lo não reescreve resultado nenhum: **ele nunca rodou no banco
real** — parou na primeira imagem, que é o motivo desta emenda existir.

**Não muda:**

- `detecta_anel_camundongo.py` — `56f1b434…`, intocado.
- `motor_v0_funcoes.py` — `1602849373157ec849cef1ff3a39b75a797f85ad4f0b8adedfb810719ae4d224`, intocado. **Nenhuma constante do v0.**
- `achata_banco.py` — `efe5081d4cbb6e91f046f71dd51cb2fda2f63e97b81d5ab424c0833b39609e1a`, **já rodou**: 255 arquivos copiados byte a byte, `MANIFESTO_ACHATAMENTO.tsv` `363b4105…`, `MAPA_FERIDA_DIA.tsv` `87c4d45a…`, com 39 GB livres na hora. Não há v2 dele: trocar cópia por hard link agora jogaria fora um achatamento feito e hasheado para ganhar nada.
- Toda a Emenda 3: estratos, nulo geométrico, ordem de abertura da P3, as quatro predições, as cinco paradas.

---

## 5 · O CUSTO, DITO COM TODAS AS LETRAS

Esta é **mais uma decisão tomada depois de olhar o banco**. A trava existia desde
antes do download e está sendo afrouxada porque se viu o que havia lá dentro.
Quem for contar ajustes pós-abertura deve contar este, e tem razão.

O que separa este de um ajuste que contamina: ele é sobre **formato de arquivo**,
não sobre medida. Não existe versão desta regra que faça a ferida sair maior ou
menor — os pixels de cor entregues ao motor são os mesmos nos dois lados da
emenda. E ela é mais **restritiva** do que simplesmente converter: barra alfa não
constante, que `convert('RGB')` deixaria passar.

---

## 6 · ENSAIO, ANTES DO BANCO

`teste_alfa.py` — SHA-256
`bcec15223ed25cb3728e78cd4336f6970d76f167a878c28a8e60c3081ca32349`, 3.105 bytes.
Imagens desenhadas por código, semente 20260928.

| caso | esperado | obtido |
|---|---|---|
| RGBA, alfa 255 em todo pixel | passa | passa, `modo_pil='RGBA'`, forma (120, 90, 3) |
| RGBA, alfa 200 em todo pixel | para | para: *"alfa entre 200 e 200, esperado 255"* |
| RGBA com **um único** pixel de alfa 254 | para | para: *"alfa entre 254 e 255"* |
| RGB puro de 8 bits | passa | passa, `modo_pil='RGB'`, inalterado |
| 16 bits | para | para: *"modo PIL 'I;16'"* |
| tons de cinza | para | para: *"modo PIL 'L'"* |

E a conferência que importa: com alfa 255, os três canais entregues são **byte a
byte iguais** ao RGB original.

O terceiro caso é o que prova a regra: um pixel em 254 no meio de uma imagem
inteira em 255 já para a rodada. `min` e `max`, não média.

O `teste_driver.py` (`b49bbdc9…`) foi re-executado inteiro com o driver novo: as
quatro etapas correm e as cinco paradas de protocolo continuam parando.

---

*Escrita pelo Opus em 01/10/2026, por decisão do Fabio, com a regra redigida pelo
Fable e o mecanismo corrigido contra o código. Nenhuma medida foi produzida até
esta linha.*
