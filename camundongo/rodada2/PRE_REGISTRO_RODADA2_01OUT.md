# PRÉ-REGISTRO · RODADA 2 (artefato declarado: a coroa do splint)

**01/10/2026, 14h03 (Brasília).** Escrito **antes de o motor rodar em qualquer
imagem do banco** — a etapa 3 da rodada 1 não foi executada até esta linha.

Substitui o esboço `ESBOCO_PRE_REGISTRO_RODADA2_01OUT.md`, SHA-256
`cf02c0d9812a97f8e488dedd8e65448d05c23d83bd2481c11b730703c0815ce9`, que fica
onde está, intocado, no commit `7928a30c6aba9a6ff57a2b61133f3146536a8cfc`. A
única coisa que muda em relação a ele é a **seção 7, que estava em branco**, mais
a operacionalização da seção 7.1 e a ressalva da 7.3.

---

## 7 · PREDIÇÃO P5 — ESCRITA PELO FABIO

Verbatim, como ele escreveu, em 01/10/2026 antes de qualquer resultado do motor:

> **P5 —** *"com a coroa excluída, o motor mede a ferida em pelo menos 55 % das
> 255, e a área mediana no dia 0 fica entre 20 e 40 mm²."*

São duas afirmações, e cada uma sai com seu próprio veredito.

### 7.1 · Como cada metade é contada

**P5a — "mede a ferida em pelo menos 55 % das 255"**

```
numerador   = imagens com  obtida = True  E  parece_anel_do_splint = False
denominador = 255
confirma se  numerador / 255  >=  0,55
```

Duas escolhas ficam declaradas aqui, antes, porque mudam o resultado:

- **O denominador é 255**, não "as com anel visível". É o que está escrito na
  predição. É mais duro que a P1, que usa as com anel visível — e fica mais duro
  de propósito: imagem marcada `SEM_ANEL` não tem D, logo não tem coroa, roda
  igual nas duas rodadas, e ainda assim conta no denominador.
- **"Mede a ferida" exige `parece_anel_do_splint = False`**, não apenas que o
  motor tenha devolvido um número. Essa é a leitura literal de *medir a ferida*
  contra *medir alguma coisa*, e usa a assinatura que já existe no código
  (`|área − 201,06| / 201,06 ≤ 0,15`, isto é, área entre 170,9 e 231,2 mm²).
  É a leitura **conservadora**: torna a P5a mais difícil de confirmar, nunca mais
  fácil.

**P5b — "a área mediana no dia 0 fica entre 20 e 40 mm²"**

```
mediana da area, entre as imagens do DIA 0 com obtida = True
confirma se  20 <= mediana <= 40
```

Dia 0 tem 16 feridas. **Não avaliável** se menos de 8 delas produzirem medida —
o mesmo limiar n ≥ 8 que o driver já usa por dia no Spearman da P2; não é
critério novo.

### 7.2 · Os números por trás da faixa

O punch declarado é de 6 mm: área nominal **28,2743 mm²**. A faixa de 20 a 40 mm²
corresponde a diâmetros equivalentes de **5,05 a 7,14 mm** — ou seja, −16 % a
+19 % sobre o diâmetro nominal. A faixa contém o valor nominal e não é centrada
nele.

Para comparação, a assinatura do splint fica entre **170,9 e 231,2 mm²**: seis a
oito vezes acima do teto da P5b. As duas metades da P5 não se confundem.

### 7.3 · A fraqueza da P5b, declarada antes

**O nulo geométrico tem área 28,27 mm², que está dentro da faixa de 20 a 40.**
Então, se o motor devolver qualquer mancha de aproximadamente 6 mm no centro do
recorte — inclusive uma que não seja a ferida —, a P5b confirma. Ela mede
*tamanho plausível*, não *acerto*.

Quem separa as duas coisas é o **Dice pareado contra o nulo**, que já é calculado
e reportado por imagem (`dice_motor_vs_nulo`). Fica registrado aqui que a P5b
**sozinha** não é evidência de acerto, e que o relatório tem de trazer a mediana
desse Dice ao lado dela. Isto está escrito **antes** de qualquer número existir,
para que não seja ressalva inventada depois de ver o resultado.

### 7.4 · Os três estados, como nas outras quatro

**confirmada** · **FALHOU** · **não avaliável** — este último sempre com o motivo
e os números, e nunca contado como falha. P5a e P5b recebem veredito separado: as
duas podem sair diferentes, e sair diferentes é informação.

---

## O RESTO DO PRÉ-REGISTRO

As seções 1 a 6 e a 8 são as do esboço `cf02c0d9…`, sem uma vírgula alterada:

1. **Por que existe** — a rodada 2 não conserta a rodada 1; as duas saem lado a lado.
2. **O mecanismo** — o parâmetro `ar` de `mapa_t` e `anel`, já no motor congelado
   `1602849373157ec849cef1ff3a39b75a797f85ad4f0b8adedfb810719ae4d224`: exclui o
   artefato da moldura de 8 % que estima a pele, do percentil 98 que normaliza e
   da banda candidata. **Excluído, nunca pintado.** Nenhuma linha do motor muda.
3. **A coroa** — entre 0,625·D e D, mesmo centro, pelo D medido à mão na etapa 2;
   e, como o recorte de 24 mm já é normalizado por D, ela cai nos mesmos raios em
   todas as imagens: **145,83 a 233,33 px em L = 700**. Imagem `SEM_ANEL` não tem
   coroa e sai do pareamento.
4. **O que não muda** — mesmas 255, uma rodada, zero exclusão, grade de 144,
   L = 700, semente 20260928, bootstrap 10000, `diam_ef` 11,5 mm, nulo pareado da
   regra 4, ordem de abertura da P3, **nenhuma constante do v0**.
5. **A comparação** — Wilcoxon pareado, motor cru × motor com declaração, sobre a
   área e sobre o Dice contra o nulo; mais a dependência de ordem: a rodada 2 só
   roda **depois** da etapa 3 da rodada 1, embora este arquivo seja hasheado
   **antes** dela.
6. **O ensaio sintético exigido** — e a decisão, escrita antes, de que **se o
   dentro passar a se conectar ao fora pela coroa excluída e `anel()` devolver
   `None` na maioria das cenas, a rodada 2 não acontece.**
8. **Proibições** — as mesmas de sempre.

---

*Pré-registro fechado pelo Opus em 01/10/2026 às 14h03, com a predição P5 escrita
pelo Fabio e copiada verbatim. A operacionalização da 7.1 e a ressalva da 7.3 são
do Opus e estão declaradas como tais; se o Fabio ou o Fable lerem a predição de
outro jeito, isto vira arquivo novo com o hash deste dentro, e não se edita.
Nenhuma medida do motor existe até esta linha.*
