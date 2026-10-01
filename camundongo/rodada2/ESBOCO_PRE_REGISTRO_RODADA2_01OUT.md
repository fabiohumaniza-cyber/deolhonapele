# ESBOÇO · pré-registro da RODADA 2 (artefato declarado: a coroa do splint)

**01/10/2026, Brasília. ESBOÇO — não é o pré-registro final.**
O campo da **predição está em branco de propósito: quem escreve é o Fabio.**
Com ele preenchido, isto vira arquivo novo, com o hash deste dentro, e é esse que
se congela **antes da etapa 3 da rodada 1**.

Escrito quando o motor ainda não tinha rodado em nenhuma imagem do banco.

---

## 1 · POR QUE EXISTE

A rodada 1 roda o motor v0 **cru**, sem declarar nada. A predição P4 diz que a
falha dominante será a referência de pele contaminada, e o modo "dois anéis" da
§3.7 prevê que o motor pode travar no anel do splint em vez da ferida — o que já
aconteceu no sintético (78,3 % das imagens) e no teste de cadeia (4 de 5 cenas).

A rodada 2 faz uma coisa só, e declarada: **diz ao motor onde está o splint**, e
roda de novo. Nada mais muda.

Isto **não é conserto da rodada 1**. As duas saem no relatório, lado a lado. A
rodada 1 continua sendo o resultado do motor sem ajuda; a rodada 2 mede quanto
daquilo era o splint.

---

## 2 · O ARTEFATO, E O MECANISMO QUE JÁ EXISTE

O motor congelado **já tem** entrada de artefato: o parâmetro `ar` de `mapa_t` e
de `anel`, em `motor_v0_funcoes.py`
(`1602849373157ec849cef1ff3a39b75a797f85ad4f0b8adedfb810719ae4d224`), extraído
verbatim de `rodar.py` (`78b193014577a45109771a2b15f3b7ff55663b0bb4312a23980c766fe7161732`).
É o mesmo mecanismo usado no porco. **Nenhuma linha dele muda.**

O que `ar` faz, nas três decisões em que entra:

| onde | linha | efeito |
|---|---|---|
| `mapa_t` | `m &= ~ar` | a moldura de 8 % que estima a pele exclui o artefato |
| `mapa_t` | `liv = ~ar` | o percentil 98 que normaliza exclui o artefato |
| `anel` | `am &= ~ar` | a banda candidata exclui o artefato |

**Excluído, nunca pintado.** Os pixels continuam no quadro; eles só deixam de
participar dessas três contas. A topologia — dentro/fora por conectividade com a
borda do quadro, e o anel como a componente vizinha dos dois — continua rodando
no quadro inteiro.

---

## 3 · A COROA

Por imagem, com o **D medido à mão na etapa 2** e o **mesmo centro**:

> coroa = { p : 0,625 · D/2 ≤ |p − centro| ≤ D/2 }

0,625 = 10/16: é exatamente a parede do splint, do diâmetro interno de 10 mm ao
externo de 16 mm, como o README descreve.

### Consequência que simplifica, e que precisa estar escrita

O recorte da etapa 3 já é de 24 mm centrado no anel, com px/mm = D/16. Então, no
quadro de trabalho, **a coroa cai nos mesmos raios em todas as imagens**:

```
raio externo = (16/24) · 700/2 = 233,33 px        (L = 700)
raio interno = 0,625 · 233,33 = 145,83 px
```

O D de cada imagem entra pelo **recorte**, não pela máscara. A máscara é
constante por construção — e isso é bom: não há parâmetro por imagem para alguém
ajustar depois.

### A exceção, declarada

Imagem no estrato **sem escala própria** (o operador marcou `SEM_ANEL`) não tem
D, logo **não tem coroa**: ela roda igual nas duas rodadas, em px², e sai do
pareamento da rodada 2 por não ter o que declarar. O número dessas imagens vai no
relatório.

---

## 4 · O QUE NÃO MUDA

- As **mesmas 255**. Uma rodada. Zero exclusão de imagem.
- Mesma grade de 144, mesmo L = 700, mesma semente **20260928**, bootstrap 10000.
- Mesmo `diam_ef` = 11,5 mm, mesmo recorte 24 mm → 1380 → 700, mesma replicação
  de borda.
- **Nenhuma constante do v0.**
- Mesmas **P1–P4**, com os mesmos três estados (confirmada · FALHOU · não
  avaliável), e a P4 descritiva.
- Mesmo **nulo geométrico pareado** da regra 4 (círculo de 6 mm no centro do
  anel).
- Mesma ordem de abertura da P3 (`81e150df…`).

---

## 5 · A COMPARAÇÃO

Pareada por imagem, motor **cru** (rodada 1) × motor **com declaração**
(rodada 2):

- **Wilcoxon pareado** sobre a área medida, e sobre o Dice contra o nulo.
- **Spearman**(dia, área mediana) nas duas, lado a lado.
- Quantas imagens mudaram de "sem medida" para "com medida", e o contrário.
- Quantas deixaram de exibir a assinatura "anel do splint" da P4.

**Dependência de ordem, obrigatória:** a rodada 2 só pode ser comparada contra
uma rodada 1 que já exista e já esteja fechada. O pré-registro final tem de ser
hasheado **antes da etapa 3 da rodada 1**, mas a rodada 2 só roda **depois** dela.
Rodar as duas e escolher qual reportar seria exatamente o que este projeto não
faz.

---

## 6 · O TESTE SINTÉTICO EXIGIDO, ANTES DE QUALQUER COISA

A pergunta não é retórica, e pode responder *não*:

> **Com a coroa excluída da banda, o anel topológico ainda fecha?**

`anel()` escolhe a componente da banda que é vizinha do **dentro** e do **fora**
ao mesmo tempo. Tirando a parede do splint da banda, três coisas podem acontecer,
e o ensaio tem de distinguir:

1. o anel da **ferida** passa a ser escolhido — é o que se espera;
2. o `binary_closing` de 7 × 7 **atravessa** a coroa excluída e recria uma
   componente que não existe;
3. o **dentro** passa a se conectar ao **fora** pela coroa excluída, a topologia
   se desfaz e `anel()` devolve `None` — o motor para de medir em vez de medir
   melhor.

O ensaio desenha cenas com a geometria do README (coroa 10 → 16 mm, ferida de 6
mm, inclinação, ruído) e conta qual dos três ocorre, em quantas. **Se o caso 3
dominar, a rodada 2 não acontece** — e isso fica escrito aqui, antes, para não
virar decisão tomada depois de ver o resultado.

---

## 7 · PREDIÇÃO

> ***(em branco — escrita pelo Fabio, com número, antes do hash final)***
>
> P5: _______________________________________________

Vale a mesma regra das quatro anteriores: três estados, e **não avaliável não é
falhada**, sempre com o motivo e os números.

---

## 8 · PROIBIÇÕES, AS MESMAS

Nenhuma constante do v0 · nenhum "v0 adaptado ao camundongo" · nenhuma segunda
tentativa com parâmetro novo · nada de mexer no detector do anel (v2 é outro
pré-registro) · arquivo com hash é imutável, extensão é arquivo novo · dúvida
para a rodada e pergunta ao Fabio.

---

*Esboço escrito pelo Opus em 01/10/2026, a pedido do Fable, com o mecanismo `ar`
lido no código congelado e não de memória. O motor não rodou em nenhuma imagem
até esta linha.*
