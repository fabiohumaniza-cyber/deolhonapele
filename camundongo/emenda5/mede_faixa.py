"""
mede_faixa.py — medida MANUAL da LARGURA da faixa de silicone do splint.

POR QUE EXISTE
Ideia do Fabio, 02/10/2026, durante a medicao do banco. O anel tem 1,6 mm de
espessura, entao numa foto obliqua um dos lados mostra o topo do silicone e o
outro mostra topo E parede: a borda vira dupla ("degrau"). Medindo as DUAS
bordas NO MESMO LADO — a externa e a interna — o deslocamento causado pela
espessura tem o mesmo sinal nas duas e se cancela na subtracao. O metodo do
diametro atravessa o anel, onde os dois lados tem geometria OPOSTA.

Contra: a faixa tem 3 mm e o diametro tem 16, entao o mesmo erro de clique pesa
5,33 vezes mais. Se a faixa serve ou nao, quem diz e a comparacao, nao o
argumento. Esta ferramenta existe para produzir essa comparacao.

ESTA FERRAMENTA NAO DETECTA NADA e NAO MOSTRA NENHUM RESULTADO ANTERIOR.
Em particular, ela NAO mostra o diametro ja medido da mesma imagem, nem px/mm
nenhum. Se mostrasse, a mao do operador seguiria o numero e a comparacao entre
os dois metodos perderia o valor. Ela so registra ONDE O OPERADOR CLICOU.

OS TRES CLIQUES
  1 e 2  na borda EXTERNA do silicone, AFASTADOS um do outro ao longo do anel
  3      na borda INTERNA, no mesmo lado, naquele trecho

A largura e a distancia PERPENDICULAR do ponto 3 a reta que passa por 1 e 2.
Com dois cliques apenas, atravessar a faixa de esguelha daria largura maior que
a real sem nenhum sinal de que isso aconteceu; a perpendicular elimina esse erro
e nao depende de onde, ao longo da borda interna, o ponto 3 caiu.

ESCOLHA DO TRECHO — e do operador, e e a parte que decide a qualidade:
  - o lado SEM degrau, onde se enxerga so o topo do silicone;
  - onde a faixa parece MAIS LARGA. Projecao so encurta, nunca alonga, entao a
    largura maxima observada e a melhor estimativa dos 3 mm.

Uso:
    python mede_faixa.py <pasta_plano> <pasta_saida> [<pasta_Cropped_images>]

Le   : <saida>/MEDIDAS.txt      — so para saber QUAIS imagens entram na fila,
                                  na ordem em que estao la. Nenhum numero desse
                                  arquivo e lido, mostrado ou usado em conta.
Grava: <saida>/FAIXAS.txt       nome<TAB>largura_px<TAB>x1<TAB>y1<TAB>x2<TAB>y2<TAB>x3<TAB>y3
       <saida>/FAIXAS_LOG.tsv   o mesmo, com fator de reducao e hora

Os dois sao abertos em APPEND e gravados a cada imagem, com fsync: fechar a
janela ou cair a luz nao perde o que ja foi medido. Ao reabrir, as imagens que
ja tem linha no FAIXAS.txt sao puladas.

Na tela:
    Enter      grava (exige os 3 cliques) e vai para a proxima
    n          grava SEM_FAIXA (nao ha trecho limpo) e vai para a proxima
    z          liga/desliga o zoom 2x, centrado em onde o mouse estava
    h          esconde/mostra a referencia do banco
    r          apaga os cliques desta imagem e recomeca
    Backspace  apaga o ultimo clique
    q          sai; da proxima vez retoma de onde parou

NAO MEXE no MEDIDAS.txt nem no MEDIDAS_LOG.tsv. Nao altera o motor, nenhuma
constante do v0, nenhum limiar e nenhum pre-registro.
"""
import os
import sys
import math
import datetime


