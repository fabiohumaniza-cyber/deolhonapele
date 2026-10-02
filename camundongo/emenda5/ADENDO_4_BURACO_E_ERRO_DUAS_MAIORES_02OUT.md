# ADENDO 4 · a medida pelo buraco, um erro meu, e o que fica fixado

**02/10/2026, Brasília, 13h00.** O motor **não rodou em imagem nenhuma** e a
etapa 3 **não foi iniciada**. Nenhum resultado do motor existe até esta linha.

Adendo ao `ADENDO_3_ANEL_E_FAIXA_02OUT.md`
(`494878252d8ced477411a629713b2e7316c186f3c40fbba8e213ef3c5ae81392`), que **não
é alterado**.

---

## 1 · ERRO MEU, COM O TAMANHO MEDIDO

Ao longo de 02/10 eu afirmei, várias vezes e como fato, que *"a conta pega as
duas maiores distâncias, que são o eixo maior da elipse — e o eixo maior de um
círculo de 16 mm visto inclinado continua sendo 16 mm"*.

**Isso só é exato quando a projeção é um círculo.** Num anel inclinado, a
**média** das duas maiores fica **abaixo** do eixo maior: a segunda maior já é
uma corda menor. Em ensaio: num círculo o valor sai exato; a 15° de inclinação,
com os quatro pontos sobre os eixos, sai 1,7 % curto; a 30°, 6,7 %; a 45°,
14,6 %.

Isso vale para o `mede_anel.py` v6 (`d4e4e81b…`), que produziu as 92 medidas da
borda externa.

**O tamanho real, recalculado a partir dos cliques brutos do
`MEDIDAS_LOG.tsv`** — 82 imagens com os 4 pontos gravados, comparando o que foi
gravado (média das duas maiores) com a **maior** distância, que é estimador
melhor do eixo maior:

| | |
|---|---|
| mediana da subestimação | **0,90 %** |
| média | 1,02 % |
| máximo | **3,32 %** (`Day 10_A8-5-R`) |
| mínimo | 0,00 % (`Day 0_A8-1-L`) |
| efeito na área | **~1,8 %** |

É pequeno porque o operador espalha bem os cliques: quando os quatro ficam
distribuídos, as duas maiores quase coincidem e o viés desaparece.

**Nada precisa ser remedido.** O log guarda os 4 pontos brutos de cada imagem,
em px da original. Qualquer estimador melhor é calculável depois, sobre as 255,
sem abrir uma fotografia. Fica declarado que esse recálculo será feito e
reportado ao lado do valor gravado.

Este é o tipo de erro que o caderno de erros existe para conter: afirmado por
mim como propriedade do método, desmentido por ensaio, medido, e registrado
antes de o resultado existir.

## 2 · O MÉTODO DA FAIXA: TESTADO E NÃO ADOTADO

O Adendo 3 declarou a faixa de 3 mm como comparação a fazer. Ela foi medida nas
5 imagens de treino e o resultado está em `FAIXAS.txt` (4 linhas gravadas, todas
`treino=S`).

Na **mesma** imagem (`Day 0_A8-1-L`, esperado 113 px), medindo em pontos
diferentes do mesmo anel:

| onde | medido | contra o esperado |
|---|---|---|
| topo | 102,4 | −9 % |
| lado limpo | 114,5 | +1 % |
| lado com degrau | 132,5 | **+17 %** |

**A escolha do ponto move ±15 % na mesma fotografia** — mais que qualquer outra
fonte de erro do método, e muito mais que o erro de clique. Ou seja: o método da
faixa *é* a escolha do ponto.

A causa dos dois sentidos está no degrau da §4 do Adendo 3. A espessura de
1,6 mm **encurta** a faixa onde ela é vista de viés e **alonga** onde a parede
lateral aparece. No método do diâmetro esses dois efeitos ficam em lados opostos
do anel e se compensam; na faixa não há compensação nenhuma, e só o olho do
operador decide.

**A faixa não é adotada.** As 4 linhas de treino ficam onde estão, como registro
do ensaio.

## 3 · O MÉTODO DO BURACO — IDEIA DO FABIO, 02/10, 12h39

> *"se o anel tem um círculo, pode ser que ele seja mais exato que seu formato"*

