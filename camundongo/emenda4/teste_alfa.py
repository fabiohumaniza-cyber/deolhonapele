"""
teste_alfa.py — ensaio da regra da EMENDA 4 no abre_rgb8 do roda_camundongo.py.
Imagens desenhadas por codigo. Nenhum arquivo do banco e aberto.

Prova as quatro saidas da regra:
  RGBA com alfa 255 em todo pixel -> passa, e os 3 canais sao IDENTICOS ao RGB
  RGBA com qualquer alfa != 255   -> PARA
  RGB puro                        -> passa inalterado
  16 bits / tons de cinza         -> PARA (travas antigas, intactas)
"""
import os, sys, tempfile
import numpy as np
from PIL import Image
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from roda_camundongo import abre_rgb8

RNG = np.random.default_rng(20260928)
TMP = tempfile.mkdtemp(prefix='alfa_')
RGB = RNG.integers(0, 256, (120, 90, 3), dtype=np.uint8)


def grava(nome, arr, modo=None):
    p = os.path.join(TMP, nome)
    Image.fromarray(arr, modo) if modo else Image.fromarray(arr)
    (Image.fromarray(arr, modo) if modo else Image.fromarray(arr)).save(p)
    return p


def tenta(p):
    """Devolve ('ok', array, modo) ou ('parado', mensagem)."""
    try:
        a, m = abre_rgb8(p)
        return 'ok', a, m
    except SystemExit as e:
        return 'parado', str(e).splitlines()[0]


casos = []

# 1 RGBA com alfa 255
a255 = np.dstack([RGB, np.full(RGB.shape[:2], 255, np.uint8)])
casos.append(('RGBA alfa 255 em todo pixel', grava('a255.tiff', a255, 'RGBA'), 'passar'))

# 2 RGBA com alfa 200 em todo pixel
a200 = np.dstack([RGB, np.full(RGB.shape[:2], 200, np.uint8)])
casos.append(('RGBA alfa 200 em todo pixel', grava('a200.tiff', a200, 'RGBA'), 'parar'))

# 3 RGBA com UM unico pixel em 254 — o caso traicoeiro
a1 = np.dstack([RGB, np.full(RGB.shape[:2], 255, np.uint8)])
a1[60, 45, 3] = 254
casos.append(('RGBA com 1 pixel de alfa 254', grava('a1.tiff', a1, 'RGBA'), 'parar'))

# 4 RGB puro
casos.append(('RGB puro de 8 bits', grava('rgb.tiff', RGB), 'passar'))

# 5 16 bits
casos.append(('16 bits', grava('u16.tiff', (np.ones((80, 80)) * 30000).astype(np.uint16)), 'parar'))

# 6 tons de cinza 8 bits
casos.append(('tons de cinza', grava('cinza.tiff', RNG.integers(0, 256, (80, 80), dtype=np.uint8)), 'parar'))

print('%-32s %-8s %-8s %s' % ('caso', 'esperado', 'obtido', 'detalhe'))
tudo_ok = True
for nome, p, esperado in casos:
    r = tenta(p)
    obtido = 'passar' if r[0] == 'ok' else 'parar'
    if r[0] == 'ok':
        det = 'modo_pil=%r forma=%s' % (r[2], r[1].shape)
    else:
        det = r[1][:72]
    marca = '' if obtido == esperado else '  <-- ERRADO'
    tudo_ok &= (obtido == esperado)
    print('%-32s %-8s %-8s %s%s' % (nome, esperado, obtido, det, marca))

# a conferencia que importa: o alfa nao mexeu em nenhum valor de cor
est, arr, modo = tenta(casos[0][1])
igual = np.array_equal(arr, RGB)
print('\nRGBA alfa 255 -> os 3 canais sao byte a byte iguais ao RGB original: %s' % igual)
print('modo_pil gravado no JSON para essa imagem: %r (o original, nao o usado)' % modo)
est2, arr2, modo2 = tenta(casos[3][1])
print('RGB puro -> inalterado: %s | modo_pil %r' % (np.array_equal(arr2, RGB), modo2))
print('\nTODOS OS SEIS CASOS COMO ESPERADO: %s' % (tudo_ok and igual))
