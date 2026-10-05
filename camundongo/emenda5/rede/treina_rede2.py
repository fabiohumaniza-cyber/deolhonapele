"""
treina_rede2.py — redes de sensibilidade pedidas na revisao externa (Adendo 68).

Mesmas fotos, rotulos, dobras, perda, otimizador, lote e aumento do treina_rede.py (b767471e...),
que e importado sem mudanca. O que muda, por variante:

  conv   U-Net base=4 do Semantic-Shapes (a MESMA do Adendo 52), treinada ate convergir:
         ate 300 epocas, para quando passam 30 epocas sem melhorar o val_dice; guarda a melhor.
  campo  igual a conv, mas a entrada fora do campo de busca do operador (r_campo do CAMPO.txt,
         o MESMO circulo que o motor recebe) vira preto (0). Na predicao, a classe ferida fora
         do campo e zerada. E a comparacao simetrica: a rede recebe a mesma ajuda manual do motor.
  mnv2   U-Net com codificador MobileNetV2 pre-treinado na ImageNet (pesos locais, arquivo e
         SHA-256 no Adendo 68), todas as camadas treinaveis, entrada x/127.5 - 1;
         ate 150 epocas (uma epoca custa ~3x a da U-Net em CPU), paciencia 30.

Retomavel como o retoma_rede.py (Adendo 59): estado por epoca em estado_dobra{k}.keras/.json.
Sementes: 20261004 + k + 1000 * epoca_inicial.

Uso: python treina_rede2.py <variante> <rede_dados.npz> <pasta_saida> [CAMPO.txt] [pesos_mnv2.h5]
"""
import os, sys, json, random
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '3')
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers as L, Model
from tensorflow.keras.optimizers import Adam
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import treina_rede as T

MAX_EPOCAS, PACIENCIA = 300, 30
MAX_POR_VARIANTE = {'conv': 300, 'campo': 300, 'mnv2': 150}


def le_campo(p):                                          # mesma leitura do prepara_rede.py, coluna r_campo_700
    c = {}
    for l in open(p, encoding='utf-8'):
        if l.startswith('#') or not l.strip():
            continue
        x = l.rstrip('\n\r').split('\t')
        n = x[0][:-5] if x[0].endswith('.tiff') else x[0]
        if x[8] != 'ok':
            c.pop(n, None); continue
        c[n] = (float(x[1]), float(x[2]), float(x[4]))  # cx_700, cy_700, r_campo_700 ; vale a ultima linha
    return c


def mascaras_campo(z, pcampo):
    C = le_campo(pcampo); yy, xx = np.mgrid[0:T.LADO, 0:T.LADO] + 0.5; M = []
    for i, n in enumerate(z['nome']):
        cx, cy, r = C[str(n)]; k = T.LADO / z['vl'][i]
        M.append((xx - (cx - z['vx0'][i]) * k) ** 2 + (yy - (cy - z['vy0'][i]) * k) ** 2 <= (r * k) ** 2)
    return np.stack(M)


def unet_mnv2(pesos):
    i = L.Input((T.LADO, T.LADO, 3)); s = L.Rescaling(1 / 127.5, offset=-1)(i)
    base = tf.keras.applications.MobileNetV2(input_shape=(T.LADO, T.LADO, 3), include_top=False, weights=None)
    base.load_weights(pesos)
    nomes = ['block_1_expand_relu', 'block_3_expand_relu', 'block_6_expand_relu', 'block_13_expand_relu', 'block_16_project']
    enc = Model(base.input, [base.get_layer(n).output for n in nomes])
    *skips, x = enc(s)
    for sk, f in zip(reversed(skips), [512, 256, 128, 64]):
        x = L.Conv2DTranspose(f, 3, strides=2, padding='same')(x)
        x = L.BatchNormalization()(x); x = L.ReLU()(x)
        x = L.concatenate([x, sk])
    x = L.Conv2DTranspose(32, 3, strides=2, padding='same')(x)
    x = L.BatchNormalization()(x); x = L.ReLU()(x)
    o = L.Conv2D(T.NC, 1, activation='softmax')(x)
    m = Model(i, o, name='unet_mnv2')
    m.compile(optimizer=Adam(1e-4), loss='categorical_crossentropy', metrics=[T.dice])
    return m