Medir o **diâmetro do buraco** do splint (10 mm nominais), atravessando a ferida.

### 3.1 · Por que é melhor que a faixa

1. **A base cresce de 3 mm para 10 mm.** O mesmo erro de clique pesa 3,3 vezes
   menos. Contra os 16 mm da borda externa, perde só 1,6×.
2. **Atravessando, a maior corda é o eixo maior**, e o eixo maior de um círculo
   de 10 mm visto inclinado continua sendo 10 mm. A faixa não tinha esse
   recurso.
3. **Quando o rato come a borda externa, o buraco pode continuar inteiro** — há
   escala onde hoje se grava `SEM_ANEL`. Era o problema que originou toda esta
   linha.

Contra, declarado: a borda interna é a mais lavada das duas, porque o coverslip
de 16 mm e o Tegaderm passam por cima do buraco. O mesmo erro de borda que na
faixa de 114 px pesava ~2 % aqui pesa ~0,5 %, mas o viés de clipar a transição
continua existindo e será medido, não suposto.

### 3.2 · O treino, com o valor esperado à vista

| imagem | externo | esperado | medido | dif |
|---|---|---|---|---|
| `Day 0_A8-1-L` | 604,9 | 378,1 | 370,5 | −2,01 % |
| `Day 0_A8-1-R` | 603,6 | 377,2 | 372,0 | −1,39 % |
| `Day 0_A8-3-L` | 595,3 | 372,1 | 379,5 | +2,00 % |
| `Day 0_A8-3-R` | 593,1 | 370,7 | 376,5 | +1,57 % |
| `Day 0_A8-4-L` | 599,1 | 374,4 | 372,0 | −0,65 % |

**Mediana −0,65 % · IIQ 3,48 % · amplitude 4,01 %.**

Passaria nos dois critérios. **Mas é treino**, com o número na barra: não conta
como evidência, e as 5 estão marcadas `treino=S` e excluídas da comparação.
Três travessias repetidas da mesma imagem deram 370, 376 e 380 px contra 374,4
esperados.

### 3.3 · A REGRA DE TRAVESSIA, FIXADA ANTES DAS 87

Decisão do Fabio, 12h56, **antes de qualquer medida às cegas**:

> **Todas as travessias verticais, de baixo para cima, pelo meio do buraco.**

Fica registrado o que isso é e o que não é. Vertical é **arbitrário** em relação
à elipse do buraco: se a foto estiver inclinada no sentido horizontal, a
travessia vertical pega a corda menor e mede curto. O que torna a regra válida
não é ela ser ótima — é ela ser **fixa, declarada antes, e igual para as 255**.
Escolher a direção imagem a imagem seria o inverso: devolveria ao operador
exatamente a liberdade que arruinou o método da faixa.

Observação anterior à regra: nas 5 de treino as travessias já saíram verticais
(`x1 = x2` nas cinco) e o espalhamento deu 2 para cima e 3 para baixo — ou seja,
não aparenta viés de direção, e sim ruído de borda. Se o recálculo mostrar viés,
ele será reportado como limitação da regra, não corrigido depois.

### 3.4 · A marca `e`

Pedida pelo Fabio em 12h56, com o `INTERNOS.txt` contendo **apenas as 5 linhas
de treino**:

| tecla | significa |
|---|---|
| `e` | anel deformado ou estragado |

Vocabulário **fechado** numa letra. Entra agora precisamente porque o arquivo
ainda não tem nenhuma medida que conte: ela vai existir em **todas** as linhas
da comparação, sem coluna pela metade — que foi a razão de recusar marca nova no
Adendo 3, e que aqui não se aplica.

A marca descreve o **anel na fotografia**, não a medida: não muda diâmetro,
centro nem escala, e **nenhuma imagem é excluída por causa dela**. As marcas
`p;d;f` do `MEDIDAS.txt` continuam valendo e se juntam a estas pelo nome do
arquivo.

As 5 linhas de treino do formato antigo são preservadas em
`INTERNOS_TREINO_SEM_MARCA.txt` e o treino é refeito, para que o arquivo saia
uniforme desde a primeira linha.

### 3.5 · O critério, o mesmo do Adendo 3

`px/mm` pelo buraco (`diâmetro_px / 10`) contra `px/mm` pelo diâmetro externo
(`diâmetro_px / 16`), par a par, nas imagens que tiverem os dois.