# ---------------------------------------------------------------- constantes
# Faixa radial do splint = (16 - 10) / 2 = 3 mm.
# Os nominais 10 mm interno e 16 mm externo vem do README do banco e estao
# registrados na EMENDA_1_CAMUNDONGO_30SET.md, anterior a qualquer medida.
FAIXA_MM = 3.0

LUPA_LADO = 220         # lado da lupa, em px de tela
LUPA_ZOOM = 4.0         # aumento da lupa (so enxergar)
ZOOM_Z = 2.0            # aumento da tecla z
SEP_MIN_PX = 12.0       # distancia minima entre os pontos 1 e 2, em px da original


# ------------------------------------------------------------------- a conta
# Funcoes puras, no nivel do modulo, para poderem ser testadas sem abrir tela.
def largura(p1, p2, p3):
    """Distancia PERPENDICULAR de p3 a reta que passa por p1 e p2.

    Devolve (largura_px, separacao_12_px). A separacao sai junto porque uma
    reta definida por dois pontos muito proximos e instavel: um erro de clique
    de 2 px entre pontos separados por 10 px gira a reta em ~11 graus.
    """
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    dx, dy = bx - ax, by - ay
    sep = math.hypot(dx, dy)
    if sep == 0.0:
        return 0.0, 0.0
    # area do paralelogramo dividida pela base = altura
    larg = abs(dx * (cy - ay) - dy * (cx - ax)) / sep
    return larg, sep


def janela_de(W, H, larg_tela, alt_tela, fator, z, off):
    """Devolve (ox, oy, ww, wh, e) da janela visivel, ja presa dentro da imagem.

    Identica a do mede_anel.py: toda a geometria vive em px da imagem ORIGINAL,
    a tela e so uma vista com deslocamento inteiro e escala conhecida, e por
    isso o zoom nao altera medida nenhuma.
    """
    e = fator * z
    ww = int(min(W, larg_tela / e))
    wh = int(min(H, alt_tela / e))
    ox = int(min(max(0, off[0]), W - ww))
    oy = int(min(max(0, off[1]), H - wh))
    return ox, oy, ww, wh, e


def tela_para_orig(sx, sy, ox, oy, e):
    return ox + sx / e, oy + sy / e


def orig_para_tela(x, y, ox, oy, e):
    return (x - ox) * e, (y - oy) * e


# ------------------------------------------------------------------ arquivos
def le_nomes(p):
    """Nomes do MEDIDAS.txt, na ordem do arquivo. SO os nomes.

    Nenhum outro campo e lido. A fila da faixa e exatamente o conjunto que o
    Fabio ja mediu pelo diametro, incluindo as linhas SEM_ANEL — nelas a faixa
    mostra se o metodo resgata o que o diametro perdeu.
    """
    if not os.path.isfile(p):
        sys.exit('PARADO: falta %s.\nA fila da faixa sai das imagens ja medidas '
                 'pelo diametro.' % p)
    nomes = []
    for linha in open(p, encoding='utf-8'):
        if linha.startswith('#') or not linha.strip():
            continue
        n = linha.split('\t')[0].strip()
        if n:
            nomes.append(n)
    if not nomes:
        sys.exit('PARADO: %s nao tem nenhuma linha de medida.' % p)
    return nomes


def le_feitas(p):
    if not os.path.isfile(p):
        return set()
    feitas = set()
    for linha in open(p, encoding='utf-8'):
        if linha.startswith('#') or not linha.strip():
            continue
        feitas.add(linha.split('\t')[0].strip())
    return feitas


