"""
mede_anel.py — medida MANUAL do anel do splint, imagem por imagem.

Existe porque o detector congelado (detecta_anel_camundongo.py, SHA-256
56f1b434…) reprovou 255 de 255 fotos reais na etapa 1. A regra 3.2 da Emenda 3
manda, sem escolha: medida manual do anel em TODA pendente, antes de o motor
rodar em qualquer uma. Mesmo precedente da escala manual da 1324·B no porco.

ESTA FERRAMENTA NAO DETECTA NADA. Ela nao calcula borda, nao procura elipse,
nao chama o detector, nao abre o JSON da deteccao e nao mostra numero nenhum
vindo dele. Ela registra ONDE O OPERADOR CLICOU, e converte para px da imagem
original. Todo o resto e aritmetica de quatro pontos.

Uso:
    python mede_anel.py <pasta_plano> <pasta_saida> [<pasta_Cropped_images>]

O terceiro argumento e opcional e e a pasta "Cropped images" do proprio banco.
Quando ele e dado, a ferramenta mostra no canto, como REFERENCIA, o recorte que
os autores do banco publicaram para esta mesma ferida-dia (Day N_<animal>-<L|R>
.png). Serve para o operador saber QUAL anel medir nas fotos em que o animal
aparece inteiro, com os dois splints no quadro. A referencia e so para ver: nao
e medida, nao e clicavel e nao entra em conta nenhuma.

Le   : <saida>/PENDENTES_ESCALA_MANUAL.txt
Grava: <saida>/MEDIDAS.txt      nome<TAB>diam<TAB>cx<TAB>cy   (ou nome<TAB>SEM_ANEL)
       <saida>/MEDIDAS_LOG.tsv  os 4 cliques brutos, o fator de reducao e a hora

Os dois sao abertos em modo APPEND e gravados a cada imagem: fechar a janela,
cair a luz ou apertar q nao perde o que ja foi medido. Ao reabrir, as imagens
que ja tem linha no MEDIDAS.txt sao puladas.

Na tela:
    clique 4 pontos na borda EXTERNA do splint, bem espalhados pela volta.
    A ORDEM NAO IMPORTA: o diametro e a media das duas maiores entre as seis
    distancias dos quatro pontos. Se os quatro ficarem amontoados de um lado,
    a barra avisa.
    Enter      grava e vai para a proxima
    n          grava SEM_ANEL (anel nao visivel) e vai para a proxima
    d          marca/desmarca "ha mais de um anel neste quadro"
    z          liga/desliga o zoom 2x, centrado em onde o mouse estava
    h          esconde/mostra a referencia do banco
    r          apaga os 4 cliques desta imagem e recomeca
    Backspace  apaga o ultimo clique
    q          sai; da proxima vez retoma de onde parou

A tecla d nao muda medida nenhuma: ela grava um fato sobre a FOTO no
MEDIDAS_LOG.tsv, para que o numero de imagens com dois splints no quadro seja
conhecido em vez de suposto.

O que grava e a COORDENADA DO CURSOR, nao o circulo verde — o circulo e so
desenho. E o zoom e so vista: toda a geometria vive em px da imagem ORIGINAL, a
tela e uma janela com deslocamento inteiro e escala conhecida, e os cliques
voltam para px da original pela mesma conta, com ou sem zoom.

A LUPA do canto e so para enxergar: ela mostra um pedaco da imagem ORIGINAL em
volta do cursor, e nao registra, nao altera e nao entra em conta nenhuma. E o
equivalente a uma lente de aumento na mao do operador.
"""
import os, sys, math, datetime

ANEL_MM = 16.0          # diametro externo do splint, README do banco
EXT = ('.tif', '.tiff')
LUPA_LADO = 180         # lado do quadro da lupa, em px de tela
LUPA_ZOOM = 4.0         # aumento da lupa sobre a imagem ORIGINAL
ZOOM_Z = 2.0            # aumento da tecla z sobre a vista inteira


