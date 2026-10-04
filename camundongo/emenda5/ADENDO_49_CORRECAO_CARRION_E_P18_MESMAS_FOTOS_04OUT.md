# ADENDO 49 · correção do número do Carrión et al. e P18, comparação nas mesmas fotos

**04/10/2026, Brasília, 12h40.** Corrige o Adendo 41 (`ee2df6a`), que **não se
edita**. A P18 foi publicada **antes** de qualquer Dice ser filtrado para as
fotos de teste do trabalho original.

## 1 · CORREÇÃO

O Adendo 41 diz: *"Não é comparável direto com o 0,96 do Carrión et al. …
o conjunto de teste tinha ~32 fotos"*. **Está errado no número.**

| | Dice | IoU |
|---|---|---|
| treino | 0,96 | 0,93 |
| **teste** (U-Net com pós-processamento) | **0,8665** | **0,8164** |

**Fonte:** Carrión et al. 2022, texto completo
(escholarship.org/content/qt8tb7r19d/qt8tb7r19d.pdf). O 0,96 é do treino. O
número de teste, que é o que se compara, é **0,8665**.

- No artigo, o traçado de referência foi feito por **um anotador leigo**, que
  traçou com o Labelme todas as fotos.
- O Emílio também é leigo. Nos dois estudos, a referência é a de um leigo.

## 2 · O CONJUNTO DE TESTE DELES, CRUZADO COM O NOSSO

O notebook público `Wound_Segmentation_Inference_and_Results_(external).ipynb`
(github.com/Gomez-Lab/WoundSizeEstimation, commit `45fb2d2`, célula 19) imprime
as **32 fotos** da pasta `test_images`:

```
Day 0_A8-1-L  Day 0_Y8-4-R  Day 10_Y8-2-L Day 10_Y8-3-R Day 11_A8-3-L Day 11_A8-5-R
Day 12_A8-3-R Day 12_A8-5-L Day 13_Y8-2-R Day 13_Y8-3-L Day 14_A8-4-L Day 14_Y8-1-R
Day 15_A8-1-R Day 15_Y8-4-L Day 1_A8-4-R  Day 1_Y8-1-L  Day 2_Y8-2-L  Day 2_Y8-3-R
Day 3_A8-3-L  Day 3_A8-5-R  Day 4_A8-3-R  Day 4_A8-5-L  Day 5_Y8-2-R  Day 5_Y8-3-L
Day 6_A8-4-L  Day 6_Y8-1-R  Day 7_A8-1-R  Day 7_Y8-4-L  Day 8_A8-1-L  Day 8_Y8-1-L
Day 8_Y8-4-R  Day 9_A8-4-R
```

| na nossa declaração | n |
|---|---|
| Fabio mediu (ok/nada) | 19 |
| Fabio excluiu (NAO_TRACAVEL, PELO, BORDA_PARCIAL) | 7 |
| fora das 201 | 6 |

- **3 das nossas 30 impossíveis** estão nesse teste: Day 10_Y8-2-L,
  Day 13_Y8-2-R e Day 14_A8-4-L.
- **2 das 14 duvidosas** também: Day 12_A8-3-R e Day 12_A8-5-L.

### Observações factuais, sem juízo

- As 32 cobrem as **16 feridas**, 2 fotos de cada. O texto do artigo descreve
  uma divisão **por ferida**: 12 de treino, 2 de validação e 2 de teste. Não
  sabemos se essa pasta é o conjunto do Dice 0,8665.
- Os traçados (`consistent_labels_full/*.json`) **não estão** no GitHub nem no
  Dryad. O repositório aponta só para um vídeo no Google Drive.

## 3 · P18 — o nosso Dice nas MESMAS fotos de teste deles

**Aposta do Fabio** (12h36: *"nosso dice foi melhor q o deles"*), feita antes do
filtro.

- **Conjunto:** das 32 fotos acima, as que o Emílio marcou `TRACADA`.
- **P18:** o Dice(r4, Emílio) **médio** nesse conjunto é **≥ 0,8665**.
- **Ao lado, sem veredito:**
  - mediana;
  - n;
  - Dice r3 e nulo;
  - as mesmas contas em **todas** as 32 que o Emílio traçou, incluindo as
    imaginadas, como fez o trabalho original.
- **Fonte:** só o `dados/emilio_por_imagem.tsv` já publicado (`8f38658f…`).
  Nenhum dado novo é gerado; a conta é um filtro.

### Limites, declarados agora

- O anotador é outro, e a regra de borda é outra.
- Ali havia uma rede **treinada**. Aqui é uma regra escrita que **nunca viu**
  o Emílio.
- Mesmo com P18 confirmada, a frase permitida no artigo é: *"nas mesmas fotos
  de teste, o Dice do motor contra um traçador leigo independente foi X,
  contra 0,8665 relatado"*. **Não** é *"melhor que o deles"* sem esses
  limites.

---

*Opus, 04/10/2026. Nenhum Dice foi filtrado para as 32 fotos até esta linha.*
