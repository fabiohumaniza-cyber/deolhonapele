"""
teste_mede_anel.py — ensaio do mede_anel.py SEM abrir janela e SEM tocar no
banco. Testa as tres coisas que podem estragar a medida:

  1. a aritmetica dos 4 cliques (circulo, elipse, deslocado, girado)
  2. o formato da linha gravada — tem de ser aceito pela etapa 2 do driver
  3. a retomada: imagem ja medida nao volta para a fila

O tkinter nao e importado: no mede_anel.py ele fica dentro de main().
"""
import os, sys, json, math, shutil, subprocess, tempfile, itertools
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from mede_anel import calcula, le_pendentes, le_feitas, ANEL_MM, FRAC_3A

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
    d, cx, cy, c1, c2, c3 = calcula(pts)
    bate = abs(d - d_alvo) < 1e-6 and abs(cx - c_alvo[0]) < 1e-6 and abs(cy - c_alvo[1]) < 1e-6
    ok &= bate
    print('%-34s %-22s %-22s %s' % (nome, '%.3f (alvo %.1f)' % (d, d_alvo),
                                    '(%.1f, %.1f)' % (cx, cy), '' if bate else '<-- ERRADO'))
print('\ndiametro = media das DUAS MAIORES entre as 6 distancias; na elipse 350x300'
      ' isso da %.1f,\nque e a media dos eixos — o que foi pedido, nao o eixo maior.'
      ' O giro nao muda nada.' % 650.0)

print('\n=== 1b. REPARO DO FABLE: a ordem do clique nao pode importar ===')
base = cardeais(1500, 2000, 350, 300)          # esquerda, direita, cima, baixo
d_ref, cx_ref, cy_ref, _, _, _ = calcula(base)
vals, cents = set(), set()
for perm in itertools.permutations(base):
    d, cx, cy, _, _, _ = calcula(list(perm))
    vals.add(round(d, 9)); cents.add((round(cx, 9), round(cy, 9)))
print('as 24 ordens possiveis dos mesmos 4 pontos ->  diametros distintos: %d  |  centros distintos: %d'
      % (len(vals), len(cents)))
print('valor unico: %.3f  (referencia %.3f)' % (list(vals)[0], d_ref))
ok &= (len(vals) == 1 and len(cents) == 1)

# o erro que isso conserta, medido na versao antiga
troca = [base[0], base[2], base[1], base[3]]   # esquerda, cima, direita, baixo
diag1 = math.hypot(troca[1][0] - troca[0][0], troca[1][1] - troca[0][1])
diag2 = math.hypot(troca[3][0] - troca[2][0], troca[3][1] - troca[2][1])
antigo = (diag1 + diag2) / 2.0
print('\nse a ordem fosse esquerda-cima-direita-baixo:')
print('  regra ANTIGA (cordas 1-2 e 3-4): %.1f px  -> %.1f %% abaixo do certo'
      % (antigo, (1 - antigo / d_ref) * 100))
print('  as duas "cordas" seriam as diagonais, iguais entre si (%.1f e %.1f):'
      ' o aviso de diferenca NAO acusaria.' % (diag1, diag2))
print('  regra NOVA (duas maiores): %.1f px  -> exata' % calcula(troca)[0])

print('\n=== 1c. ate onde as duas maiores sao os dois eixos ===')
print('%-12s %-10s %-12s %-12s' % ('b/a', 'diam', 'alvo', ''))
for ba in (1.00, 0.90, 0.80, 0.70, 0.60, 0.577, 0.55, 0.45):
    a, b = 350.0, 350.0 * ba
    d = calcula(cardeais(0, 0, a, b))[0]
    alvo = a + b
    print('%-12.3f %-10.2f %-12.2f %s' % (ba, d, alvo,
          'ok' if abs(d - alvo) < 1e-6 else 'degrada (%+.2f %%)' % ((d / alvo - 1) * 100)))
print('limite teorico: a lateral passa o eixo menor quando b/a < 1/raiz(3) = %.3f,'
      ' ou seja\num splint visto a ~55 graus. O detector ja exigia achatamento >= 0,80.' % (1 / math.sqrt(3)))

print('\n=== 1d. aviso de pontos amontoados (3a maior > %.0f%% do diametro) ===' % (FRAC_3A * 100))
for nome, pts in (('4 pontos bem espalhados', cardeais(0, 0, 350, 350)),
                  ('3 pontos de um lado so', [(-350, 0), (-330, 120), (-300, -150), (350, 0)])):
    d, _, _, c1, c2, c3 = calcula(pts)
    frac = c3 / d
    print('%-26s diametro %7.1f   3a maior %7.1f  = %.0f%% -> %s'
          % (nome, d, c3, frac * 100, 'AVISA' if frac > FRAC_3A else 'nao avisa'))

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
d, cx, cy, _, _, _ = calcula(cardeais(1500, 2000, 350, 350))
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
