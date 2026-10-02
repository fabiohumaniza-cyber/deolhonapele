"""
mede_buraco2.py — medida MANUAL do BURACO do splint (borda interna, 10 mm),
com a mesma regua de UM GESTO e angulo travado da mede_faixa3.py.

POR QUE EXISTE
Ideia do Fabio, 02/10/2026, 12h39: "se o anel tem um circulo, pode ser que ele
seja mais exato que seu formato". Medir o DIAMETRO DO BURACO, atravessando a
ferida, em vez da faixa de 3 mm.

O argumento, e ele e forte:
  1. A base cresce de 3 mm (faixa) para 10 mm (buraco): o mesmo erro de clique
     pesa 3,3 vezes menos. Contra os 16 mm da borda externa, perde so 1,6x.
  2. Atravessando o buraco, a perspectiva deixa de depender de escolher o lado
     certo: a maior corda de uma elipse e o eixo maior, e o eixo maior de um
     circulo de 10 mm visto inclinado continua sendo 10 mm. A faixa nao tinha
     esse recurso, e era o buraco dela — ali a espessura de 1,6 mm do silicone
     inflava um lado e encurtava o outro, e so o olho decidia.
  3. Quando o rato come a borda EXTERNA, o buraco pode continuar inteiro — ou
     seja, ha escala onde hoje se grava SEM_ANEL.

Contra, declarado: a borda interna e a mais lavada das duas, porque o coverslip
plastico de 16 mm e o Tegaderm passam por cima do buraco. O mesmo erro de borda
que na faixa de 114 px pesava ~2 % aqui pesa ~0,5 %, mas o vies de clipar a
transicao continua existindo e sera medido, nao suposto.

ESTA FERRAMENTA E A mede_faixa3.py COM TRES TROCAS, E SO ELAS
  - nominal de 3 mm passa a 10 mm;
  - o valor esperado mostrado no treino passa a ser externo x 10/16;
  - grava em INTERNOS.txt / INTERNOS_LOG.tsv, nao em FAIXAS.txt.
O gesto, o travamento do angulo, o zoom pela roda, a lupa, as teclas e a
aritmetica sao identicos, byte a byte, ao que o operador validou a mao.

O GESTO
    0. botao DIREITO        -> arrasta a imagem, para centralizar
    1. roda do mouse        -> zoom, centrado onde o ponteiro esta
    2. aperta numa ponta do buraco
    3. move alguns pixels   -> O ANGULO TRAVA na direcao desse movimento
    4. arrasta ate a outra ponta, PASSANDO PELO MEIO. A regua so estica e
       encolhe naquela direcao: o ponteiro pode sair da linha que a medida nao
       gira.
    5. solta -> fixa  ·  Enter -> grava

COMO ACERTAR
A maior corda do buraco e o diametro. Corda fora do centro mede MENOS. Entao
atravesse pelo meio, no sentido em que o buraco parece mais comprido. Em ensaio
do operador na imagem 5 do treino, tres travessias deram 370, 376 e 380 px
contra 374,4 esperados — dispersao de +-1,3 %.

MAS NAO FIQUE COM O MAIOR DE MUITAS TENTATIVAS: passar do centro encurta, e
passar da borda lavada alonga. Pegar sempre o maior seleciona as travessias que
estouraram a borda. Uma travessia feita com cuidado basta; em duvida, duas, e
fica com a do meio.

TREINO
As TREINO_N primeiras mostram o diametro EXTERNO ja medido e o interno esperado
(externo x 10/16). Ficam marcadas treino=S e sao EXCLUIDAS da comparacao entre
metodos. Da seguinte em diante o numero esperado SOME: medir com o gabarito a
vista nao e medir.

Uso:
    python mede_buraco2.py <pasta_plano> <pasta_saida> [<pasta_Cropped_images>]

Le   : <saida>/MEDIDAS.txt   — os nomes, na ordem; e o diametro externo APENAS
                               das TREINO_N primeiras.
Grava: <saida>/INTERNOS.txt      nome<TAB>diametro_px<TAB>treino<TAB>x1<TAB>y1<TAB>x2<TAB>y2
       <saida>/INTERNOS_LOG.tsv  o mesmo, com zoom, fator de reducao e hora

APPEND com fsync a cada imagem. Ao reabrir, pula o que ja tem linha.

Teclas: Enter grava · n SEM_BURACO · r refaz · h referencia · q sai
        (zoom e a roda do mouse; a tecla z continua funcionando)

NAO MEXE no MEDIDAS.txt, no MEDIDAS_LOG.tsv nem no FAIXAS.txt. Nao altera o
motor, nenhuma constante do v0, nenhum limiar e nenhum pre-registro.
"""
import os
import sys
import math
import datetime