# --------------------------------------------------------------- a aritmetica
def calcula(pontos):
    """4 pontos na borda externa do splint, em px da imagem ORIGINAL.

    diametro = media das DUAS MAIORES entre as 6 distancias dos 4 pontos
    centro   = media dos 4 pontos

    A ORDEM DO CLIQUE NAO IMPORTA — e o reparo do Fable, 01/10/2026. A versao
    anterior (42e77a0d…) fazia corda1 = |p1 p2| e corda2 = |p3 p4|: clicar
    esquerda-cima-direita-baixo transformava as duas cordas em diagonais, o
    diametro saia ~30 % menor, e o aviso de diferenca entre cordas nao acusava,
    porque as duas diagonais sao iguais. Em 255 imagens uma troca de ordem
    passaria despercebida.

    Com as duas maiores, num circulo as duas diametrais ganham das quatro
    laterais (D contra 0,707·D) e o resultado independe da ordem. Numa elipse,
    as duas maiores sao os dois eixos — enquanto b/a > 1/raiz(3) = 0,577, que e
    um splint visto a ~55 graus. Abaixo disso a lateral passa o eixo menor e a
    conta degrada; o ensaio mede esse limite e ele esta declarado na nota.

    Nao ajusta elipse, nao pondera, nao descarta ponto: seis distancias, duas
    maiores, uma media — conferivel a mao a partir do log dos cliques.

    Devolve tambem a TERCEIRA maior: se ela passar de 0,80 do diametro, os
    quatro pontos estao mal distribuidos (amontoados num lado) e a barra avisa."""
    if len(pontos) != 4:
        raise ValueError('sao exatamente 4 pontos')
    dists = []
    for i in range(4):
        for j in range(i + 1, 4):
            dists.append(math.hypot(pontos[j][0] - pontos[i][0],
                                    pontos[j][1] - pontos[i][1]))
    dists.sort(reverse=True)
    c1, c2, c3 = dists[0], dists[1], dists[2]
    diam = (c1 + c2) / 2.0
    cx = sum(p[0] for p in pontos) / 4.0
    cy = sum(p[1] for p in pontos) / 4.0
    return diam, cx, cy, c1, c2, c3


FRAC_3A = 0.80          # 3a maior acima disso = pontos mal distribuidos


# ------------------------------------------------ a vista (zoom e deslocamento)
# Estas tres funcoes sao o unico lugar onde tela e imagem se encontram. Ficam
# fora da janela, no nivel do modulo, para poderem ser testadas sem abrir tela.
#
# Toda a geometria vive em px da imagem ORIGINAL. A tela e uma JANELA: canto
# (ox, oy) inteiro, escala efetiva e = fator x zoom. Como ox e oy sao inteiros e
# e e conhecida, ida e volta sao exatas, e o zoom nao pode mexer em medida.
def janela_de(W, H, larg, alt, fator, z, off):
    """Devolve (ox, oy, ww, wh, e) da janela visivel, ja presa dentro da imagem."""
    e = fator * z
    ww = int(min(W, larg / e)); wh = int(min(H, alt / e))
    ox = int(min(max(0, off[0]), W - ww))
    oy = int(min(max(0, off[1]), H - wh))
    return ox, oy, ww, wh, e


def tela_para_orig(sx, sy, ox, oy, e):
    return ox + sx / e, oy + sy / e


def orig_para_tela(x, y, ox, oy, e):
    return (x - ox) * e, (y - oy) * e


# ------------------------------------------------------------------- arquivos
def le_pendentes(p):
    if not os.path.isfile(p):
        sys.exit('PARADO: falta %s.\nEle sai da etapa 1 do roda_camundongo.py.' % p)
    nomes = []
    for linha in open(p, encoding='utf-8'):
        if linha.startswith('#') or not linha.strip():
            continue
        nomes.append(linha.split('\t')[0].strip())
    return [n for n in nomes if n]


