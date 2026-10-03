"""
campo_disco.py — o operador declara o CAMPO: o maior circulo dentro do buraco
do splint que nao toca o laranja.

POR QUE EXISTE
A rodada 1 do motor v0 (Adendo 14) pintou a faixa do splint e o pelo do canto
do recorte em vez da ferida. Em 02/10, as 21h13, o Fabio propos restringir o
campo a um circulo dentro do anel laranja. Em 03/10, as 06h56, o ve_disco.py
mostrou que um disco de tamanho fixo (4,5 mm) quase encosta no laranja ja na
imagem mais limpa do banco, porque o buraco que aparece na foto e menor que os
10 mm do README. As 06h58 o Fabio fixou a regra:

    o circulo vai ate o FINAL DA BORDA DE DENTRO DO LARANJA,
    e NAO PODE PEGAR NENHUM PEDACO DELE.
As 07h00 acrescentou: com uma MARGEM BOA. Para a margem nao virar decisao
imagem por imagem, ela e FIXA e declarada aqui: o operador encosta o circulo na
borda (o ato objetivo, achar a borda) e o campo que o motor usa e esse circulo
menos MARGEM_MM, igual em todas as imagens.

REGRA, imagem por imagem
  - o circulo VERDE encosta na borda de dentro do laranja, sem passar dela;
  - o TRACEJADO, MARGEM_MM para dentro, e o campo de verdade — automatico;
  - centrar no BURACO, nao na ferida — nao olhar para onde a lesao esta;
  - anel comido: onde falta laranja, o circulo nao cresce pelo vao aberto;
    segue o arco que sobrou;
  - filme ou reflexo em cima do laranja: vale onde o laranja esta, mesmo
    apagado;
  - se nao da para definir o buraco, tecla n.

NAO RODA O MOTOR, NAO MEDE A FERIDA, NAO ALTERA NADA DO QUE EXISTE.
Recorta exatamente como a etapa 3 recorta — importa o roda_camundongo.py
(8c1f6e4d...) e chama abre_rgb8() e recorta() — no centro e na escala que o
operador ja mediu. O circulo vive no quadro de trabalho de 700 px, o mesmo do
motor, de modo que a rodada 3 usa o que foi gravado aqui sem conversao.

Grava: <saida>/CAMPO.txt   (APPEND com fsync; vale a ULTIMA linha de cada nome)
       nome  cx_700  cy_700  r_borda_700  r_campo_700  r_campo_mm  dx_mm  dy_mm  estado  quando_iso
       r_borda = o circulo que o operador encostou; r_campo = r_borda - margem.
       dx_mm, dy_mm = quanto o circulo foi deslocado do centro dos cliques.
       estado = ok | NAO_DA
Grava: <pasta_png>/<nome>_campo.png   imagem PEQUENA (350 px) com o circulo,
       para o trabalho.

Na tela:
    arrastar com o botao esquerdo   move o circulo
    roda do mouse                   circulo maior / menor (1 px)
    Shift + roda                    maior / menor de 5 px
    setas  cima / baixo             maior / menor (1 px)
    Enter                           grava e vai para a proxima
    n                               nao da para definir o buraco
    r                               volta o circulo ao centro dos cliques
    setas  esquerda / direita       anda entre as imagens
    q                               sai; da proxima vez retoma onde parou
A LUPA no canto mostra, aumentado, o pedaco embaixo do ponteiro, com o
circulo desenhado — e para conferir se ele toca o laranja.

Uso:
    python campo_disco.py <pasta_tiffs> <pasta_saida> <pasta_png>
"""
import os, sys, json, datetime
import numpy as np
from PIL import Image, ImageDraw

import roda_camundongo as R
import motor_v0_funcoes as M

PX_MM_700 = R.S_1380 * M.L / R.LADO_1380      # 29,1667 px/mm no quadro de 700
R_INICIAL_MM = 4.5                            # so o ponto de partida; o operador ajusta
MARGEM_MM = 0.3                               # FIXA, declarada 03/10/2026; nao muda depois de comecar
ESC = 1.25                                    # 700 px -> 875 px na tela
LUPA_LADO, LUPA_ZOOM = 220, 4.0
PNG_LADO = 350
C0 = (M.L - 1) / 2.0                          # centro dos cliques no quadro de 700

CAB = ('# nome\tcx_700\tcy_700\tr_borda_700\tr_campo_700\tr_campo_mm\tdx_mm\tdy_mm\testado\tquando_iso\n'
       '# r_borda: circulo encostado pelo operador na borda de dentro do laranja, sem toca-lo\n'
       '# r_campo = r_borda - MARGEM_MM (%.2f mm, fixa): e o campo que o motor usa\n'
       '# dx_mm, dy_mm: deslocamento do circulo em relacao ao centro dos cliques do anel\n'
       '# vale a ULTIMA linha de cada nome; as anteriores ficam como historico\n' % MARGEM_MM)


