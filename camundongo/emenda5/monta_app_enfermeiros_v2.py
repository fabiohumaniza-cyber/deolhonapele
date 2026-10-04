"""
monta_app_enfermeiros_v2.py — v2 (Adendo 44: possiveis = as mais claras) — monta o aplicativo da pesquisa com enfermeiros
("Voce conseguiria tracar com seguranca a borda desta ferida? Sim / Nao").

As 74 fotos vem de SELECAO_ENFERMEIROS.json (30 impossiveis, 14 duvidosas,
30 possiveis sorteadas) e sao as MESMAS vistas da declaracao v8 (43e0b7ab...),
copiadas byte a byte. O aplicativo leva so um codigo por foto (F01...F74),
sem nome, dia nem grupo. O mapa codigo -> imagem -> grupo vai para
_CHAVE_enfermeiros.json, que fica com o Fabio e nao vai no aplicativo.
A ordem de apresentacao e sorteada no proprio celular de cada pessoa e gravada.

Uso:
    python monta_app_enfermeiros.py <declaracao_v8.html> <SELECAO_ENFERMEIROS.json> <pasta_destino>
"""
import os, sys, json, re, base64, hashlib, random

AQUI = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.join(AQUI, 'tpl_app_enfermeiros_v2.html')
SEMENTE = 20261004


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main(html, psel, destino):
    t = open(html, encoding='utf-8').read()
    fig = {f['nome']: f for f in json.loads(re.search(r'var FIG = (\[.*?\]);\nvar META', t, re.S).group(1))}
    sel = json.load(open(psel, encoding='utf-8'))
    itens = [(n, 'impossivel') for n in sel['impossiveis']] + [(n, 'duvidosa') for n in sel['duvidosas']] + \
            [(n, 'possivel') for n in sel['possiveis']]
    random.Random(SEMENTE + 1).shuffle(itens)            # o codigo nao revela o grupo
    FIG, CH = [], []
    for k, (n, g) in enumerate(itens, 1):
        f = fig[n]; b = base64.b64decode(f['img'].split(',', 1)[1]); cod = 'F%02d' % k
        FIG.append({'id': cod, 'img': f['img'], 'sha': sha(b)})
        CH.append({'id': cod, 'nome': n, 'grupo': g, 'sha256_imagem': sha(b)})
    os.makedirs(destino, exist_ok=True)
    p = os.path.join(destino, 'de_olho_na_pele_enfermeiros_v2.html')
    pc = os.path.join(destino, '_CHAVE_enfermeiros_v2.json')
    if os.path.exists(p) or os.path.exists(pc):
        sys.exit('PARADO: aplicativo ou chave ja existe.')
    s = open(TPL, encoding='utf-8').read().replace('__FIGS__', json.dumps(FIG)).replace('__N__', str(len(FIG)))
    open(p, 'w', encoding='utf-8').write(s)
    json.dump({'selecao_sha256': sha(open(psel, 'rb').read()), 'declaracao_html_sha256': sha(open(html, 'rb').read()),
               'chave': CH}, open(pc, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('app   %s  (%.1f MB)\nsha256 %s' % (p, os.path.getsize(p) / 1e6, sha(open(p, 'rb').read())))
    print('chave %s\nsha256 %s' % (pc, sha(open(pc, 'rb').read())))


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
