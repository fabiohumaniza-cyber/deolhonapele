# COMANDO PARA O OPUS — Redigir o Certificado de Adição nº 2: triagem de câncer de pele

> **SUSPENSO em 07/10/2026 14h (decisão do Fabio):** NÃO depositar agora. As reivindicações 1 do pedido principal e da adição v1.1 falam em "estrutura cutânea" sem limitar a ferida — o uso em pinta/carcinoma/melanoma já está coberto com a data existente. O depósito do braço de câncer virá depois do Dice no ISIC, com ABCDE implementado e testado. Não executar este comando até lá.
*(do Fabio, preparado pelo Fable, 07/10/2026, 13h50. Cole este comando numa sessão do Opus.)*

Opus, redige o **relatório descritivo, as reivindicações e o resumo** de um **segundo Certificado de Adição** (art. 76 da LPI), vinculado ao pedido principal **BR 10 2026 024571 2**, cobrindo a **aplicação do método a lesões cutâneas suspeitas de câncer** (carcinoma basocelular, carcinoma espinocelular e melanoma) com **triagem por aceitação/recusa declarada**. Mesma disciplina do certificado da v1.1 depositado hoje de manhã (BR 13 2026 025394-3) — reaproveite o formato.

## Por que agora
Prioridade de depósito: a varredura em banco humano já demonstrou o efeito e nada disso foi publicado ainda. Depositar ANTES de qualquer artigo, preprint ou divulgação do braço do câncer.

## O que esta adição protege (núcleo)
1. **Uso do mesmo motor de regras pré-registradas (v1.1, SHA-256 6399ab42…) para localizar e delimitar lesões cutâneas não traumáticas** — pigmentadas, ulceradas ou queratósicas — em fotografia clínica de celular, sem marcação manual.
2. **Triagem por recusa declarada**: a lesão que cumpre as condições das regras é delimitada; a que não cumpre é recusada com causa textual — e a taxa diferencial de aceitação por tipo de lesão é usada como sinal de triagem (lesões que "parecem ferida" — os carcinomas e o melanoma — são as mais aceitas).
3. **Modalidades ABCDE** (descrever como modalidades/desenvolvimentos; ver trava abaixo): sobre o contorno delimitado, medir assimetria (comparação das metades), irregularidade de borda (razão perímetro²/área, maior trecho reto), variação de cor dentro do contorno (número de modos em Lab) e diâmetro com referência de escala declarada.

## Insumos
- `C:\projeto de olho na pele\09_PATENTE\` — minuta da adição v1.1 de hoje (usar como molde de formato e de linguagem).
- Motor congelado: `C:\projeto de olho na pele\06_MOTOR_DE_REGISTRO\v1_1_congelado\motor_v1_1_CONGELADO_05OUT.py` (SHA-256 `6399ab42…`) — fonte da verdade.
- **Exemplo de realização (dados de hoje, não publicados)**: varredura PAD-UFES-20 (banco humano público, diagnóstico por biópsia, Pacheco et al. 2020, CC BY 4.0), 1.770 fotos com o motor intocado: aceitação BCC 98,2%, SCC 97,4%, MEL 96,2%, contra NEV (pinta benigna) 89,5% — gradiente de aceitação alinhado à malignidade ulcerada. Arquivos em `C:\projeto de olho na pele\05_BASE_CIENTIFICA_E_LEGAL\PAD-UFES-20\varredura_v11\` (varredura_parcial_1770.jsonl; a completa de 2.298 chega hoje). Quando a varredura completa chegar, atualizar os números pelo RELATORIO.
- Projeto: `claude/PLANO_PINTAS_RASCUNHO_07OUT.md` (braço ABCDE) e `claude/DECLARACAO_ESCOPO_E_LIMITES_07OUT.md`.

## A REGRA DE OURO — com uma decisão explícita do Fabio
O código congelado executa a delimitação e a recusa (itens 1 e 2): essas reivindicações seguem a regra de sempre — nada além do que o código faz; os números do PAD entram como exemplo de realização.
O ABCDE (item 3) **ainda não está implementado**. Não reivindicar como executado: redigir como **reivindicações dependentes de modalidade projetada / desenvolvimento** com descrição suficiente para executar (fórmulas explícitas), e marcar no texto interno que são projetadas. Se você, Opus, julgar que isso fragiliza o pedido, apresente as duas versões (com e sem ABCDE) e o Fabio escolhe antes do protocolo.

## Vocabulário que importa
Usar sempre **"lesão cutânea"** (gênero), nunca só "ferida" — e citar ferida, lesão pigmentada, lesão neoplásica e queratose como espécies. É isso que faz uma peça só alcançar os dois braços.

## Formato e travas (iguais ao de hoje)
- Relatório com parágrafos [001]…; reivindicações "caracterizado por compreender"; resumo ≤ 200 palavras; PDFs pesquisáveis separados.
- Título: sugerir 2–3 opções; o Fabio decide.
- Nada vai a público antes do protocolo; dúvidas jurídicas viram lista de "perguntas ao agente", não travam a minuta.
- GRU: gerar nova GRU de certificado de adição (mesmo código de serviço da de hoje, R$130 pessoa física); o Fabio paga na hora do protocolo.

## Entrega
Minuta em `09_PATENTE\MINUTA_ADICAO_CANCER_<data>.md` + PDFs quando aprovada. O Fable audita contra o código congelado antes do Pix e do protocolo.