def le_campo(p):
    feito = {}
    if not os.path.isfile(p):
        return feito
    for linha in open(p, encoding='utf-8'):
        if linha.startswith('#') or not linha.strip():
            continue
        c = linha.rstrip('\n\r').split('\t')
        if len(c) >= 9:
            feito[c[0]] = c
    return feito


def linha_campo(nome, cx, cy, r, estado):
    q = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
    if estado != 'ok':
        return '%s\t\t\t\t\t\t\t\t%s\t%s\n' % (nome, estado, q)
    rc = r - MARGEM_MM * PX_MM_700
    return '%s\t%.2f\t%.2f\t%.2f\t%.2f\t%.3f\t%+.3f\t%+.3f\t%s\t%s\n' % (
        nome, cx, cy, r, rc, rc / PX_MM_700,
        (cx - C0) / PX_MM_700, (cy - C0) / PX_MM_700, estado, q)


def png_pequeno(rgb, cx, cy, r, nome):
    im = Image.fromarray(rgb.astype(np.uint8)).convert('RGB')
    d = ImageDraw.Draw(im)
    rc = r - MARGEM_MM * PX_MM_700
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 230, 0), width=2)
    d.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], outline=(255, 220, 0), width=3)
    im = im.resize((PNG_LADO, PNG_LADO), Image.LANCZOS)
    f = Image.new('RGB', (PNG_LADO, PNG_LADO + 18), (16, 16, 16))
    f.paste(im, (0, 18))
    ImageDraw.Draw(f).text((4, 3), '%s  campo r = %.2f mm (amarelo)' % (nome, rc / PX_MM_700),
                           fill=(235, 235, 235))
    return f


def lista(saida):
    reg = json.load(open(os.path.join(saida, 'camundongo_v0.json'),
                         encoding='utf-8'))['imagens']
    return reg, sorted(n for n, v in reg.items() if v.get('px_mm'))


