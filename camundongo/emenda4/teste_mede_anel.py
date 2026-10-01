"""
teste_mede_anel.py — ensaio do mede_anel.py SEM abrir janela e SEM tocar no
banco. Testa as tres coisas que podem estragar a medida:

  1. a aritmetica dos 4 cliques (circulo, elipse, deslocado, girado)
  2. o formato da linha gravada — tem de ser aceito pela etapa 2 do driver
  3. a retomada: imagem ja medida nao volta para a fila

O tkinter nao e importado: no mede_anel.py ele fica dentro de main().
"""
import os, sys, json, math, shutil, subprocess, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from mede_anel import calcula, le_pendentes, le_feitas, ANEL_MM

print('=== 1. aritmetica dos 4 cliques ===')
print('%-34s %-22s %-22s' % ('caso', 'diametro', 'centro'))


def cardeais(cx, cy, a, b, th=0.0):
    """4 pontos nos extremos de uma elipse de semieixos a e b, girada de th."""
    pts = []
    for dx, dy in ((-a, 0), (a, 0), (0, -b), (0, b)):
        x = cx + dx * math.cos(th) - dy * math.sin(th)
        y = cy + dx * math.sin(th) + dy * math.cos(th)
        pts.append((x, y))
    return [pts[0], pts[1], pts[2], pts[3]]


casos = [
    ('circulo r=350, centro (1500,2000)', cardeais(1500, 2000, 350, 350), 700.0, (1500, 2000)),
    ('elipse 350 x 300 (b/a 0,857)', cardeais(1500, 2000, 350, 300), 650.0, (1500, 2000)),
    ('circulo deslocado p/ canto', cardeais(380, 410, 290, 290), 580.0, (380, 410)),
    ('elipse girada 25 graus', cardeais(1500, 2000, 350, 300, math.radians(25)), 650.0, (1500, 2000)),
]
ok = True
for nome, pts, d_alvo, c_alvo in casos:
    d, cx, cy, c1, c2 = calcula(pts)
    bate = abs(d - d_alvo) < 1e-6 and abs(cx - c_alvo[0]) < 1e-6 and abs(cy - c_alvo[1]) < 1e-6
    ok &= bate
    print('%-34s %-22s %-22s %s' % (nome, '%.3f (alvo %.1f)' % (d, d_alvo),
                                    '(%.1f, %.1f)' % (cx, cy), '' if bate else '<-- ERRADO'))
print('\ndiametro = media das duas cordas; na elipse 350x300 isso da %.1f, que e a'
      ' media dos eixos — e o que foi pedido, nao o eixo maior.' % 650.0)
print('o giro nao muda nada: as cordas sao as mesmas, so rodadas.')

print('\n=== 2. o formato e aceito pela etapa 2 do driver? ===')
TMP = tempfile.mkdtemp(prefix='med_')
reg = {'_meta': {'sha256_mapa_ferida_dia': 'x'}}
nomes = ['Day 0_A8-1-L.tiff', 'Day 1_A8-1-L.tiff', 'Day 2_A8-1-L.tiff']
for n in nomes:
    reg[n] = {'arquivo': n, 'sha256': 'z', 'modo_pil': 'RGBA',
              'deteccao': {'ok': False, 'motivo': 'setores;residuo'},
              'px_mm': None, 'escala_manual': False}
json.dump(reg, open(os.path.join(TMP, 'deteccao_camundongo.json'), 'w'), indent=1)

# linhas escritas EXATAMENTE como o mede_anel.py escreve
d, cx, cy, _, _ = calcula(cardeais(1500, 2000, 350, 350))
with open(os.path.join(TMP, 'MEDIDAS.txt'), 'w', encoding='utf-8') as f:
    f.write('# nome\tdiametro_px\tcentro_x_px\tcentro_y_px   (ou SEM_ANEL)\n')
    f.write('%s\t%.3f\t%.3f\t%.3f\n' % (nomes[0], d, cx, cy))
    f.write('%s\t%.3f\t%.3f\t%.3f\n' % (nomes[1], d * 0.9, cx, cy))
    f.write('%s\tSEM_ANEL\n' % nomes[2])

o = subprocess.run([sys.executable, os.path.join(AQUI, 'roda_camundongo.py'),
                    'medir', TMP, os.path.join(TMP, 'MEDIDAS.txt')],
                   capture_output=True, text=True)
print('codigo de saida %d | %s' % (o.returncode, (o.stdout + o.stderr).strip().splitlines()[-1]))
com = json.load(open(os.path.join(TMP, 'deteccao_camundongo_com_manual.json')))
print('px/mm gravado para a 1a: %.4f   (diametro %.1f / %.0f mm = %.4f)'
      % (com[nomes[0]]['px_mm'], d, ANEL_MM, d / ANEL_MM))
print('centro gravado para a 1a: %s' % com[nomes[0]]['centro_manual'])
print('estrato da 3a (SEM_ANEL): %r | px_mm %r'
      % (com[nomes[2]]['estrato'], com[nomes[2]]['px_mm']))
ok &= (o.returncode == 0 and abs(com[nomes[0]]['px_mm'] - d / ANEL_MM) < 1e-9
       and com[nomes[2]]['estrato'] == 'sem escala propria')

print('\n=== 3. retomada: o que ja foi medido nao volta para a fila ===')
with open(os.path.join(TMP, 'PENDENTES_ESCALA_MANUAL.txt'), 'w', encoding='utf-8') as f:
    f.write('# cabecalho de comentario\n')
    for n in nomes:
        f.write('%s\t\t\t\n' % n)
pend = le_pendentes(os.path.join(TMP, 'PENDENTES_ESCALA_MANUAL.txt'))
feitas = le_feitas(os.path.join(TMP, 'MEDIDAS.txt'))
fila = [n for n in pend if n not in feitas]
print('pendentes lidas: %d | ja feitas: %d | fila: %d %s'
      % (len(pend), len(feitas), len(fila), fila))
ok &= (len(pend) == 3 and len(feitas) == 3 and len(fila) == 0)

# e uma sessao parcial: so a primeira medida
with open(os.path.join(TMP, 'PARCIAL.txt'), 'w', encoding='utf-8') as f:
    f.write('# cab\n%s\t1.0\t2.0\t3.0\n' % nomes[0])
fila2 = [n for n in pend if n not in le_feitas(os.path.join(TMP, 'PARCIAL.txt'))]
print('sessao interrompida apos 1 de 3 -> fila na volta: %d %s' % (len(fila2), fila2))
ok &= (len(fila2) == 2)

shutil.rmtree(TMP, ignore_errors=True)
print('\nTUDO COMO ESPERADO: %s' % ok)
