import numpy as np
from keras.layers import Input, Dense
from keras.models import Model
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils
from keras.utils.np_utils import to_categorical
from keras import backend as K
from kdd_input import kdd_test, kdd_train
from sklearn.metrics import accuracy_score, f1_score
from sklearn.svm import SVC

nb_class = 3
nb_epoch = 40
batch_size = 32
encoding_dim = 15

def ae():
    print "Loading data ..."
    x_train,y_train = kdd_train()
    x_test, y_test = kdd_test()

    print "Loading data sucess"

#    y_train = to_categorical(y_train, nb_class)
#    y_test = to_categorical(y_test, nb_class)

    input = Input(shape=(26,))

    encoded = Dense(20, activation='relu')(input)
    encoded = Dense(14, activation='relu')(encoded)
    encoded = Dense(8, activation='relu')(encoded)
    encoded_output = Dense(encoding_dim)(encoded)

    decoded = Dense(8, activation='relu')(encoded_output)
    decoded = Dense(14, activation='relu')(decoded)
    decoded = Dense(20, activation='relu')(decoded)
    decoded = Dense(26, activation='tanh')(decoded)

    autoencoder = Model(inputs=input, outputs=decoded)

    encoder = Model(inputs=input, outputs=encoded_output)

    autoencoder.compile(optimizer='adam', loss='mse')

    autoencoder.fit(x_train, x_train, epochs=nb_epoch, batch_size=batch_size,shuffle=True)

    x_train = encoder.predict(x_train, batch_size=batch_size, verbose=0)

    x_test = encoder.predict(x_test, batch_size=batch_size, verbose=0)

    K.clear_session()
    print x_train.shape
    clf = SVC(C=0.01)
    clf.fit(x_train,y_train.ravel())
    y_pre = clf.predict(x_test)

    return y_test, y_pre



if __name__ == '__main__':
    y_test, y_pre =  ae()
    print accuracy_score(y_test,y_pre)
    print f1_score(y_test, y_pre, average=None)
    print f1_score(y_test, y_pre, average='macro')
