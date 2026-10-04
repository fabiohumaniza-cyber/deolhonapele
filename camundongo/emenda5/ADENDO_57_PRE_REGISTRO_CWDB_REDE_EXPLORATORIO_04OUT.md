# ADENDO 57 · pré-registro EXPLORATÓRIO: U-Net × motor no banco humano (ComplexWoundDB)

**04/10/2026, Brasília, 15h25.** Publicado antes de qualquer treino neste banco.

## A liberação

A regra *"não tocar no CWDB"* era do Fabio. Ele liberou por escrito, às 15h10:

> *"liberado tem q entrar junto no emsmo artigo"*

Às 15h09 ele tinha dito o motivo:

> *"agora qndo a gente usou nos humanos a gente nao delimitou campo foi um erro q
> aprendemos"*

## Status: EXPLORATÓRIO, sem veredito

- As 27 imagens já foram vistas e o motor foi ajustado olhando para elas. O
  manuscrito já declara o braço humano como desenvolvimento.
- A condição 3, a do recorte, já era pós-hoc.
- Por isso a comparação **favorece o motor**, e isso fica dito aqui, antes de
  qualquer resultado.
- Não há previsão com veredito. Sai a tabela.

## O desenho

| | escolha |
|---|---|
| campo | **o mesmo recorte que o motor usou na condição 3**: K = 1,40 × maior eixo declarado, centro clicado pelo operador (`resultado_27_cond3.json`, `a98227b0…`) |
| rede | a mesma U-Net do Adendo 52 (`treina_rede.py`): épocas, lote, otimizador, aumento e checkpoint iguais; 2 classes (fundo e ferida) |
| rótulo | a máscara de **cada um dos 4 especialistas**, como amostra separada, binarizada como no `roda_27.py` |
| divisão | 5 dobras por imagem, sorteadas com semente 20261004; 3 imagens de validação por dobra; cada imagem é predita por um modelo que nunca a viu |
| métrica | por imagem, a **mediana do Dice contra os 4**, na imagem inteira, a mesma do `dice_mediana` do motor (K = 1,4) |
| comparação | mediana da diferença pareada motor − rede, IC 95 % por bootstrap por imagem (2000 sorteios, semente 20261004), Wilcoxon, e o recorte por grupo: elegíveis e não elegíveis |

**As dobras:**

| dobra | imagens de teste |
|---|---|
| 0 | 20, 22, 26, 23, 17, 2 |
| 1 | 1, 15, 18, 19, 9, 6 |
| 2 | 14, 21, 4, 16, 13 |
| 3 | 8, 3, 27, 5, 10 |
| 4 | 11, 12, 24, 7, 25 |

## Arquivos

| arquivo | SHA-256 |
|---|---|
| `rede/cwdb_rede.py` | `4b50302a3ae21e8b795caaa821efc27dc2effc16869199a1e278bd0d944ab6e8` |
| `cwdb_dados.npz` (108 amostras = 27 imagens × 4 especialistas) | `84d15b848699b47458b0bce6f94f5b5ae96c1dc7f63f08700cdfef18153034b8` |

O treino começa **depois** de terminarem as 4 dobras do camundongo, para não
atrasar a P19 e a P20.

## Limites, declarados agora

- **São 27 imagens.** A rede treina com cerca de 19 por dobra, um número
  desfavorável a ela.
- **O motor foi desenvolvido nessas 27 imagens.** A rede nunca vê a imagem que
  vai testar.
- A mediana de 4 especialistas que discordam entre si tem teto. O piso entre
  avaliadores sai ao lado.

---

*Opus, 04/10/2026. Nenhuma rede foi treinada no CWDB até esta linha.*
