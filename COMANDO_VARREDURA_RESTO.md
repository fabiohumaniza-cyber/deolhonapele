# COMANDO — terminar a varredura PAD-UFES-20 com a v1.1 congelada (07/10/2026)

Você é uma sessão de execução. Tarefa mecânica, sem decisões de projeto. Respostas curtas.

## Situação
A v1.1 congelada (motor.py, SHA-256 `6399ab42ac5d40ea39e938d7e6587363a6f7aa0988f646e9158c8631b448672b`) já varreu 1.770 das 2.298 fotos do PAD-UFES-20. **Faltam 528 fotos**, todas em `imgs_part_3`, listadas em `restantes.json`.

Tudo o que você precisa está em:
`C:\projeto de olho na pele\05_BASE_CIENTIFICA_E_LEGAL\PAD-UFES-20\varredura_v11\`
- `motor.py` — v1.1 congelada. NÃO EDITAR. O script confere o hash e para se não bater.
- `roda_resto.py` — processa as fotos staged, grava `varredura_resto.jsonl` (append) + miniaturas em `annot/`, apaga o staged.
- `restantes.json` — 528 caminhos Windows das fotos pendentes.
- `varredura_parcial_1770.jsonl` — o que já foi feito (não tocar).
- `agrega.py` — relatório final por tipo de lesão.
- `metadata.csv` — copiar da pasta mãe (`..\metadata.csv`) para dentro de `varredura_v11\` se não estiver lá.

## Passos
1. Stage a pasta `varredura_v11` inteira (menos os zips `annot_parte*.zip`, que não são necessários) para o container. Instale se faltar: `pip install opencv-python-headless numpy --break-system-packages`.
2. Leia `restantes.json`. Em rodadas de ~200 fotos: 4 chamadas paralelas de `device_stage_files` com ~50 caminhos cada (limite de ~50 por chamada), depois rode `python3 roda_resto.py` (ajuste o bloco CONFIG na primeira rodada: RAIZ = pasta de uploads onde as fotos caem, SAI = pasta varredura_v11 staged). Cada rodada leva ~45–70 s. São ~3 rodadas (200+200+128).
3. Ao final, confira: `varredura_resto.jsonl` deve ter 528 linhas. Se faltar alguma (compare com restantes.json), stage e rode de novo só as que faltam.
4. Copie `metadata.csv` para a pasta e rode `python3 agrega.py`. Ele imprime o relatório por tipo (BCC/ACK/NEV/SEK/SCC/MEL): taxa de recusa, área mediana, compacidade.
5. Grave de volta no PC, dentro de `varredura_v11\`: `varredura_resto.jsonl`, `varredura_completa.json`, um zip `annot_resto.zip` com as novas miniaturas, e um `RELATORIO_VARREDURA_COMPLETA.md` curto com a tabela do agrega.py e as causas de recusa.
6. Grave o mesmo relatório no Projeto como `claude/RELATORIO_VARREDURA_PAD_COMPLETA_<data>.md`.

## Referência parcial (1.770 fotos, para conferir se o resto seguiu o padrão)
| tipo | fotos | recusa | area_med | compac_med |
|------|------:|-------:|---------:|-----------:|
| BCC  | 845 | 1,8% | 0,0184 | 0,398 |
| SCC  | 192 | 2,6% | 0,0158 | 0,406 |
| MEL  |  52 | 3,8% | 0,0123 | 0,409 |
| ACK  | 442 | 5,4% | 0,0079 | 0,345 |
| SEK  |  96 | 7,3% | 0,0076 | 0,360 |
| NEV  | 143 | 10,5% | 0,0203 | 0,449 |

Regras: não editar o motor; não refazer as 1.770; qualquer erro que não se resolva em 2 tentativas, parar e relatar.
