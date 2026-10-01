# NOTA · etapa 1 fechada e a ferramenta de medida manual

**01/10/2026, Brasília.** Anexa à `EMENDA_4_CAMUNDONGO_01OUT.md`
(`1f369e4d66d89096bb9b2fd5b76c94fd28a5a8d3a593d365a6a9f3c4674a8b0a`).
O motor ainda **não rodou em nenhuma imagem**.

---

## 1 · O RESULTADO DA ETAPA 1, COMO ACHADO PRÉ-REGISTRADO

O detector do anel — `detecta_anel_camundongo.py`, SHA-256 `56f1b434…`,
congelado pela Emenda 2 **antes de qualquer contato com o banco** — reprovou
**255 de 255** fotos reais.

`deteccao_camundongo.json`, mapa `87c4d45a…`, etapa 1 em 01/10/2026 13:21:53 −03.

| motivo | imagens |
|---|---|
| `achatamento;setores;residuo` | 145 |
| `setores;residuo` | 110 |
| **detecção aceita** | **0** |

**Não foi por pouco.** Os três critérios, contra os limiares congelados:

| critério | limiar | mínimo | mediana | máximo | passaram |
|---|---|---|---|---|---|
| `fracao_setores` | ≥ 0,90 | 0,250 | 0,500 | 0,806 | **0 de 255** |
| `residuo` | ≤ 0,02 | 0,029 | 0,043 | 0,059 | **0 de 255** |
| `achatamento` | ≥ 0,80 | 0,229 | 0,772 | 0,970 | 110 de 255 |

Nenhuma imagem chegou perto em setores, e nenhuma em resíduo — o menor resíduo
do banco inteiro já é 45 % acima do teto.

E o diâmetro que ele devolveu diz o resto: mediana **2.672 px**, num quadro de
3000 × 4000. A curva que ele escolheu ocupa dois terços do lado menor da foto.
Um splint de 16 mm, nessas fotos, não tem esse tamanho — então o detector não
errou a medida do anel: ele mediu **outra coisa**, uma estrutura concêntrica
muito maior. O quanto maior sai da própria etapa 2, quando o Fabio tiver medido
os 255 anéis à mão: aí a comparação é número contra número, e entra no relatório.

**A leitura, em uma frase:** a regra "entre as curvas concêntricas, fica com a de
maior eixo" resolveu o sintético, onde o splint **era** a maior; na foto real
existem coisas concêntricas maiores que o splint, e a regra escolhe errado.

**Transferência sintético → real: 16 de 16 contra 0 de 255.** Isto é resultado,
não contratempo: o código foi congelado e hasheado antes de ver o banco, falhou
no banco, e o fracasso está registrado com os números dele. É o que um
pré-registro serve para produzir.

Nada será mexido por causa disso. **Detector v2 é outro pré-registro, depois da
rodada** — e esta nota não o esboça, de propósito.

### Dois registros que vêm de brinde

- **A Emenda 4 funcionou no banco real:** `modo_pil` gravado nas 255 é
  254 `RGBA` + 1 `RGB`, exatamente o que a emenda previu, e nenhuma parou por
  alfa.
- **A ressalva da P3 caiu.** A `DECISAO_REVISOR_P3_01OUT.md` (`81e150df…`)
  declarava que uma imagem de escala manual poderia aparecer no painel e ser
  reconhecida como tal — pista parcial, declarada. Com 255 de 255 em escala
  manual, "ter escala manual" deixa de distinguir qualquer imagem de qualquer
  outra: a pista some por aritmética, não por decisão. A P3 fica mais limpa do
  que estava escrito.

---

## 2 · A FERRAMENTA, E O QUE ELA NÃO FAZ

Regra 3.2 da Emenda 3, sem escolha: medida manual do anel nas **255**, antes de o
motor rodar em qualquer uma. Precedente da escala manual da 1324·B no porco.

`mede_anel.py` — SHA-256
`42e77a0d5a973d64aa4c1d402ed5eacc63a48d5d0782bb8273f82aa87f31b388`, tkinter + PIL.

**Não detecta nada.** Não calcula borda, não ajusta elipse, não chama o detector,
não abre `deteccao_camundongo.json` e não mostra na tela nenhum número vindo
dele. Registra **onde o operador clicou** e converte para px da imagem original.

Quatro cliques na borda **externa** do splint — esquerda, direita, cima, baixo:

