# ADENDO 38 · protocolo do traçador cego — Emílio

**04/10/2026, Brasília, 08h27.** Escrito e publicado **antes** de o Emílio
abrir o painel. Complementa os Adendos 19 e 33.

## 0 · OS ARQUIVOS

| arquivo | SHA-256 |
|---|---|
| `tpl_tracador_camundongo.html` (modelo do painel) | `690e17e49af98fba10ec5ca622b02be24eccda2b0cc9f8fcaa6a6a0fd670c997` |
| `monta_tracador_camundongo.py` (montador) | `e0b15e213a40ac6a842512a6048ecc3185f45f4a1cd14531a6a887992d739312` |
| `tracador_camundongo_emilio.html` (o painel que ele usa) | `fdee7c8471b7dd3d5b19b7520578774a56ec015bbe5fb5bdea2b2b2d482ad48e` |
| `_ORDEM_emilio.json` (código → imagem; **fica com o Fabio**) | `e44ee2e7704ce4f418c483ec1404689e399ef2368bcdfdddc2bdfc47e0bc68be` |

As fotos do painel são **as mesmas vistas** da declaração
(`declaracao_camundongo_v8.html`, `43e0b7ab…`), copiadas byte a byte, com o
SHA de cada uma gravado.

## 1 · O QUE O EMÍLIO VÊ E O QUE NÃO VÊ

**Vê:** só a foto, em ordem sorteada (semente 20261004, mais a soma dos
códigos das letras do nome), com um código de C001 a C201.

**Não vê:**
- nome da imagem, dia ou animal;
- o campo amarelo;
- máscara do motor de nenhuma rodada;
- marcas, notas ou exclusões do Fabio;
- o número de exclusões do Fabio, que ele não sabe.

O mapa entre código e imagem está num arquivo separado, que não vai para ele.

## 2 · A INSTRUÇÃO (a mesma que aparece no painel)

- Traçar a borda da **ferida aberta**, a parte vermelha ou rosada. Se houver
  um anel claro em volta do vermelho, **a borda é o limite do vermelho**
  (Adendo 36, §2).
- Ignorar o anel laranja, os pontos, os pelos e o brilho.
- Se não der para traçar, **não chutar**. Ele tem cinco saídas:
  - `TRACADA`;
  - `PARCIAL`: traçou, mas parte da borda não se vê, e escreve o motivo;
  - `NAO_TRACAVEL`, com o motivo;
  - `PELO`, com o motivo;
  - `FECHADA`: sem parte aberta.
- Ele não pode voltar a uma foto já fechada.

## 3 · O REGISTRO QUE PROVA A CEGUEIRA E O TEMPO

- Antes de começar, ele marca a declaração: *"não vi estas fotos antes, nem
  traçados de outra pessoa ou de máquina sobre elas, e ninguém me disse o que
  esperar"*. A hora fica gravada.
- **Cada foto grava a hora ISO em que abriu e em que fechou.** O tempo total
  aparece na tela e vai no arquivo.
- O arquivo final leva o `navigator.userAgent`, o SHA de cada imagem e o
  histórico completo de eventos (abriu, traçou, apagou, fechou, salvou).

**O que o Fabio disse, às 08h25:** o Emílio vai traçar agora e vai fazer
rápido. **O tempo por foto será relatado** junto com o Dice, porque traçar
rápido é uma condição de uso e não pode ficar escondida.

## 4 · COMO VAI SER USADO

- **Referência para a P12.1 e a P12.3** (Adendo 36): Dice entre a máscara r4 e
  o traçado do Emílio, no braço principal, com o Emílio separado dos outros
  traçadores.
- **Concordância de traçabilidade:** as exclusões do Emílio contra as do Fabio,
  imagem por imagem, com kappa. Isso responde quantas imagens do banco têm
  borda que uma segunda pessoa, cega, também consegue traçar.
- **O Emílio é o leigo** (Adendo 19): não é especialista em ferida, como o
  anotador do trabalho original (Carrión et al.).
- O script que calcula tudo isso será publicado **antes** de o JSON do Emílio
  ser aberto pelo Opus.

---

*Opus, 04/10/2026. Nenhum traçado do Emílio existe até esta linha.*
