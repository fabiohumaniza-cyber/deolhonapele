# NOTA DE SUBSTITUIÇÃO · a ordem do clique deixou de importar

**01/10/2026, Brasília.** Reparo apontado pelo Fable na revisão do
`mede_anel.py`, antes de o Fabio medir qualquer imagem.

---

## O FURO

A versão `42e77a0d5a973d64aa4c1d402ed5eacc63a48d5d0782bb8273f82aa87f31b388`
calculava:

```
diâmetro = média de |p1 p2| e |p3 p4|
```

Isso **depende da ordem do clique**. Clicando esquerda → cima → direita → baixo,
em vez de esquerda → direita → cima → baixo, as duas "cordas" viram as duas
diagonais do quadrilátero. E o aviso que existia — "as cordas diferem X %" — não
acusaria nada, **porque as duas diagonais são iguais entre si**.

Medido no ensaio, numa elipse 350 × 300:

```
regra antiga, ordem trocada : 461,0 px   ->  29,1 % abaixo do certo
as duas "cordas" seriam 461,0 e 461,0    ->  o aviso NÃO acusaria
```

Em 255 imagens, uma troca de ordem passaria sem deixar rastro. O log guardaria os
cliques certos e o `MEDIDAS.txt` guardaria o número errado.

Nenhuma medida foi feita com a versão furada: ela não chegou a ser usada.

## O REPARO

```
diâmetro = média das DUAS MAIORES entre as 6 distâncias dos 4 pontos
centro   = média dos 4 pontos        (já era independente da ordem)
```

Prova no ensaio: as **24 ordens possíveis** dos mesmos quatro pontos devolvem
**1 diâmetro distinto e 1 centro distinto**. Na ordem trocada acima, agora dá
650,0 px — exato.

**Aviso novo:** se a terceira maior distância passar de **0,80** do diâmetro, os
quatro pontos estão amontoados de um lado e a barra avisa. Medido: quatro pontos
bem espalhados dão 71 % (não avisa); três de um lado só dão 96 % (avisa).

**Na tela**, as duas linhas verdes agora desenham as duas maiores distâncias —
as mesmas que entram na conta, não um par fixo.

## O LIMITE, DECLARADO

As duas maiores são os dois eixos enquanto **b/a > 1/√3 = 0,577** — um splint
visto a cerca de 55°. Abaixo disso a lateral do quadrilátero ultrapassa o eixo
menor e a conta começa a superestimar. Medido:

| b/a | 0,90 | 0,80 | 0,70 | 0,60 | 0,577 | 0,55 | 0,45 |
|---|---|---|---|---|---|---|---|
| erro | 0 | 0 | 0 | 0 | +0,02 % | +1,33 % | +6,78 % |

Fica escrito porque é limite real, não porque seja provável: o detector já exigia
achatamento ≥ 0,80, e a foto é tirada de frente, a 12 cm fixos.

## A SUBSTITUIÇÃO

| | hash | onde |
|---|---|---|
| antes | `42e77a0d5a973d64aa4c1d402ed5eacc63a48d5d0782bb8273f82aa87f31b388` | commit `9fe8dcce5fb4c978745237b5237a91ad7bd8483f` |
| agora | `7bee9991f28740c4ded02f9fe0a0c1a3591113d4d3463dd60e3c677cc7a9861b` | 12.437 B |

| | hash |
|---|---|
| `teste_mede_anel.py` antes | `a4ec0a4a0bd1a5f89781a1ffba289e21dce3017bba7893657fca5c0e75bc695a` |
| `teste_mede_anel.py` agora | `5c02a439ffc8cce893a61ab5268067e41e2c5d7f2d36119905c15bfedd3f28cc` (7.345 B) |

O arquivo antigo foi **substituído no mesmo caminho**, e não movido para pasta
nova como se fez com o `roda_camundongo.py`. A razão: ele nunca foi confirmado
pelo Fabio e nunca produziu medida nenhuma — não há resultado a proteger. Os
bytes antigos continuam recuperáveis no commit acima, e estão declarados aqui.
Se o Fable preferir o outro tratamento, é um `git mv` e uma linha.

A `NOTA_MEDIDA_MANUAL_01OUT.md`
(`0f8515301a5e9fdf6329599b535d607228ba9ed8664648ee9481ac5daee8d6cd`) **não é
alterada**: ela cita o hash antigo, e é assim que fica. Esta nota é que diz que
aquele hash foi substituído.

---

*Opus, 01/10/2026. Hashes colados do `sha256sum`. Nenhuma medida existe até esta
linha.*