def main(pasta, saida, destino):
    import tkinter as tk
    from PIL import ImageTk

    reg, nomes = lista(saida)
    p_campo = os.path.join(saida, 'CAMPO.txt')
    feito = le_campo(p_campo)
    os.makedirs(destino, exist_ok=True)
    novo = not os.path.isfile(p_campo)
    f = open(p_campo, 'a', encoding='utf-8')
    if novo:
        f.write(CAB); f.flush(); os.fsync(f.fileno())
    print('%d imagens com escala | %d ja com campo' % (len(nomes), len(feito)))

    est = {'i': next((k for k, n in enumerate(nomes) if n not in feito), 0),
           'rgb': None, 'cx': C0, 'cy': C0, 'r': R_INICIAL_MM * PX_MM_700,
           'arr': None, 'mouse': None, 'foto': None, 'lupa': None}

    raiz = tk.Tk()
    raiz.title('campo_disco — o maior circulo dentro do buraco, sem tocar o laranja')
    topo = tk.Label(raiz, font=('Consolas', 12), anchor='w', justify='left')
    topo.pack(fill='x')
    L = int(M.L * ESC)
    tela = tk.Canvas(raiz, width=L + LUPA_LADO + 20, height=L, bg='#202020',
                     highlightthickness=0)
    tela.pack()

    def carrega():
        nome = nomes[est['i']]
        v = reg[nome]
        im, _ = R.abre_rgb8(os.path.join(pasta, nome))
        rgb, _ = R.recorta(im, v['centro_px'][0], v['centro_px'][1], v['px_mm'])
        est['rgb'] = rgb
        c = feito.get(nome)
        if c and c[8] == 'ok':
            est['cx'], est['cy'], est['r'] = float(c[1]), float(c[2]), float(c[3])
        else:
            est['cx'], est['cy'], est['r'] = C0, C0, R_INICIAL_MM * PX_MM_700
        est['foto'] = ImageTk.PhotoImage(
            Image.fromarray(rgb).resize((L, L), Image.LANCZOS))
        desenha()

    def desenha():
        tela.delete('all')
        tela.create_image(0, 0, anchor='nw', image=est['foto'])
        cx, cy, r = est['cx'] * ESC, est['cy'] * ESC, est['r'] * ESC
        tela.create_oval(cx - r, cy - r, cx + r, cy + r, outline='#00e600', width=2)
        rc = (est['r'] - MARGEM_MM * PX_MM_700) * ESC
        tela.create_oval(cx - rc, cy - rc, cx + rc, cy + rc, outline='#ffdc00',
                         width=2, dash=(6, 4))
        c = C0 * ESC
        tela.create_line(c - 6, c, c + 6, c, fill='white')
        tela.create_line(c, c - 6, c, c + 6, fill='white')
        lupa()
        nome = nomes[est['i']]
        ja = feito.get(nome)
        topo.config(text=(
            '%d/%d   %s   borda r = %.2f mm   campo r = %.2f mm   desloc = %+.2f, %+.2f mm   %s\n'
            '[arrasta move · roda tamanho · Shift+roda x5 · Enter grava · n nao da · '
            'r reset · <- -> anda · q sai]'
            % (est['i'] + 1, len(nomes), nome, est['r'] / PX_MM_700,
               est['r'] / PX_MM_700 - MARGEM_MM,
               (est['cx'] - C0) / PX_MM_700, (est['cy'] - C0) / PX_MM_700,
               ('JA GRAVADA: ' + ja[8]) if ja else '')))

    def lupa():
        if est['mouse'] is None:
            return
        mx, my = est['mouse'][0] / ESC, est['mouse'][1] / ESC
        meio = LUPA_LADO / LUPA_ZOOM / 2
        x0, y0 = int(round(mx - meio)), int(round(my - meio))
        lado = int(round(2 * meio))
        pad = np.pad(est['rgb'], ((lado, lado), (lado, lado), (0, 0)), mode='edge')
        cai = Image.fromarray(pad[y0 + lado:y0 + 2 * lado, x0 + lado:x0 + 2 * lado])
        cai = cai.resize((LUPA_LADO, LUPA_LADO), Image.NEAREST)
        d = ImageDraw.Draw(cai)
        k = LUPA_LADO / lado
        cx, cy, r = (est['cx'] - x0) * k, (est['cy'] - y0) * k, est['r'] * k
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 230, 0), width=2)
        rc = (est['r'] - MARGEM_MM * PX_MM_700) * k
        d.ellipse([cx - rc, cy - rc, cx + rc, cy + rc], outline=(255, 220, 0), width=1)
        est['lupa'] = ImageTk.PhotoImage(cai)
        lx = L + 10
        tela.create_image(lx, 10, anchor='nw', image=est['lupa'])
        tela.create_rectangle(lx, 10, lx + LUPA_LADO, 10 + LUPA_LADO, outline='#00e600')

    def aperta(e):
        est['arr'] = (e.x / ESC - est['cx'], e.y / ESC - est['cy'])

    def arrasta(e):
        est['mouse'] = (e.x, e.y)
        if est['arr'] is not None:
            est['cx'] = e.x / ESC - est['arr'][0]
            est['cy'] = e.y / ESC - est['arr'][1]
        desenha()

    def solta(e):
        est['arr'] = None

    def move(e):
        est['mouse'] = (e.x, e.y)
        desenha()

    def raio(d):
        est['r'] = max(10.0, min(C0, est['r'] + d))
        desenha()

    def roda(e):
        passo = 5 if (e.state & 0x0001) else 1
        raio(passo if (getattr(e, 'delta', 0) > 0 or getattr(e, 'num', 0) == 4) else -passo)

    def grava(estado):
        nome = nomes[est['i']]
        lin = linha_campo(nome, est['cx'], est['cy'], est['r'], estado)
        f.write(lin); f.flush(); os.fsync(f.fileno())
        feito[nome] = lin.rstrip('\n').split('\t')
        if estado == 'ok':
            png_pequeno(est['rgb'], est['cx'], est['cy'], est['r'], nome).save(
                os.path.join(destino, os.path.splitext(nome)[0] + '_campo.png'))
        anda(+1)

    def anda(d):
        j = est['i'] + d
        if 0 <= j < len(nomes):
            est['i'] = j
            carrega()
        elif j >= len(nomes):
            topo.config(text='ACABOU: %d de %d com campo gravado. q para sair.'
                        % (len(feito), len(nomes)))

    def tecla(e):
        k = e.keysym
        if k == 'Return':
            grava('ok')
        elif k in ('n', 'N'):
            grava('NAO_DA')
        elif k in ('r', 'R'):
            est['cx'], est['cy'] = C0, C0
            desenha()
        elif k == 'Up':
            raio(+1)
        elif k == 'Down':
            raio(-1)
        elif k == 'Right':
            anda(+1)
        elif k == 'Left':
            anda(-1)
        elif k in ('q', 'Q', 'Escape'):
            raiz.destroy()

    tela.bind('<ButtonPress-1>', aperta)
    tela.bind('<B1-Motion>', arrasta)
    tela.bind('<ButtonRelease-1>', solta)
    tela.bind('<Motion>', move)
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
