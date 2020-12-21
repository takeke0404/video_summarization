import sys
import pandas as pd
import sentencepiece as spm
import numpy as np
import csv
import tensorflow as tf
from keras import utils
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from keras_bert import load_trained_model_from_checkpoint
from keras_bert import get_custom_objects
from sklearn.metrics import classification_report, confusion_matrix
from keras.layers import Dense
from keras import Input, Model

sys.path.append('modules')

# SentencePieceProccerモデルの読込
spp = spm.SentencePieceProcessor()
spp.Load('./model/wiki-ja.model')

SEQ_LEN = 512
maxlen = SEQ_LEN

def _create_model(input_shape, class_count):
    # BERTのロード
    config_path = './model/bert_finetuning_config.json'
    # 拡張子まで記載しない
    checkpoint_path = './model/model.ckpt-1400000'

    bert = load_trained_model_from_checkpoint(config_path, checkpoint_path, training=True,  trainable=False, seq_len=SEQ_LEN)

    bert_last = bert.get_layer(name='NSP-Dense').output
    x1 = bert_last
    output_tensor = Dense(class_count, activation='sigmoid')(x1)

    model = Model([bert.input[0], bert.input[1]], output_tensor)

    return model

def _get_indice(feature):
    indices = np.zeros((maxlen), dtype=np.int32)

    tokens = []
    tokens.append('[CLS]')
    tokens.extend(spp.encode_as_pieces(feature))
    tokens.append('[SEP]')

    for t, token in enumerate(tokens):
        if t >= maxlen:
            break
        try:
            indices[t] = spp.piece_to_id(token)
        except:
            logging.warn('unknown')
            indices[t] = spp.piece_to_id('<unk>')
    return indices

if __name__ == "__main__":
    name=sys.argv[1]
    features = []
    time=[]
    with open('./data/'+name+'.csv') as f:
        for t,s,e,text in csv.reader(f):
            features.append(_get_indice(text))
            time.append([t,s,e])
    segments = np.zeros((len(features), maxlen), dtype=np.float32)
    # BERTの学習したモデルの読込
    model = _create_model(np.array(features).shape, 2)
    model.load_weights('./model/youtube_finetuning.h5')

    predicted_labels = model.predict([np.array(features), segments])
    predict = np.append(time,predicted_labels,axis=1)
    with open('./predict_result/'+name+'.csv',mode='w') as f:
        for row in predict:
            print(*row, sep=',', file=f)
