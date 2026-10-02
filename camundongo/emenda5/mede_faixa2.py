"""
mede_faixa2.py — a mesma medida da faixa, com regua de angulo TRAVADO.

POR QUE EXISTE (v2)
A v1 (df8d779f56686a78c6f986e3f45c1379aa9c53d28cc2bf84a20d00bf02e1e29d, 17.032 B)
pedia tres cliques e calculava a perpendicular. A conta estava certa, mas a mao
nao: o operador nao via o angulo enquanto clicava. Pedido do Fabio, 02/10/2026,
11h53 e 11h57: "o certo e uma regua que eu arrasto", "essa regua nao pode mudar
angulo quando eu arrastar, senao a gente perde a medida".

A v1 NAO e alterada e continua valendo com o hash dela. Esta e arquivo novo.

O QUE MUDA, E SO ISSO
1. O angulo passa a ser DEFINIDO e depois TRAVADO:
   - voce ARRASTA em cima da borda EXTERNA, acompanhando o anel;
   - ao soltar, a direcao fica travada;
   - a partir dai a regua so anda PERPENDICULAR a ela. Nao ha como torce-la.
2. Fase de TREINO declarada: nas 5 PRIMEIRAS da fila, na ordem do arquivo, a
   ferramenta mostra o diametro ja medido e a largura esperada. Serve para o
   operador pegar a mao. Essas 5 ficam marcadas treino=S e SAO EXCLUIDAS da
   comparacao entre os metodos.
3. Da 6a em diante o numero esperado SOME. Medir com o gabarito a vista nao e
   medir: a mao procura o valor que ja conhece, e a comparacao passaria a dizer
   so que o operador acerta um alvo conhecido.

A ARITMETICA E A MESMA DA v1
largura = distancia PERPENDICULAR do ponto da borda interna a reta da borda
externa. Nao depende de onde, ao longo da borda interna, o ponto caiu, e um
atravessamento de esguelha nao infla a medida — agora nem e possivel faze-lo.

ESCOLHA DO TRECHO — do operador, e e o que decide a qualidade:
  - o lado SEM degrau, onde se enxerga so o topo do silicone;
  - onde a faixa parecer MAIS LARGA. Projecao so encurta, nunca alonga.

Uso:
    python mede_faixa2.py <pasta_plano> <pasta_saida> [<pasta_Cropped_images>]

Le   : <saida>/MEDIDAS.txt   — os nomes, na ordem, para formar a fila; e o
                               diametro APENAS das 5 primeiras, para o treino.
Grava: <saida>/FAIXAS.txt      nome<TAB>largura_px<TAB>treino<TAB>x1..y3
       <saida>/FAIXAS_LOG.tsv  o mesmo, com separacao da reta, fator e hora

APPEND com fsync a cada imagem. Ao reabrir, pula o que ja tem linha.

Na tela:
    arrasta    sobre a borda EXTERNA  -> trava o angulo
    move       a regua anda perpendicular, com a largura ao vivo
    clique     fixa o ponto da borda INTERNA
    Enter      grava e vai para a proxima
    n          grava SEM_FAIXA e vai para a proxima
    z          zoom 2x  ·  h  referencia  ·  r  recomeca  ·  q  sai

NAO MEXE no MEDIDAS.txt nem no MEDIDAS_LOG.tsv. Nao altera o motor, nenhuma
constante do v0, nenhum limiar e nenhum pre-registro.
"""
import os
import sys
import math
import datetime


# ---------------------------------------------------------------- constantes
# Faixa radial do splint = (16 - 10) / 2 = 3 mm. Os nominais 10 interno e 16
# externo vem do README e estao na EMENDA_1_CAMUNDONGO_30SET.md, anterior a
# qualquer medida.
FAIXA_MM = 3.0
ANEL_MM = 16.0

TREINO_N = 5            # quantas imagens da fila mostram o valor esperado
LUPA_LADO = 220
LUPA_ZOOM = 4.0
ZOOM_Z = 2.0
SEP_MIN_PX = 12.0       # arrasto mais curto que isso nao trava angulo confiavel


# ------------------------------------------------------------------- a conta
def largura(p1, p2, p3):
    """Distancia PERPENDICULAR de p3 a reta p1-p2. Devolve (largura, sep12)."""
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    dx, dy = bx - ax, by - ay
    sep = math.hypot(dx, dy)
    if sep == 0.0:
        return 0.0, 0.0
    return abs(dx * (cy - ay) - dy * (cx - ax)) / sep, sep


def pe_da_perpendicular(p1, p2, p3):
    """Onde a perpendicular baixada de p3 encontra a reta p1-p2. So desenho."""
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    dx, dy = bx - ax, by - ay
    dd = dx * dx + dy * dy
    if dd == 0.0:
        return p1
    t = ((cx - ax) * dx + (cy - ay) * dy) / dd
    return ax + t * dx, ay + t * dy


