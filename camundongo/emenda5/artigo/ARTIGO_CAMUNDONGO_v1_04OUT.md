# Nem toda ferida fotografada pode ser medida: traçabilidade, regra escrita e dois leitores cegos em um banco público de feridas de camundongo

**Rascunho v1 · 04/10/2026** · não revisado · não submetido

Fabio da Camara Oliveira Ferreira¹ (ORCID 0009-0009-0997-3275)

¹ Pesquisador independente, Águas de Lindóia, SP, Brasil. fabiohumaniza@gmail.com

---

## RESUMO

**Introdução.** Estudos que medem feridas em fotografia costumam relatar a
concordância contra um traçado de referência, sem dizer se a borda era visível
em cada imagem. Quando a borda não é visível, o traçado de referência é um
palpite, e a concordância contra ele não mede acerto.

**Objetivo.** Testar, com previsões registradas antes de cada execução, uma
regra escrita e congelada de detecção de borda (motor v0, desenvolvida em
modelo suíno) em um banco público de feridas de camundongo. Medir também
quantas imagens permitem traçar a borda.

**Métodos.**
- **Banco:** 255 fotografias de 16 feridas excisionais de 8 camundongos,
  fotografadas entre os dias 0 e 15 (Dryad, doi:10.25338/B84W8Q).
- **Escala e área:** a escala foi medida à mão no anel de silicone (splint).
  A área de busca foi restrita ao interior do anel, num círculo colocado à mão
  e registrado com hash antes de qualquer execução que o usasse.
- **Classificação:** o operador classificou cada imagem quanto à
  traçabilidade da borda e declarou os artefatos.
- **Referência:** dois leitores, um leigo e uma enfermeira, traçaram, cegos e
  com ordens diferentes,
  as mesmas 201 imagens. Em cada imagem, cada um declarou se viu a borda, se
  viu parte dela ou se a imaginou.
- **Métrica:** Dice no quadro inteiro, sempre ao lado de um comparador nulo
  (círculo do tamanho do punch no centro do campo).

**Resultados.**
- **Sem restrição de área, o motor falhou** (ρ de Spearman entre dia e área
  = −0,16; previsto ≤ −0,8). Com a área fixada no interior do anel, a curva das
  imagens sem filme plástico caiu de 26,2 mm² no dia 0 para 3 a 8 mm² nos dias
  7 a 13 (ρ = −0,88).
- **Contra os leitores, nas imagens em que cada um viu a borda**, a mediana
  do Dice do motor foi:

  | leitor | Dice motor | Dice nulo |
  |---|---|---|
  | leitor 1 | 0,899 (n = 48) | 0,602 |
  | leitor 2 | 0,906 (n = 44) | 0,651 |

- **Entre os dois leitores**, nessas imagens, o Dice foi 0,976 (n = 55).
- **Onde a borda foi imaginada**, o Dice do motor caiu para 0,51 a 0,75, perto
  do nulo.
- **Traçabilidade:** os leitores concordaram sobre quais imagens são
  traçáveis (κ = 0,69). Nenhuma imagem que um viu com clareza o outro marcou
  como imaginada.
- **Imagens não mensuráveis:** cerca de um terço das imagens com campo (64 de
  201) foi julgada não mensurável pelo operador antes de qualquer traçado.
- **Cicatrizadas:** o motor mediu área do tamanho do punch nas 5 feridas
  cicatrizadas.

**Conclusão.** Onde a borda é visível, uma regra escrita, sem treino nesse
banco, fica perto da concordância entre leitores humanos. Onde não é visível,
nenhum método pode ser avaliado contra traçado, e a imagem deve ser relatada
como não mensurável, não medida.

**Palavras-chave:** cicatrização de feridas; fotografia; segmentação de
imagem; reprodutibilidade; pré-registro; camundongo.

---

## 1 · INTRODUÇÃO

Medir a área de uma ferida por fotografia é rotina em pesquisa e começa a ser
rotina na clínica. A forma habitual de validar um método é compará-lo a um
traçado humano de referência, pelo coeficiente de Dice ou pela correlação de
áreas.

Essa validação pressupõe que a borda esteja visível. Em fotografia de ferida,
muitas vezes não está. Ela pode estar coberta por:
- curativo plástico;
- reflexo;
- pelo que volta a crescer;
- crosta;
- sangue.

Em modelos experimentais, o próprio anel que imobiliza a pele pode cobrir
parte da ferida. Quando a borda não é visível, quem traça imagina onde ela
está. Um método que concorde com esse traçado concorda com um palpite.

