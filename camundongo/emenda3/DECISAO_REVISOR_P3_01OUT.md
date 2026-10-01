# DECISÃO · quem é o revisor cego da P3

**01/10/2026, 07h30 (Brasília). Escrita ANTES de qualquer byte de imagem do banco
Dryad 10.25338/B84W8Q ser baixado ou aberto.**

Resolve a seção 4 da `EMENDA_3_CAMUNDONGO_01OUT.md`, SHA-256
`299c91818ef9db680d6b2bbdaa1e4bf5bf4eed9a7c097a63a5a8544ffeab68ce`. A Emenda 3
**não é alterada por este arquivo**; a decisão estava declarada ali como pendente
e é fechada aqui, em arquivo próprio, com hash próprio.

---

## A DECISÃO

> **O revisor cego da P3 é o próprio Fabio.** O cegamento não é **por pessoa** —
> é **por ordem de abertura**, e é ato declarado.

Isso é mais fraco que um revisor independente, e fica dito assim. O Emílio fez o
papel de observador 2 no porco; aqui não faz. O que sustenta a cegueira é a
ordem abaixo, e só ela.

---

## A ORDEM, OBRIGATÓRIA

1. **Etapa 4 roda.** O Fabio **não abre** `camundongo_v0.json`,
   `CHAVE_P3_NAO_ABRIR.json` nem `CAMUNDONGO_V0_RELATORIO.md`.
2. Abre **somente** `PAINEL_P3.txt` e as **fotos originais** dos pares.
   Preenche `resposta` e `causa` de cada par.
3. `certutil -hashfile PAINEL_P3.txt SHA256` sobre o painel **preenchido**.
   O hash vai para o log **com a hora**.
4. **Só então** abre a chave, o relatório e o JSON.

**O painel não se corrige depois.** O acerto da P3 é calculado sobre o arquivo
hasheado no passo 3, e sobre nenhum outro. Painel reaberto, reeditado ou
regravado depois do passo 4 **anula a P3** — que então sai como *não avaliável*,
com o motivo escrito, e não como falhada.

---

## O QUE O CEGAMENTO NÃO COBRE, DECLARADO

Antes de preencher o painel, o operador já viu, por força do próprio protocolo:

1. **O console da etapa 1** — quais imagens o **detector do anel** reprovou, e o
   px/mm das que passaram.
2. **A etapa 2** — ele mediu à mão o anel das pendentes, ou as declarou
   `SEM_ANEL`. Logo, sabe quais imagens têm `escala_manual`.

**Nenhuma das duas diz qual imagem o motor falhou.** Falha do detector e falha do
motor são coisas distintas: imagem com escala manual roda normalmente e costuma
produzir medida; imagem com detecção perfeita pode não produzir nenhuma. A P3
pergunta pela segunda, e dela o operador não tem notícia até o passo 4.

3. **A etapa 3 imprime só o contador** (`17/255`). Não imprime área, nota,
   px/mm, estrato nem se a medida saiu — essa última é, literalmente, a resposta
   do painel.

Fica declarado, ainda, que **uma imagem de escala manual pode aparecer no painel**
e que o operador a reconhecerá como tal. Isso não é excluído do sorteio: excluir
encolheria o painel e seria regra nova depois do pré-registro. É cue parcial,
está escrito, e quem for ler que desconte.

---

## POR QUE ISTO VALE MENOS QUE UM REVISOR INDEPENDENTE, E MESMO ASSIM VALE

Vale menos porque a pessoa que responde é a que tem interesse no resultado, e
nenhuma ordem de abertura apaga isso. Vale alguma coisa porque o que a P3 mede é
**discriminação** — apontar qual das duas falhou —, e o operador, no passo 2, não
tem como saber a resposta: ela só existe depois que o motor roda, na etapa 3, que
não a imprime.

A lição que motivou a P3 continua valendo: em 29/09, no painel do porco, um
revisor cego aos números **nomeou causa em 8 de 8 pastas**, incluindo as quatro de
controle. Nomear qualquer humano entrega. Discriminar, não. É por isso que esta
predição pede a segunda coisa, e é por isso que ela ainda significa algo com o
operador no lugar do revisor.

---

*Escrita pelo Opus em 01/10/2026, por decisão do Fabio relatada às 07h24, com a
ordem redigida pelo Fable. Nenhuma imagem do banco foi baixada, aberta ou
inspecionada até esta linha.*
