# ADENDO 43 · pesquisa com enfermeiros — "você conseguiria traçar com segurança?"

**04/10/2026, Brasília, 11h23.** Publicado **antes** de o aplicativo ser
mandado a qualquer enfermeiro.

## 1 · A PERGUNTA (do Fabio, 11h17)

> **"Você conseguiria traçar com segurança a borda desta ferida?"**
> Sim · Não

Sem campo de motivo (decisão do Fabio, 11h19: *"se não, ninguém faz"*).

## 2 · AS 74 FOTOS

| grupo | n | regra |
|---|---|---|
| impossíveis | 30 | Fabio `NAO_TRACAVEL` **e** Emílio `IMAGINADA`: todas as que cumprem as duas condições |
| duvidosas | 14 | Fabio mediu (ok/nada) **e** Emílio `IMAGINADA`: todas |
| possíveis | 30 | **sorteadas** com `random.Random(20261004).sample` sobre a lista ordenada das 71 em que o Fabio mediu e o Emílio marcou `TRACADA` |

A seleção foi feita **sem olhar o Dice**.

| arquivo | SHA-256 |
|---|---|
| `dados/SELECAO_ENFERMEIROS.json` | `c9e70fcb297141b3321bca3f466c76362dc1a678d8af7df2961f1fab3329776c` |
| `tpl_app_enfermeiros.html` | `de62860ba327cfb0407c18f3683e67a37b26daea0cd9a68882ecbf2416e78af8` |
| `monta_app_enfermeiros.py` | `5d50b18d4be703bcfec4c13b0c2de51ef9d947ae2a4baf55f11cec651028788c` |
| `de_olho_na_pele_enfermeiros.html` (o aplicativo) | `dd5f31a60da6c79c4081fe4e75aad8309db62c10d045024982a9b243520dfeef` |
| `_CHAVE_enfermeiros.json` (código → foto → grupo; **fica com o Fabio** até o fim) | `893cf846c5c85134351956ad2ca3febf49b083fa0bd76174f7d11829630fca53` |

## 3 · O APLICATIVO

- Fotos com código de F01 a F74, **sem nome, dia ou grupo**. O código não
  revela o grupo, porque foi embaralhado com semente própria.
- A ordem é sorteada **no celular de cada pessoa** e fica gravada.
- Cadastro: nome completo, COREN e UF (obrigatórios), foto (opcional), e duas
  caixas de consentimento:
  - autorização para o nome e o COREN aparecerem no trabalho como
    colaborador(a);
  - declaração de não ter visto as fotos antes e de responder sem ajuda.
- Tempo de cada resposta em milissegundos.
- Nada é enviado pela internet. A pessoa manda o arquivo ao Fabio.

## 4 · A ANÁLISE, DECIDIDA AGORA

Só entram arquivos completos (74 respostas), com as duas caixas marcadas e com
o SHA de cada foto igual ao da chave. A análise roda com **pelo menos 10
enfermeiros**.

- **% Sim por foto** e **kappa de Fleiss**, no geral e em cada grupo.
- **Consenso:** "traçável" se ≥ 80 % disserem Sim; "não traçável" se ≤ 20 %.

### P16 — a aposta implícita do Fabio, de que as 30 impossíveis são impossíveis para outros também

- **P16.1:** a mediana de % Sim nas **30 impossíveis** é **≤ 20 %**.
- **P16.2:** a mediana de % Sim nas **30 possíveis** é **≥ 80 %**.
- As **duvidosas** ficam descritivas, sem veredito.

### Uso no Dice (secundário)

O Dice(r4, Emílio) será recalculado só nas fotos **"traçáveis por consenso"**
em que o Emílio traçou. É **secundário**: o confirmatório continua sendo o do
Adendo 41 (0,899). O conjunto é definido **só pelos enfermeiros**, sem olhar o
Dice.

## 5 · O QUE DECLARAR

- As fotos foram escolhidas pela opinião de dois leitores (Fabio e Emílio).
  Por isso os grupos extremos tendem a dar concordância alta. As duvidosas
  estão lá para mostrar onde a dificuldade é real.
- No artigo, os participantes entram como colaboradores nos agradecimentos, com
  o consentimento registrado no próprio arquivo.

---

*Opus, 04/10/2026. Nenhuma resposta de enfermeiro existe até esta linha.*
