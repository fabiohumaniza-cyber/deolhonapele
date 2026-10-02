# ADENDO 5 · o resultado da medida pelo buraco

**02/10/2026, Brasília, 13h55.** O motor **não rodou em imagem nenhuma** e a
etapa 3 **não foi iniciada**. Nenhum resultado do motor existe até esta linha.

Resultado da comparação declarada na §3.5 do `ADENDO_4_BURACO_E_ERRO_DUAS_MAIORES_02OUT.md`
(`d2351b1a5d0f5ee056e9e83445b9c7a96d9ba0d7357522de488591f80abbcb11`), que **não
é alterado**. O critério abaixo é o que estava escrito **antes** de a primeira
medida às cegas existir.

## 0 · OS ARQUIVOS

| arquivo | SHA-256 | bytes |
|---|---|---|
| `INTERNOS.txt` | `c0063eb1c3e3cb3fdff6d3fce0f53fa1e04761ebcc39d9330b331874a669bc31` | 5.804 |
| `INTERNOS_LOG.tsv` | `d8feb963db30e9dc87a950e117aaf326e513bffbed4939ba6ab4deec755de1df` | 8.882 |

92 linhas: 5 de treino, 64 com buraco medido, 28 `SEM_BURACO`, 6 marcadas `e`.
Ferramenta: `mede_buraco3.py`
(`5564c314be972081d1930e44b5ec23dc2b69b30a207d52045f4b953c061afff4`).
Regra de travessia: vertical, de baixo para cima, pelo meio, fixada às 12h56.

---

## 1 · O CRITÉRIO FOI CUMPRIDO

**59 pares** diâmetro externo × buraco, treino excluído:

| | valor | critério | |
|---|---|---|---|
| mediana da diferença relativa | **−0,72 %** | \|mediana\| ≤ 2 % | **passa** |
| intervalo interquartil | **3,27 %** | IIQ ≤ 5 % | **passa** |

Q1 −2,37 % · Q3 +0,90 % · mínimo −7,45 % · máximo +4,65 %.
IC95 da mediana, bootstrap de 10000 com semente 20260928: **−1,25 % a −0,51 %**.

**O intervalo não contém o zero.** Existe, portanto, um viés pequeno e real: a
escala pelo buraco sai cerca de 0,7 % menor que a escala pela borda externa.

Esse viés foi **previsto antes de existir**. A §3.1 do Adendo 4 declarou que a
borda interna é a mais lavada das duas, por causa do coverslip de 16 mm e do
Tegaderm, e que o viés de clipar a transição "continua existindo e será medido,
não suposto". A direção e a ordem de grandeza batem com o previsto.

## 2 · E A RAZÃO PRINCIPAL DO MÉTODO NÃO SE SUSTENTOU

O terceiro e mais forte argumento da §3.1 do Adendo 4 era:

> *"Quando o rato come a borda EXTERNA, o buraco pode continuar inteiro — ou
> seja, há escala onde hoje se grava `SEM_ANEL`."*

**Resgatou 0 de 28.**

As 28 imagens `SEM_ANEL` e as 28 `SEM_BURACO` são **exatamente o mesmo
conjunto** — nenhuma a mais, nenhuma a menos, verificado nome a nome.

A explicação é simples e deveria ter sido antecipada: quando o splint se
desprende, ele se desprende **inteiro**. O caso "borda externa destruída, buraco
intacto" não existe neste banco. O que destrói a borda externa — o animal
arrancar o splint — leva o buraco junto.

**O método do buraco não acrescenta cobertura nenhuma.** As 28 imagens sem
escala continuam sem escala e seguem para o estrato px², como o pré-registro
manda.

## 3 · O QUE ELE PASSA A VALER

Outra coisa, e ela tem valor próprio.

São **duas medições manuais independentes da mesma escala**, por dois objetos
diferentes do mesmo splint — 16 mm na borda externa, 10 mm no buraco —, feitas
em momentos diferentes, com ferramentas diferentes, a segunda **às cegas**, sob
critério escrito antes. Elas concordam com IIQ de 3,27 % e viés de 0,72 %.

Isso responde com número a uma pergunta que a medida manual sempre atrai:
*"como se sabe que a escala manual está certa?"* A resposta deixa de ser "o
operador mediu com cuidado" e passa a ser um intervalo.

