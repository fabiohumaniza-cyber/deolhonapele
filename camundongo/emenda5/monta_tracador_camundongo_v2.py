"""
monta_tracador_camundongo_v2.py — v2 (Adendo 39: traca TODAS, marcando visto/parte/imaginado) — monta o painel do TRACADOR CEGO do camundongo.

As fotos sao as MESMAS vistas da declaracao (declaracao_camundongo_v8.html,
43e0b7ab...), copiadas byte a byte: mesmo recorte, mesma escala, sem o circulo
amarelo (que a pagina desenha por cima e nao esta na foto) e sem nenhuma marca.

O painel NAO leva nome de imagem nem dia. Cada foto recebe um codigo (C001...)
na ordem sorteada com semente fixa. O mapa codigo -> imagem vai para um arquivo
separado (_ORDEM_<tracador>.json), que fica com o Fabio e nao vai ao tracador.

Uso:
    python monta_tracador_camundongo.py <declaracao_v8.html> <pasta_destino> <tracador>
"""
import os, sys, json, re, base64, hashlib, random

AQUI = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(AQUI, 'tpl_tracador_camundongo_v2.html')
SEMENTE = 20261004


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main(html, destino, tracador):
    t = open(html, encoding='utf-8').read()
    fig = json.loads(re.search(r'var FIG = (\[.*?\]);\nvar META', t, re.S).group(1))
    rnd = random.Random(SEMENTE + sum(map(ord, tracador)))   # ordem diferente para cada tracador
    idx = list(range(len(fig))); rnd.shuffle(idx)
    FIG, ORDEM = [], []
    for k, i in enumerate(idx, 1):
        f = fig[i]
        b = base64.b64decode(f['img'].split(',', 1)[1])
        cod = 'C%03d' % k
        FIG.append({'id': cod, 'img': f['img'], 'sha': sha(b)})
        ORDEM.append({'id': cod, 'nome': f['nome'], 'arquivo': f['arquivo'], 'vx0': f['vx0'],
                      'vy0': f['vy0'], 'vl': f['vl'], 'sha256_imagem': sha(b)})
    os.makedirs(destino, exist_ok=True)
    p = os.path.join(destino, 'tracador_camundongo_v2_%s.html' % tracador)
    po = os.path.join(destino, '_ORDEM_v2_%s.json' % tracador)
    if os.path.exists(p) or os.path.exists(po):
        sys.exit('PARADO: painel ou ordem de %s ja existe.' % tracador)
    s = open(TPL, encoding='utf-8').read()
    s = s.replace('__FIGS__', json.dumps(FIG)).replace('__TRACADOR__', tracador).replace('__N__', str(len(FIG)))
    open(p, 'w', encoding='utf-8').write(s)
    json.dump({'tracador': tracador, 'semente': SEMENTE, 'regra': 'Random(semente + soma dos codigos das letras do nome)',
               'declaracao_html_sha256': sha(open(html, 'rb').read()),
               'coordenadas': 'fracao 0..1 do lado vl; ponto no quadro de 700 = (vx0 + x*vl, vy0 + y*vl)',
               'ordem': ORDEM}, open(po, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('painel %s  (%.1f MB)\nsha256 %s' % (p, os.path.getsize(p) / 1e6, sha(open(p, 'rb').read())))
    print('ordem  %s\nsha256 %s' % (po, sha(open(po, 'rb').read())))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