O banco público de feridas de camundongo de Carrión et al. (2022) ilustra bem
o problema.
- **Os próprios autores** listam, entre as dificuldades das imagens:
  - leito ocluído por cobertura plástica, reflexo e sujeira;
  - borrão;
  - pelo que volta a crescer;
  - anel ausente ou muito danificado em mais de 25 % das imagens.
- **No trabalho original:**
  - um anotador leigo traçou um polígono em todas as 256 imagens;
  - uma rede neural foi treinada sobre esse traçado;
  - o Dice relatado no conjunto de teste foi 0,8665.
- **O que não foi relatado:** em quantas imagens a borda era visível.

Neste trabalho, a mesma pergunta foi feita de outro jeito. Primeiro, quantas
imagens permitem traçar a borda. Depois, quanto uma regra escrita acerta
nessas imagens e onde ela erra. O método é uma regra de detecção de borda por
anel fechado, desenvolvida e publicada para modelo suíno (Ferreira, 2026,
doi:10.5281/zenodo.23062849). Ela foi aplicada **congelada**: nenhuma
constante foi alterada. Cada execução teve as previsões registradas antes, em
repositório público com hash. Os fracassos foram publicados junto com os
acertos.

## 2 · MÉTODOS

### 2.1 · Registro e transparência

Todo o trabalho foi registrado em uma sequência de adendos datados, cada um
com o hash SHA-256 dos arquivos que fixa. O código, os dados derivados e os
adendos estão em repositório público. Nenhum arquivo com hash foi alterado
depois de registrado: correções foram para arquivos novos.

Cada execução do motor foi precedida da publicação:
- do código;
- das entradas;
- das previsões, com critério de acerto numérico.

### 2.2 · O banco

O banco tem 255 fotografias, disponíveis no Dryad (doi:10.25338/B84W8Q):
- **8 camundongos**, 4 jovens (Y8-1 a Y8-4) e 4 idosos (A8-1, A8-3, A8-4 e
  A8-5);
- **16 feridas**, duas por animal, uma de cada lado (L e R), feitas com punch
  de 6 mm (28,27 mm²);
- cada ferida com anel de silicone (splint) suturado em volta;
- **dias de fotografia:** 0 a 15.

Nenhuma imagem foi excluída do conjunto de partida.

### 2.3 · Escala

O operador mediu o diâmetro interno do anel em cada imagem, com quatro cliques
em cruz e uma regra escrita: média das duas maiores distâncias. O erro dessa
regra foi medido nos próprios cliques, contra um círculo ajustado por mínimos
quadrados:
- mediana −0,19 %;
- **sempre negativa**, por construção.

Das 255 imagens, **204** tinham anel medível e **51** não tinham anel visível.
Cinco imagens medidas duas vezes, em dias diferentes, variaram entre −1,9 % e
+0,6 %.

### 2.4 · Classificação e área de busca

**Classificação, antes de qualquer execução do motor.** O operador marcou
cada imagem como:
- laudável;
- duvidosa;
- não laudável;
- cicatrizada;
- com ou sem filme plástico.

**O campo de busca.** O operador colocou, em cada uma das 204 imagens com
escala, um círculo encostado na borda interna do anel, sem tocá-lo. O campo é
esse círculo encolhido 0,3 mm, margem fixada antes da primeira imagem.
- 201 imagens receberam campo;
- 3 não couberam, todas da mesma ferida, com o plástico deformado;
- o raio mediano do campo foi de 3,99 mm.

O campo foi registrado com hash antes de qualquer execução que o usasse.

**A declaração do operador.** Na fase final, o operador marcou cada uma das
201 imagens:

| estado | n | o que significa |
|---|---|---|
| sem nada a corrigir | 81 | — |
| com correção | 56 | conta-gotas na cor da ferida e/ou contorno de artefato |
| não traçável | 49 | — |
| borda parcial | 11 | — |
| pelo sobre o leito | 4 | — |

A regra de traçabilidade foi escrita assim: *"a borda pode ser seguida com
confiança na maior parte da volta"*. As cinco imagens com ferida cicatrizada
ficaram fora da medida, num braço exploratório em que a resposta certa é área
zero.

**Os braços de análise:**
- **principal:** as imagens medidas pelo operador e sem filme plástico (71);
- **com filme:** exploratório (66).

### 2.5 · O motor

O motor v0 é a regra de anel fechado publicada para modelo suíno, sem nenhuma
constante alterada. Os módulos foram lidos do local onde foram congelados, com
o hash conferido a cada execução.

