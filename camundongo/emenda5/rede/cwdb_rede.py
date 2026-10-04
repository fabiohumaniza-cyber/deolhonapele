"""
cwdb_rede.py — EXPLORATORIO (Adendo 57): U-Net x motor nas 27 do ComplexWoundDB, no MESMO campo
que o motor usou na condicao 3 (recorte K = 1,40 x maior eixo declarado, centro clicado).

  prepara  <pasta_banco> <resultado_27_cond3.json> <saida.npz>
      Recorta cada imagem pelo 'recorte' K=1.4 do resultado_27_cond3.json (preenche com 0 o que
      sai do quadro), redimensiona para 352. Rotulo = mascara de CADA especialista, binarizada
      exatamente como no roda_27.py: ~(RGB > 240 em todos os canais). 4 amostras por imagem.
  treina   <dados.npz> <pasta> [dobra]
      5 dobras por IMAGEM (random.Random(20261004)); validacao = 3 imagens das de treino (as 3
      primeiras do sorteio dentro da dobra). Mesma U-Net, otimizador, epocas (100), lote (5),
      aumento e checkpoint (maior val_dice) do treina_rede.py; 2 classes (fundo, ferida).
  analisa  <dados.npz> <pasta> <pasta_banco> <resultado_27_cond3.json>
      Pos-processamento igual ao do camundongo (mancha >= 50 px mais perto do centro).
      Mascara volta ao tamanho do recorte e e colada na imagem inteira (fora do recorte = 0).
      Dice contra CADA especialista na imagem inteira; por imagem, a MEDIANA dos 4 —
      a mesma metrica do 'dice_mediana' do motor no resultado_27_cond3.json (K = 1,4).
      Compara pareado: mediana das diferencas motor - rede, IC 95 % por bootstrap por imagem
      (2000, semente 20261004), Wilcoxon. Sem veredito: e exploratorio.
"""
import os, sys, json, random
import numpy as np
from PIL import Image

AQ = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, AQ)
SEMENTE, LADO, K = 20261004, 352, '1.4'


def masc_esp(banco, e, k):
    A = np.asarray(Image.open(os.path.join(banco, 'annotations', 'masks', 'expert_%d' % e, '%s.png' % k)).convert('RGB'))[:, :, :3]
    return ~((A > 240).all(axis=2))


