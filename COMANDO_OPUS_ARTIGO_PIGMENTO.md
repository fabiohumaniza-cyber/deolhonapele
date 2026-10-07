# COMANDO PARA O OPUS — Escrever o artigo da Ferramenta de Pigmento v1.2
*(do Fabio, preparado pelo Fable, 07/10/2026 ~18h20. O Fable só audita no final, para economizar créditos.)*

Opus, escreve o manuscrito completo, em inglês, no padrão dos nossos anteriores (WRR/camundongo). Entrega em `C:\projeto de olho na pele\12_ARTIGO_PINTAS\MANUSCRITO_PIGMENTO_v1_<data>.md` e grava cópia no Projeto como `claude/MANUSCRITO_PIGMENTO_v1_<data>.md`.

## Título (fechado pelo Fabio)
"The border is in the image: a clinician-written, training-free rule delineates pigmented skin lesions in a pre-registered blind test of 1,000 dermoscopic images"
Primeira linha da introdução (obrigatória): a regra-mãe foi ditada em voz alta por um enfermeiro em uma única frase e implementada literalmente, com hora registrada.

## Fontes (tudo já existe — não recalcular nada, só citar)
- Projeto: `claude/CONGELAMENTO_PIGMENTO_V12_07OUT.md` (regras, hashes, previsões), `claude/RESULTADO_TESTE_CEGO_PIGMENTO_V12_07OUT.md`, `claude/ADENDO_METRICA_DESAFIO_E_IC_PIGMENTO_07OUT.md` (Jaccard limiarizado + bootstrap + hash do jsonl), `claude/RESULTADO_V11_ISIC2018_07OUT.md` (o "antes"), `claude/DECLARACAO_ESCOPO_E_LIMITES_07OUT.md`.
- PC: `05_BASE_CIENTIFICA_E_LEGAL\ISIC2018_Task1\` (CONGELAMENTO, teste_cego\, bancada_pigmento\, minuta da adição em 09_PATENTE para conferir o que NÃO pode vazar).

## Estrutura e pontos obrigatórios
1. **Introdução**: linha da frase ditada; linhagem (porco → camundongo → rede×regra → pele); lacuna: segmentação sem treino, auditável, com recusa declarada, para triagem no SUS.
2. **Métodos**: cadeia de pré-registro com horários do dia 07/10 (regra ditada 16h31→16h35; congelada 16h45 com hashes e previsões; teste único 17h06); ISIC 2018 Task 1 CC-0 (Codella 2018; Tschandl 2018); Validation=desenvolvimento, Training=v1.1 "antes", Test=cego; comparadores fixados (2 círculos + Otsu 1979); métricas: Dice mediano global (recusa=0, principal), aceitas, Jaccard limiarizado do desafio, IC bootstrap ferramenta−Otsu. As regras aparecem DESCRITAS EM EFEITO (o que a ferramenta faz), SEM o texto literal RP1–RP5 nem parâmetros — confidenciais até orientação do agente de PI; declarar "rule text and code available after patent publication / on reasonable request".
3. **Resultados**: tabela principal (0,882 × 0,661 × 0,598 × 0,695; aceitas 0,910; recusa 15,1% com causas; vitórias par a par; IC bootstrap; Jaccard limiarizado com a comparação honesta ao ~0,80 das redes vencedoras — nós não ganhamos das redes e o texto diz isso com todas as letras); o "antes": v1.1 de ferida 0,36 nas 2.584, perdendo do círculo, com a tabela por caminho (L3=0,00) explicando o porquê; previsões pré-registradas × observado (0,88→0,882).
4. **Discussão**: recusa declarada como conduta clínica (as 151 têm causa escrita); limitações com nome: lesão bitonal subsegmentada, lesão clara recusada, vinheta, não é diagnóstico nem classificação; comparação com a literatura pré-rede (citar revisões de Celebi et al. sobre border detection — a receita tem parentes; o ineditismo é a cadeia auditável); generalização entre clínicas do test set.
5. **Declarações**: dados CC-0; sem financiamento; autor único Fabio (ORCID 0009-0009-0997-3275) + agradecimentos a definir por ele; patente: pedido principal BR 10 2026 024571-2 e certificados de adição depositados (citar sem revelar conteúdo).

## Travas
- NADA do texto literal das regras, parâmetros numéricos ou código no manuscrito.
- Nenhuma palavra: diagnosis, classification, cancer detection, replace (verbo sobre médicos/redes).
- Revista-alvo: seguir `claude/ESTRATEGIA_REVISTAS_07OUT.md` (sem APC ou APC baixo); sugerir 3 opções com justificativa de 1 linha cada.
- Dúvidas que travariam → lista no fim, não param o texto.
- Ao terminar: avisar que está pronto para a auditoria do Fable (ele confere números contra os registros e o vazamento de regras).
