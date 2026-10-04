"""
retoma_rede.py — o MESMO treino do treina_rede.py (Adendo 52), so que retomavel (Adendo 59).

Por que existe: o ambiente de treino e reiniciado quando a conversa fica parada; o treino de
uma dobra (~60 min) foi interrompido tres vezes (epocas 32, 46 e 74 da dobra 0).

O que NAO muda (importado do treina_rede.py, b767471e...): dobras, arquitetura unet(), metrica
dice, perda, otimizador Adam(1e-4), 100 epocas, lote 5, aumento (lotes()), checkpoint pelo
maior val_dice, predicao e formato de saida pred_dobra{k}.npz.

O que muda, declarado:
  - ao fim de CADA epoca grava o modelo inteiro (pesos + estado do otimizador) em
    estado_dobra{k}.keras e {epoca, melhor val_dice} em estado_dobra{k}.json;
  - ao recomecar, carrega esse estado e segue da epoca seguinte (initial_epoch);
  - o gerador de lotes e semeado com 20261004 + k + 1000 * epoca_inicial, entao a sequencia
    de lotes de um treino retomado nao e identica a de um treino sem interrupcao;
  - o checkpoint do melhor modelo continua de onde parou (initial_value_threshold).

Uso: python retoma_rede.py <rede_dados.npz> <pasta_saida>
"""
import os, sys, json, random, time
os.environ.setdefault('TF_CPP_MIN_LOG_LEVEL', '3')
import numpy as np
import tensorflow as tf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import treina_rede as T


class Estado(tf.keras.callbacks.Callback):
    def __init__(self, pm, pj, melhor):
        super().__init__(); self.pm, self.pj, self.melhor = pm, pj, melhor

    def on_epoch_end(self, epoch, logs=None):
        v = (logs or {}).get('val_dice')
        if v is not None and (self.melhor is None or v > self.melhor):
            self.melhor = float(v)
        self.model.save(self.pm)
        json.dump({'epoca_feita': epoch + 1, 'melhor_val_dice': self.melhor}, open(self.pj, 'w'))


def roda(D, X, Y, fer, k, pasta):
    pred = os.path.join(pasta, 'pred_dobra%d.npz' % k)
    if os.path.exists(pred):
        return
    pm_best = os.path.join(pasta, 'modelo_dobra%d.keras' % k)
    pm_est, pj = os.path.join(pasta, 'estado_dobra%d.keras' % k), os.path.join(pasta, 'estado_dobra%d.json' % k)
    st = lambda nomes: np.isin(fer, nomes)
    tr, va, te = st(D[k]['treino']), st(D[k]['validacao']), st(D[k]['teste'])
    e0, melhor = 0, None
    if os.path.exists(pj) and os.path.exists(pm_est):
        j = json.load(open(pj)); e0, melhor = j['epoca_feita'], j['melhor_val_dice']
    random.seed(T.SEMENTE + k + 1000 * e0); np.random.seed(T.SEMENTE + k + 1000 * e0)
    tf.random.set_seed(T.SEMENTE + k + 1000 * e0)
    if e0 >= T.EPOCAS:
        pass
    else:
        m = tf.keras.models.load_model(pm_est, custom_objects={'dice': T.dice}) if e0 else T.unet()
        ck = tf.keras.callbacks.ModelCheckpoint(pm_best, monitor='val_dice', mode='max', save_best_only=True,
                                                initial_value_threshold=melhor)
        cb = [ck, tf.keras.callbacks.CSVLogger(os.path.join(pasta, 'log_dobra%d.csv' % k), append=True),
              Estado(pm_est, pj, melhor)]
        print('dobra %d: retomando da epoca %d' % (k, e0), flush=True)
        m.fit(T.lotes(X[tr], Y[tr], np.random.RandomState(T.SEMENTE + k + 1000 * e0)),
              steps_per_epoch=int(tr.sum()) // T.LOTE, initial_epoch=e0, epochs=T.EPOCAS,
              validation_data=(X[va].astype('float32'), tf.one_hot(Y[va], T.NC).numpy()), callbacks=cb, verbose=2)
    m = tf.keras.models.load_model(pm_best, custom_objects={'dice': T.dice})
    p = m.predict(X[te].astype('float32'), batch_size=T.LOTE, verbose=0)
    np.savez_compressed(pred, idx=np.where(te)[0], prob_ferida=p[..., 2].astype('float16'),
                        classe=p.argmax(-1).astype('uint8'))
    print('dobra %d: pronta (%d fotos de teste)' % (k, te.sum()), flush=True)


def main(pdados, pasta):
    z = np.load(pdados); X, Y, fer = z['X'], z['Y'], z['ferida']
    os.makedirs(pasta, exist_ok=True)
    D = T.dobras(fer); json.dump(D, open(os.path.join(pasta, 'DOBRAS.json'), 'w'), indent=1)
    for k in range(4):
        roda(D, X, Y, fer, k, pasta)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
