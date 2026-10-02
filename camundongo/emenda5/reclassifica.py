"""
reclassifica.py — reabre um subconjunto nomeado de imagens no classificador.

POR QUE EXISTE
Em 02/10/2026, as 18h24, o Fabio relatou que em varias imagens escreveu no
comentario que havia plastico sobre a ferida mas NAO acionou a marca p. A
varredura do CLASSIFICACAO.txt encontrou 11 casos. Arrastar as setas por 255
imagens para corrigir 11 e inviavel, e sair editando o arquivo a mao e pior.

ESTE ARQUIVO E UMA COPIA do classifica_ferida.py
(ddbee3eaa44146be7e259783e8e2b04d81c1c0cf28c268fa0e6cc7fecbcc5f93), com UMA
mudanca: um quarto argumento opcional, um arquivo de texto com um nome de
imagem por linha. Quando ele e dado, o censo da sessao e so aquela lista, na
mesma ordem alfabetica. Todo o resto — vocabulario, gravacao, lupa, zoom,
arrasto, referencia do banco — e identico, byte a byte.

Arquivo novo e nao edicao porque o classifica_ferida.py ja tem hash citado nos
Adendos 6 e 9, e arquivo com hash e imutavel.

O ARQUIVO DE SAIDA NAO E REESCRITO. A declaracao nova entra como LINHA NOVA no
mesmo CLASSIFICACAO.txt, com hora. Vale a ultima; a anterior fica como
historico, e e assim que se audita quem mudou de ideia e quando.

Uso:
    python reclassifica.py <pasta_plano> <pasta_saida> <pasta_Cropped> <lista.txt>

O quarto argumento e obrigatorio nesta versao: sem lista, use o
classifica_ferida.py original.

Na tela, igual ao original:
    botoes grandes, ou as teclas v  c  n  d
    p ou o botao     liga/desliga plastico sobre a ferida
    setas  <-  ->    andam entre as imagens sem classificar
    roda do mouse    zoom          botao direito    arrasta a imagem
    h                esconde/mostra o recorte de referencia do banco
    q                sai; da proxima vez retoma onde parou

NAO MEXE no MEDIDAS.txt, no INTERNOS.txt nem em nada do motor. Nao altera
constante, limiar ou pre-registro.
"""
import os
import sys
import datetime


CLASSES = [('v', 'Vejo a ferida',      '#1f7a3d'),
           ('c', 'Cicatrizada',        '#1f5f9e'),
           ('n', 'Nao da para laudar', '#a33019'),
           ('d', 'Em duvida',          '#5a5a5a')]

LUPA_LADO = 200
LUPA_ZOOM = 4.0
ZOOMS = (1.0, 1.5, 2.0, 3.0, 4.0, 6.0)
EXTS = ('.tif', '.tiff')


# ------------------------------------------------------------------ a vista
def janela_de(W, H, larg_tela, alt_tela, fator, z, off):
    e = fator * z
    ww = int(min(W, larg_tela / e))
    wh = int(min(H, alt_tela / e))
    ox = int(min(max(0, off[0]), W - ww))
    oy = int(min(max(0, off[1]), H - wh))
    return ox, oy, ww, wh, e


def tela_para_orig(sx, sy, ox, oy, e):
    return ox + sx / e, oy + sy / e


def limpa(txt):
    """Comentario em uma linha, sem tabulacao: o arquivo e TSV."""
    return ' '.join(str(txt).replace('\t', ' ').split())


# ---------------------------------------------------------------- arquivos
def le_lista(p):
    """Um nome de imagem por linha. Linhas vazias e comecadas por # sao ignoradas."""
    if not os.path.isfile(p):
        sys.exit('PARADO: nao achei a lista %s' % p)
    nomes = []
    for linha in open(p, encoding='utf-8'):
        n = linha.strip()
        if n and not n.startswith('#'):
            nomes.append(n)
    if not nomes:
        sys.exit('PARADO: a lista %s esta vazia' % p)
    return nomes