def janela_de(W, H, larg_tela, alt_tela, fator, z, off):
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
    if not os.path.isfile(p):
        sys.exit('PARADO: falta %s.' % p)
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


def le_diametros(p, apenas):
    """Diametro em px, SO dos nomes em `apenas` — as imagens de treino.

    Limitado de proposito: fora do treino a ferramenta nao tem como mostrar o
    valor esperado nem por engano, porque ele nao esta na memoria dela.
    """
    d = {}
    if not apenas:
        return d
    for linha in open(p, encoding='utf-8'):
        if linha.startswith('#') or not linha.strip():
            continue
        c = [x.strip() for x in linha.split('\t')]
        if c[0] in apenas and len(c) > 1 and c[1].upper() != 'SEM_ANEL':
            try:
                d[c[0]] = float(c[1])
            except ValueError:
                pass
    return d


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

    # treino: as TREINO_N primeiras da LISTA TOTAL, nao da fila da sessao, para
    # que reabrir a ferramenta no meio nao crie imagens de treino novas.
    treino = set(nomes[:TREINO_N])
    diam = le_diametros(p_med, treino)
    print('%d na lista | %d ja com faixa | %d nesta sessao | treino: %s'
          % (len(nomes), len(feitas), len(fila),
             ', '.join(sorted(treino & set(fila))) or 'nenhuma restante'))

    novo_fai = not os.path.isfile(p_fai) or not le_feitas(p_fai)
    novo_log = not os.path.isfile(p_log) or not le_feitas(p_log)
    f_fai = open(p_fai, 'a', encoding='utf-8')
    f_log = open(p_log, 'a', encoding='utf-8')
    if novo_fai:
        f_fai.write('# nome\tlargura_px\ttreino\tx1\ty1\tx2\ty2\tx3\ty3   '
                    '(largura=SEM_FAIXA quando nao ha trecho limpo)\n')
        f_fai.write('# largura = distancia PERPENDICULAR do ponto 3 a reta 1-2, '
                    'em px da imagem ORIGINAL. Faixa nominal %.1f mm.\n' % FAIXA_MM)
        f_fai.write('# treino=S: as %d primeiras, medidas COM o valor esperado a '
                    'vista. EXCLUIDAS da comparacao entre metodos.\n' % TREINO_N)
        f_fai.flush()
    if novo_log:
        f_log.write('# nome\tlargura_px\ttreino\tsep12_px\tx1\ty1\tx2\ty2\tx3\ty3'
                    '\tfator_reducao\tquando_iso\n')
        f_log.flush()

    raiz = tk.Tk()
    raiz.title('mede_faixa2 — regua de angulo travado · faixa de 3 mm')
    larg = raiz.winfo_screenwidth() - 60
    alt = raiz.winfo_screenheight() - 200
    barra = tk.Label(raiz, text='', font=('Consolas', 12), anchor='w', justify='left')
    barra.pack(fill='x')
    tela = tk.Canvas(raiz, width=larg, height=alt, bg='#202020', highlightthickness=0)
    tela.pack()

    # fase: 'borda'   -> arrastando/esperando o arrasto na borda externa
    #       'regua'   -> angulo travado, regua andando perpendicular
    #       'pronto'  -> ponto interno fixado, esperando Enter
    est = {'i': 0, 'fase': 'borda', 'a': None, 'b': None, 'c': None,
           'tk': None, 'fator': 1.0, 'z': 1.0, 'off': (0, 0), 'orig': None,
           'lupa': None, 'ref': None, 'ref_on': True, 'mouse': (0.0, 0.0),
           'arrastando': False}

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

    def desenha():
        """Desenha a reta da borda e a regua perpendicular. So vista."""
        tela.delete('marca')
        if est['a'] is None or est['b'] is None:
            return
        sa = para_tela(*est['a'])
        sb = para_tela(*est['b'])
        tela.create_line(sa[0], sa[1], sb[0], sb[1], fill='#00ff88', width=2,
                         tags='marca')
        for s in (sa, sb):
            tela.create_oval(s[0] - 4, s[1] - 4, s[0] + 4, s[1] + 4,
                             outline='#00ff88', width=2, tags='marca')
        if est['fase'] == 'borda':
            return
        # ponto que a regua esta apontando: o fixado, ou o mouse ao vivo
        c = est['c'] if est['c'] is not None else est['mouse']
        pe = pe_da_perpendicular(est['a'], est['b'], c)
        sc = para_tela(*c)
        sp = para_tela(*pe)
        cor = '#ffcc00' if est['c'] is not None else '#ff9900'
        tela.create_line(sp[0], sp[1], sc[0], sc[1], fill=cor, width=3, tags='marca')
        tela.create_oval(sc[0] - 5, sc[1] - 5, sc[0] + 5, sc[1] + 5,
                         outline=cor, width=2, tags='marca')

    def mostra_referencia(nome):
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
        e_treino = nome in treino
        msg = '%d/%d  %s%s   ' % (est['i'] + 1, len(fila), nome,
                                  '   [TREINO]' if e_treino else '')
        if est['fase'] == 'borda':
            msg += 'ARRASTE sobre a borda EXTERNA para travar o angulo'
        elif est['fase'] == 'regua':
            lg, _s = largura(est['a'], est['b'], est['mouse'])
            msg += 'angulo TRAVADO · largura %.1f px · clique na borda INTERNA' % lg
        else:
            lg, _s = largura(est['a'], est['b'], est['c'])
            msg += 'largura %.1f px · Enter grava' % lg
        aviso = ''
        if est['a'] is not None and est['b'] is not None:
            _l, sep = largura(est['a'], est['b'], est['mouse'])
            if sep < SEP_MIN_PX:
                aviso = ('ATENCAO: o arrasto tem so %.0f px (minimo %.0f) — a reta '
                         'fica instavel e o angulo travado sai errado. r para refazer.'
                         % (sep, SEP_MIN_PX))
        if e_treino and nome in diam:
            esperado = diam[nome] * FAIXA_MM / ANEL_MM
            msg += '   | TREINO: diametro %.0f px, faixa esperada %.0f px' % (
                diam[nome], esperado)
        if est['z'] > 1.0:
            msg += '   [z] ZOOM %gx' % est['z']
        msg += ('    [n SEM_FAIXA · z zoom · h referencia · r recomeca · q sai]')
        if aviso:
            msg += '\n' + aviso
        if extra:
            msg += '\n' + extra
        barra.config(text=msg)

    def carrega():
        est['fase'] = 'borda'
        est['a'] = est['b'] = est['c'] = None
        est['arrastando'] = False
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

    # ------------------------------------------------------------ o mouse
    def aperta(ev):
        if est['fase'] == 'borda':
            est['a'] = para_orig(ev.x, ev.y)
            est['b'] = est['a']
            est['arrastando'] = True
            desenha(); status()
        elif est['fase'] == 'regua':
            est['c'] = para_orig(ev.x, ev.y)
            est['fase'] = 'pronto'
            desenha(); status()

    def arrasta(ev):
        if est['arrastando']:
            est['b'] = para_orig(ev.x, ev.y)
            desenha(); status()

    def solta(ev):
        if not est['arrastando']:
            return
        est['arrastando'] = False
        est['b'] = para_orig(ev.x, ev.y)
        _l, sep = largura(est['a'], est['b'], est['a'])
        if sep < SEP_MIN_PX:
            status('arrasto curto demais — refaca sobre a borda EXTERNA')
            est['a'] = est['b'] = None
            tela.delete('marca')
            return
        est['fase'] = 'regua'          # a partir daqui o angulo nao muda mais
        desenha(); status()

    def move(ev):
        """Lupa e regua ao vivo. So enxergar: nao registra nada."""
        im = est['orig']
        if im is None:
            return
        x, y = para_orig(ev.x, ev.y)
        est['mouse'] = (x, y)
        if est['fase'] == 'regua':
            desenha()
            status()
        xi, yi = int(x), int(y)
        lado = int(LUPA_LADO / LUPA_ZOOM)
        cai = im.crop((xi - lado // 2, yi - lado // 2, xi + lado // 2, yi + lado // 2))
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
        t = 'S' if nome in treino else 'N'
        agora = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
        if k == 'q':
            print('saiu em %s — %d faixas gravadas nesta sessao' % (nome, est['i']))
            raiz.destroy()
        elif k == 'r':
            carrega()
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
            desenha_fundo(); desenha(); mostra_referencia(nome)
            status()
        elif k == 'n':
            grava('%s\tSEM_FAIXA\t%s\t-\t-\t-\t-\t-\t-\n' % (nome, t),
                  '%s\tSEM_FAIXA\t%s\t\t\t\t\t\t\t\t%.6f\t%s\n'
                  % (nome, t, est['fator'], agora))
            proxima()
        elif k == 'return':
            if est['fase'] != 'pronto':
                status('falta: arraste na borda EXTERNA e clique na INTERNA')
                return
            lg, sep = largura(est['a'], est['b'], est['c'])
            pts = '\t'.join('%.3f\t%.3f' % p for p in (est['a'], est['b'], est['c']))
            grava('%s\t%.3f\t%s\t%s\n' % (nome, lg, t, pts),
                  '%s\t%.3f\t%s\t%.3f\t%s\t%.6f\t%s\n'
                  % (nome, lg, t, sep, pts, est['fator'], agora))
            proxima()

    tela.bind('<ButtonPress-1>', aperta)
    tela.bind('<B1-Motion>', arrasta)
    tela.bind('<ButtonRelease-1>', solta)
    tela.bind('<Motion>', move)
    raiz.bind('<Key>', tecla)
    carrega()
    raiz.mainloop()
    f_fai.close(); f_log.close()


if __name__ == '__main__':
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else None)
