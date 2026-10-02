"""
reabre_pendentes.py — devolve a pendente imagens que ja tem linha no
MEDIDAS.txt, sem apagar nada.

POR QUE EXISTE
Em 01/10/2026 o Fabio mediu 27 imagens com a v3 do mede_anel.py, em que a
miniatura de referencia ficava no canto inferior esquerdo e TAPAVA o anel nas
fotos de dia 10 em diante. Dez imagens foram marcadas SEM_ANEL por causa da
posicao da miniatura, nao por o anel nao existir. A v5 move a miniatura; essas
dez precisam voltar para a fila.

O QUE ELE FAZ, E O QUE NAO FAZ
NAO apaga, NAO edita no lugar e NAO reescreve linha nenhuma. Ele:
  1. copia o MEDIDAS.txt atual para MEDIDAS_ATE_<data-hora>.txt, byte a byte,
     conferindo o SHA-256 dos dois;
  2. grava um MEDIDAS.txt novo SEM as linhas reabertas, e com as outras
     intocadas, na mesma ordem;
  3. grava REABERTURA_<data-hora>.tsv dizendo, linha a linha, o que saiu, qual
     era o conteudo e por que.
O arquivo antigo fica. O que se perde nao existe: esta tudo nos tres arquivos.

Uso:
    python reabre_pendentes.py <pasta_saida> <motivo> [<nome1> <nome2> ...]
    python reabre_pendentes.py <pasta_saida> <motivo> --sem-anel-do-dia 10 11 12
    python reabre_pendentes.py <pasta_saida> <motivo> --todas

A segunda forma reabre as linhas SEM_ANEL cujos nomes comecem por "Day N_" para
cada N listado. A terceira reabre TODAS as linhas de medida do arquivo — usada
quando a ferramenta muda de versao e o banco inteiro precisa sair de uma so.
Em qualquer das tres, o script IMPRIME o que vai fazer e espera o operador
digitar SIM.
"""
import os, sys, shutil, hashlib, datetime


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def le(p):
    """Devolve a lista de (linha_crua, nome, e_sem_anel) na ordem do arquivo."""
    fora = []
    for linha in open(p, encoding='utf-8'):
        cru = linha.rstrip('\n')
        if not cru.strip() or cru.startswith('#'):
            fora.append((cru, None, False)); continue
        c = [x.strip() for x in cru.split('\t')]
        fora.append((cru, c[0], len(c) > 1 and c[1].upper() == 'SEM_ANEL'))
    return fora


def main(saida, motivo, alvos, dias, todas=False):
    p = os.path.join(saida, 'MEDIDAS.txt')
    if not os.path.isfile(p):
        sys.exit('PARADO: nao achei %s' % p)
    linhas = le(p)
    h_antes = sha256(p)

    if todas:
        escolhidas = [n for _c, n, _s in linhas if n]
    elif dias:
        pref = tuple('Day %s_' % d for d in dias)
        escolhidas = [n for _c, n, sem in linhas
                      if n and sem and n.startswith(pref)]
    else:
        escolhidas = [n for _c, n, _s in linhas if n and n in set(alvos)]
    faltam = [a for a in alvos if a not in escolhidas]
    if faltam:
        sys.exit('PARADO: nao estao no MEDIDAS.txt: %s' % ', '.join(faltam))
    if not escolhidas:
        sys.exit('PARADO: nada a reabrir — nenhuma linha casou com o pedido.')

    print('MEDIDAS.txt  SHA-256 %s' % h_antes)
    print('linhas de medida hoje: %d' % sum(1 for _c, n, _s in linhas if n))
    print('\nVAO VOLTAR PARA PENDENTE (%d):' % len(escolhidas))
    for _c, n, _s in linhas:
        if n in escolhidas:
            print('   %s' % _c)
    print('\nmotivo que ficara registrado: %s' % motivo)
    print('\nO MEDIDAS.txt atual sera COPIADO para MEDIDAS_ATE_<data-hora>.txt e')
    print('nada sera apagado. Digite SIM para seguir, qualquer outra coisa para parar.')
    if input('> ').strip() != 'SIM':
        sys.exit('parado pelo operador; nada foi tocado.')

    quando = datetime.datetime.now().astimezone()
    carimbo = quando.strftime('%Y%m%d_%H%M%S')
    p_velho = os.path.join(saida, 'MEDIDAS_ATE_%s.txt' % carimbo)
    shutil.copy2(p, p_velho)
    if sha256(p_velho) != h_antes:
        sys.exit('PARADO: a copia divergiu da origem. Nada mais foi feito.')

    alvo = set(escolhidas)
    with open(p, 'w', encoding='utf-8') as f:
        for cru, n, _s in linhas:
            if n in alvo:
                continue
            f.write(cru + '\n')

    p_reab = os.path.join(saida, 'REABERTURA_%s.tsv' % carimbo)
    with open(p_reab, 'w', encoding='utf-8') as f:
        f.write('# quando\t%s\n' % quando.isoformat(timespec='seconds'))
        f.write('# motivo\t%s\n' % motivo)
        f.write('# sha256_medidas_antes\t%s\n' % h_antes)
        f.write('# copia_integral_em\t%s\n' % os.path.basename(p_velho))
        f.write('# nome\tlinha_retirada\n')
        for cru, n, _s in linhas:
            if n in alvo:
                f.write('%s\t%s\n' % (n, cru))

    print('\ncopia integral : %s  SHA-256 %s' % (p_velho, sha256(p_velho)))
    print('MEDIDAS.txt    : %s  SHA-256 %s' % (p, sha256(p)))
    print('declaracao     : %s  SHA-256 %s' % (p_reab, sha256(p_reab)))
    print('\n%d imagens voltaram para a fila. Abra o mede_anel.py e meca de novo.'
          % len(escolhidas))


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) < 3:
        sys.exit(__doc__)
    saida, motivo, resto = a[0], a[1], a[2:]
    if resto and resto[0] == '--todas':
        main(saida, motivo, [], [], todas=True)
    elif resto and resto[0] == '--sem-anel-do-dia':
        main(saida, motivo, [], resto[1:])
    else:
        main(saida, motivo, resto, [])