def lista_imagens(pasta, so=None):
    if not os.path.isdir(pasta):
        sys.exit('PARADO: nao achei a pasta %s' % pasta)
    ns = sorted(n for n in os.listdir(pasta) if n.lower().endswith(EXTS))
    if not ns:
        sys.exit('PARADO: nenhuma imagem .tif/.tiff em %s' % pasta)
    if so is not None:
        tem = set(ns)
        faltam = [n for n in so if n not in tem]
        if faltam:
            sys.exit('PARADO: a lista pede nomes que nao estao na pasta:\n  ' +
                     '\n  '.join(faltam))
        ns = sorted(set(so))
    return ns


def le_classificacao(p):
    """Ultima linha de cada nome. As anteriores ficam no arquivo, como historico."""
    feito = {}
    if not os.path.isfile(p):
        return feito
    for linha in open(p, encoding='utf-8'):
        if linha.startswith('#') or not linha.strip():
            continue
        c = linha.rstrip('\n\r').split('\t')
        if len(c) >= 3:
            feito[c[0]] = (c[1], c[2], c[3] if len(c) > 3 else '')
    return feito


def main(pasta, saida, recortes=None, lista=None):
    import tkinter as tk
    from PIL import Image, ImageTk

    p_cla = os.path.join(saida, 'CLASSIFICACAO.txt')
    so = le_lista(lista) if lista else None
    nomes = lista_imagens(pasta, so)
    feito = le_classificacao(p_cla)
    print('%d imagens na pasta | %d ja classificadas' % (len(nomes), len(feito)))

    novo = not os.path.isfile(p_cla)
    f = open(p_cla, 'a', encoding='utf-8')
    if novo:
        f.write('# nome\tclasse\tplastico\tcomentario\tquando_iso\n')
        f.write('# classe: v=vejo a ferida · c=cicatrizada · n=nao da para laudar '
                '· d=em duvida\n')
        f.write('# plastico: S quando ha filme/plastico sobre a FERIDA, N quando nao\n')
        f.write('# comentario: texto livre, descritivo. NAO e categoria e nao entra '
                'em contagem.\n')
        f.write('# censo: todas as imagens da pasta, em ordem alfabetica, sem amostra '
                'e sem selecao.\n')
        f.write('# vale a ULTIMA linha de cada nome; as anteriores ficam como '
                'historico.\n')
        f.flush()

    raiz = tk.Tk()
    raiz.title('classifica_ferida — a ferida esta na fotografia?')
    LARG = raiz.winfo_screenwidth() - 60
    ALT = raiz.winfo_screenheight() - 300

    barra = tk.Label(raiz, text='', font=('Consolas', 13), anchor='w', justify='left')
    barra.pack(fill='x')
    tela = tk.Canvas(raiz, width=LARG, height=ALT, bg='#202020', highlightthickness=0)
    tela.pack()

    rodape = tk.Frame(raiz)
    rodape.pack(fill='x', pady=6)

    est = {'i': 0, 'tk': None, 'fator': 1.0, 'iz': 0, 'off': (0, 0), 'orig': None,
           'lupa': None, 'ref': None, 'ref_on': True, 'pan': None,
           'plastico': False}

    def z():
        return ZOOMS[est['iz']]

    def janela():
        W, H = est['orig'].size
        ox, oy, ww, wh, e = janela_de(W, H, LARG, ALT, est['fator'], z(), est['off'])
        est['off'] = (ox, oy)
        return ox, oy, ww, wh, e

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

    def mostra_referencia():
        tela.delete('ref')
        est['ref'] = None
        if not recortes or not est['ref_on']:
            return
        p = os.path.join(recortes, os.path.splitext(nomes[est['i']])[0] + '.png')
        if not os.path.isfile(p):
            return
        im = Image.open(p).convert('RGB')
        im.thumbnail((230, 230), Image.LANCZOS)
        est['ref'] = ImageTk.PhotoImage(im)
        _ox, _oy, ww, _wh, e = janela()
        rx = min(int(ww * e) + 12, LARG - im.size[0] - 10)
        ry = 10 + LUPA_LADO + 30
        tela.create_text(rx, ry - 14, anchor='w', fill='#ffcc00',
                         font=('Consolas', 10, 'bold'), tags='ref',
                         text='referencia do banco — e ESTA ferida  [h]')
        tela.create_image(rx, ry, anchor='nw', image=est['ref'], tags='ref')
        tela.create_rectangle(rx, ry, rx + im.size[0], ry + im.size[1],
                              outline='#ffcc00', width=2, tags='ref')

    def status():
        nome = nomes[est['i']]
        ja = feito.get(nome)
        msg = '%d/%d   %s' % (est['i'] + 1, len(nomes), nome)
        if ja:
            rot = dict((k, t) for k, t, _c in CLASSES).get(ja[0], ja[0])
            msg += '   [ja classificada: %s%s]' % (rot, ', plastico' if ja[1] == 'S' else '')
        msg += '    plastico: %s' % ('SIM' if est['plastico'] else 'nao')
        msg += '    zoom %gx' % z()
        msg += '    [setas andam · roda zoom · botao direito arrasta · h referencia · q sai]'
        barra.config(text=msg)
        bt_pl.config(relief='sunken' if est['plastico'] else 'raised',
                     bg='#e8c33a' if est['plastico'] else '#dddddd')

    def carrega():
        est['iz'] = 0
        est['off'] = (0, 0)
        nome = nomes[est['i']]
        ja = feito.get(nome)
        est['plastico'] = bool(ja and ja[1] == 'S')
        cx.delete(0, 'end')
        if ja and ja[2]:
            cx.insert(0, ja[2])
        barra.config(text='carregando %s …' % nome)
        raiz.update_idletasks()
        est['orig'] = Image.open(os.path.join(pasta, nome)).convert('RGB')
        W, H = est['orig'].size
        est['fator'] = min(LARG / float(W), ALT / float(H), 1.0)
        desenha_fundo()
        mostra_referencia()
        status()

    def anda(passo):
        novo_i = est['i'] + passo
        if 0 <= novo_i < len(nomes):
            est['i'] = novo_i
            carrega()

    def declara(k):
        nome = nomes[est['i']]
        com = limpa(cx.get())
        agora = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
        linha = '%s\t%s\t%s\t%s\t%s\n' % (nome, k, 'S' if est['plastico'] else 'N',
                                          com, agora)
        f.write(linha); f.flush(); os.fsync(f.fileno())
        feito[nome] = (k, 'S' if est['plastico'] else 'N', com)
        if est['i'] + 1 >= len(nomes):
            print('fim: %d de %d classificadas' % (len(feito), len(nomes)))
            status()
            return
        anda(1)

    # ------------------------------------------------------------- mouse
    def pan_aperta(ev):
        _ox, _oy, _ww, _wh, e = janela()
        est['pan'] = (ev.x, ev.y, est['off'][0], est['off'][1], e)

    def pan_arrasta(ev):
        if est['pan'] is None:
            return
        sx, sy, ox0, oy0, e = est['pan']
        est['off'] = (int(ox0 - (ev.x - sx) / e), int(oy0 - (ev.y - sy) / e))
        desenha_fundo(); mostra_referencia()

    def pan_solta(_ev):
        est['pan'] = None

    def move(ev):
        im = est['orig']
        if im is None:
            return
        x, y = para_orig(ev.x, ev.y)
        xi, yi = int(x), int(y)
        lado = int(LUPA_LADO / LUPA_ZOOM)
        cai = im.crop((xi - lado // 2, yi - lado // 2, xi + lado // 2, yi + lado // 2))
        cai = cai.resize((LUPA_LADO, LUPA_LADO), Image.NEAREST)
        est['lupa'] = ImageTk.PhotoImage(cai)
        tela.delete('lupa')
        lx = LARG - LUPA_LADO - 10
        tela.create_image(lx, 10, anchor='nw', image=est['lupa'], tags='lupa')
        tela.create_rectangle(lx, 10, lx + LUPA_LADO, 10 + LUPA_LADO,
                              outline='#00ff88', tags='lupa')

    def roda(ev):
        if est['orig'] is None:
            return
        passo = 1 if getattr(ev, 'delta', 0) > 0 or getattr(ev, 'num', 0) == 4 else -1
        novo_iz = min(max(est['iz'] + passo, 0), len(ZOOMS) - 1)
        if novo_iz == est['iz']:
            return
        mx, my = para_orig(ev.x, ev.y)
        est['iz'] = novo_iz
        W, H = est['orig'].size
        e = est['fator'] * z()
        ww = int(min(W, LARG / e)); wh = int(min(H, ALT / e))
        est['off'] = (int(mx - ww / 2), int(my - wh / 2))
        desenha_fundo(); mostra_referencia(); status()

    def plastico():
        est['plastico'] = not est['plastico']
        status()

    def tecla(ev):
        if raiz.focus_get() is cx and ev.keysym.lower() not in ('left', 'right', 'escape'):
            return                      # digitando comentario: nao atalha
        k = ev.keysym.lower()
        if k == 'q':
            raiz.destroy()
        elif k == 'h':
            est['ref_on'] = not est['ref_on']; mostra_referencia()
        elif k == 'p':
            plastico()
        elif k == 'left':
            anda(-1)
        elif k == 'right':
            anda(1)
        elif k == 'escape':
            tela.focus_set()
        elif k in [c for c, _t, _cor in CLASSES]:
            declara(k)

    # ------------------------------------------------------------ rodape
    for c, titulo, cor in CLASSES:
        tk.Button(rodape, text='%s   [%s]' % (titulo, c), font=('Segoe UI', 13, 'bold'),
                  fg='white', bg=cor, activebackground=cor, padx=18, pady=10,
                  command=(lambda kk=c: declara(kk))).pack(side='left', padx=6)

    bt_pl = tk.Button(rodape, text='Plastico sobre a ferida   [p]',
                      font=('Segoe UI', 12), padx=14, pady=10, command=plastico)
    bt_pl.pack(side='left', padx=18)

    tk.Button(rodape, text='<', font=('Segoe UI', 13, 'bold'), padx=12, pady=10,
              command=lambda: anda(-1)).pack(side='left', padx=(18, 2))
    tk.Button(rodape, text='>', font=('Segoe UI', 13, 'bold'), padx=12, pady=10,
              command=lambda: anda(1)).pack(side='left', padx=2)

    tk.Label(rodape, text='  comentario:', font=('Segoe UI', 11)).pack(side='left')
    cx = tk.Entry(rodape, font=('Segoe UI', 12), width=46)
    cx.pack(side='left', padx=6, fill='x', expand=True)

    tela.bind('<ButtonPress-3>', pan_aperta)
    tela.bind('<B3-Motion>', pan_arrasta)
    tela.bind('<ButtonRelease-3>', pan_solta)
    tela.bind('<Motion>', move)
    tela.bind('<MouseWheel>', roda)
    tela.bind('<Button-4>', roda)
    tela.bind('<Button-5>', roda)
    tela.bind('<Button-1>', lambda _e: tela.focus_set())
    raiz.bind_all('<Key>', tecla)

    # comeca na primeira ainda nao classificada
    for j, n in enumerate(nomes):
        if n not in feito:
            est['i'] = j
            break
    tela.focus_set()
    carrega()
    raiz.mainloop()
    f.close()


if __name__ == '__main__':
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
