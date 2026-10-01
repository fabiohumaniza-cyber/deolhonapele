"""
teste_driver.py — ensaio das quatro etapas do roda_camundongo.py num BANCO
SINTETICO desenhado por codigo. Nenhuma imagem do banco real e usada.

O que se testa aqui e o DRIVER, nao o resultado: se as quatro etapas correm,
se o recorte que nao cabe e completado por replicacao (e nao por preto), se a
pendencia de escala barra a etapa 3, se os estratos e o painel da P3 saem.
Semente 20260928.
"""
import os, sys, shutil, json, subprocess
import numpy as np
from PIL import Image
sys.path.insert(0, '/home/claude/cam')

RNG = np.random.default_rng(20260928)
BASE = '/home/claude/cam/ensaio'
TIF, SAI = BASE + '/tiffs', BASE + '/saida'
for d in (TIF, SAI):
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)

DIAS = [0, 3, 6, 9, 12, 15]
FER = [('A8-%d' % i, s) for i in (1, 3) for s in ('L', 'R')] + \
      [('Y8-%d' % i, s) for i in (1, 2) for s in ('L', 'R')]
mapa = []


def cena(H, W, cx, cy, a, b, th, d_ferida_mm, pxmm, com_anel=True):
    yy, xx = np.mgrid[0:H, 0:W]
    X = (xx - cx) * np.cos(th) + (yy - cy) * np.sin(th)
    Y = -(xx - cx) * np.sin(th) + (yy - cy) * np.cos(th)
    im = np.full((H, W, 3), 180.)
    if com_anel:
        r = np.hypot(X / a, Y / b)
        im[(r >= 10 / 16) & (r <= 1.0)] = 45.
    if d_ferida_mm > 0:
        im[np.hypot(xx - cx, yy - cy) <= (d_ferida_mm / 2) * pxmm] = 60.
    return np.clip(im + RNG.normal(0, 4, im.shape), 0, 255).astype(np.uint8)


n = 0
for dia in DIAS:
    d_fer = max(0.6, 6.0 * (1 - dia / 18.0))           # ferida encolhendo
    for k, (an, lado) in enumerate(FER):
        pxmm = float(RNG.uniform(34, 46))
        a = 8.0 * pxmm
        H = W = int(a * 2 * 1.9)
        cx, cy = W / 2, H / 2
        com_anel = True
        if dia == 9 and k == 0:                        # 1 sem anel -> estrato 3.1
            com_anel = False
        if dia == 12 and k == 1:                        # anel na beira -> replicacao
            cx = a * 1.05
        im = cena(H, W, cx, cy, a, a * float(RNG.uniform(0.90, 1.0)),
                  np.deg2rad(RNG.uniform(-15, 15)), d_fer, pxmm, com_anel)
        nome = 'D%02d_%s_%s.tif' % (dia, an, lado)
        Image.fromarray(im).save(os.path.join(TIF, nome))
        mapa.append('%s\t%d\t%s\t%s' % (nome, dia, an, lado))
        n += 1
with open(os.path.join(SAI, 'MAPA_FERIDA_DIA.tsv'), 'w') as f:
    f.write('# nome\tdia\tanimal\tlado\n' + '\n'.join(mapa) + '\n')
print('banco sintetico: %d imagens\n' % n)

R = lambda *a: subprocess.run([sys.executable, '/home/claude/cam/roda_camundongo.py'] + list(a),
                              capture_output=True, text=True)

print('=== etapa 1 detectar ===')
o = R('detectar', TIF, SAI); print(o.stdout.strip().splitlines()[-1]); print(o.stderr.strip()[-200:])

print('\n=== etapa 3 SEM a etapa 2 (tem de parar) ===')
o = R('rodar', TIF, SAI)
print('saiu com codigo %d | %s' % (o.returncode, (o.stdout + o.stderr).strip().splitlines()[-1][:90]))

print('\n=== etapa 2 medir ===')
reg = json.load(open(os.path.join(SAI, 'deteccao_camundongo.json')))
pend = [a for a, v in reg.items() if not v['deteccao']['ok']]
with open(os.path.join(SAI, 'MEDIDAS.txt'), 'w') as f:
    for a in pend:
        f.write('%s\tSEM_ANEL\n' % a)        # o operador declarou sem anel visivel
print('pendentes declarados SEM_ANEL: %d' % len(pend))
o = R('medir', SAI, os.path.join(SAI, 'MEDIDAS.txt')); print(o.stdout.strip())

print('\n=== etapa 3 rodar ===')
o = R('rodar', TIF, SAI)
ls = o.stdout.strip().splitlines()
print('\n'.join(ls[:3])); print('…'); print('\n'.join(ls[-3:])); print(o.stderr.strip()[-300:])

print('\n=== etapa 4 relatorio ===')
o = R('relatorio', SAI)
print(o.stdout.strip()); print(o.stderr.strip()[-300:])

d = json.load(open(os.path.join(SAI, 'camundongo_v0.json')))['imagens']
rep = [l for l in d.values() if l['fracao_replicada'] > 0]
sem = [l for l in d.values() if l['estrato'] == 'sem escala propria']
print('\n--- conferencias do driver ---')
print('imagens com recorte replicado : %d  (fracao max %.3f)'
      % (len(rep), max([l['fracao_replicada'] for l in rep], default=0)))
print('imagens no estrato sem escala : %d  (unidade %s, criterio %s)'
      % (len(sem), sem[0]['unidade'] if sem else '—', sem[0]['criterio'] if sem else '—'))
print('imagens com medida obtida     : %d de %d' % (sum(1 for l in d.values() if l['obtida']), len(d)))
print('painel P3 emitido             : %s'
      % os.path.isfile(os.path.join(SAI, 'PAINEL_P3.txt')))