Diferença relativa **mediana** e **intervalo interquartil**; bootstrap de 10000
com semente 20260928 para o intervalo de 95 % da mediana.

O buraco é admitido como escala **secundária**, e **só** para imagens em que a
borda externa é impossível, se e somente se:

- `|mediana| ≤ 2 %` **e**
- `IIQ ≤ 5 %`

**O resultado é publicado seja qual for**, inclusive se reprovar. Se passar,
toda imagem resgatada por ele entra marcada como **escala por buraco**, e as
análises são reportadas nas duas formas: só com escala externa, e com as duas.

## 4 · A MEDIÇÃO EXTERNA CONTINUA PAUSADA EM 92

Sem alteração em relação à §5 do Adendo 3. As 92 ficam com os hashes de lá;
as 163 restantes serão medidas pelo mesmo `mede_anel.py` v6, sem alteração,
quando o Fabio retomar.

## 5 · FERRAMENTAS

Nenhuma delas detecta coisa alguma; todas registram onde o operador clicou.
Nenhuma lê o `deteccao_camundongo.json`, nenhuma altera o `MEDIDAS.txt`.

| arquivo | SHA-256 | bytes | situação |
|---|---|---|---|
| `mede_faixa.py` | `df8d779f56686a78c6f986e3f45c1379aa9c53d28cc2bf84a20d00bf02e1e29d` | 17.032 | 3 cliques; não usada |
| `mede_faixa2.py` | `31b28d0d0d9114423260bf14ce74ac327f311335ee4bf1ca255912a9733655f6` | 18.365 | arrasto + clique; não usada |
| `mede_faixa3.py` | `7a8db25e40a6b8d5234d2ddf222cea1a2972bfbde9a4ffb840798399d9e23502` | 18.336 | régua travada; produziu as 4 linhas de `FAIXAS.txt` |
| `mede_buraco.py` | `e07789ab8202ddc43e18f91d743399ffb6d8e8dbbb037f1cbbbe4758473d5c77` | 19.190 | não usada |
| `mede_buraco2.py` | `01b93f66e237fa6383ba3da2ca45a9ca52db74263d3dcfcc1d6562a3b153fd80` | 20.173 | + arrasto da imagem; produziu as 5 de treino |
| `mede_buraco3.py` | `5564c314be972081d1930e44b5ec23dc2b69b30a207d52045f4b953c061afff4` | 21.230 | **a que vale**: + marca `e` |

Cada uma é arquivo novo porque a anterior já recebeu hash em registro. Nenhuma
foi editada depois de hasheada.

**Ensaios, antes de qualquer uso** — régua travada: o ponteiro a 800 px fora da
linha não muda a medida; a régua estica e encolhe só na direção travada; não
mede para trás; travada a 37° mede o valor exato; ida e volta tela↔original
exata nos 6 níveis de zoom e em qualquer posição de arrasto, inclusive nos
cantos; a janela nunca sai da imagem. Marcas: campo vazio vira `-`, letra fora
do vocabulário é ignorada no campo.

## 6 · O QUE NÃO MUDA

Escala pelo anel **externo** de 16 mm como método primário; `px_mm = D/16`;
recorte de 24 mm → 1380 → 700; `diam_ef` 11,5 mm; a grade de 144; a coroa da
rodada 2 entre 145,83 e 233,33 px; semente 20260928; as 255; uma rodada; zero
exclusão; **nenhuma constante do v0**; o detector congelado, reprovado nas 255 e
intocado; o `roda_camundongo.py` da Emenda 5 (`8c1f6e4d…`); o vocabulário
`p;d;f` do `MEDIDAS.txt`; a P5 do pré-registro da rodada 2 (`3a27e63c…`) e o
Adendo 1, com o texto do Fabio inalterado; e as três regras do anel e o achado
dos 52 % contra 9 % do Adendo 3.

---

*Opus, 02/10/2026. Hashes colados do `sha256sum`. As contagens da §1 foram
calculadas sobre o `MEDIDAS_LOG.tsv` de hash `01d81d98…` e as da §3.2 sobre o
`INTERNOS.txt` trazido do PC do Fabio neste instante. O motor não rodou em
nenhuma imagem até esta linha.*