```
diâmetro = média das duas cordas     corda1 = |p1 p2|   corda2 = |p3 p4|
centro   = média dos quatro pontos
```

Sem ajuste de elipse, sem ponderação, sem descarte de ponto. A conta é
conferível à mão a partir do log.

Grava `nome⇥diâmetro⇥centro_x⇥centro_y`, exatamente os quatro campos que a
etapa 2 exige, ou `nome⇥SEM_ANEL`. `px/mm` sai depois, no driver, como
`diâmetro / 16 mm`.

**Teclas:** `Enter` grava · `n` SEM_ANEL · `r` refaz os quatro · `Backspace`
apaga o último clique · `q` sai.

**Dá para parar.** `MEDIDAS.txt` e `MEDIDAS_LOG.tsv` abrem em *append* e são
gravados com `fsync` a cada imagem. Fechar a janela, apertar `q` ou cair a luz
não perde o que já foi medido; ao reabrir, quem já tem linha é pulado.

**O log separado** (`MEDIDAS_LOG.tsv`) guarda, por imagem, os **quatro cliques
brutos** em px da original, o fator de redução da tela e a hora ISO. Com ele
qualquer pessoa refaz a conta sem a ferramenta, e qualquer medida esquisita tem
como ser auditada até o clique que a gerou.

### Uma coisa que eu acrescentei, e que não foi pedida

Há uma **lupa** no canto: ela mostra um pedaço da imagem original, ampliado 3×,
em volta do cursor. É auxílio de visão, como uma lente na mão do operador — **não
registra, não altera e não entra em conta nenhuma**; o que vai para o arquivo é o
clique, e o clique está no log. Fica declarado aqui porque não estava na
especificação do Fable. Se ele preferir sem, sai numa linha.

---

## 3 · ENSAIO

`teste_mede_anel.py`. Sem janela, sem tocar no banco — o `tkinter` fica dentro
de `main()`, então a aritmética e os arquivos se testam sozinhos.

**A conta dos quatro cliques**, quatro casos, todos exatos:

| caso | diâmetro | centro |
|---|---|---|
| círculo r = 350 em (1500, 2000) | 700,000 (alvo 700) | (1500,0; 2000,0) |
| elipse 350 × 300 | 650,000 (alvo 650) | (1500,0; 2000,0) |
| círculo deslocado para o canto | 580,000 (alvo 580) | (380,0; 410,0) |
| elipse girada 25° | 650,000 (alvo 650) | (1500,0; 2000,0) |

Na elipse, a média das cordas dá a média dos eixos — que é o que foi pedido, não
o eixo maior. O giro não muda nada.

**O formato é aceito pela etapa 2:** linhas escritas exatamente como a ferramenta
escreve, passadas ao `roda_camundongo.py medir` → saída 0, *"medidas manuais: 2 |
marcadas SEM_ANEL: 1 | pendências abertas: 0"*, `px_mm` gravado = 43,7500 =
700 / 16, centro `[1500.0, 2000.0]`, e a `SEM_ANEL` no estrato *sem escala
própria* com `px_mm` nulo.

**A retomada:** com as três já medidas, a fila volta vazia; com a sessão
interrompida depois da primeira, a fila volta com as duas que faltam.

---

## 4 · ORDEM DE USO

```
python mede_anel.py "D:\...\10_CAMUNDONGO\plano" "D:\...\10_CAMUNDONGO\saida"
```

Quantas sessões quiser. Quando as 255 tiverem linha:

```
python roda_camundongo.py medir "D:\...\10_CAMUNDONGO\saida" "D:\...\10_CAMUNDONGO\saida\MEDIDAS.txt"
```

A etapa 2 **para** se faltar uma linha sequer. Só depois dela a etapa 3 roda.

---

## 5 · HASHES

| arquivo | SHA-256 | bytes |
|---|---|---|
| `mede_anel.py` | `42e77a0d5a973d64aa4c1d402ed5eacc63a48d5d0782bb8273f82aa87f31b388` | 10.560 |
| `teste_mede_anel.py` | `a4ec0a4a0bd1a5f89781a1ffba289e21dce3017bba7893657fca5c0e75bc695a` | 4.890 |

Os dois colados do `sha256sum`, nunca completados de prefixo.

---

*Escrita pelo Opus em 01/10/2026. Os números da seção 1 saíram do
`deteccao_camundongo.json` do PC do Fabio, lido para esta nota. Nenhuma medida do
motor existe até esta linha.*