def main(pasta, saida, recortes=None):
    import tkinter as tk
    from PIL import Image, ImageTk

    p_med = os.path.join(saida, 'MEDIDAS.txt')
    p_fai = os.path.join(saida, 'FAIXAS.txt')
    p_log = os.path.join(saida, 'FAIXAS_LOG.tsv')

    nomes = le_nomes(p_med)
    feitas = le_feitas(p_fai)
    fila = [n for n in nomes if n not in feitas]
    if not fila:
        print('nada a medir: as %d imagens ja tem linha em FAIXAS.txt' % len(nomes))
        return
    print('%d na lista | %d ja com faixa | %d nesta sessao'
          % (len(nomes), len(feitas), len(fila)))

    novo_fai = not os.path.isfile(p_fai) or not le_feitas(p_fai)
    novo_log = not os.path.isfile(p_log) or not le_feitas(p_log)
    f_fai = open(p_fai, 'a', encoding='utf-8')
    f_log = open(p_log, 'a', encoding='utf-8')
    if novo_fai:
        f_fai.write('# nome\tlargura_px\tx1\ty1\tx2\ty2\tx3\ty3   '
                    '(largura=SEM_FAIXA quando nao ha trecho limpo)\n')
        f_fai.write('# largura = distancia PERPENDICULAR do ponto 3 a reta 1-2, '
                    'em px da imagem ORIGINAL\n')
        f_fai.write('# 1 e 2 na borda EXTERNA, 3 na borda INTERNA, no mesmo lado. '
                    'Faixa nominal %.1f mm = (16 - 10) / 2.\n' % FAIXA_MM)
        f_fai.flush()
    if novo_log:
        f_log.write('# nome\tlargura_px\tsep12_px\tx1\ty1\tx2\ty2\tx3\ty3'
                    '\tfator_reducao\tquando_iso\n')
        f_log.write('# sep12 = distancia entre os pontos 1 e 2; reta curta = reta instavel\n')
        f_log.flush()

    raiz = tk.Tk()
    raiz.title('mede_faixa — largura da faixa de silicone (3 mm nominais)')
    larg = raiz.winfo_screenwidth() - 60
    alt = raiz.winfo_screenheight() - 200
    barra = tk.Label(raiz, text='', font=('Consolas', 12), anchor='w', justify='left')
    barra.pack(fill='x')
    tela = tk.Canvas(raiz, width=larg, height=alt, bg='#202020', highlightthickness=0)
    tela.pack()

    est = {'i': 0, 'pts': [], 'tk': None, 'fator': 1.0, 'z': 1.0, 'off': (0, 0),
           'orig': None, 'lupa': None, 'ref': None, 'ref_on': True,
           'mouse': (0.0, 0.0)}

    REF_LADO = 240

    def janela():
        W, H = est['orig'].size
        ox, oy, ww, wh, e = janela_de(W, H, larg, alt, est['fator'], est['z'], est['off'])
        est['off'] = (ox, oy)
        return ox, oy, ww, wh, e

    def para_tela(x, y):
        ox, oy, _ww, _wh, e = janela()
        return orig_para_tela(x, y, ox, oy, e)

    def para_orig(sx, sy):
        ox, oy, _ww, _wh, e = janela()
        return tela_para_orig(sx, sy, ox, oy, e)

    def desenha_fundo():
        ox, oy, ww, wh, e = janela()
        cai = est['orig'].crop((ox, oy, ox + ww, oy + wh))
        cai = cai.resize((max(1, int(ww * e)), max(1, int(wh * e))), Image.LANCZOS)
        est['tk'] = ImageTk.PhotoImage(cai)
        tela.delete('fundo')
        tela.create_image(0, 0, anchor='nw', image=est['tk'], tags='fundo')
        tela.tag_lower('fundo')

    def desenha_marcas():
        """Desenha os pontos, a reta 1-2 e a perpendicular que esta sendo medida.

        A perpendicular aparece para o operador VER o que a conta vai usar. E
        desenho: nada aqui entra em conta nenhuma.
        """
        tela.delete('marca')
        p = [para_tela(a, b) for a, b in est['pts']]
        cores = ('#00ff88', '#00ff88', '#ffcc00')
        for i, (sx, sy) in enumerate(p):
            r = 6
            tela.create_oval(sx - r, sy - r, sx + r, sy + r,
                             outline=cores[i], width=2, tags='marca')
            tela.create_text(sx + 12, sy - 12, text=str(i + 1), fill=cores[i],
                             font=('Consolas', 12, 'bold'), tags='marca')
        if len(p) >= 2:
            tela.create_line(p[0][0], p[0][1], p[1][0], p[1][1],
                             fill='#00ff88', width=1, tags='marca')
        if len(p) == 3:
            # pe da perpendicular, em coordenadas de TELA, so para desenhar
            ax, ay = p[0]; bx, by = p[1]; cx, cy = p[2]
            dx, dy = bx - ax, by - ay
            dd = dx * dx + dy * dy
            if dd:
                t = ((cx - ax) * dx + (cy - ay) * dy) / dd
                fx, fy = ax + t * dx, ay + t * dy
                tela.create_line(cx, cy, fx, fy, fill='#ffcc00', width=2, tags='marca')

    def mostra_referencia(nome):
        """Recorte publicado pelos autores do banco. So para o operador saber de
        qual ferida se trata. Nao e medida e nao entra em conta."""
        tela.delete('ref')
        est['ref'] = None
        if not recortes or not est['ref_on']:
            return
        p = os.path.join(recortes, os.path.splitext(nome)[0] + '.png')
        if not os.path.isfile(p):
            return
        im = Image.open(p).convert('RGB')
        im.thumbnail((REF_LADO, REF_LADO), Image.LANCZOS)
        est['ref'] = ImageTk.PhotoImage(im)
        _ox, _oy, ww, wh, e = janela()
        dir_foto = int(ww * e)
        livre = larg - dir_foto - 20
        if livre >= im.size[0]:
            rx = dir_foto + 12
            ry = 10 + LUPA_LADO + 26 if rx + im.size[0] > larg - LUPA_LADO - 20 else 10 + 16
        else:
            rx = larg - im.size[0] - 10
            ry = 10 + LUPA_LADO + 26
        tela.create_text(rx, ry - 14, anchor='w', fill='#ffcc00',
                         font=('Consolas', 10, 'bold'), tags='ref',
                         text='referencia do banco — e ESTA ferida  [h]')
        tela.create_image(rx, ry, anchor='nw', image=est['ref'], tags='ref')
        tela.create_rectangle(rx, ry, rx + im.size[0], ry + im.size[1],
                              outline='#ffcc00', width=2, tags='ref')

    def status(extra=''):
        nome = fila[est['i']]
        msg = '%d/%d  %s   cliques: %d/3' % (
            est['i'] + 1, len(fila), nome, len(est['pts']))
        aviso = ''
        if len(est['pts']) == 3:
            lg, sep = largura(*est['pts'])
            msg += '   largura %.1f px' % lg
            if sep < SEP_MIN_PX:
                aviso = ('ATENCAO: os pontos 1 e 2 estao a %.0f px um do outro '
                         '(minimo %.0f) — a reta fica instavel e a perpendicular '
                         'tambem. r para refazer.' % (sep, SEP_MIN_PX))
        if est['z'] > 1.0:
            msg += '   [z] ZOOM %gx' % est['z']
        msg += ('    [1 e 2 na borda EXTERNA, afastados · 3 na INTERNA, mesmo lado'
                ' · Enter grava · n SEM_FAIXA · z zoom · h referencia · r refaz'
                ' · Backspace apaga · q sai]')
        if aviso:
            msg += '\n' + aviso
        if extra:
            msg += '\n' + extra
        barra.config(text=msg)

    def carrega():
        est['pts'] = []
        est['z'] = 1.0
        est['off'] = (0, 0)
        tela.delete('marca')
        nome = fila[est['i']]
        barra.config(text='carregando %s …' % nome)
        raiz.update_idletasks()
        est['orig'] = Image.open(os.path.join(pasta, nome))
        W, H = est['orig'].size
        est['fator'] = min(larg / float(W), alt / float(H), 1.0)
        desenha_fundo()
        mostra_referencia(nome)
        status()

    def clique(ev):
        if len(est['pts']) >= 3:
            return
        est['pts'].append(para_orig(ev.x, ev.y))
        desenha_marcas()
        status()

    def move(ev):
        """Lupa: so enxergar. Nao registra, nao altera, nao entra em conta."""
        im = est['orig']
        if im is None:
            return
        x, y = para_orig(ev.x, ev.y)
        est['mouse'] = (x, y)
        x = int(x); y = int(y)
        lado = int(LUPA_LADO / LUPA_ZOOM)
        cai = im.crop((x - lado // 2, y - lado // 2, x + lado // 2, y + lado // 2))
        cai = cai.resize((LUPA_LADO, LUPA_LADO), Image.NEAREST)
        est['lupa'] = ImageTk.PhotoImage(cai)
        tela.delete('lupa')
        lx = larg - LUPA_LADO - 10
        tela.create_image(lx, 10, anchor='nw', image=est['lupa'], tags='lupa')
        tela.create_rectangle(lx, 10, lx + LUPA_LADO, 10 + LUPA_LADO,
                              outline='#00ff88', tags='lupa')
        tela.create_line(lx + LUPA_LADO // 2, 10, lx + LUPA_LADO // 2, 10 + LUPA_LADO,
                         fill='#ff4444', tags='lupa')
        tela.create_line(lx, 10 + LUPA_LADO // 2, lx + LUPA_LADO, 10 + LUPA_LADO // 2,
                         fill='#ff4444', tags='lupa')

    def grava(linha, log):
        f_fai.write(linha); f_fai.flush(); os.fsync(f_fai.fileno())
        f_log.write(log); f_log.flush(); os.fsync(f_log.fileno())

    def proxima():
        est['i'] += 1
        if est['i'] >= len(fila):
            print('fim da fila: %d faixas nesta sessao' % len(fila))
            raiz.destroy()
            return
        carrega()

    def tecla(ev):
        k = ev.keysym.lower()
        nome = fila[est['i']]
        agora = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
        if k == 'q':
            print('saiu em %s — %d faixas gravadas nesta sessao' % (nome, est['i']))
            raiz.destroy()
        elif k == 'r':
            carrega()
        elif k == 'backspace':
            if est['pts']:
                est['pts'].pop()
                desenha_marcas()
                status()
        elif k == 'h':
            est['ref_on'] = not est['ref_on']
            mostra_referencia(nome)
        elif k == 'z':
            est['z'] = ZOOM_Z if est['z'] == 1.0 else 1.0
            W, H = est['orig'].size
            e = est['fator'] * est['z']
            ww = int(min(W, larg / e)); wh = int(min(H, alt / e))
            mx, my = est['mouse']
            est['off'] = (int(mx - ww / 2), int(my - wh / 2))
            desenha_fundo(); desenha_marcas(); mostra_referencia(nome)
            status()
        elif k == 'n':
            grava('%s\tSEM_FAIXA\t-\t-\t-\t-\t-\t-\n' % nome,
                  '%s\tSEM_FAIXA\t\t\t\t\t\t\t\t%.6f\t%s\n'
                  % (nome, est['fator'], agora))
            proxima()
        elif k == 'return':
            if len(est['pts']) != 3:
                status('faltam %d clique(s) — 2 na borda EXTERNA (afastados) e '
                       '1 na INTERNA, no mesmo lado' % (3 - len(est['pts'])))
                return
            lg, sep = largura(*est['pts'])
            pts = '\t'.join('%.3f\t%.3f' % p for p in est['pts'])
            grava('%s\t%.3f\t%s\n' % (nome, lg, pts),
                  '%s\t%.3f\t%.3f\t%s\t%.6f\t%s\n'
                  % (nome, lg, sep, pts, est['fator'], agora))
            proxima()

    tela.bind('<Button-1>', clique)
    tela.bind('<Motion>', move)
    raiz.bind('<Key>', tecla)
    carrega()
    raiz.mainloop()
    f_fai.close(); f_log.close()


if __name__ == '__main__':
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else None)
