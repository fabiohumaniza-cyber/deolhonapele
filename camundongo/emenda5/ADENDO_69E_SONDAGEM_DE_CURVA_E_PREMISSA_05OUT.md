# ADENDO 69-E · sondagem de curva (diagnóstico) e a premissa da nota do 69-D

**05/10/2026, Brasília, 05h39.** Publicado antes de rodar a sondagem.

## 1 · A premissa da nota do Adendo 69-D era falsa

A nota previa a conv "perto de +0,030", porque ela convergiria cedo. O teste
de janelas na curva inteira da rede original (log público, Adendo 67) mostrou
o contrário: nas quatro dobras, o Dice de validação ainda subia entre as
épocas 13–40 e 70–100.

| dobra | média épocas 13–40 (dp) | média épocas 70–100 (dp) | diferença |
|---|---|---|---|
| 0 | 0,873 (0,011) | 0,900 (0,006) | +0,027 |
| 1 | 0,887 (0,012) | 0,926 (0,006) | +0,039 |
| 2 | 0,905 (0,019) | 0,943 (0,004) | +0,038 |
| 3 | 0,781 (0,023) | 0,833 (0,017) | +0,052 |

**O que caiu foi a premissa, não a previsão.** Se a conv sair pior que a
original, por ter parado cedo, a diferença deve subir acima de +0,030: o
contrário do que a nota previa. O resultado decide. O Adendo 69-B não muda.

**A paciência de 30 é curta para esta curva.** Numa subida dessa taxa, com
esse ruído, 30 épocas sem novo máximo podem acontecer mesmo com a rede
melhorando. Isso entra no Adendo 70 como limitação da rede conv. A regra
registrada não muda.

## 2 · A sondagem

**Diagnóstico de curva, sem veredito e fora da comparação.**

| item | escolha |
|---|---|
| rede | a mesma U-Net da original, sem nenhuma mudança |
| dobra | só a 3: maior subida entre janelas (+0,052) e menor Dice de validação |
| épocas | 300, fixas, sem parada antecipada |
| código | `rede/sonda_rede.py`, SHA-256 `0345dcde9c24f86052aca4971e7062c982d7460ab8abeb1a25ec1540432592ae`, que chama `treina_rede2.roda` (`286a478e…`) com a paciência desligada |
| saída usada | só o `log_dobra3.csv` (Dice de validação por época) |
| saída não usada | a predição que o código grava no fim **não é aberta nem analisada** |

**A pergunta.** O Dice de validação continua subindo depois da época 100?

**A regra, fixada agora.** Compara-se a média das épocas 151–200 com a média
das épocas 251–300.
- **Platô:** a diferença é menor que o desvio padrão das épocas 151–200.
  Então 300 épocas bastam, e decide-se, com esse dado, se vale treinar as
  quatro dobras com 300 épocas fixas.
- **Ainda subindo:** a diferença é igual ou maior que esse desvio. Então o
  limite continua restritivo, e o treino das quatro dobras se justifica.

**O que a sondagem não faz.**
- Nenhuma rede nova entra na comparação sem pré-registro próprio.
- O que já está registrado (Adendos 68, 69, 69-A a 69-D) não muda.

**Como roda.** Em paralelo com a fila do Adendo 68, em CPU de 2 núcleos, o
que deixa as duas mais lentas. Estimativa de 3 a 5 horas.

---

*Opus, 05/10/2026. A sondagem não rodou até esta linha.*