class Estado(tf.keras.callbacks.Callback):
    def __init__(self, pm, pj, melhor, ep_melhor):
        super().__init__(); self.pm, self.pj, self.melhor, self.ep_melhor = pm, pj, melhor, ep_melhor

    def on_epoch_end(self, epoch, logs=None):
        v = (logs or {}).get('val_dice')
        if v is not None and (self.melhor is None or v > self.melhor):
            self.melhor, self.ep_melhor = float(v), epoch + 1
        self.model.save(self.pm)
        json.dump({'epoca_feita': epoch + 1, 'melhor_val_dice': self.melhor, 'epoca_melhor': self.ep_melhor},
                  open(self.pj, 'w'))
        if epoch + 1 - self.ep_melhor >= PACIENCIA:
            self.model.stop_training = True


def roda(var, D, X, Y, fer, MC, k, pasta, pesos):
    mx = min(MAX_EPOCAS, MAX_POR_VARIANTE[var])
    pred = os.path.join(pasta, 'pred_dobra%d.npz' % k)
    if os.path.exists(pred):
        return
    pm_best = os.path.join(pasta, 'modelo_dobra%d.keras' % k)
    pm_est, pj = os.path.join(pasta, 'estado_dobra%d.keras' % k), os.path.join(pasta, 'estado_dobra%d.json' % k)
    st = lambda nomes: np.isin(fer, nomes)
    tr, va, te = st(D[k]['treino']), st(D[k]['validacao']), st(D[k]['teste'])
    e0, melhor, ep_melhor = 0, None, 0
    if os.path.exists(pj) and os.path.exists(pm_est):
        j = json.load(open(pj)); e0, melhor, ep_melhor = j['epoca_feita'], j['melhor_val_dice'], j['epoca_melhor']
    sem = T.SEMENTE + k + 1000 * e0
    random.seed(sem); np.random.seed(sem); tf.random.set_seed(sem)
    parou = e0 >= mx or (e0 and e0 - ep_melhor >= PACIENCIA)
    if not parou:
        if e0:
            m = tf.keras.models.load_model(pm_est, custom_objects={'dice': T.dice})
        else:
            m = unet_mnv2(pesos) if var == 'mnv2' else T.unet()
        ck = tf.keras.callbacks.ModelCheckpoint(pm_best, monitor='val_dice', mode='max', save_best_only=True,
                                                initial_value_threshold=melhor)
        cb = [ck, tf.keras.callbacks.CSVLogger(os.path.join(pasta, 'log_dobra%d.csv' % k), append=True),
              Estado(pm_est, pj, melhor, ep_melhor)]
        print('%s dobra %d: retomando da epoca %d' % (var, k, e0), flush=True)
        m.fit(T.lotes(X[tr], Y[tr], np.random.RandomState(sem)), steps_per_epoch=int(tr.sum()) // T.LOTE,
              initial_epoch=e0, epochs=mx,
              validation_data=(X[va].astype('float32'), tf.one_hot(Y[va], T.NC).numpy()), callbacks=cb, verbose=2)
    m = tf.keras.models.load_model(pm_best, custom_objects={'dice': T.dice})
    p = m.predict(X[te].astype('float32'), batch_size=T.LOTE, verbose=0)
    if MC is not None:
        p[..., 2] *= MC[te]
    np.savez_compressed(pred, idx=np.where(te)[0], prob_ferida=p[..., 2].astype('float16'),
                        classe=p.argmax(-1).astype('uint8'))
    print('%s dobra %d: pronta (%d fotos de teste)' % (var, k, te.sum()), flush=True)


def main(var, pdados, pasta, pcampo=None, pesos=None):
    if var not in ('conv', 'campo', 'mnv2'):
        sys.exit(__doc__)
    z = np.load(pdados); X, Y, fer = z['X'], z['Y'], z['ferida']
    MC = None
    if var == 'campo':
        MC = mascaras_campo(z, pcampo)
        X = (X * MC[..., None]).astype(np.uint8)
    os.makedirs(pasta, exist_ok=True)
    D = T.dobras(fer); json.dump(D, open(os.path.join(pasta, 'DOBRAS.json'), 'w'), indent=1)
    for k in range(4):
        roda(var, D, X, Y, fer, MC, k, pasta, pesos)


if __name__ == '__main__':
    if len(sys.argv) not in (4, 5, 6):
        sys.exit(__doc__)
    main(*sys.argv[1:])
