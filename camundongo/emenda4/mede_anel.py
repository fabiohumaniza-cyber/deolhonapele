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
    python mede_anel.py <pasta_plano> <pasta_saida>

Le   : <saida>/PENDENTES_ESCALA_MANUAL.txt
Grava: <saida>/MEDIDAS.txt      nome<TAB>diam<TAB>cx<TAB>cy   (ou nome<TAB>SEM_ANEL)
       <saida>/MEDIDAS_LOG.tsv  os 4 cliques brutos, o fator de reducao e a hora

Os dois sao abertos em modo APPEND e gravados a cada imagem: fechar a janela,
cair a luz ou apertar q nao perde o que ja foi medido. Ao reabrir, as imagens
que ja tem linha no MEDIDAS.txt sao puladas.

Na tela:
    clique 4 pontos na borda EXTERNA do splint — esquerda, direita, cima, baixo
    Enter      grava e vai para a proxima
    n          grava SEM_ANEL (anel nao visivel) e vai para a proxima
    r          apaga os 4 cliques desta imagem e recomeca
    Backspace  apaga o ultimo clique
    q          sai; da proxima vez retoma de onde parou

A LUPA do canto e so para enxergar: ela mostra um pedaco da imagem ORIGINAL em
volta do cursor, e nao registra, nao altera e nao entra em conta nenhuma. E o
equivalente a uma lente de aumento na mao do operador.
"""
import os, sys, math, datetime

ANEL_MM = 16.0          # diametro externo do splint, README do banco
EXT = ('.tif', '.tiff')
LUPA_LADO = 180         # lado do quadro da lupa, em px de tela
LUPA_ZOOM = 3.0         # aumento sobre a imagem ORIGINAL


# --------------------------------------------------------------- a aritmetica
def calcula(pontos):
    """4 pontos (esquerda, direita, cima, baixo) em px da imagem ORIGINAL.

    diametro = media das duas cordas    corda1 = |p0 p1|, corda2 = |p2 p3|
    centro   = media dos 4 pontos

    Nao ajusta elipse, nao pondera, nao descarta ponto. Quatro cliques, duas
    distancias, uma media — para que a conta seja conferivel a mao."""
    if len(pontos) != 4:
        raise ValueError('sao exatamente 4 pontos')
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = pontos
    c1 = math.hypot(x1 - x0, y1 - y0)
    c2 = math.hypot(x3 - x2, y3 - y2)
    diam = (c1 + c2) / 2.0
    cx = (x0 + x1 + x2 + x3) / 4.0
    cy = (y0 + y1 + y2 + y3) / 4.0
    return diam, cx, cy, c1, c2


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


def main(pasta, saida):
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
        f_log.write('# nome\tx1\ty1\tx2\ty2\tx3\ty3\tx4\ty4\tfator_reducao\tquando_iso\n')
        f_log.write('# cliques em px da imagem ORIGINAL; fator = lado_tela / lado_original\n')
        f_log.flush()

    raiz = tk.Tk()
    raiz.title('mede_anel — borda EXTERNA do splint')
    larg = raiz.winfo_screenwidth() - 60
    alt = raiz.winfo_screenheight() - 200
    barra = tk.Label(raiz, text='', font=('Consolas', 12), anchor='w', justify='left')
    barra.pack(fill='x')
    tela = tk.Canvas(raiz, width=larg, height=alt, bg='#202020', highlightthickness=0)
    tela.pack()

    est = {'i': 0, 'pts': [], 'img': None, 'tk': None, 'fator': 1.0,
           'orig': None, 'lupa': None, 'marcas': []}

    def status(extra=''):
        n = est['i'] + 1
        nome = fila[est['i']]
        msg = '%d/%d  %s   cliques: %d/4' % (n, len(fila), nome, len(est['pts']))
        if len(est['pts']) == 4:
            d, cx, cy, c1, c2 = calcula(est['pts'])
            dif = abs(c1 - c2) / d * 100 if d else 0
            msg += '   diametro %.1f px   px/mm %.3f   cordas diferem %.1f%%' % (
                d, d / ANEL_MM, dif)
        msg += '    [Enter grava · n SEM_ANEL · r refaz · Backspace apaga · q sai]'
        if extra:
            msg += '\n' + extra
        barra.config(text=msg)

    def carrega():
        for m in est['marcas']:
            tela.delete(m)
        est['marcas'] = []
        est['pts'] = []
        nome = fila[est['i']]
        barra.config(text='carregando %s …' % nome)
        raiz.update_idletasks()
        im = Image.open(os.path.join(pasta, nome))
        est['orig'] = im
        W, H = im.size
        fator = min(larg / float(W), alt / float(H), 1.0)
        est['fator'] = fator
        vis = im.resize((max(1, int(W * fator)), max(1, int(H * fator))), Image.LANCZOS)
        est['tk'] = ImageTk.PhotoImage(vis)
        tela.delete('fundo')
        tela.create_image(0, 0, anchor='nw', image=est['tk'], tags='fundo')
        tela.tag_lower('fundo')
        status()

    def clique(ev):
        if len(est['pts']) >= 4:
            return
        x = ev.x / est['fator']; y = ev.y / est['fator']
        est['pts'].append((x, y))
        r = 6
        est['marcas'].append(tela.create_oval(ev.x - r, ev.y - r, ev.x + r, ev.y + r,
                                              outline='#00ff88', width=2))
        est['marcas'].append(tela.create_text(ev.x + 12, ev.y - 12,
                                              text=str(len(est['pts'])),
                                              fill='#00ff88', font=('Consolas', 12, 'bold')))
        if len(est['pts']) == 4:
            p = [(a * est['fator'], b * est['fator']) for a, b in est['pts']]
            est['marcas'].append(tela.create_line(p[0][0], p[0][1], p[1][0], p[1][1],
                                                  fill='#00ff88', width=1))
            est['marcas'].append(tela.create_line(p[2][0], p[2][1], p[3][0], p[3][1],
                                                  fill='#00ff88', width=1))
        status()

    def move(ev):
        """Lupa: so enxergar. Nao registra, nao altera, nao entra em conta."""
        im = est['orig']
        if im is None:
            return
        lado = int(LUPA_LADO / LUPA_ZOOM)
        x = int(ev.x / est['fator']); y = int(ev.y / est['fator'])
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
                for _ in range(2):
                    if est['marcas']:
                        tela.delete(est['marcas'].pop())
                status()
        elif k == 'n':
            grava('%s\tSEM_ANEL\n' % nome,
                  '%s\t\t\t\t\t\t\t\t\t%.6f\t%s\n'
                  % (nome, est['fator'], datetime.datetime.now().astimezone().isoformat(timespec='seconds')))
            proxima()
        elif k == 'return':
            if len(est['pts']) != 4:
                status('faltam %d clique(s) — sao 4 na borda EXTERNA do splint'
                       % (4 - len(est['pts'])))
                return
            d, cx, cy, _c1, _c2 = calcula(est['pts'])
            grava('%s\t%.3f\t%.3f\t%.3f\n' % (nome, d, cx, cy),
                  '%s\t%s\t%.6f\t%s\n'
                  % (nome,
                     '\t'.join('%.3f\t%.3f' % p for p in est['pts']),
                     est['fator'],
                     datetime.datetime.now().astimezone().isoformat(timespec='seconds')))
            proxima()

    tela.bind('<Button-1>', clique)
    tela.bind('<Motion>', move)
    raiz.bind('<Key>', tecla)
    carrega()
    raiz.mainloop()
    f_med.close(); f_log.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
