# ADENDO 1 ao PRÉ-REGISTRO DA RODADA 2 · a segunda assinatura

**01/10/2026, Brasília. Antes da etapa 3 da rodada 1.** O motor não rodou em
nenhuma imagem do banco até esta linha.

Adendo ao `PRE_REGISTRO_RODADA2_01OUT.md`, SHA-256
`3a27e63ce867080baa171306abaa8ac3e260db080a8658a755c964b69be5c6d9`, que **não é
alterado por este arquivo** — ele previa esta forma: predição lida de outro jeito
vira arquivo novo, com o hash do anterior dentro.

Apontado pelo Fable na conferência do `3a27e63c…`.

---

## 1 · O BURACO

A seção 7.1 exigia, para contar como "mede a ferida", que a imagem tivesse
`obtida = True` **e** `parece_anel_do_splint = False`. Essa assinatura cobre
**só a borda externa** do splint: área 201,06 mm², faixa 170,90 a 231,22.

Com a coroa excluída — que é exatamente o que a rodada 2 faz —, a parede some da
banda candidata, e o concorrente mais provável da ferida passa a ser **a borda
interna do splint**: o círculo de 10 mm, **78,5398 mm²**.

Essa medida **não é a ferida**, **não cai** na faixa de 201, e a 7.1, como estava
escrita, **contaria como acerto**. A P5a confirmaria pelo motivo errado — e o
erro seria de um fator 2,78 em área sobre a ferida de 28,27 mm².

É o mesmo mecanismo da primeira assinatura, deslocado para dentro: a rodada 2
remove o estímulo que o motor preferia, e o anel tem **duas** bordas.

## 2 · O QUE MUDA

Segunda assinatura, com a mesma forma e a mesma tolerância da primeira:

```
parece_anel_interno = |area − 78,5398| / 78,5398 <= 0,15
                    = area entre 66,76 e 90,32 mm²
```

E a **P5a passa a exigir as três condições**:

```
obtida = True   E   parece_anel_do_splint = False   E   parece_anel_interno = False
denominador = 255        confirma se >= 0,55
```

O relatório traz **as duas assinaturas separadas**, nunca somadas: quantas no
anel externo, quantas no interno, e quantas em nenhum dos dois.

Como as outras duas decisões da 7.1, esta deixa a P5a **mais difícil** de
confirmar, nunca mais fácil.

## 3 · AS TRÊS FAIXAS NÃO SE TOCAM

| o que | área | faixa ±15 % |
|---|---|---|
| ferida de 6 mm (nominal) | 28,2743 mm² | — |
| **P5b** (faixa escrita pelo Fabio) | — | **20 a 40 mm²** |
| **anel interno**, 10 mm | 78,5398 mm² | **66,76 a 90,32 mm²** |
| **anel do splint**, 16 mm | 201,0619 mm² | **170,90 a 231,22 mm²** |

Conferido: não há sobreposição entre a faixa da P5b e a do anel interno, nem
entre a do anel interno e a do splint. Uma imagem não pode confirmar a P5b e ser
classificada como anel, em nenhuma das duas assinaturas. As duas assinaturas
distam entre si por um fator 2,56 em área.

## 4 · NENHUM CÓDIGO CONGELADO MUDA POR ISTO

As duas assinaturas são **função pura da área já registrada por imagem** no JSON.
Não é detecção nova, não é critério que o motor aplique: é classificação feita
sobre um número que o driver já grava.

Portanto:

- `roda_camundongo.py` (`3b787ef95a344ddba94fa5520feadb54e20afaffd1d399816a085947e9a35a55`) **não muda**, e a rodada 1 roda como está;
- `motor_v0_funcoes.py`, `detecta_anel_camundongo.py`: **intocados**;
- o driver da **rodada 2**, que ainda não existe, nasce já com as duas;
- e, para a rodada 1, as duas assinaturas podem ser calculadas **a posteriori** a
  partir do `area` do `camundongo_v0.json`, sem reexecutar nada.

## 5 · UM ACRÉSCIMO MEU, SEPARÁVEL

*(Fora do que o Fable pediu — ele disse "nada mais muda". Fica isolado aqui de
propósito, e sai numa linha se ele preferir.)*

O relatório traz também a **distribuição das áreas obtidas** — mínimo, quartis,
máximo —, e não só as três contagens. Não é regra nem veredito: é descrição.

A razão é esta nota: a gente descobriu o anel interno **pensando**, e acertou. Um
terceiro agrupamento que ninguém previu — a borda do Tegaderm, a lamínula, a
sombra do campo — só aparece se os números forem olhados. Contagem em três
caixas esconde o que não tem caixa; um histograma, não.

---

## 6 · O QUE NÃO MUDA

Tudo o mais do `3a27e63c…` e do esboço `cf02c0d9…`: a coroa entre 0,625·D e D
pelos mesmos raios de 145,83 a 233,33 px em L = 700; o mecanismo `ar` de
`mapa_t` e `anel`, excluído e nunca pintado; as mesmas 255, uma rodada, zero
exclusão; semente 20260928; o nulo pareado; a P5b com o limiar n ≥ 8 no dia 0; a
ressalva 7.3 de que a P5b mede tamanho plausível e não acerto, e que o Dice
pareado contra o nulo tem de sair ao lado dela; os três estados; a dependência de
ordem — a rodada 2 só roda depois da etapa 3 da rodada 1; e a decisão, escrita
antes, de que se o `anel()` devolver `None` na maioria das cenas sintéticas com a
coroa excluída, **a rodada 2 não acontece**.

Nenhuma constante do v0.

---

*Adendo escrito pelo Opus em 01/10/2026, a pedido do Fable, com as áreas
conferidas por cálculo e não de cabeça. A etapa 3 da rodada 1 não foi executada
até esta linha.*