Foram feitas quatro execuções, cada uma com pré-registro próprio:

| execução | o que muda |
|---|---|
| 1 | foto, sem restrição de área |
| 2 | a coroa do anel é excluída da busca |
| 3 | só o campo declarado (§2.4) |
| 4 | o campo, mais a declaração do operador (cores e artefatos) |

A execução 3 é o motor sozinho dentro do campo. A execução 4 é a medida
assistida.

### 2.6 · Os leitores

Dois leitores traçaram a borda da ferida nas 201 imagens com campo.

- **Leitor 1:** bacharel em ciência da computação, com dois anos de veterinária
  e parente do autor.
- **Leitora 2:** enfermeira, ex-diretora de Saúde de Águas de Lindóia (SP)
  (COREN-SP 115508); foi chefe do autor na Secretaria de Saúde do
  município, sem vínculo de trabalho atual entre os dois [confirmar].

**O painel.** Cada leitor recebeu o mesmo painel em navegador:
- as mesmas vistas, conferidas pelo SHA-256 de cada imagem;
- sem nome, dia ou máscara;
- em **ordem sorteada própria**, com semente registrada.

**A declaração inicial.** Antes de começar, cada leitor declarou não ter visto
as imagens, traçados de outra pessoa ou de máquina, nem expectativas.

**A instrução:**
- traçar a borda da parte vermelha ou rosada;
- ignorar o anel, a sutura, o pelo e o brilho;
- traçar **todas** as imagens, inclusive imaginando a borda;
- em cada imagem, declarar uma de quatro opções: vi a borda (TRACADA), vi
  parte (PARCIAL), imaginei (IMAGINADA) ou ferida fechada (FECHADA).

A hora de abrir e de fechar cada imagem foi gravada. Cada arquivo de traçado
foi lacrado com hash antes de ser aberto.

### 2.7 · Métricas e análise

**O Dice.** Calculado no quadro inteiro de 700 px, sem recortar pelo campo:
se o leitor traçou fora do campo, isso conta contra o motor.

**O comparador nulo.** Todo Dice foi relatado ao lado de um nulo: um círculo
do tamanho do punch no centro do campo, desenhado sem olhar a imagem.

**O conjunto principal.** As imagens do braço principal que o leitor marcou
como TRACADA. As demais foram relatadas à parte, sem veredito.

**Concordância de traçabilidade.** Medida pelo kappa de Cohen, com a
classificação "TRACADA ou não", entre:
- os dois leitores;
- cada leitor e o operador.

### 2.8 · Comparação com o trabalho original

O caderno público do trabalho original lista as 32 imagens do seu conjunto de
teste. O Dice do motor foi calculado nessas imagens, onde elas estavam entre
as 201. A comparação foi registrada antes de ser feita.

## 3 · RESULTADOS

### 3.1 · Sem restrição de área, o motor falhou

**Execução 1.** O motor devolveu medida em todas as 255 imagens, sem recusar
nenhuma. A curva de área por dia não caiu (ρ = −0,16; previsto ≤ −0,8). Nas
imagens limpas, **nenhuma** das 70 máscaras estava dentro do anel: o motor
mediu o próprio anel e o pelo em volta.

**Execução 2.** Com a coroa do anel excluída, o motor migrou para o pelo, a
luva e a régua. Só 26 de 70 máscaras caíram dentro do anel.

Esse foi um erro de método do autor, não do motor nem do banco: o estudo de
origem mede **só** dentro do anel. O código dele:
- recorta a imagem com o anel no centro;
- fica com a mancha de ferida mais próxima do centro;
- calcula a área em relação ao interior do anel.

A área de busca foi então fixada no interior do anel (§2.4), antes das
execuções seguintes.

### 3.2 · Com a área fixada, a curva caiu

**Execução 3.** Todas as 70 máscaras das imagens limpas ficaram dentro do
campo. Nas imagens sem filme, a curva caiu (ρ = −0,86). Com filme plástico, a
curva ficou reta, em torno de 26 mm², do primeiro ao último dia: **o plástico
trava o número**.

**Execução 4**, braço principal (71 imagens):
- área mediana de 26,2 mm² no dia 0 (93 % do punch);
- 3,1 a 7,7 mm² entre os dias 7 e 13;
- ρ = −0,88.

**O efeito da correção do operador.** Das 56 imagens corrigidas, 24 saíram
praticamente iguais à execução 3 (Dice ≥ 0,95 entre as duas máscaras). A
previsão de que mais da metade sairia igual falhou.

