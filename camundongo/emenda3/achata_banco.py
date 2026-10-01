"""
achata_banco.py — copia os TIFFs brutos do banco de camundongo para uma pasta
plana com nome unico, e gera o MAPA_FERIDA_DIA.tsv.

CONGELADO PELA NOTA DE ACHATAMENTO (01/10/2026), anexa a Emenda 3.
Escrito ANTES de qualquer imagem do banco ser aberta: ele COPIA bytes e calcula
SHA-256; nao decodifica, nao reamostra, nao olha pixel nenhum.

POR QUE EXISTE
Os TIFFs brutos do Dryad 10.25338/B84W8Q vem em arvore, com nome repetido:
    <animal>/Left wound/Day 0.tiff
    <animal>/Right wound/Day 0.tiff
"Day 0.tiff" aparece 16 vezes no banco. O driver usa o nome do arquivo como
chave do JSON, do mapa e do painel da P3 — com a arvore como vem, ou ele nao
acha nada, ou chaves colidem em silencio. Colisao silenciosa e a classe de erro
que este projeto existe para nao cometer.

A convencao de destino NAO e invencao: e a que o proprio README usa nos PNGs
recortados — "Day 9_A8-1-L.png". Aqui: "Day 9_A8-1-L.tiff".

Uso:
    python achata_banco.py <raiz_do_banco> <pasta_plana>

Saidas, na pasta plana:
    MANIFESTO_ACHATAMENTO.tsv   origem, destino, SHA-256 de cada um
    MAPA_FERIDA_DIA.tsv         nome, dia, animal, lado  (da ARVORE, nunca de resultado)
"""
import os, sys, re, hashlib

EXT = ('.tif', '.tiff')
RE_ANIMAL = re.compile(r'^([AY])8-(\d+)$', re.I)
RE_LADO = re.compile(r'^(left|right)\s+wound$', re.I)
RE_DIA = re.compile(r'^Day\s+(\d+)\.tiff?$', re.I)

# fatos do README, conferidos antes de rodar (SHA-256 1c414307...)
N_ESPERADO = 255
ANIMAIS = ['A8-1', 'A8-3', 'A8-4', 'A8-5', 'Y8-1', 'Y8-2', 'Y8-3', 'Y8-4']
DIAS = list(range(0, 16))
FALTA_DECLARADA = ('Y8-2', 'R', 9)     # README: "The Y8-2, Right wound, Day 9 photo is missing."


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def varre(raiz):
    """Devolve (caminho, animal, lado, dia) de cada TIFF da arvore.
    Animal e lado vem das DUAS pastas acima do arquivo, nao do nome."""
    achados, recusados = [], []
    for base, _dirs, arqs in os.walk(raiz):
        for a in sorted(arqs):
            if not a.lower().endswith(EXT):
                continue
            p = os.path.join(base, a)
            pasta_lado = os.path.basename(base)
            pasta_animal = os.path.basename(os.path.dirname(base))
            ml, ma, md = RE_LADO.match(pasta_lado), RE_ANIMAL.match(pasta_animal), RE_DIA.match(a)
            if not (ml and ma and md):
                recusados.append((p, 'pasta ou nome fora da convencao do README'))
                continue
            achados.append((p, pasta_animal.upper(), ml.group(1)[0].upper(), int(md.group(1))))
    return achados, recusados


def main(raiz, destino):
    if not os.path.isdir(raiz):
        sys.exit('PARADO: %s nao e uma pasta.' % raiz)
    os.makedirs(destino, exist_ok=True)
    achados, recusados = varre(raiz)

    if recusados:
        print('ARQUIVOS .tif FORA DA CONVENCAO (%d):' % len(recusados))
        for p, m in recusados[:10]:
            print('  %s  [%s]' % (p, m))
        sys.exit('PARADO: ha .tif fora da convencao <animal>/<Left|Right> wound/Day N.tiff.\n'
                 'Nada foi copiado. Conferir a arvore antes de seguir.')

    if len(achados) != N_ESPERADO:
        sys.exit('PARADO: encontrados %d TIFFs, esperados %d pelo README.\n'
                 'Nada foi copiado.' % (len(achados), N_ESPERADO))

    # conferencia contra o README: quais ferida-dia existem
    tem = {(an, la, di) for _p, an, la, di in achados}
    esperado = {(an, la, di) for an in ANIMAIS for la in ('L', 'R') for di in DIAS}
    esperado.discard(FALTA_DECLARADA)
    if tem != esperado:
        faltam = sorted(esperado - tem)
        sobram = sorted(tem - esperado)
        sys.exit('PARADO: o conjunto de ferida-dia nao bate com o README.\n'
                 '  faltam: %s\n  sobram: %s\nNada foi copiado.'
                 % (faltam[:8] or '—', sobram[:8] or '—'))

    # copia byte a byte, com nome unico
    manifesto, mapa, vistos = [], [], {}
    for p, an, la, di in sorted(achados, key=lambda z: (z[1], z[2], z[3])):
        nome = 'Day %d_%s-%s.tiff' % (di, an, la)
        if nome in vistos:
            sys.exit('PARADO: nome de destino repetido: %s\n  %s\n  %s'
                     % (nome, vistos[nome], p))
        vistos[nome] = p
        q = os.path.join(destino, nome)
        with open(p, 'rb') as fi, open(q, 'wb') as fo:
            while True:
                b = fi.read(1 << 20)
                if not b:
                    break
                fo.write(b)
        ho, hd = sha256(p), sha256(q)
        if ho != hd:
            sys.exit('PARADO: copia divergiu da origem.\n  %s  %s\n  %s  %s'
                     % (p, ho, q, hd))
        manifesto.append((p, nome, ho, hd))
        mapa.append((nome, di, an, la))
        print('%4d  %-24s <- %s' % (len(manifesto), nome, os.path.relpath(p, raiz)))

    pm = os.path.join(destino, 'MANIFESTO_ACHATAMENTO.tsv')
    with open(pm, 'w', encoding='utf-8') as f:
        f.write('# origem\tdestino\tsha256_origem\tsha256_destino\n')
        f.write('# copia byte a byte: os dois hashes sao iguais por construcao\n')
        for o, d, ho, hd in manifesto:
            f.write('%s\t%s\t%s\t%s\n' % (o, d, ho, hd))

    pmap = os.path.join(destino, 'MAPA_FERIDA_DIA.tsv')
    with open(pmap, 'w', encoding='utf-8') as f:
        f.write('# nome\tdia\tanimal\tlado\n')
        f.write('# derivado da ARVORE DE PASTAS do banco, nunca de resultado\n')
        for n, di, an, la in mapa:
            f.write('%s\t%d\t%s\t%s\n' % (n, di, an, la))

    print('\n%d arquivos copiados, nenhum movido, nenhum reamostrado.' % len(manifesto))
    print('%s  SHA-256 %s' % (pm, sha256(pm)))
    print('%s  SHA-256 %s' % (pmap, sha256(pmap)))


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
