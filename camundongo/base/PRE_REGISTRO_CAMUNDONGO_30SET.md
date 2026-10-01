# PRÉ-REGISTRO · motor v0 congelado no banco público de camundongo (UC Davis)

**Escrito em 30/09/2026, 04h55 (Brasília), por Fable a pedido do Fabio ("sim", 04h47). Hash deste arquivo a ser gravado antes de qualquer download do banco. Nenhuma imagem do banco foi vista por nenhum membro da equipe até a gravação deste hash.**

## Banco
Dryad doi:10.25338/B84W8Q — "Photographs of 15-day wound closure progress in C57BL/6J mice", Yang, Bagood, Carrión, Isseroff (UC Davis), publicado 2022. 256 imagens, 15 dias, anel de contenção (splint) presente na maioria das imagens como referência de tamanho. **Fonte de tudo que se sabe até aqui: a página de metadados do Dryad, somente.** O README (24,61 KB) será lido antes de rodar e depois deste hash; os fatos de protocolo extraídos dele (diâmetro nominal do punch e do anel, dias exatos, n por dia) serão registrados em **emenda datada, anterior à abertura de qualquer imagem**.

## Pergunta
O motor v0, congelado como está (`v0_congelado_2026-09-22`, regras da §2.3 do manuscrito, sem nenhum parâmetro novo — não há fator a escolher), produz medida e curva de fechamento numa **segunda espécie**, em banco que não participou de nenhuma decisão de desenho?

Isto é teste de transferência/replicação, não demonstração: resultado ruim publica igual.

## Regras fixadas antes
1. **As 256 imagens, sem exceção.** Nenhuma exclusão por resultado. Imagem sem anel visível: rodada e reportada em estrato próprio ("sem escala própria").
2. **Escala por imagem**: diâmetro externo do anel de contenção medido em px (maior eixo do ajuste elíptico, para tolerar inclinação) ÷ diâmetro nominal do anel lido do README/artigo-fonte. Se o nominal não constar em documento anterior à rodada, a saída fica **em px²** e assim se reporta — não se estima escala olhando resultado.
3. **Diâmetro declarado** (termo de tamanho): o nominal do punch lido do README/artigo-fonte, um valor único para o banco inteiro, registrado na emenda. Se não constar: rodada **sem o termo de tamanho**, declarado.
4. **Comparador nulo geométrico**, pareado, mesma estatística: círculo do diâmetro declarado no **centro do anel de contenção** — o nulo que o próprio desenho do banco fornece. Sem traçado de referência neste banco, o nulo é o comparador primário de contorno; concordância com traçado humano fica fora deste pré-registro.
5. **Uma rodada.** Sem reprocessamento, sem ajuste, sem segunda tentativa por imagem.

## Predições (escritas antes de ver qualquer imagem)
- **P1** · Medida obtida (anel fechado) em **≥ 50 %** das imagens com anel visível. (Barra baixa de propósito: pelo escuro do C57, o próprio anel de silicone e o quadro pequeno são condições que o v0 nunca viu; abaixo de 50 % a transferência falhou e assim se escreve.)
- **P2** · Entre as medidas obtidas, a **área mediana por dia decresce** ao longo da janela: Spearman(dia, área mediana) **≤ −0,8**.
- **P3** · Modos de falha **discrimináveis**, não só nomeáveis (lição do P4 de 29/09): revisor cego aos números recebe pares (uma imagem com medida obtida plausível, uma com falha), mesmos dias, ordem sorteada, e aponta **qual das duas** falhou, com a causa. Acerto ≥ 75 % dos pares. Pedimos discriminação porque nomeação um humano sempre entrega.
- **P4** · O modo de falha previsto dominante: **referência de pele contaminada pelo anel de silicone ou pelo pelo escuro na moldura de 8 %** — previsto aqui, antes de qualquer imagem, como assinatura esperada; se a falha dominante for outra, registra-se a surpresa.

## O que não se faz
- Excluir imagem por resultado. Trocar canal, faixa, patamar ou qualquer constante do v0. Criar "v0 adaptado ao camundongo" nesta rodada (isso é motor v2, outro pré-registro). Abrir dias 7/16/19 do porco. Tocar no CWDB. Traçar referência depois de ver saídas e chamá-la de cega.

## Execução
Executor: Opus, no PC do Fabio. **Download do banco somente após o DOI do preprint estar público** (o preprint citará este hash como anterior ao DOI). Ordem: gravar hash deste arquivo → baixar → ler README → emenda datada com os nominais → rodar → `saida\camundongo_v0.json` (por imagem: arquivo, SHA-256, px/mm ou px², área, nota, canal, obtida/não, diâmetro do anel em px) → `CAMUNDONGO_V0_RELATORIO.md` com P1–P4 marcadas confirmada/falhou e a tabela por dia. IC bootstrap 10 000, semente 20260928.

## Papel no programa
Segunda espécie, mesmo grupo de origem do banco suíno. Não substitui validação humana: o par humano deste desenho não existe público (busca de 30/09), e o caminho humano é protocolo de captura + coleta com CEP (artigo 2). Este teste responde uma pergunta anterior: a regra escrita para uma espécie carrega para outra sem retoque — e, onde não carrega, diz por quê?
