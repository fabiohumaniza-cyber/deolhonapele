"""
marca_artefato.py — o operador marca, DENTRO do campo amarelo, o que nao e
ferida, e diz por que. Entrada da RODADA 4 (Adendos 34 e 35).

NAO RODA O MOTOR E NAO MOSTRA A MASCARA DELE. Mostra a foto com o anel em volta
(3,2 x o raio do campo) e o circulo amarelo; so se pinta DENTRO do amarelo. O
mapa gravado fica no quadrado do campo, recortado exatamente como a rodada 3 recorta (roda_rodada3.recorte_campo, 72cfb5cc...),
na mesma escala do quadro de 700.

As 201 imagens com campo 'ok' no CAMPO.txt (91160713...), em ordem de nome.

MOTIVOS (tecla escolhe o pincel)
  1 reflexo / brilho         2 filme / transparencia      3 sangue / crosta
  4 ponto cirurgico          5 outra lesao, nao e a ferida

MOUSE
  botao esquerdo, arrastando   pinta com o motivo escolhido
  botao direito                CONTA-GOTAS: pinta a mancha de cor parecida,
                               ligada ao ponto clicado, so dentro do campo
  rodinha                      tamanho do pincel
TECLAS
  + / -       tolerancia do conta-gotas
  z           desfaz           c   limpa tudo nesta imagem
  h           esconde/mostra a pintura, para ver a foto por baixo
  p           PELO SOBRE A LESAO: nao da para arrumar (a imagem sai da rodada 4)
  Enter ou -> grava e vai para a proxima ('nada' se nao pintou nada)
  <-          volta (sem gravar)        q   sai

Grava (append + fsync; vale a ULTIMA linha de cada nome):
  <saida>/ARTEFATO.txt
  <destino>/<nome>_artefato.png   mapa de motivos 0-5 no quadrado do campo

Uso:
    python marca_artefato.py <pasta_tiffs> <pasta_saida> <pasta_destino>
"""
import os, sys, json, datetime
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

import roda_camundongo as R
import motor_v0_funcoes as M
import roda_rodada2 as R2
import roda_rodada3 as R3

TELA = 680
MOTIVO = {1: 'reflexo', 2: 'filme', 3: 'sangue', 4: 'ponto', 5: 'outra_lesao'}
COR = {1: (0, 230, 255), 2: (255, 0, 255), 3: (255, 40, 40), 4: (255, 230, 0), 5: (40, 90, 255)}
CAB = ('# nome\testado\tx0_700\ty0_700\tlado\tpx_reflexo\tpx_filme\tpx_sangue\tpx_ponto'
       '\tpx_outra_lesao\tquando_iso\n'
       '# estado: ok (pintou), nada (nada a tirar), PELO (pelo sobre a lesao, fora da rodada 4)\n'
       '# mapa em <destino>/<nome>_artefato.png: 0 nada, 1 reflexo, 2 filme, 3 sangue, 4 ponto, 5 outra lesao\n'
       '# vale a ULTIMA linha de cada nome\n')


def le_feito(p):
    f = {}
    if os.path.isfile(p):
        for l in open(p, encoding='utf-8'):
            if l.startswith('#') or not l.strip():
                continue
            c = l.rstrip('\n\r').split('\t')
            if len(c) >= 11:
                f[c[0]] = c
    return f


