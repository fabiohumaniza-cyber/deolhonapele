# Levantamento de literatura: avaliabilidade da borda em imagens de ferida (2015–2026)

Data: 04/10/2026. Busca: WebSearch (standard; uma extended) + WebFetch em resumos/textos completos. PubMed/PMC estavam bloqueados por reCAPTCHA na maior parte das tentativas; usei a página da editora, DOAJ, arXiv/bioRxiv ou repositórios institucionais.

**Regra de codificação (coluna "evaluability"):**
- **sim** = informa contagem/proporção de imagens não avaliáveis, excluídas ou de qualidade insuficiente, imagem a imagem.
- **parcial** = informa critérios de exclusão no nível da imagem sem contagem, OU exclusão no nível da ferida/paciente/animal, OU uma redução de contagem sem motivo declarado.
- **não** = não encontrei nenhuma informação desse tipo no material lido. Quando só li o resumo, "não" quer dizer "não consta no resumo".
- **não verificado** = não consegui ler resumo/métodos suficientes para codificar.

## Tabela principal (estudos primários, n = 35)

| # | first author, year | journal | DOI or PMID (verified) | wound type / species | n images | reference standard | evaluability? | what exactly they report (≤25 words; quotes <15 words) | verified |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Carrión, 2022 | PLoS Comput Biol 18(3) | 10.1371/journal.pcbi.1009852 | Camundongo C57BL/6J, ferida excisional com splint (Dryad 10.25338/B84W8Q) | ~256 | Anotação manual no Labelme feita por um único não especialista | parcial | Diz que mais de 25% das imagens não tinham splint ou tinham "substantial damage"; cita oclusão, pelo, foco. Não conta bordas não avaliáveis | resumo (PLoS) + texto completo (preprint no bioRxiv) |
| 2 | Wang C, 2020 | Sci Rep | 10.1038/s41598-020-78799-w | Úlcera de pé diabético (AZH) | 1.109 | Máscaras manuais revisadas por especialistas em feridas | não | Iluminação "uncontrolled"; sem exclusão de imagens relatada | texto completo |
| 3 | Wang C, 2024 (FUSeg; desafio MICCAI 2021) | Information 15(3):140 | 10.3390/info15030140 | Úlcera de pé diabético | 1.210 | Anotadores não especialistas (Photoshop), revisão por 2 médicos com >20 anos de experiência e decisão em reunião | não | Sem critério de exclusão/qualidade; divisão aleatória 1.010/200 | texto completo |
| 4 | Kendrick, 2022 (conjunto DFUC2022) | arXiv 2204.11618 (status de revisão por pares não verificado) | não verificado | Úlcera de pé diabético | 4.000 (2.000 treino + 2.000 teste) | Polígonos de podólogos no VGG, refinados por contorno ativo | não | Inclui de propósito "non-DFU cases" e casos com divergência entre anotadores; não relata exclusões | texto completo |
| 5 | Yap, 2024 (relatório do DFUC2022) | Med Image Anal 94:103153 | 10.1016/j.media.2024.103153 | Úlcera de pé diabético | 2.000 treino + 2.000 teste | Máscaras de referência do desafio | não | Resumo sem menção a qualidade ou exclusão | resumo |
| 6 | Goyal, 2017 | IEEE SMC 2017 (arXiv 1708.01928) | não verificado | Úlcera de pé diabético | 705 (600 com úlcera + 105 pés saudáveis) | Podólogo delineia, consultor em diabetes valida | não | Só descreve a padronização da captura (30–40 cm, sem flash); sem exclusões | texto completo |
| 7 | Pereira TA, 2022 (ComplexWoundDB) | IWSSIP 2022 (arXiv 2209.12822) | não verificado | Feridas complexas mistas (pressão, vascular, diabetes, queimadura, cirúrgica) | 27 | 4 especialistas (3 enfermeiros, 1 médico), classificação por pixel | não | Imagens domiciliares "in the wild"; sem critério de exclusão | texto completo |
| 8 | Oota, 2023 (WSNet / WoundSeg) | WACV 2023 | não verificado | Feridas mistas | 2.686 de 3.000 | 3 especialistas em feridas, concordância intra-anotador de ~0,95 | parcial | "two sanity checks" reduziram de 3.000 para 2.686; motivo não declarado | texto completo |
| 9 | Scebba, 2022 | Inform Med Unlocked | 10.1016/j.imu.2022.100884 | Pé diabético, úlcera digital de esclerose sistêmica, Medetec, SIH, FUSC | ~1.330 para segmentação (+2.000 DFUC para o detector) | Máscaras binárias de assistentes de pesquisa treinados e especialistas | parcial | Imagens de esclerose sistêmica com ferida <0,1% da imagem foram excluídas; sem outras exclusões por qualidade | texto completo (arXiv 2111.01590) |
| 10 | Zhang J, 2021 | JMIR mHealth uHealth 9(7) | 10.2196/26149 | Úlcera digital de esclerose sistêmica, fotografada pelo próprio paciente em casa | 382 (199 + 183) | Métricas objetivas de qualidade (detecção da carta de cor; nitidez) | **sim** | Carta de cor detectada em "0.96 (191/199)" com feedback e "0.86 (158/183)" sem | resumo |
| 11 | Gunter, 2016 | JMIR mHealth uHealth 4(3):e113 | 10.2196/mhealth.6023 | Ferida pós-operatória, foto feita pelo paciente | 9 pacientes (n de imagens não está no resumo) | Julgamento clínico de suficiência diagnóstica | **sim** | "81.8% of images were sufficient for diagnostic purposes"; não mede área | resumo |
| 12 | Liu TJ, 2023 | Sci Rep | 10.1038/s41598-022-26812-9 | Lesão por pressão | 528 | Margens anotadas por 3 cirurgiões plásticos certificados | não | Resumo sem exclusões; ERM de 26,2% contra o método manual | resumo |
| 13 | Chang CW, 2022 | PLoS One 17(2) | 10.1371/journal.pone.0264139 | Lesão por pressão | >5.700 rotuladas | Rotulagem por especialistas assistida por superpixel | não | Resumo sem exclusões | resumo |
| 14 | Chang C, 2021 | JMIR Med Inform | 10.2196/22798 | Queimadura (%SCQ pela regra da mão) | 2.591 de queimadura + 400 de mão | "labeled by burn surgeons" | não | Resumo sem exclusões | resumo |
| 15 | Chang CW, 2025 | Front Artif Intell | 10.3389/frai.2025.1510905 | Queimadura aguda (2D vs LiDAR 3D) | 11.514 (10.088 treino; 1.426 validação) | Rótulos revisados; template de cera de cicatriz de ~43 cm² | parcial | Exclui imagens com pomada/curativo; descarta imagens com divergência de rótulo, por "poor lighting or slight out-of-focus". Sem contagem | texto completo |
| 16 | Zahia, 2020 | Sensors 20(10):2933 | 10.3390/s20102933 | Lesão por pressão (2D + malha 3D) | 210 fotos | Segmentação manual validada por 2 médicos | parcial | 6 de 21 malhas 3D excluídas (calcanhar/quadril, osso deformando o leito); nada sobre fotos | texto completo |
| 17 | Kręcichwost, 2021 (WoundsDB) | Comput Med Imaging Graph 88:101844 | 10.1016/j.compmedimag.2020.101844 | Feridas crônicas, multimodal (foto, térmica, estéreo, profundidade) | 188 conjuntos (79 visitas) | Contornos de especialistas | não verificado | Li só a página do banco; não li o artigo | página do banco |
| 18 | Sanchez, 2024 (CO2Wounds-V2) | IEEE ICIP 2024 (arXiv 2408.10827) | não verificado | Feridas crônicas de hanseníase (Colômbia) | 764 (607 com contorno) | Contorno manual no CVAT | parcial | Removeu duplicatas, imagens sem ferida e imagens borradas "where the edges of the ulcer are difficult to detect". Sem contagem | texto completo |
| 19 | Hsu JT, 2019 | BMC Med Inform Decis Mak | 10.1186/s12911-019-0813-0 | Feridas cirúrgicas (vários sítios) | 293 | 3 médicos, voto de maioria | não | Sem exclusões por qualidade relatadas | texto completo |
| 20 | Blanco, 2019 | Comput Methods Programs Biomed | 10.1016/j.cmpb.2019.105079 | Úlcera arterial/venosa de membro inferior | 217 (40 rotuladas) | Superpixels rotulados por médicos especialistas | não | 40 imagens escolhidas para "maximizing diversity"; é seleção, não exclusão | texto completo (arXiv 1909.06264) |
| 21 | Li KC, 2025 | Medicina 61(6):1099 | 10.3390/medicina61061099 | Feridas ambulatoriais variadas | 120 (40 pacientes × 3 distâncias) | Calibração por QR code; validação com moeda | parcial | Exclui pacientes com ferida obstruída por curativo extenso ou líquido; exige ferida "flat, uncovered" | texto completo |
| 22 | Wang SC, 2017 (Swift) | PLoS One | 10.1371/journal.pone.0183139 | Pé diabético, venosa, pressão + feridas de modelo plástico | 45 feridas (+12 modelos; 15 fotos de modelo) | Planímetro digital Placom (nos modelos); régua | parcial | Só pacientes com uma ferida; régua excluída se ferida >17 cm; reconhece que feridas reais têm margens mal definidas | texto completo |
| 23 | Foltynski, 2015 | PLoS One 10(8) | 10.1371/journal.pone.0134622 | Feridas crônicas / modelos (calibração com 2 réguas) | não verificado | Áreas conhecidas (detalhe não verificado) | não | Resumo sem exclusões | resumo |
| 24 | Seat, 2017 | Wounds | não verificado | Fotos de feridas (Tissue Analytics) | 12 | Régua C×L | não | Nenhuma exclusão; cita reflexo de luz e ângulo como limitação | texto (página HMP) |
| 25 | Bigham, 2016 | Wounds 28(11):379-386 | não verificado | Feridas crônicas mistas (dispositivo 3D em iPad) | 45 feridas | Régua + planimetria no ImageJ | parcial | Excluídas de antemão: fixador externo, circunferenciais, em dobras de pele, <4 cm² | texto (página HMP) |
| 26 | Biagioni, 2021 | J Vasc Surg Cases Innov Tech 7(2):258-261 | não verificado | Feridas vasculares (app imito) | 85 | ImageJ sobre foto de câmera de 10 MP | não | Nenhuma exclusão relatada | resumo (DOAJ) |
| 27 | Aarts, 2023 | Dermatology | 10.1159/000525844 | Feridas pós-cirúrgicas de hidradenite (inSight 3D, ImitoWound) | 52 feridas | Régua e traçado | não | Resumo sem exclusões | resumo |
| 28 | Alonso, 2023 | Wounds 35(10):E330-E338 | 10.25270/wnds/23031 | Feridas ambulatoriais (sistema digital Swift) | 177 feridas | Régua de papel vs sistema digital | não | Resumo sem exclusões | resumo |
| 29 | Kanogsunthornrat, 2018 | Nurs Res Innov J 24(2):150-162 | não verificado | Feridas abertas (Photoshop, ImageJ) | 45 feridas | Visitrak | não | Resumo sem exclusões | resumo |
| 30 | Mikhailov, 2025 | Sci Innov Med 10(2):161-168 | 10.35693/SIM643331 | Modelos 2D/3D, feridas de animais de laboratório, defeitos faciais (3 apps) | 190 feridas reais; 4.480 medições | Malha milimetrada (método de Popova) | não | Resumo sem exclusões | resumo |
| 31 | Huang, 2023 | Lab Anim Res | 10.1186/s42826-023-00176-1 | Camundongo C57BL/6J diabético/controle, 4 feridas de 4 mm | 28 feridas, fotos diárias por 10 dias | 2 avaliadores (contorno e reepitelização) vs paquímetro vs histologia | parcial | Excluiu imagens de má qualidade "heavily covered by hair or fused together", sem contagem | texto completo |
| 32 | Marcato, 2024 | KDMiLe 2024 (SBC) | não verificado | Camundongo, ferida dorsal | 71 | Rótulo manual no Labelme | não | Nenhuma exclusão; aponta 3 imagens difíceis (ferida pequena, cor parecida com a pele) | texto completo |
| 33 | Alves, 2022 | Res Soc Dev 11(5) | 10.33448/rsd-v11i5.28187 | Rato | 160 fotos | Régua manual vs ImageTool/ImageJ/AutoCAD | não | Resumo sem exclusões | resumo |
| 34 | Fischer, 2023 | Bio-protocol | 10.21769/BioProtoc.4606 | Camundongo, ferida excisional com splint (protocolo) | não se aplica | Traçado à mão livre/polígono no ImageJ | parcial | Exclui o animal se houver "severe displacement of the splint, infection, or auto-mutilation" | texto completo |
| 35 | Brown, 2025 | BMJ Open | 10.1136/bmjopen-2024-090299 | Úlcera de pé diabético, foto 2D dentro de ECR (protocolo) | 300 planejadas | Painel central cego | parcial | Antecipa dificuldade de obter "photograph of sufficient quality" por curvatura; sem resultados | texto completo |