def le_feitas(p):
    """Nomes que ja tem linha no MEDIDAS.txt — para retomar sem repetir."""
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

    p_pend = os.path.join(saida, 'PENDENTES_ESCALA_MANUAL.txt')
    p_med = os.path.join(saida, 'MEDIDAS.txt')
    p_log = os.path.join(saida, 'MEDIDAS_LOG.tsv')

    pendentes = le_pendentes(p_pend)
    feitas = le_feitas(p_med)
    fila = [n for n in pendentes if n not in feitas]
    if not fila:
        print('nada a medir: as %d pendentes ja tem linha em MEDIDAS.txt' % len(pendentes))
        return
    print('%d pendentes | %d ja medidas | %d nesta sessao' % (len(pendentes), len(feitas), len(fila)))

    novo_med = not os.path.isfile(p_med)
    novo_log = not os.path.isfile(p_log)
    f_med = open(p_med, 'a', encoding='utf-8')
    f_log = open(p_log, 'a', encoding='utf-8')
    if novo_med:
        f_med.write('# nome\tdiametro_px\tcentro_x_px\tcentro_y_px   (ou SEM_ANEL)\n')
        f_med.flush()
    if novo_log:
        f_log.write('# nome\tx1\ty1\tx2\ty2\tx3\ty3\tx4\ty4\tfator_reducao\tquando_iso\tmais_de_um_anel\n')
        f_log.write('# cliques em px da imagem ORIGINAL; fator = lado_tela / lado_original\n')
        f_log.write('# mais_de_um_anel: fato sobre a FOTO declarado pelo operador (tecla d), nao medida\n')
        f_log.flush()

    raiz = tk.Tk()
    raiz.title('mede_anel — borda EXTERNA do splint')
    larg = raiz.winfo_screenwidth() - 60
    alt = raiz.winfo_screenheight() - 200
    barra = tk.Label(raiz, text='', font=('Consolas', 12), anchor='w', justify='left')
    barra.pack(fill='x')
    tela = tk.Canvas(raiz, width=larg, height=alt, bg='#202020', highlightthickness=0)
    tela.pack()

    est = {'i': 0, 'pts': [], 'tk': None, 'fator': 1.0, 'z': 1.0, 'off': (0, 0),
           'orig': None, 'lupa': None, 'dois': False, 'ref': None,
           'ref_on': True, 'mouse': (0.0, 0.0)}

    REF_LADO = 240

    # ---------------------------------------------------- janela visivel
    # Toda a geometria vive em px da imagem ORIGINAL. A tela e so uma vista:
    # deslocamento inteiro (off) e escala efetiva (fator x zoom). Por isso o
    # zoom NAO altera medida nenhuma — ele muda o que se ve, nunca o que se
    # grava, e os cliques voltam para px da original pela mesma conta.
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
        tela.delete('marca')
        p = [para_tela(a, b) for a, b in est['pts']]
        for i, (sx, sy) in enumerate(p):
            r = 6
            tela.create_oval(sx - r, sy - r, sx + r, sy + r,
                             outline='#00ff88', width=2, tags='marca')
            tela.create_text(sx + 12, sy - 12, text=str(i + 1), fill='#00ff88',
                             font=('Consolas', 12, 'bold'), tags='marca')
        if len(p) == 4:
            # as DUAS MAIORES distancias — as mesmas que entram na conta
            pares = sorted(((math.hypot(p[j][0] - p[i][0], p[j][1] - p[i][1]), i, j)
                            for i in range(4) for j in range(i + 1, 4)), reverse=True)
            for _d, i, j in pares[:2]:
                tela.create_line(p[i][0], p[i][1], p[j][0], p[j][1],
                                 fill='#00ff88', width=1, tags='marca')

    def mostra_referencia(nome):
        """Recorte publicado pelos autores do banco, so para o operador saber
        QUAL anel e o desta imagem. Nao e medida e nao entra em conta.

        v5: vai para a FAIXA LIVRE a direita da foto desenhada, quando ela
        couber — assim nao tapa nada da imagem. So quando nao ha faixa (foto
        larga, ou zoom ligado) ele volta a sobrepor, no canto superior direito,
        abaixo da lupa. A tecla h esconde e mostra em qualquer um dos dois."""
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
        dir_foto = int(ww * e)                      # onde a foto desenhada acaba
        livre = larg - dir_foto - 20
        if livre >= im.size[0]:                     # cabe fora da foto
            rx = dir_foto + 12
            ry = 10 + LUPA_LADO + 26 if rx + im.size[0] > larg - LUPA_LADO - 20 else 10 + 16
        else:                                       # sem faixa: sobrepoe
            rx = larg - im.size[0] - 10
            ry = 10 + LUPA_LADO + 26
        tela.create_text(rx, ry - 14, anchor='w', fill='#ffcc00',
                         font=('Consolas', 10, 'bold'), tags='ref',
                         text='referencia do banco — e ESTA ferida  [h]')
        tela.create_image(rx, ry, anchor='nw', image=est['ref'], tags='ref')
        tela.create_rectangle(rx, ry, rx + im.size[0], ry + im.size[1],
                              outline='#ffcc00', width=2, tags='ref')

    def status(extra=''):
        n = est['i'] + 1
        nome = fila[est['i']]
        msg = '%d/%d  %s   cliques: %d/4%s' % (n, len(fila), nome, len(est['pts']),
                                               '   [d] MAIS DE UM ANEL' if est['dois'] else '')
        aviso = ''
        if len(est['pts']) == 4:
            d, cx, cy, c1, c2, c3 = calcula(est['pts'])
            dif = abs(c1 - c2) / d * 100 if d else 0
            msg += '   diametro %.1f px   px/mm %.3f   as duas maiores diferem %.1f%%' % (
                d, d / ANEL_MM, dif)
            if d and c3 > FRAC_3A * d:
                aviso = ('ATENCAO: a 3a maior distancia e %.0f%% do diametro (limite %.0f%%) — '
                         'os 4 pontos parecem amontoados de um lado. r para refazer.'
                         % (c3 / d * 100, FRAC_3A * 100))
        if est['z'] > 1.0:
            msg += '   [z] ZOOM %gx' % est['z']
        msg += ('    [Enter grava · n SEM_ANEL · d dois aneis · z zoom · h referencia'
                ' · r refaz · Backspace apaga · q sai]')
        if aviso:
            msg += '\n' + aviso
        if extra:
            msg += '\n' + extra
        barra.config(text=msg)

    def carrega():
        est['pts'] = []
        est['dois'] = False
        est['z'] = 1.0
        est['off'] = (0, 0)
        tela.delete('marca')
        nome = fila[est['i']]
        barra.config(text='carregando %s …' % nome)
        raiz.update_idletasks()
        im = Image.open(os.path.join(pasta, nome))
        est['orig'] = im
        W, H = im.size
        est['fator'] = min(larg / float(W), alt / float(H), 1.0)
        desenha_fundo()
        mostra_referencia(nome)
        status()

    def clique(ev):
        if len(est['pts']) >= 4:
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

    def grava(linha, log=None):
        f_med.write(linha); f_med.flush(); os.fsync(f_med.fileno())
        if log:
            f_log.write(log); f_log.flush(); os.fsync(f_log.fileno())

    def proxima():
        est['i'] += 1
        if est['i'] >= len(fila):
            print('fim da fila: %d medidas nesta sessao' % len(fila))
            raiz.destroy()
            return
        carrega()

    def tecla(ev):
        k = ev.keysym.lower()
        nome = fila[est['i']]
        if k == 'q':
            print('saiu em %s — %d medidas gravadas nesta sessao' % (nome, est['i']))
            raiz.destroy()
        elif k == 'r':
            carrega()
        elif k == 'backspace':
            if est['pts']:
                est['pts'].pop()
                desenha_marcas()
                status()
        elif k == 'd':
            est['dois'] = not est['dois']
            status()
        elif k == 'h':
            est['ref_on'] = not est['ref_on']
            mostra_referencia(nome)
        elif k == 'z':
            # zoom centrado no ultimo ponto do mouse. So vista: os cliques ja
            # gravados estao em px da original e sao redesenhados no lugar.
            est['z'] = ZOOM_Z if est['z'] == 1.0 else 1.0
            W, H = est['orig'].size
            e = est['fator'] * est['z']
            ww = int(min(W, larg / e)); wh = int(min(H, alt / e))
            mx, my = est['mouse']
            est['off'] = (int(mx - ww / 2), int(my - wh / 2))
            desenha_fundo(); desenha_marcas(); mostra_referencia(nome)
            status()
        elif k == 'n':
            grava('%s\tSEM_ANEL\n' % nome,
                  '%s\t\t\t\t\t\t\t\t\t%.6f\t%s\t%d\n'
                  % (nome, est['fator'],
                     datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
                     int(est['dois'])))
            proxima()
        elif k == 'return':
            if len(est['pts']) != 4:
                status('faltam %d clique(s) — sao 4 na borda EXTERNA do splint'
                       % (4 - len(est['pts'])))
                return
            d, cx, cy, _c1, _c2, _c3 = calcula(est['pts'])
            grava('%s\t%.3f\t%.3f\t%.3f\n' % (nome, d, cx, cy),
                  '%s\t%s\t%.6f\t%s\t%d\n'
                  % (nome,
                     '\t'.join('%.3f\t%.3f' % p for p in est['pts']),
                     est['fator'],
                     datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
                     int(est['dois'])))
            proxima()

    tela.bind('<Button-1>', clique)
    tela.bind('<Motion>', move)
    raiz.bind('<Key>', tecla)
    carrega()
    raiz.mainloop()
    f_med.close(); f_log.close()


if __name__ == '__main__':
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else None)
