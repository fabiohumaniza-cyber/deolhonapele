"""
sonda_rede.py — sondagem diagnostica de curva (Adendo 69-E). NAO e comparacao.

A mesma U-Net (treina_rede.py, b767471e...), dobra 3 apenas, 300 epocas FIXAS, sem parada
antecipada, retomavel. Usa treina_rede2.roda (286a478e...) com a paciencia desligada.
Pergunta: o Dice de validacao continua subindo depois da epoca 100?
A predicao que o roda() grava no fim NAO e aberta nem analisada.

Uso: python sonda_rede.py <rede_dados.npz> <pasta_saida>
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import treina_rede2 as R

R.PACIENCIA = 10 ** 9
R.MAX_POR_VARIANTE['conv'] = 300


def main(pdados, pasta):
    z = np.load(pdados)
    os.makedirs(pasta, exist_ok=True)
    D = R.T.dobras(z['ferida'])
    R.roda('conv', D, z['X'], z['Y'], z['ferida'], None, 3, pasta, None)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
