# ADENDO 56 · resultado da Helga: P15 confirmada

**04/10/2026, Brasília, 15h05.** Traçado lacrado no Adendo 55 (`bcb051a`).
Rodou o `analisa_emilio.py` (`8c5f9233…`) **sem nenhuma mudança no código**.

- Os rótulos "Emilio" no relatório estão fixos no código e, aqui, se referem
  à Helga.
- Para não sobrescrever os arquivos do Emílio, a saída foi renomeada para
  `dados/HELGA_RELATORIO.md` (`aa229627…`) e `dados/helga_por_imagem.tsv`
  (`a1977bee…`).
- Publicados também: `dados/tracado_camundongo_v2_Helga_2026-10-04.json`
  (`9616bb21…`) e `dados/_ORDEM_v2_Helga.json` (`48dbca77…`).

## Integridade

- Painel v2.
- Declaração inicial marcada às 16h32:07 UTC (13h32 em Brasília).
- 201 de 201 fotos fechadas, com o SHA de cada foto conferido.
- Tempo total de 82,7 min; mediana de 21 s por foto.

## P15 (Adendo 42), a previsão do Fabio: "vai dar igual do emilio o da helga"

| | critério | Helga | Emílio | veredito |
|---|---|---|---|---|
| **P15.1** | mediana Dice(r4, Helga) entre 0,849 e 0,949 · braço principal e TRACADA | **0,906** (n = 44) | 0,899 (n = 48) | **confirmada** |
| **P15.2** | fração com Dice ≥ 0,70 entre 80 % e 100 % | **86 %** | 90 % | **confirmada** |

A P12.1 e a P12.3 também se confirmam contra a Helga.

## Ao lado, sem veredito

| conjunto | n | r4 | r3 | nulo |
|---|---|---|---|---|
| principal + TRACADA | 44 | 0,906 | 0,887 | 0,651 |
| todas as traçadas, incluindo imaginadas | 194 | 0,834 | 0,807 | 0,692 |
| só as IMAGINADAS | 47 | 0,750 | 0,667 | 0,568 |

Estados da Helga: TRACADA 67 · PARCIAL 80 · IMAGINADA 47 · FECHADA 7.

## Helga × Emílio (Adendo 55, descritivo)

| | |
|---|---|
| kappa de traçabilidade (TRACADA ou não) | **0,691** |
| ambos marcaram TRACADA | 55 fotos |
| Dice entre os dois traçados, nas 55 TRACADA dos dois | **0,976** |
| Dice entre os dois, nas fotos em que ao menos um não marcou TRACADA | 0,947 (n = 138) |

Estado do Emílio (linhas) × estado da Helga (colunas):

| | TRACADA | PARCIAL | IMAGINADA | FECHADA |
|---|---|---|---|---|
| TRACADA | 55 | 16 | 0 | 0 |
| PARCIAL | 12 | 51 | 20 | 1 |
| IMAGINADA | 0 | 12 | 27 | 6 |
| FECHADA | 0 | 1 | 0 | 0 |

**Nenhuma foto que um dos dois marcou TRACADA o outro marcou IMAGINADA.**

Kappa entre a Helga e o Fabio: **0,361**. Entre o Emílio e o Fabio: 0,407.

## O que isto quer dizer

1. Dois leitores leigos, cegos e independentes concordam entre si (Dice 0,976)
   bem mais do que qualquer um deles concorda com o motor (0,906).
2. **O motor fica perto da concordância humana, mas abaixo dela.**
3. As fotos que os dois julgaram traçáveis quase coincidem. O que um chama de
   impossível o outro nunca chama de fácil.

## P19 e P20

Saem quando as 4 dobras da rede terminarem.

---

*Opus, 04/10/2026. Placar copiado da saída do script.*
