# NOTA · v5 da ferramenta, reabertura de pendentes, e o que a v3 causou

**01/10/2026, Brasília.** 27 de 255 medidas. O motor não rodou em nenhuma imagem.

---

## 1 · O QUE DE FATO ACONTECEU COM AS DEZ `SEM_ANEL`

A miniatura de referência estava no canto **inferior esquerdo** e tapava o anel
nas fotos de dia 10 em diante. Isso é verdade — mas a causa é outra, e precisa
ficar escrita: **a versão que rodou foi a v3.**

Prova, lida na barra de estado das telas do Fabio:

```
[Enter grava · n SEM_ANEL · d dois aneis · r refaz · Backspace apaga · q sai]
```

Sem `z zoom`, sem `h referencia`, e a miniatura embaixo à esquerda. Essa é a
assinatura exata da v3 (`5fc3f957…`). A **v4** (`259430d8…`), que já estava no
branch desde o commit `7fca6dc6…`, move a miniatura para o canto superior
direito e acrescenta `h` para escondê-la e `z` para o zoom 2×.

Ou seja: **as dez `SEM_ANEL` foram produzidas por uma versão para a qual já
havia correção publicada e não baixada.** Não é falha de método nem de operador
— é a cadeia de atualização. Fica registrado porque o registro é a regra, e
porque a lição é barata: **conferir o hash antes de medir não serve só para
detectar adulteração, serve para detectar versão velha.**

Também explica o `d` que "não fez nada": na v3 ele existia e marcava, mas o aviso
`[d] MAIS DE UM ANEL` cai no fim da barra, que estava cortada fora da tela.

## 2 · AS 27 MEDIDAS, CONFERIDAS

Dia 0, 17 feridas: **584 a 614 px**, mediana ~600, dispersão ~2,5 %.
Com o splint de 16 mm externo: **~37,5 px/mm**.

A conferência que vale é esta: `Day 10_Y8-2-L` deu **612,6 px → 38,289 px/mm**,
e bate com o dia 0 da mesma ferida. A escala é propriedade da foto, não do dia;
se batesse por acaso, não bateria duas vezes.

A retomada funcionou como projetada: *"27 já medidas | 228 nesta sessão"*.

## 3 · A v5

| | antes (v4) | agora (v5) |
|---|---|---|
| miniatura de referência | sobreposta no canto superior direito | na **faixa livre à direita da foto**, quando couber; só sobrepõe quando não há faixa (foto larga, ou zoom ligado) |

`h` continua escondendo e mostrando nos dois casos. **Nada mais muda** — nem a
conta dos quatro cliques, nem o formato de quatro campos do `MEDIDAS.txt`, nem o
`z`, nem a lupa de 4×, nem o `d`, nem a retomada. O ensaio
`teste_mede_anel.py` passa inteiro, inclusive a prova de que o zoom não altera o
diâmetro (diferença `0.00e+00`).

| arquivo | antes | agora | bytes |
|---|---|---|---|
| `mede_anel.py` | `259430d84b9bb2ea43e49271119707c4150bca13d895acc3cc17611252a1b3dd` | `ba018034d9d441fca30da539217f911b7c193bf531bc169d635d9585cc30a298` | 18.624 |

## 4 · COMO AS DEZ VOLTAM PARA A FILA

**Resposta à pergunta do Fable: nem uma coisa nem outra.** Nem o Fabio edita dez
linhas à mão — num arquivo que é o registro primário da etapa 2, e com TDAH
declarado, é convite a erro —, nem a ferramenta de medida ganha poder de apagar
linha. Ferramenta que mede não apaga medida.

`reabre_pendentes.py` — SHA-256
`3e31fcb4922d2f7b20d6a1bfff4b6d908825384a993e75f8514a76490b83715c`, 4.896 bytes.
Script separado, de um uso só, que **não apaga, não edita no lugar e não
reescreve linha nenhuma**:

1. copia o `MEDIDAS.txt` atual para `MEDIDAS_ATE_<data-hora>.txt`, byte a byte,
   conferindo o SHA-256 dos dois;
2. grava um `MEDIDAS.txt` novo **sem** as linhas reabertas, as outras intocadas e
   na mesma ordem;
3. grava `REABERTURA_<data-hora>.tsv` com a hora, o **motivo**, o SHA-256 de
   antes, o nome da cópia integral e cada linha retirada, verbatim.

Ele imprime o que vai fazer e **espera o operador digitar `SIM`**. É o mesmo
princípio da regra de imutabilidade: o arquivo antigo fica, a correção é arquivo
novo, e o motivo é declarado no momento, não depois.

Ensaiado num `MEDIDAS.txt` sintético de 27 linhas com 10 `SEM_ANEL` de dia 10 e
11: 28 linhas antes, 18 depois, cópia com hash idêntico ao de antes, declaração
com as dez linhas retiradas.

### O comando

```
python reabre_pendentes.py "D:\...\10_CAMUNDONGO\saida" "miniatura da v3 tapava o anel; refeito com a v5" --sem-anel-do-dia 10
```

Ele lista as dez e pede `SIM`. Se alguma `SEM_ANEL` de dia 10 for legítima — anel
de fato ausente —, basta marcá-la `SEM_ANEL` de novo na v5, agora enxergando.

## 5 · O ADENDO DA RODADA 2 JÁ ESTAVA NO BRANCH

O Fable não o viu; ele subiu antes da v4.

```
commit 95699d9c34a441aad2cdb032bd12568a77210097
camundongo/rodada2/ADENDO_1_PRE_REGISTRO_RODADA2_01OUT.md
03bb1be8e8b47205f7c79049379d81a954b741662525f5f260831edf35d228e3
```

Traz a segunda assinatura `parece_anel_interno = |área − 78,5398|/78,5398 ≤ 0,15`
(66,76 a 90,32 mm²) e a P5a exigindo as três condições.

**A nota do marcador NÃO existe.** Ela foi oferecida em conversa — a lição de que
o marcador de referência do De Olho na Pele não pode ser um círculo colorido, sob
pena de o método medir o marcador — e o Fabio não pediu para escrevê-la. Fica
como pendência declarada, não como arquivo que se supõe existir.

## 6 · A AUTORIZAÇÃO DA UNESP

Registrada em `camundongo/registros/AUTORIZACAO_COMPLEXWOUNDDB_01OUT.md`, com a
frase de autorização verbatim, a data e a resposta do Fabio.

**O telefone pessoal que vinha na assinatura foi omitido**, e isto fica dito: o
repositório é público, e número de WhatsApp de uma pesquisadora não entra em
repositório público por causa de um registro de procedência. O e-mail
institucional, esse sim, é endereço profissional e público.

---

*Opus, 01/10/2026. Hashes colados do `sha256sum`. O motor não rodou em nenhuma
imagem até esta linha.*
