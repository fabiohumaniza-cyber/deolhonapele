# ADENDO 46 · aplicativo dos enfermeiros v4 — só o botão "Começar"

**04/10/2026, Brasília, 12h15.** No teste do Fabio no próprio celular, às 12h13,
o botão "Começar" do v3 não avançava. Ele ficava desativado até todos os campos
estarem certos, sem dizer o que faltava. Nenhum enfermeiro recebeu o v3.

## O que muda (só a interface)

- O botão fica **sempre ativo**. Se faltar algo, ele mostra em vermelho **o
  que falta**: nome e sobrenome, número do COREN, UF com 2 letras ou as duas
  caixas.
- O COREN aceita ponto e traço, e a UF aceita espaço sobrando.

**Não muda:** as 74 fotos, os códigos e a chave. A `_CHAVE_enfermeiros_v4.json`
tem o mesmo conteúdo da v3 (`2b8a6d6d…`).

| arquivo | SHA-256 |
|---|---|
| `tpl_app_enfermeiros_v4.html` | `21b7b023b62c48b94d94f3a2dacccab595d1d8b1cd161bf12ed7b41a9d8b9428` |
| `monta_app_enfermeiros_v4.py` | `ef6067bf014b520e27886f0d8688c0949a40e59d06045fc1e5012be6b1eb7b7f` |
| `de_olho_na_pele_enfermeiros_v4.html` (o que vai aos enfermeiros) | `2f676f38a7482410adab65d5413980e92a317c20441f0a091170056ff249d334` |

---

*Opus, 04/10/2026. Nenhuma resposta de enfermeiro existe até esta linha.*
