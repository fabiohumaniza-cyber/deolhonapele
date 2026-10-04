"""
treina_rede.py — treina a U-Net do Carrion et al. (Semantic-Shapes, seth814, commit 00289c01)
nas vistas do camundongo, com o tracado do Emilio como rotulo (Adendo 52).

DESENHO (fixado no Adendo 52, antes de qualquer treino)
  - 16 feridas -> 4 dobras de 4 feridas (2 A + 2 Y), sorteio random.Random(20261004).
  - Dobra k: TESTE = as 4 feridas da dobra k; VALIDACAO = 1 A + 1 Y da dobra (k+1) % 4;
    TREINO = as outras 10. Toda foto recebe UMA predicao, de um modelo que nunca viu a ferida dela.
  - Arquitetura: unet(base=4) do Semantic-Shapes, igual camada a camada; entrada 352x352x3;
    3 classes (fundo, interior do anel, ferida), softmax; Adam(1e-4); entropia cruzada categorica;
    metrica 'dice' do Semantic-Shapes (achata todos os canais). Preprocessamento: x/255.
  - 100 epocas, lote 5, guarda o modelo da epoca de maior val_dice (como o log deles: UWound_v9).
  - Aumento: espelho horizontal p = 0,5 e rotacao de 90 graus k em {0,1,2,3}, sorteados por lote.
  - Sementes: tf/np/random = 20261004 + k.
  - NAO le nenhum tracado alem do Emilio. NAO le o motor.

Saida em <pasta>: pred_dobra{k}.npz (prob da classe ferida e argmax, 352x352, das fotos de teste),
modelo_dobra{k}.keras, log_dobra{k}.csv, DOBRAS.json.

Uso: python treina_rede.py <rede_dados.npz> <pasta_saida> [dobra]
"""
import os, sys, json, random, time
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '3')
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers as L, Model, backend as K
from tensorflow.keras.optimizers import Adam

SEMENTE = 20261004
EPOCAS, LOTE, LADO, NC = 100, 5, 352, 3


def dobras(feridas):
    a = sorted(f for f in set(feridas) if f.startswith('A'))
    y = sorted(f for f in set(feridas) if f.startswith('Y'))
    rnd = random.Random(SEMENTE); rnd.shuffle(a); rnd.shuffle(y)
    D = [{'teste': a[2 * k:2 * k + 2] + y[2 * k:2 * k + 2]} for k in range(4)]
    for k in range(4):
        n = (k + 1) % 4
        D[k]['validacao'] = [a[2 * n], y[2 * n]]
        D[k]['treino'] = sorted(set(a + y) - set(D[k]['teste']) - set(D[k]['validacao']))
    return D


def dice(y_true, y_pred, smooth=1.):                      # verbatim do Semantic-Shapes/models.py
    y_true_f = K.flatten(y_true)
    y_pred_f = K.flatten(y_pred)
    intersection = K.sum(y_true_f * y_pred_f)
    return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)


def unet(b=4):                                           # Semantic-Shapes unet(), mesma sequencia de camadas
    i = L.Input((LADO, LADO, 3)); s = L.Rescaling(1 / 255.)(i)
    def blk(x, f, d):
        x = L.Conv2D(f, 3, activation='elu', kernel_initializer='he_normal', padding='same')(x)
        x = L.Dropout(d)(x)
        return L.Conv2D(f, 3, activation='elu', kernel_initializer='he_normal', padding='same')(x)
    c1 = blk(s, 2 ** b, .1)
    c2 = blk(L.MaxPooling2D()(c1), 2 ** (b + 1), .1)
    c3 = blk(L.MaxPooling2D()(c2), 2 ** (b + 2), .2)
    c4 = blk(L.MaxPooling2D()(c3), 2 ** (b + 3), .2)
    u = blk(L.MaxPooling2D()(c4), 2 ** (b + 4), .3)
    for c, f, d in [(c4, b + 3, .2), (c3, b + 2, .2), (c2, b + 1, .1), (c1, b, .1)]:
        u = L.concatenate([L.Conv2DTranspose(2 ** f, 2, strides=2, padding='same')(u), c])
        u = blk(u, 2 ** f, d)
    o = L.Conv2D(NC, 1, activation='softmax')(u)
    m = Model(i, o, name='unet_multi')
    m.compile(optimizer=Adam(1e-4), loss='categorical_crossentropy', metrics=[dice])
    return m


def lotes(X, Y, rnd):
    while True:
        idx = rnd.permutation(len(X))
        for j in range(0, len(idx) - LOTE + 1, LOTE):
            x = X[idx[j:j + LOTE]].copy(); y = Y[idx[j:j + LOTE]].copy()
            if rnd.random() < 0.5:
                x = x[:, :, ::-1]; y = y[:, :, ::-1]
            kk = rnd.randint(4)
            x = np.rot90(x, kk, axes=(1, 2)); y = np.rot90(y, kk, axes=(1, 2))
            yield x.astype('float32'), tf.one_hot(y, NC).numpy()


def roda(D, X, Y, fer, k, pasta):
    random.seed(SEMENTE + k); np.random.seed(SEMENTE + k); tf.random.set_seed(SEMENTE + k)
    st = lambda nomes: np.isin(fer, nomes)
    tr, va, te = st(D[k]['treino']), st(D[k]['validacao']), st(D[k]['teste'])
    m = unet()
    pm = os.path.join(pasta, 'modelo_dobra%d.keras' % k)
    cb = [tf.keras.callbacks.ModelCheckpoint(pm, monitor='val_dice', mode='max', save_best_only=True),
          tf.keras.callbacks.CSVLogger(os.path.join(pasta, 'log_dobra%d.csv' % k))]
    t0 = time.time()
    m.fit(lotes(X[tr], Y[tr], np.random.RandomState(SEMENTE + k)), steps_per_epoch=int(tr.sum()) // LOTE,
          epochs=EPOCAS, validation_data=(X[va].astype('float32'), tf.one_hot(Y[va], NC).numpy()),
          callbacks=cb, verbose=2)
    m = tf.keras.models.load_model(pm, custom_objects={'dice': dice})
    p = m.predict(X[te].astype('float32'), batch_size=LOTE, verbose=0)
    np.savez_compressed(os.path.join(pasta, 'pred_dobra%d.npz' % k), idx=np.where(te)[0],
                        prob_ferida=p[..., 2].astype('float16'), classe=p.argmax(-1).astype('uint8'))
    print('dobra %d: treino %d, validacao %d, teste %d fotos · %.1f min' % (k, tr.sum(), va.sum(), te.sum(),
                                                                         (time.time() - t0) / 60), flush=True)


def main(pdados, pasta, so=None):
    z = np.load(pdados); X, Y, fer = z['X'], z['Y'], z['ferida']
    os.makedirs(pasta, exist_ok=True)
    D = dobras(fer)
    json.dump(D, open(os.path.join(pasta, 'DOBRAS.json'), 'w'), indent=1)
    for k in ([int(so)] if so is not None else range(4)):
        roda(D, X, Y, fer, k, pasta)


if __name__ == '__main__':
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    main(*sys.argv[1:])