def main(pasta, saida, destino):
    import tkinter as tk
    from PIL import ImageTk

    v0 = json.load(open(os.path.join(saida, 'camundongo_v0.json'), encoding='utf-8'))['imagens']
    campo = R2.le_campo(os.path.join(saida, 'CAMPO.txt'))
    nomes = sorted(n for n in campo if v0.get(n, {}).get('px_mm'))
    pa = os.path.join(saida, 'ARTEFATO.txt')
    feito = le_feito(pa)
    os.makedirs(destino, exist_ok=True)
    novo = not os.path.isfile(pa)
    f = open(pa, 'a', encoding='utf-8')
    if novo:
        f.write(CAB); f.flush(); os.fsync(f.fileno())
    print('%d imagens com campo | %d ja marcadas' % (len(nomes), len(feito)))

    est = {'i': next((k for k, n in enumerate(nomes) if n not in feito), 0),
           'mot': 1, 'pincel': 4, 'tol': 25, 'ver': True, 'desfaz': [],
           'sub': None, 'lab': None, 'dentro': None, 'x0': 0, 'y0': 0, 'esc': 1.0,
           'base': None, 'foto': None}

    raiz = tk.Tk()
    raiz.title('marca_artefato — o que, dentro do campo, NAO e ferida')
    topo = tk.Label(raiz, font=('Consolas', 11), anchor='w', justify='left')
    topo.pack(fill='x')
    tela = tk.Canvas(raiz, width=TELA, height=TELA, bg='#202020', highlightthickness=0)
    tela.pack()

    def carrega():
        nome = nomes[est['i']]
        v = v0[nome]
        im, _ = R.abre_rgb8(os.path.join(pasta, nome))
        rgb, _ = R.recorta(im, v['centro_px'][0], v['centro_px'][1], v['px_mm'])
        cx, cy, rb, rc = campo[nome]
        sub, ar, (x0, y0) = R3.recorte_campo(rgb, cx, cy, rc)
        # VISTA: quadrado de 3,2 x o raio do campo, com o anel em volta, como nas pranchas
        meio = 1.6 * rc
        vx0, vy0 = int(round(cx - meio)), int(round(cy - meio))
        vl = int(round(2 * meio))
        pad = vl
        big = np.pad(rgb, ((pad, pad), (pad, pad), (0, 0)), mode='edge')
        vista = big[vy0 + pad:vy0 + pad + vl, vx0 + pad:vx0 + pad + vl]
        est.update(sub=sub, dentro=~ar, x0=x0, y0=y0, vx0=vx0, vy0=vy0, vl=vl,
                   esc=TELA / float(vl), desfaz=[], campo=(cx, cy, rc))
        pm = os.path.join(destino, os.path.splitext(nome)[0] + '_artefato.png')
        lab = np.zeros(sub.shape[:2], np.uint8)
        if nome in feito and os.path.isfile(pm):
            a = np.asarray(Image.open(pm))
            if a.shape == lab.shape:
                lab = a.copy()
        est['lab'] = lab
        est['base'] = Image.fromarray(vista).resize((TELA, TELA), Image.LANCZOS)
        desenha()

    def desenha():
        img = est['base']
        if est['ver'] and est['lab'].any():
            rgba = np.zeros(est['lab'].shape + (4,), np.uint8)
            for k, c in COR.items():
                s = est['lab'] == k
                rgba[s, :3] = c; rgba[s, 3] = 120
            big = np.zeros((est['vl'], est['vl'], 4), np.uint8)
            ox, oy = est['x0'] - est['vx0'], est['y0'] - est['vy0']
            h, w = est['lab'].shape
            big[oy:oy + h, ox:ox + w] = rgba          # o quadrado do campo cabe sempre na vista (1,6 rc > rc)
            ov = Image.fromarray(big, 'RGBA').resize((TELA, TELA), Image.NEAREST)
            img = Image.alpha_composite(img.convert('RGBA'), ov).convert('RGB')
        est['foto'] = ImageTk.PhotoImage(img)
        tela.delete('all')
        tela.create_image(0, 0, anchor='nw', image=est['foto'])
        cx, cy, rc = est['campo']; k = est['esc']
        ex, ey, er = (cx - est['vx0']) * k, (cy - est['vy0']) * k, rc * k
        tela.create_oval(ex - er, ey - er, ex + er, ey + er, outline='#ffdc00', width=2)
        nome = nomes[est['i']]
        conta = '  '.join('%s %d' % (MOTIVO[k][:7], int((est['lab'] == k).sum())) for k in MOTIVO)
        ja = feito.get(nome)
        topo.config(text=(
            '%d/%d  %s   %s\n'
            'PINCEL: [%d] %s   tamanho %d   conta-gotas tol %d   %s\n'
            'MOTIVO: 1 reflexo  2 filme  3 sangue  4 ponto  5 outra lesao   |  esq pinta  dir conta-gotas  roda tamanho\n'
            '+/- tol   z desfaz   c limpa   h ver   p PELO   Enter ou -> grava   <- volta   q sai\n%s'
            % (est['i'] + 1, len(nomes), nome, ('JA GRAVADA: ' + ja[1]) if ja else '',
               est['mot'], MOTIVO[est['mot']].upper(), est['pincel'], est['tol'],
               '' if est['ver'] else '(PINTURA ESCONDIDA)', conta)))

    def guarda():
        est['desfaz'].append(est['lab'].copy())
        est['desfaz'] = est['desfaz'][-40:]

    def pos(e):
        k = est['esc']   # tela -> vista -> quadro de 700 -> quadrado do campo
        return int(e.y / k + est['vy0'] - est['y0']), int(e.x / k + est['vx0'] - est['x0'])

    def pinta(e):
        y, x = pos(e)
        h, w = est['lab'].shape
        r = est['pincel']
        ya, yb, xa, xb = max(0, y - r), min(h, y + r + 1), max(0, x - r), min(w, x + r + 1)
        if ya >= yb or xa >= xb:
            return                      # fora do campo: nao pinta
        yy, xx = np.ogrid[ya:yb, xa:xb]
        m = ((yy - y) ** 2 + (xx - x) ** 2 <= r * r) & est['dentro'][ya:yb, xa:xb]
        est['lab'][ya:yb, xa:xb][m] = est['mot']
        desenha()

    def aperta(e):
        guarda(); pinta(e)

    def conta_gotas(e):
        y, x = pos(e)
        h, w = est['lab'].shape
        if not (0 <= y < h and 0 <= x < w) or not est['dentro'][y, x]:
            return
        guarda()
        sub = est['sub'].astype(np.float32)
        d = np.sqrt(((sub - sub[y, x]) ** 2).sum(axis=2))
        parecido = (d <= est['tol']) & est['dentro']
        lbl, _ = ndi.label(parecido)
        est['lab'][lbl == lbl[y, x]] = est['mot']
        desenha()

    def roda(e):
        sobe = getattr(e, 'delta', 0) > 0 or getattr(e, 'num', 0) == 4
        est['pincel'] = max(1, min(40, est['pincel'] + (1 if sobe else -1)))
        desenha()

    def grava(estado=None):
        nome = nomes[est['i']]
        lab = est['lab']
        if estado is None:
            estado = 'ok' if lab.any() else 'nada'
        q = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
        cont = '\t'.join(str(int((lab == k).sum())) for k in MOTIVO)
        lin = '%s\t%s\t%d\t%d\t%d\t%s\t%s\n' % (nome, estado, est['x0'], est['y0'], lab.shape[0], cont, q)
        Image.fromarray(lab).save(os.path.join(destino, os.path.splitext(nome)[0] + '_artefato.png'))
        f.write(lin); f.flush(); os.fsync(f.fileno())
        feito[nome] = lin.rstrip('\n').split('\t')
        anda(+1)

    def anda(d):
        j = est['i'] + d
        if 0 <= j < len(nomes):
            est['i'] = j
            carrega()
        elif j >= len(nomes):
            topo.config(text='ACABOU: %d de %d marcadas. q para sair.' % (len(feito), len(nomes)))

    def tecla(e):
        k = e.keysym
        if k in ('1', '2', '3', '4', '5'):
            est['mot'] = int(k); desenha()
        elif k in ('plus', 'equal', 'KP_Add'):
            est['tol'] = min(150, est['tol'] + 5); desenha()
        elif k in ('minus', 'KP_Subtract'):
            est['tol'] = max(5, est['tol'] - 5); desenha()
        elif k in ('z', 'Z'):
            if est['desfaz']:
                est['lab'] = est['desfaz'].pop(); desenha()
        elif k in ('c', 'C'):
            guarda(); est['lab'][:] = 0; desenha()
        elif k in ('h', 'H'):
            est['ver'] = not est['ver']; desenha()
        elif k in ('p', 'P'):
            grava('PELO')
        elif k in ('Return', 'Right'):
            grava()
        elif k == 'Left':
            anda(-1)
        elif k in ('q', 'Q', 'Escape'):
            raiz.destroy()

    tela.bind('<ButtonPress-1>', aperta)
    tela.bind('<B1-Motion>', pinta)
    tela.bind('<ButtonPress-3>', conta_gotas)
    tela.bind('<MouseWheel>', roda)
    tela.bind('<Button-4>', roda)
    tela.bind('<Button-5>', roda)
    raiz.bind('<Key>', tecla)
    carrega()
    raiz.mainloop()
    f.close()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3])