# ---------------------------------------------------------------- constantes
# Buraco do splint = 10 mm de diametro. Nominais do README, registrados
# na EMENDA_1_CAMUNDONGO_30SET.md, anterior a qualquer medida.
BURACO_MM = 10.0
ANEL_MM = 16.0

TREINO_N = 5
LUPA_LADO = 220
LUPA_ZOOM = 4.0
TRAVA_PX = 6.0          # movimento minimo, em px de tela, para travar o angulo
ZOOMS = (1.0, 1.5, 2.0, 3.0, 4.0, 6.0)


# ------------------------------------------------------------------- a conta
def direcao(p, q):
    """Vetor unitario de p para q. Devolve None se forem o mesmo ponto."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy)
    if n == 0.0:
        return None
    return dx / n, dy / n


def projeta(ancora, u, m):
    """Ponto final da regua: projecao de m sobre a semirreta ancora+t*u, t>=0.

    E AQUI que o angulo fica travado. O ponteiro pode sair da linha o quanto
    quiser; o que entra na medida e so o quanto ele andou NA DIRECAO u. A regua
    estica e encolhe, nunca gira.
    """
    t = (m[0] - ancora[0]) * u[0] + (m[1] - ancora[1]) * u[1]
    if t < 0.0:
        t = 0.0
    return (ancora[0] + t * u[0], ancora[1] + t * u[1]), t


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
    """Diametro em px SO dos nomes de treino. Fora deles a ferramenta nao tem o
    valor na memoria e nao pode mostra-lo nem por engano."""
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
    s = set()
    for linha in open(p, encoding='utf-8'):
        if linha.startswith('#') or not linha.strip():
            continue
        s.add(linha.split('\t')[0].strip())
    return s


def main(pasta, saida, recortes=None):
    import tkinter as tk
    from PIL import Image, ImageTk

    p_med = os.path.join(saida, 'MEDIDAS.txt')
    p_bur = os.path.join(saida, 'INTERNOS.txt')
    p_log = os.path.join(saida, 'INTERNOS_LOG.tsv')

    nomes = le_nomes(p_med)
    feitas = le_feitas(p_bur)
    fila = [n for n in nomes if n not in feitas]
    if not fila:
        print('nada a medir: as %d imagens ja tem linha em INTERNOS.txt' % len(nomes))
        return
    treino = set(nomes[:TREINO_N])
    diam = le_diametros(p_med, treino)
    print('%d na lista | %d ja com buraco | %d nesta sessao' %
          (len(nomes), len(feitas), len(fila)))

    novo_bur = not os.path.isfile(p_bur) or not le_feitas(p_bur)
    novo_log = not os.path.isfile(p_log) or not le_feitas(p_log)
    f_bur = open(p_bur, 'a', encoding='utf-8')
    f_log = open(p_log, 'a', encoding='utf-8')
    if novo_bur:
        f_bur.write('# nome\tdiametro_px\ttreino\tx1\ty1\tx2\ty2   '
                    '(largura=SEM_BURACO quando nao ha trecho limpo)\n')
        f_bur.write('# 1 e 2 = as duas pontas da travessia do '
                    'buraco, na direcao travada. Buraco nominal %.1f mm.\n' % BURACO_MM)
        f_bur.write('# treino=S: as %d primeiras, medidas COM o valor esperado a '
                    'vista. EXCLUIDAS da comparacao entre metodos.\n' % TREINO_N)
        f_bur.flush()
    if novo_log:
        f_log.write('# nome\tdiametro_px\ttreino\tx1\ty1\tx2\ty2\tzoom'
                    '\tfator_reducao\tquando_iso\n')
        f_log.flush()

    raiz = tk.Tk()
    raiz.title('mede_buraco — regua travada · buraco do splint (10 mm)')
    larg = raiz.winfo_screenwidth() - 60
    alt = raiz.winfo_screenheight() - 200
    barra = tk.Label(raiz, text='', font=('Consolas', 12), anchor='w', justify='left')
    barra.pack(fill='x')
    tela = tk.Canvas(raiz, width=larg, height=alt, bg='#202020', highlightthickness=0)
    tela.pack()

    # fase: 'livre'  -> nada comecado
    #       'arrasta'-> botao apertado; angulo pode ainda nao ter travado
    #       'pronto' -> soltou; medida fixada, esperando Enter
    est = {'i': 0, 'fase': 'livre', 'anc': None, 'u': None, 'fim': None,
           'diam_px': 0.0, 'tk': None, 'fator': 1.0, 'iz': 0, 'off': (0, 0),
           'orig': None, 'lupa': None, 'ref': None, 'ref_on': True,
           'mouse': (0.0, 0.0), 'pan': None}

    REF_LADO = 240

    def z():
        return ZOOMS[est['iz']]

    def janela():
        W, H = est['orig'].size
        ox, oy, ww, wh, e = janela_de(W, H, larg, alt, est['fator'], z(), est['off'])
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
        tela.delete('marca')
        if est['anc'] is None:
            return
        sa = para_tela(*est['anc'])
        cor = '#ffcc00' if est['fase'] == 'pronto' else '#00ff88'
        tela.create_oval(sa[0] - 4, sa[1] - 4, sa[0] + 4, sa[1] + 4,
                         outline=cor, width=2, tags='marca')
        if est['fim'] is None:
            return
        sb = para_tela(*est['fim'])
        tela.create_line(sa[0], sa[1], sb[0], sb[1], fill=cor, width=3, tags='marca')
        tela.create_oval(sb[0] - 4, sb[1] - 4, sb[0] + 4, sb[1] + 4,
                         outline=cor, width=2, tags='marca')
        # traco curto perpendicular nas duas pontas, so para enxergar a regua
        if est['u'] is not None:
            ux, uy = est['u']
            px, py = -uy * 7, ux * 7
            for s in (sa, sb):
                tela.create_line(s[0] - px, s[1] - py, s[0] + px, s[1] + py,
                                 fill=cor, width=2, tags='marca')

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
        _ox, _oy, ww, _wh, e = janela()
        dir_foto = int(ww * e)
        livre = larg - dir_foto - 20
        if livre >= im.size[0]:
            rx = dir_foto + 12
            ry = 10 + LUPA_LADO + 26 if rx + im.size[0] > larg - LUPA_LADO - 20 else 26
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
        e_tr = nome in treino
        msg = '%d/%d  %s%s   ' % (est['i'] + 1, len(fila), nome,
                                  '  [TREINO]' if e_tr else '')
        if est['fase'] == 'livre':
            msg += 'APERTE numa ponta do BURACO e arraste ate a outra, passando pelo MEIO'
        elif est['fase'] == 'arrasta':
            msg += ('ANGULO TRAVADO · diametro interno %.1f px · solte na outra ponta do buraco'
                    % est['diam_px'] if est['u'] else 'mova para travar o angulo')
        else:
            msg += 'diametro interno %.1f px · Enter grava · r refaz' % est['diam_px']
        if e_tr and nome in diam:
            msg += '   | TREINO: externo %.0f px, interno esperado %.0f px' % (
                diam[nome], diam[nome] * BURACO_MM / ANEL_MM)
        msg += '   zoom %gx' % z()
        msg += '    [roda = zoom · botao direito arrasta a imagem · n SEM_BURACO · r refaz · h referencia · q sai]'
        if extra:
            msg += '\n' + extra
        barra.config(text=msg)

    def carrega():
        est['fase'] = 'livre'
        est['anc'] = est['u'] = est['fim'] = None
        est['diam_px'] = 0.0
        est['iz'] = 0
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

    def lupa(x, y):
        im = est['orig']
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

    # ------------------------------------------------------------- o mouse
    def aperta(ev):
        est['anc'] = para_orig(ev.x, ev.y)
        est['u'] = None
        est['fim'] = None
        est['diam_px'] = 0.0
        est['fase'] = 'arrasta'
        desenha(); status()

    def arrasta(ev):
        if est['fase'] != 'arrasta' or est['anc'] is None:
            return
        m = para_orig(ev.x, ev.y)
        est['mouse'] = m
        if est['u'] is None:
            # ainda nao travou: trava assim que o movimento passar do minimo
            sa = para_tela(*est['anc'])
            if math.hypot(ev.x - sa[0], ev.y - sa[1]) < TRAVA_PX:
                lupa(*m)
                return
            est['u'] = direcao(est['anc'], m)
            if est['u'] is None:
                return
        est['fim'], est['diam_px'] = projeta(est['anc'], est['u'], m)
        desenha(); status(); lupa(*m)

    def solta(ev):
        if est['fase'] != 'arrasta':
            return
        if est['u'] is None or est['diam_px'] <= 0.0:
            est['fase'] = 'livre'
            est['anc'] = est['fim'] = None
            tela.delete('marca')
            status('arrasto curto demais — atravesse o buraco inteiro')
            return
        est['fase'] = 'pronto'
        desenha(); status()

    def move(ev):
        if est['orig'] is None:
            return
        m = para_orig(ev.x, ev.y)
        est['mouse'] = m
        lupa(*m)

    def roda(ev):
        """Zoom pela roda, centrado onde o ponteiro esta.

        So vista: a geometria vive em px da imagem ORIGINAL, entao mudar o zoom
        nao altera medida nenhuma — nem a que ja esta fixada na tela.
        """
        if est['orig'] is None:
            return
        passo = 1 if getattr(ev, 'delta', 0) > 0 or getattr(ev, 'num', 0) == 4 else -1
        novo = min(max(est['iz'] + passo, 0), len(ZOOMS) - 1)
        if novo == est['iz']:
            return
        mx, my = para_orig(ev.x, ev.y)
        est['iz'] = novo
        W, H = est['orig'].size
        e = est['fator'] * z()
        ww = int(min(W, larg / e)); wh = int(min(H, alt / e))
        est['off'] = (int(mx - ww / 2), int(my - wh / 2))
        desenha_fundo(); desenha(); mostra_referencia(fila[est['i']])
        status()

    # ------------------------------------------------- arrastar a imagem
    # Botao DIREITO move a vista. So vista: a geometria vive em px da imagem
    # ORIGINAL, entao arrastar a imagem nao altera medida nenhuma — nem a que ja
    # esta fixada, que e redesenhada no mesmo lugar da foto.
    def pan_aperta(ev):
        _ox, _oy, _ww, _wh, e = janela()
        est['pan'] = (ev.x, ev.y, est['off'][0], est['off'][1], e)

    def pan_arrasta(ev):
        if est['pan'] is None:
            return
        sx, sy, ox0, oy0, e = est['pan']
        est['off'] = (int(ox0 - (ev.x - sx) / e), int(oy0 - (ev.y - sy) / e))
        desenha_fundo(); desenha(); mostra_referencia(fila[est['i']])

    def pan_solta(_ev):
        est['pan'] = None

    def grava(linha, log):
        f_bur.write(linha); f_bur.flush(); os.fsync(f_bur.fileno())
        f_log.write(log); f_log.flush(); os.fsync(f_log.fileno())

    def proxima():
        est['i'] += 1
        if est['i'] >= len(fila):
            print('fim da fila: %d buracos nesta sessao' % len(fila))
            raiz.destroy()
            return
        carrega()

    def tecla(ev):
        k = ev.keysym.lower()
        nome = fila[est['i']]
        t = 'S' if nome in treino else 'N'
        agora = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
        if k == 'q':
            print('saiu em %s — %d gravados nesta sessao' % (nome, est['i']))
            raiz.destroy()
        elif k == 'r':
            carrega()
        elif k == 'h':
            est['ref_on'] = not est['ref_on']
            mostra_referencia(nome)
        elif k == 'z':
            est['iz'] = 0 if est['iz'] else 2
            desenha_fundo(); desenha(); mostra_referencia(nome); status()
        elif k == 'n':
            grava('%s\tSEM_BURACO\t%s\t-\t-\t-\t-\n' % (nome, t),
                  '%s\tSEM_BURACO\t%s\t\t\t\t\t%g\t%.6f\t%s\n'
                  % (nome, t, z(), est['fator'], agora))
            proxima()
        elif k == 'return':
            if est['fase'] != 'pronto':
                status('falta medir: aperte numa ponta do buraco e arraste ate a outra')
                return
            pts = '%.3f\t%.3f\t%.3f\t%.3f' % (est['anc'][0], est['anc'][1],
                                              est['fim'][0], est['fim'][1])
            grava('%s\t%.3f\t%s\t%s\n' % (nome, est['diam_px'], t, pts),
                  '%s\t%.3f\t%s\t%s\t%g\t%.6f\t%s\n'
                  % (nome, est['diam_px'], t, pts, z(), est['fator'], agora))
            proxima()

    tela.bind('<ButtonPress-1>', aperta)
    tela.bind('<B1-Motion>', arrasta)
    tela.bind('<ButtonRelease-1>', solta)
    tela.bind('<ButtonPress-3>', pan_aperta)
    tela.bind('<B3-Motion>', pan_arrasta)
    tela.bind('<ButtonRelease-3>', pan_solta)
    tela.bind('<Motion>', move)
    tela.bind('<MouseWheel>', roda)          # Windows e macOS
    tela.bind('<Button-4>', roda)            # Linux
    tela.bind('<Button-5>', roda)
    raiz.bind('<Key>', tecla)
    carrega()
    raiz.mainloop()
    f_bur.close(); f_log.close()


if __name__ == '__main__':
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) == 4 else None)
