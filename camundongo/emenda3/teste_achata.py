"""
teste_achata.py — ensaio do achata_banco.py numa ARVORE SINTETICA que imita a
estrutura descrita no README do Dryad. Nenhum byte do banco real e tocado.
Os "TIFFs" aqui sao bytes aleatorios com extensao .tiff: o achata_banco.py nao
decodifica imagem nenhuma, so copia e hasheia — e e exatamente isso que se testa.
"""
import os, sys, shutil, subprocess, hashlib
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(AQUI, 'ensaio_achata')
RNG = np.random.default_rng(20260928)
ANIMAIS = ['A8-1', 'A8-3', 'A8-4', 'A8-5', 'Y8-1', 'Y8-2', 'Y8-3', 'Y8-4']


def arvore(raiz, faltas=(('Y8-2', 'Right', 9),), extras=(), sobra=None):
    shutil.rmtree(raiz, ignore_errors=True)
    n = 0
    for an in ANIMAIS:
        for lado in ('Left', 'Right'):
            d = os.path.join(raiz, an, '%s wound' % lado)
            os.makedirs(d)
            for dia in range(16):
                if (an, lado, dia) in faltas:
                    continue
                with open(os.path.join(d, 'Day %d.tiff' % dia), 'wb') as f:
                    f.write(bytes(RNG.integers(0, 256, 2048, dtype=np.uint8)))
                n += 1
            for dia in extras:
                with open(os.path.join(d, 'Day %d.tiff' % dia), 'wb') as f:
                    f.write(bytes(RNG.integers(0, 256, 2048, dtype=np.uint8)))
                n += 1
    if sobra:
        p = os.path.join(raiz, sobra)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'wb') as f:
            f.write(b'\x00' * 32)
        n += 1
    return n


R = lambda raiz, dest: subprocess.run(
    [sys.executable, os.path.join(AQUI, 'achata_banco.py'), raiz, dest],
    capture_output=True, text=True)

shutil.rmtree(BASE, ignore_errors=True)

print('=== arvore completa do README (255) ===')
raiz = os.path.join(BASE, 'ok'); dest = os.path.join(BASE, 'plano')
n = arvore(raiz); print('arvore montada com %d .tiff' % n)
o = R(raiz, dest)
ls = (o.stdout + o.stderr).strip().splitlines()
print('\n'.join(ls[:2])); print('…'); print('\n'.join(ls[-4:]))
print('codigo de saida %d' % o.returncode)

cop = sorted(f for f in os.listdir(dest) if f.lower().endswith('.tiff'))
print('arquivos na pasta plana: %d | nomes unicos: %d' % (len(cop), len(set(cop))))
print('exemplos: %s … %s' % (cop[0], cop[-1]))

# os bytes sao os mesmos?
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
man = [l.split('\t') for l in open(os.path.join(dest, 'MANIFESTO_ACHATAMENTO.tsv'))
       if not l.startswith('#')]
dif = [m for m in man if sha(m[0]) != sha(os.path.join(dest, m[1]))]
print('linhas no manifesto: %d | copias que divergem da origem: %d' % (len(man), len(dif)))
mapa = [l for l in open(os.path.join(dest, 'MAPA_FERIDA_DIA.tsv')) if not l.startswith('#')]
print('linhas no mapa: %d' % len(mapa))
print('ultima linha do mapa: %s' % mapa[-1].strip())

print('\n=== 254 arquivos: falta um nao declarado (tem de parar) ===')
r2 = os.path.join(BASE, 'faltando'); d2 = os.path.join(BASE, 'plano2')
arvore(r2, faltas=(('Y8-2', 'Right', 9), ('A8-4', 'Left', 3)))
o = R(r2, d2)
print('codigo %d | %s' % (o.returncode, (o.stdout + o.stderr).strip().splitlines()[-1][:90]))
print('arquivos copiados: %d' % len([f for f in os.listdir(d2) if f.endswith('.tiff')] if os.path.isdir(d2) else []))

print('\n=== 255 arquivos mas conjunto errado: Day 7 de A8-1-L trocado por Day 16 (tem de parar) ===')
r3 = os.path.join(BASE, 'conjunto'); d3 = os.path.join(BASE, 'plano3')
arvore(r3, faltas=(('Y8-2', 'Right', 9), ('A8-1', 'Left', 7)))
with open(os.path.join(r3, 'A8-1', 'Left wound', 'Day 16.tiff'), 'wb') as f:
    f.write(b'\x01' * 2048)
print('arvore com %d .tiff' % sum(len([a for a in f if a.endswith('.tiff')])
                                  for _b, _d, f in os.walk(r3)))
o = R(r3, d3)
sai = (o.stdout + o.stderr).strip().splitlines()
print('codigo %d | %s' % (o.returncode, ' / '.join(s.strip()[:70] for s in sai[-3:])))

print('\n=== .tiff fora da convencao (tem de parar) ===')
r4 = os.path.join(BASE, 'fora'); d4 = os.path.join(BASE, 'plano4')
arvore(r4, sobra=os.path.join('solta', 'foto.tiff'))
o = R(r4, d4)
print('codigo %d | %s' % (o.returncode, (o.stdout + o.stderr).strip().splitlines()[-1][:90]))

print('\n=== rodar duas vezes na mesma pasta plana da o mesmo resultado? ===')
h1 = sha(os.path.join(dest, 'MANIFESTO_ACHATAMENTO.tsv'))
hm1 = sha(os.path.join(dest, 'MAPA_FERIDA_DIA.tsv'))
o = R(raiz, dest)
print('codigo %d | manifesto igual: %s | mapa igual: %s'
      % (o.returncode,
         sha(os.path.join(dest, 'MANIFESTO_ACHATAMENTO.tsv')) == h1,
         sha(os.path.join(dest, 'MAPA_FERIDA_DIA.tsv')) == hm1))