### Contexto (revisão; fora da contagem)
| first author, year | journal | DOI | o que interessa |
|---|---|---|---|
| Jørgensen LB, 2015 | Int Wound J | 10.1111/iwj.12472 | Revisão sistemática de 43 estudos (1994–2014). Cita um estudo que excluiu 4 feridas "because of difficulties in assessing the wound margins", e a confiabilidade melhorou |

### Encontrados mas não incluídos
- **Só achei metadados, sem resumo/métodos (não verificado):** Chino 2020, CMPB 191:105376 (10.1016/j.cmpb.2020.105376); Chan KS 2021, Int Wound J (10.1111/iwj.13603, CARES4WOUNDS); Ramachandram 2022, JMIR mHealth (10.2196/36977); Mohammed HT 2022 (Swift, confiabilidade entre avaliadores; PMC9766476 bloqueado); Swerdlow 2023 (eKare, periódico não identificado); Cavazzana 2025, Appl Sci (10.3390/app15020833; resumo sem n).
- **Fora do escopo:** Cassidy 2023, Diabetes Res Clin Pract (detecção, não borda); Kuo 2022, Sci Rep, minipig (traçado em filme transparente, não em foto); Tuca 2024, IJMS, suíno (histologia); Jørgensen 2020, J Wound Care (classificação Wagner em foto); Kabir 2025, arXiv (preprint).
- **Antes de 2015, mas relevantes como exemplo:** Wild 2013, Wounds (3 de 18 imagens excluídas por calibrador desalinhado: o único caso de contagem de exclusão por imagem que achei); Chang AC 2011, ePlasty (suíno, Visitrak vs foto); Comfort 2011, Wounds; Gardner 2012, Wounds; Van Poucke 2010, Int Wound J; Dini 2008, Wounds.

