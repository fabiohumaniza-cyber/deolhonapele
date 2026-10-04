# ADENDO 39 · o Emílio traça todas, mesmo imaginando a borda

**04/10/2026, Brasília, 08h30.** Altera o Adendo 38 (`f97b82d`), que **não se
edita**. Escrito antes de o Emílio abrir qualquer painel. O painel v1 não deve
ser usado.

## O que o Fabio pediu, às 08h29, verbatim

> *"coloca q ele vai tracar mesmo nas que naum sao possiveis... vai tentar
> imagnar a broda"*

## Por quê

Assim o Emílio faz **o mesmo que o anotador leigo do Carrión et al.**, que
traçou um polígono em todas as fotos. A diferença é que aqui **cada traçado
diz quanto foi visto e quanto foi imaginado**. Isso permite as duas análises:
- com tudo, comparável ao trabalho original;
- só com o que ele viu, comparável à regra de traçabilidade do Fabio.

## O que muda no painel (v2)

| | v1 (Adendo 38) | v2 (este) |
|---|---|---|
| traçar | só o que dá para ver | **todas**, mesmo imaginando |
| como fecha cada foto | TRACADA · PARCIAL · NAO_TRACAVEL · PELO · FECHADA | **TRACADA** (vejo a borda) · **PARCIAL** (vejo parte, imaginei o resto) · **IMAGINADA** (não vejo, imaginei) · **FECHADA** (sem parte aberta, sem traço) |
| motivo na nota | obrigatório em PARCIAL, NAO_TRACAVEL e PELO | obrigatório em PARCIAL e IMAGINADA |

O resto não muda: as mesmas fotos, **a mesma ordem** (o `_ORDEM` da v2 é byte
a byte igual ao da v1), a mesma cegueira, a mesma declaração inicial e o mesmo
registro de hora por foto.

## Os arquivos

| arquivo | SHA-256 |
|---|---|
| `tpl_tracador_camundongo_v2.html` | `251ae4b56094236bf877b1cfd54681e52af5d4c504abb317ee8f0301a58078fb` |
| `monta_tracador_camundongo_v2.py` | `0ceedccc9c1dfe3b5c1f07a7765b36eea5b2a77119af824704d4a1fc2554575c` |
| `tracador_camundongo_v2_emilio.html` (o painel que ele usa) | `008f863d4621738764093d5edbe5180a4afbccbe400bc2af5a847bc04cf85abe` |
| `_ORDEM_v2_emilio.json` (fica com o Fabio) | `e44ee2e7704ce4f418c483ec1404689e399ef2368bcdfdddc2bdfc47e0bc68be` |

## O que fica declarado

- A mudança foi feita **depois** de o Fabio ver as rodadas 3 e 4, e **antes**
  de existir qualquer traçado do Emílio.
- A P12.1 e a P12.3 (Adendo 36) são avaliadas **só nas fotos que o Emílio
  marcou como TRACADA**, porque o Dice contra uma borda imaginada não mede
  acerto. A análise com todas as fotos sai ao lado, **separada**, para a
  comparação com o trabalho original.

---

*Opus, 04/10/2026. Nenhum traçado do Emílio existe até esta linha.*