def corta(a, box):
    x0, y0, x1, y1 = box
    H, W = a.shape[:2]
    out = np.zeros((y1 - y0, x1 - x0) + a.shape[2:], a.dtype)
    sx0, sy0, sx1, sy1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
    out[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = a[sy0:sy1, sx0:sx1]
    return out


def prepara(banco, pres, psaida):
    R = json.load(open(pres, encoding='utf-8'))['por_imagem']
    X, Y, img, box = [], [], [], []
    for k in sorted(R, key=int):
        b = R[k]['por_K'][K]['recorte']
        rgb = np.asarray(Image.open(os.path.join(banco, 'images', '%s.png' % k)).convert('RGB'))
        xi = np.asarray(Image.fromarray(corta(rgb, b)).resize((LADO, LADO), Image.BILINEAR))
        for e in range(1, 5):
            m = corta(masc_esp(banco, e, k).astype(np.uint8), b)
            Y.append((np.asarray(Image.fromarray(m * 255).resize((LADO, LADO), Image.NEAREST)) > 127).astype(np.uint8))
            X.append(xi); img.append(k); box.append(b)
    np.savez_compressed(psaida, X=np.stack(X), Y=np.stack(Y), img=np.array(img), box=np.array(box))
    print('%d amostras de %d imagens -> %s' % (len(X), len(set(img)), psaida))


def dobras(imgs):
    u = sorted(set(imgs), key=int); random.Random(SEMENTE).shuffle(u)
    D = []
    for f in range(5):
        te = u[f::5]
        tr = [i for i in u if i not in te]
        D.append({'teste': te, 'validacao': tr[:3], 'treino': tr[3:]})
    return D


def treina(pdados, pasta, so=None):
    import treina_rede as T
    import tensorflow as tf
    T.NC = 2
    z = np.load(pdados); X, Y, im = z['X'], z['Y'], z['img']
    os.makedirs(pasta, exist_ok=True)
    D = dobras(im); json.dump(D, open(os.path.join(pasta, 'DOBRAS_CWDB.json'), 'w'), indent=1)
    for f in ([int(so)] if so is not None else range(5)):
        random.seed(SEMENTE + f); np.random.seed(SEMENTE + f); tf.random.set_seed(SEMENTE + f)
        tr, va = np.isin(im, D[f]['treino']), np.isin(im, D[f]['validacao'])
        te = np.isin(im, D[f]['teste']) & (np.arange(len(im)) % 4 == 0)     # 1 vez por imagem
        m = T.unet(); pm = os.path.join(pasta, 'modelo_cwdb%d.keras' % f)
        cb = [tf.keras.callbacks.ModelCheckpoint(pm, monitor='val_dice', mode='max', save_best_only=True),
              tf.keras.callbacks.CSVLogger(os.path.join(pasta, 'log_cwdb%d.csv' % f))]
        m.fit(T.lotes(X[tr], Y[tr], np.random.RandomState(SEMENTE + f)), steps_per_epoch=int(tr.sum()) // T.LOTE,
              epochs=T.EPOCAS, validation_data=(X[va].astype('float32'), tf.one_hot(Y[va], 2).numpy()),
              callbacks=cb, verbose=2)
        m = tf.keras.models.load_model(pm, custom_objects={'dice': T.dice})
        p = m.predict(X[te].astype('float32'), batch_size=T.LOTE, verbose=0)
        np.savez_compressed(os.path.join(pasta, 'pred_cwdb%d.npz' % f), img=im[te], classe=p.argmax(-1).astype('uint8'))
        print('dobra %d pronta' % f, flush=True)


def analisa(pdados, pasta, banco, pres):
    from analisa_rede import pos_rede, dice
    from scipy import stats
    z = np.load(pdados)
    R = json.load(open(pres, encoding='utf-8'))['por_imagem']
    pred = {}
    for f in range(5):
        q = np.load(os.path.join(pasta, 'pred_cwdb%d.npz' % f))
        for k, c in zip(q['img'], q['classe']):
            pred[str(k)] = c
    if len(pred) != 27:
        sys.exit('PARADO: %d predicoes' % len(pred))
    L = []
    for k in sorted(pred, key=int):
        b = R[k]['por_K'][K]['recorte']; x0, y0, x1, y1 = b
        H, W = np.asarray(Image.open(os.path.join(banco, 'images', '%s.png' % k))).shape[:2]
        m = pos_rede(np.where(pred[k] == 1, 2, 0))
        big = np.asarray(Image.fromarray(m.astype(np.uint8) * 255).resize((x1 - x0, y1 - y0), Image.NEAREST)) > 127
        full = np.zeros((H, W), bool)
        sx0, sy0, sx1, sy1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
        full[sy0:sy1, sx0:sx1] = big[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0]
        d = [dice(full, masc_esp(banco, e, k)) or 0.0 for e in range(1, 5)]
        L.append({'img': k, 'elegivel': R[k]['elegivel'], 'rede': float(np.median(d)), 'rede_4': d,
                  'motor': R[k]['por_K'][K]['dice_mediana'], 'piso': R[k]['por_K'][K].get('piso_inter_avaliador')})
    dd = [r['motor'] - r['rede'] for r in L]
    rnd = random.Random(SEMENTE)
    bs = sorted(float(np.median([dd[rnd.randrange(27)] for _ in range(27)])) for _ in range(2000))
    w = stats.wilcoxon([r['motor'] for r in L], [r['rede'] for r in L])
    md = lambda s, c: float(np.median([r[c] for r in s]))
    S = ['# CWDB — motor (condicao 3, K = 1,4) x U-Net no mesmo recorte · EXPLORATORIO', '',
         '| conjunto | n | motor | rede | piso inter-avaliador |', '|---|---|---|---|---|']
    for rot, s in [('as 27', L), ('elegiveis', [r for r in L if r['elegivel']]), ('nao elegiveis', [r for r in L if not r['elegivel']])]:
        S.append('| %s | %d | %.3f | %.3f | %.3f |' % (rot, len(s), md(s, 'motor'), md(s, 'rede'), md([r for r in s if r['piso']], 'piso')))
    S += ['', 'mediana da diferenca motor - rede: %+.3f · IC 95 %% [%+.3f, %+.3f] · Wilcoxon p = %.4f'
          % (float(np.median(dd)), bs[50], bs[1949], w.pvalue),
          'rede melhor em %d de 27 imagens' % sum(x < 0 for x in dd)]
    open(os.path.join(pasta, 'CWDB_REDE_x_MOTOR.md'), 'w', encoding='utf-8').write('\n'.join(S) + '\n')
    json.dump(L, open(os.path.join(pasta, 'cwdb_rede_por_imagem.json'), 'w'), indent=1)
    print('\n'.join(S))


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    {'prepara': prepara, 'treina': treina, 'analisa': analisa}[a[0]](*a[1:])
