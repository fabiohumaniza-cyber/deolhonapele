# EMENDA 1 · pré-registro do camundongo — nominais do README
**30/09/2026, 05h05 (Brasília). Anterior à abertura de qualquer imagem do banco. Pré-registro: `PRE_REGISTRO_CAMUNDONGO_30SET.md`, SHA-256 `d0989cf7a2ff8ad1185744f4afca4b3c3071119401f844b7cd52281ac9dac9a8`. Fonte desta emenda: `README_MouseWound_20220320.txt` (Yang, 2022-03-20), SHA-256 `1c41430786690cfea4e7246b3c9d1cf5eb0e3a23bab8a749ed678d2db22f542f`, baixado pelo Fabio do Dryad em 30/09 ~04h50 — só o README; o pacote de imagens (4,48 GB) permanece não baixado.**

## Nominais lidos do README (JID 2021, doi:10.1016/j.jid.2020.10.022)
- Ferida: punch excisional de **6 mm**, espessura total, com splint, dorso raspado.
- Splint de silicone: **10 mm interno / 16 mm externo**, 1,6 mm de espessura, colado à pele.
- Sobre o splint: **coverslip plástico circular de 16 mm** + curativo transparente Tegaderm selando tudo.
- Câmera: celular a **12 cm fixos**, diária, dias 0–15.
- Animais: 8 (4 idosos A8-1/3/4/5, 22–24 meses; 4 jovens Y8-1/2/3/4, 12–14 semanas), 2 feridas cada (L/R) = **16 feridas**.
- **n real = 255**, não 256: falta Day 9 da Y8-2-R (declarado no README). "As 256" do pré-registro lê-se "todas as disponíveis".
- O banco traz **dois conjuntos**: TIFFs brutos por ferida-dia e PNGs recortados por um **YOLOv3 treinado** (PLOS Comp Biol 2022). Licença: sem restrição.

## Decisões fixadas por esta emenda (regras, antes de ver)
1. **Conjunto primário = os 255 TIFFs brutos.** Os PNGs recortados por YOLO ficam fora da rodada primária: recorte por rede treinada não entra numa cadeia que se declara sem treinamento. Podem entrar depois como sensibilidade, rotulada.
2. **Escala e centro, por foto, do mesmo ajuste**: círculo/elipse ajustado ao **anel de 16 mm** (borda externa do splint; o coverslip tem o mesmo nominal de 16 mm, então a ambiguidade splint×coverslip não afeta a escala — declarado). px/mm = diâmetro ajustado em px ÷ 16.
3. **Recorte de 24 mm** (1,5× o anel) centrado no centro do ajuste, reamostrado a **1380 px** — o motor congelado roda intocado, como no porco; a identidade algébrica da escala é a mesma da reauditoria d3.
4. **Diâmetro declarado = 6 mm** (nominal do punch). Nulo geométrico = círculo de 6 mm no centro do anel.
5. **Modos de falha previstos** (soma-se ao P4 do pré-registro): reflexo especular do Tegaderm/coverslip; a borda interna do splint (10 mm) como anel concorrente do candidato — o modo "dois anéis" da §3.7 do artigo, agora previsto *antes*; pelo escuro na moldura.
6. **Idade (A×Y) e lado (L×R)**: estratos descritivos pré-declarados; nenhum teste confirmatório entre estratos nesta rodada.
7. P2 (Spearman dia × área mediana ≤ −0,8) calculado sobre os dias 0–15 com n ≥ 8 feridas medidas no dia.

## O que continua valendo do pré-registro
Tudo: uma rodada, nenhuma exclusão por resultado, nenhuma constante do v0 tocada, P1–P4 como escritos, download das imagens só após o DOI do preprint, executor Opus.