### 3.3 · Contra os leitores

**Tabela 1.** Mediana do Dice do motor contra cada leitor.

| conjunto | leitor | n | motor assistido (exec. 4) | motor sozinho (exec. 3) | nulo |
|---|---|---|---|---|---|
| principal, borda vista | 1 | 48 | **0,899** | 0,895 | 0,602 |
| principal, borda vista | 2 | 44 | **0,906** | 0,887 | 0,651 |
| todas as traçadas | 1 | 200 | 0,845 | 0,814 | 0,700 |
| todas as traçadas | 2 | 194 | 0,834 | 0,807 | 0,692 |
| só as imaginadas | 1 | 45 | 0,511 | 0,475 | 0,496 |
| só as imaginadas | 2 | 47 | 0,750 | 0,667 | 0,568 |

As quatro previsões registradas para os leitores se confirmaram:

| previsão | critério | leitor 1 | leitor 2 |
|---|---|---|---|
| mediana | ≥ 0,70 | 0,899 | 0,906 |
| fração das imagens com Dice ≥ 0,70 | ≥ 80 % | 90 % | 86 % |

A previsão de que o leitor 2 daria resultado igual ao do leitor 1 (0,899 ±
0,05) também se confirmou.

O que a tabela mostra:
- **A correção do operador quase não mudou o acerto** nas imagens com borda
  visível: 0,899 com correção e 0,895 sem, no leitor 1. Onde a borda é
  visível, o motor sozinho já acerta.
- **Com filme plástico, o nulo já chega a 0,86** (leitor 1). Ali, um Dice alto
  do motor diz pouco.

### 3.4 · Os dois leitores concordam entre si

- **Nas 55 imagens que os dois marcaram como TRACADA**, o Dice entre os dois
  traçados teve mediana de **0,976**.
- **O kappa de traçabilidade entre os dois foi 0,69.** Nenhuma imagem que um
  leitor marcou como TRACADA o outro marcou como IMAGINADA (Tabela 2).
- **Contra o operador**, a concordância foi menor (κ 0,41 e 0,36). Os leitores
  foram mais rigorosos: das 137 imagens que o operador mediu, cada leitor
  julgou ver a borda em cerca de metade.
- **Das 64 imagens que o operador excluiu**, o leitor 1 não marcou nenhuma como
  TRACADA, e o leitor 2 marcou uma.

**Tabela 2.** Estado declarado pelo leitor 1 (linhas) × pelo leitor 2 (colunas).

| | TRACADA | PARCIAL | IMAGINADA | FECHADA |
|---|---|---|---|---|
| TRACADA | 55 | 16 | 0 | 0 |
| PARCIAL | 12 | 51 | 20 | 1 |
| IMAGINADA | 0 | 12 | 27 | 6 |
| FECHADA | 0 | 1 | 0 | 0 |

### 3.5 · As imagens que ninguém consegue traçar

Trinta imagens foram julgadas não traçáveis pelo operador **e** imaginadas
pelo leitor 1.
- **Motivos descritos:**
  - filme plástico cobrindo ou deformando a borda;
  - pelo sobre o leito;
  - artefato atravessando a lesão;
  - borda que se confunde com cicatriz;
  - segunda ferida ao lado.
- **Nessas imagens**, o Dice do motor contra o traçado imaginado teve mediana
  de 0,37 (exploratório).
- **Figura 1** (a produzir): exemplos dessas imagens, para que o leitor possa
  tentar traçá-las.

### 3.6 · Feridas cicatrizadas

Nas cinco imagens em que a ferida já tinha fechado, a resposta certa é área
zero. **O motor deu entre 25,7 e 28,6 mm²**, o tamanho do punch. O motor v0
não sabe dizer "não há ferida". Diante de pele fechada, ele acha um contorno
do tamanho que espera achar.

### 3.7 · No conjunto de teste do trabalho original

Das 32 imagens de teste do trabalho original, 26 estão entre as 201. Três
estão entre as 30 que nenhum leitor conseguiu traçar.

| conjunto | n | Dice médio do motor |
|---|---|---|
| imagens em que o leitor 1 viu a borda | 8 | **0,908** |
| todas, incluindo as imaginadas | 26 | 0,764 |

O valor relatado no trabalho original foi 0,8665. A comparação não é direta:
- o anotador é outro;
- lá havia uma rede treinada, aqui uma regra que nunca viu o leitor;
- o modo de cálculo do Dice original não está publicado.

## 4 · DISCUSSÃO