**Não substitui a escala primária.** A borda externa de 16 mm continua sendo o
método, pelos motivos de sempre: base maior, ambiguidade splint × coverslip
inócua, e cobertura idêntica.

## 4 · O QUE A MARCA `e` MOSTROU

Das 59 com par, **6 estavam marcadas `e`** (anel deformado ou estragado):

| imagem | diferença |
|---|---|
| `Day 11_A8-5-L` | −5,44 % |
| `Day 12_A8-1-L` | −2,29 % |
| `Day 13_A8-1-L` | −1,69 % |
| `Day 13_A8-5-L` | +0,03 % |
| `Day 14_A8-1-R` | +0,25 % |
| `Day 14_A8-5-L` | −7,45 % |

Mediana das marcadas `e`: **−1,99 %**. Mediana das 53 não marcadas: **−0,67 %**.

As duas maiores divergências de todo o conjunto estão entre as marcadas. Com
n = 6 isso **não é teste de nada** — é observação descritiva, e fica registrada
como tal. Mas é exatamente para isso que a marca foi criada às 12h56, antes de
qualquer uma delas ser medida.

## 5 · VALORES REPETIDOS: É GRANULARIDADE DE TELA, NÃO DADO REPETIDO

Onze valores de diâmetro aparecem em mais de uma imagem; um deles, **379,518 px,
em nove imagens**. Isto precisa estar escrito, porque quem ler a tabela sem a
explicação vai suspeitar de outra coisa.

A causa é aritmética. O clique vive em pixel **de tela**, que é inteiro, e a
conversão para pixel da imagem original divide por `fator × zoom`. Nas imagens
em paisagem o fator é 0,221333; nos zooms usados (1,5× a 4×) o passo resultante
é múltiplo de 0,753 px. E **379,518 = 2,259 × 168 exatamente**, com 2,259 px
sendo o valor de um pixel de tela no zoom 2×.

Ou seja: os valores só **podem** cair em múltiplos do passo, e imagens cujo anel
tem tamanho parecido caem no mesmo múltiplo. O passo é de 0,2 % a 0,6 % do
diâmetro do buraco, bem abaixo da dispersão medida de 3,27 %, então não afeta a
conclusão — mas afeta a leitura da tabela, e por isso está aqui.

Os zooms usados estão no `INTERNOS_LOG.tsv`, coluna própria: 2× em 30 imagens,
3× em 24, 4× em 7, 1,5× em 3.

## 6 · O QUE FICA DECIDIDO

1. A escala primária continua sendo a **borda externa de 16 mm**, sem alteração.
2. O buraco **não** é adotado como escala secundária para resgate, porque não há
   o que resgatar — e não porque reprovou. Ele passou no critério.
3. O resultado do buraco entra no relatório como **validação cruzada da escala
   manual**, com os números da §1, e com a §2 dita com todas as letras: a
   motivação original falhou.
4. As 28 sem escala seguem para px². Nada muda no pré-registro.
5. A medição da borda externa continua **pausada em 92 de 255** e retoma com o
   `mede_anel.py` v6, sem alteração.

## 7 · O QUE NÃO MUDA

`px_mm = D/16`; recorte de 24 mm → 1380 → 700; `diam_ef` 11,5 mm; a grade de
144; a coroa da rodada 2 entre 145,83 e 233,33 px; semente 20260928; as 255; uma
rodada; zero exclusão; **nenhuma constante do v0**; o detector congelado,
reprovado nas 255 e intocado; o `roda_camundongo.py` da Emenda 5 (`8c1f6e4d…`);
o vocabulário `p;d;f` do `MEDIDAS.txt`; a P5 do pré-registro da rodada 2
(`3a27e63c…`) e o Adendo 1; e tudo dos Adendos 3 e 4, inclusive o achado dos
52 % contra 9 % e o erro medido da média das duas maiores.

---

*Opus, 02/10/2026. Hashes colados do `sha256sum`. Todos os números desta nota
foram calculados sobre o `INTERNOS.txt` de hash `c0063eb1…` e o `MEDIDAS.txt` de
hash `9a035e9d…`, trazidos do PC do Fabio neste instante. O critério da §1 estava
escrito no Adendo 4 antes de a primeira medida às cegas existir. O motor não
rodou em nenhuma imagem até esta linha.*