## Contagens

- **Estudos primários incluídos:** 35. Por tipo: 29 com feridas humanas (Wang SC 2017 também usa modelos plásticos), 5 em roedores (camundongo 4, rato 1) e 1 misto (Mikhailov 2025: modelos + animais + humanos).
- **Avaliabilidade:**
  - **sim:** 2 de 35 (5,7%): Zhang 2021 e Gunter 2016. Os dois medem qualidade fotográfica ou suficiência diagnóstica. Nenhum mede se a **borda** estava visível ou traçável.
  - **parcial:** 12 de 35 (34,3%). Só 1 deles (Sanchez 2024) cita explicitamente a borda ("edges of the ulcer are difficult to detect"), e sem contagem.
  - **não:** 20 de 35 (57,1%). Destes, 9 lidos no texto completo e 11 só no resumo.
  - **não verificado:** 1 de 35 (2,9%).
- **Nenhum** dos 35 estudos informa, imagem a imagem ou no agregado, quantas imagens tinham **borda visível/traçável** como desfecho declarado.
- **Padrão de referência:** quase todos usam traçado/anotação humana (especialista ou não) ou um instrumento de contato (régua, Visitrak, planímetro, malha). Só Carrión declara explicitamente um único anotador não especialista. Nenhum descreve uma regra escrita e pré-registrada para decidir se a borda é traçável.

## Resumo para a Introdução (PT)

Num levantamento de 35 estudos (2015–2026) que medem área ou segmentam a borda de feridas em fotografias, em humanos e em modelos animais, só 2 (5,7%) informaram quantas imagens tinham qualidade insuficiente, e nos dois o critério era a qualidade fotográfica ou a suficiência diagnóstica, não a visibilidade da borda. Outros 12 (34,3%) mencionaram exclusões só de forma parcial (critérios sem contagem, exclusão por ferida ou por animal, ou redução do conjunto sem motivo declarado), e os 20 restantes (57,1%) não relataram nada sobre avaliabilidade no material consultado. Nenhum estudo tratou como desfecho a proporção de imagens com borda traçável, e a referência foi quase sempre um traçado humano sem regra escrita de decisão; por isso, o denominador real das métricas de concordância e de acurácia relatadas continua desconhecido.
