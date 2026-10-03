# ADENDO 13 · errata — dois erros do Opus em documentos com hash

**03/10/2026, Brasília, 06h50.** Os Adendos citados abaixo **não são alterados**:
cada um permanece com o hash que tem. As correções vivem aqui, pela regra de
imutabilidade.

Os dois erros são do Opus, que redigiu os documentos. Nenhum deles afetou a
execução da rodada, os arquivos de entrada ou o motor.

---

## 1 · ADENDO 9, §9: "O MOTOR JÁ EXCLUI O ANEL POR CONSTRUÇÃO"

### O que estava escrito

> *"O motor já exclui o anel por construção, pelo mecanismo `ar` congelado em
> `motor_v0_funcoes.py` (`m &= ~ar`, `liv = ~ar`, `am &= ~ar`): a região do
> artefato é **excluída, nunca pintada**."*

### O que é verdade

Na **rodada 1**, o `ar` está **desligado**. O `roda_camundongo.py`
(`8c1f6e4d…`), na função `roda_motor`, chama:

```python
cache[kt] = M.mapa_t(cache[ka], g, dsl, al, 4, None)
r = M.anel(cache[kt], lo, hi, 3, None, diam)
```

O `None` é o parâmetro `ar`. A rodada 1 rodou **sem declaração de artefato**.

### Isto não é defeito da rodada — é o desenho dela

O `PRE_REGISTRO_RODADA2_01OUT.md` diz, desde 01/10:

> *"Isto não é conserto da rodada 1. As duas saem no relatório, lado a lado. A
> rodada 1 continua sendo o resultado do motor **sem ajuda**; a rodada 2 mede
> quanto daquilo era o splint."*

O mecanismo `ar` existe no motor congelado e é o que a **rodada 2** usa, com a
coroa de 145,83 a 233,33 px. A frase do Adendo 9 descreveu a rodada 2 como se
fosse a rodada 1. **O erro está na descrição, não na execução.** Nada a
refazer.

## 2 · ADENDOS 9 E 10: OS COMENTÁRIOS FORAM CONTADOS

### O que tinha sido declarado antes

O Adendo 6, §2.1, e o cabeçalho do próprio `CLASSIFICACAO.txt`:

> *"comentário: texto livre, descritivo. NÃO é categoria e não entra em
> contagem."*

### O que foi feito depois

O Adendo 9 (§§2 e 6) e o Adendo 10 (§2) reportaram **frequências de palavras
nos comentários** — pelo 55, reflexo 39, plástico 33; e, entre as `n`, pelo 30
contra plástico 18 — como se fossem contagens.

### O que tornou o erro concreto

O operador declarou, em 02/10 às 20h22, depois do censo e antes de qualquer
conferência:

> *"tinha mais reflexo eu q marquei e nao coloquei"*

Ou seja: ele viu reflexo em mais imagens do que escreveu. O comentário é
**subregistro** por natureza — escreve-se o que chama atenção, não tudo o que se
vê.

### Consequências, uma a uma

1. **Os números de pelo, plástico e reflexo nos comentários são pisos de
   menção, não contagens de ocorrência.** Devem ser lidos como "pelo menos N
   imagens em que o operador julgou valer a pena escrever isto".

2. **A direção pelo > plástico provavelmente se sustenta.** Não há motivo para o
   subregistro afetar uma palavra mais que a outra. Mas a razão 30 : 18 não é
   uma medida.

3. **A correção do Adendo 9, §6, fica enfraquecida.** Ela dizia que reflexo não
   é obstáculo humano porque 35 das 39 menções estavam em imagens `v`. Com o
   subregistro declarado, essa razão não se sustenta. A hipótese do Adendo 8,
   §3 — de que o filme age pelo mecanismo do reflexo — volta ao estado de **não
   confirmada e não refutada**.

4. **Para que reflexo, pelo no leito e sangue virem contagem**, é preciso uma
   passada própria, com botão para cada um, no mesmo modelo da marca `p`. Ela
   está prevista e será registrada antes de ser feita.

## 3 · O QUE NÃO É AFETADO

As classes `v`/`c`/`n`/`d` e a marca `p` **são** contagens: foram declaradas por
botão, imagem a imagem, com vocabulário fechado. Os números do Adendo 10 que
vêm delas — 132 `v`, 62 `n`, 52 `d`, 9 `c`, 116 `p`, os 70 do braço principal,
zero `v` entre as 51 sem anel — **continuam valendo**, sem ressalva.

O mesmo para toda a medida manual dos Adendos 5, 7 e 11.

---

*Opus, 03/10/2026. Dois erros de redação, ambos do Opus, nenhum de execução.*