**O principal achado é anterior a qualquer número de acerto: nem toda ferida
fotografada pode ser medida.**
- Neste banco, cerca de um terço das imagens com campo foi julgada não
  mensurável pelo operador.
- Dois leitores independentes concordaram sobre quais eram.
- Nessas imagens, todo traçado é palpite, e todo Dice contra ele mede apenas o
  quanto dois palpites coincidem.
- Um estudo que traça todas as imagens e relata um Dice só mistura medida com
  palpite.

**Onde a borda é visível, a regra escrita acerta.** O motor ficou em 0,90
contra dois leitores. A concordância entre os próprios leitores foi de 0,98.
Os 0,08 que separam um número do outro são o quanto falta à regra para
igualar uma pessoa nessas imagens. A regra:
- não foi treinada neste banco;
- não tem nenhuma constante ajustada para camundongo;
- foi desenvolvida em modelo suíno.

**A restrição de área não é ajuste: é a condição de uso.** Sem ela, o motor
mediu o anel e o pelo. Com ela, mediu a ferida. O estudo de origem faz a mesma
restrição, por construção. O primeiro resultado, o fracasso, é relatado como
resultado negativo.

**O comparador nulo separa o que o Dice sozinho esconde.** Com filme plástico,
um círculo cego já chega a 0,86. Nessas imagens, um Dice alto não mostra
nada.

**A limitação mais séria é o caso da ferida cicatrizada.** O motor v0 sempre
encontra um contorno. Um sistema clínico precisa saber dizer "não há o que
medir". Essa é a primeira prioridade da versão seguinte.

### Limitações

- **Nenhum leitor é especialista em feridas,** e o leitor 1 é parente do
  autor. Um leigo e uma enfermeira concordaram 0,98 entre si, o que sugere
  que a tarefa, onde a borda é visível, não exige especialista. Mas isso não
  substitui um leitor especialista.
- **O operador que colocou o campo e fez a declaração já tinha visto as
  imagens.** A execução 4 é uma medida assistida, não automática.
- **A regra de traçabilidade foi aplicada por uma pessoa.** A concordância
  com os leitores mostra que ela é reprodutível, mas não perfeita (κ 0,36 a
  0,69).
- **O braço principal tem 71 imagens,** com poucas por dia nos dias finais.
- **Não há medida física independente da área ao longo dos dias.** Só o
  punch, no dia 0.

## 5 · CONCLUSÃO

Em um banco público de feridas de camundongo, uma regra escrita e congelada,
desenvolvida em outra espécie:
- atingiu Dice de 0,90 contra dois leitores cegos (um leigo e uma enfermeira), cuja concordância mútua foi
  de 0,98, nas imagens em que a borda era visível;
- seguiu uma curva de área compatível com o fechamento da ferida.

Cerca de um terço das imagens não permitiu traçar a borda. Para essas imagens,
o resultado honesto é "não mensurável", e ele deveria ser relatado em qualquer
estudo de medida de ferida por fotografia.

---

## DISPONIBILIDADE DE DADOS E CÓDIGO

O repositório público reúne:
- código;
- dados derivados (escala, campo, classificação, declaração, máscaras e
  traçados dos dois leitores);
- 60 adendos com hash.

[link do repositório e DOI do Zenodo a inserir]. As imagens originais estão no
Dryad (doi:10.25338/B84W8Q).

## AGRADECIMENTOS

Aos autores do banco público de feridas de camundongo (Yang, Bagood, Carrión,
Isseroff e colaboradores), por disponibilizá-lo. Aos dois leitores, Emílio [sobrenome a inserir] e Helga Emanuele Resquioto
(enfermeira, COREN-SP 115508), que traçaram as 201 imagens.

**Compensação.** A segunda leitora recebeu compensação fixa pelo tempo,
combinada antes da leitura e independente do resultado.

## CONFLITO DE INTERESSES

O autor é titular de pedido de patente do método (BR 10 2026 024571 2) e de
registro de programa de computador (512026008413-0).

## REFERÊNCIAS (a completar)

1. Carrión H, Jafari M, Bagood MD, Yang HY, Isseroff RR, Gomez M. Automatic wound detection and size estimation using deep learning algorithms. *PLoS Comput Biol.* 2022;18(3):e1009852.
2. Ferreira FCO. A borda da ferida existe na fotografia: medição auditável baseada em regras em relação a um padrão físico em um modelo suíno (versão v5n). Zenodo; 2026. doi:10.5281/zenodo.23062849.
3. Banco Dryad: doi:10.25338/B84W8Q.
