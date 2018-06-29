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
nb_epoch = 50
batch_size = 32
encoding_dim = 3
neighbor = 5

def idae():
    print "Loading data ..."
    x_train,y_train = kdd_train()
    x_test, y_test = kdd_test()

    noise_factor = 0.2
    #improve1
    # noise = noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_train.shape)
    # x_train_noise = x_train
    #
    # (r, c) = x_train.shape
    # for i in xrange(r):
    #     for j in xrange(c):
    #         if noise[i][j] <= 0:
    #             x_train_noise[i][j] = np.sum(x_train[i][j - neighbor:j]) / neighbor
    #
    # noise = noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_test.shape)
    # x_test_noise = x_test + noise

    # (r, c) = x_test.shape
    # for i in xrange(r):
    #     for j in xrange(c):
    #         if noise[i][j] <= 0:
    #             x_test_noise[i][j] = np.sum(x_test[i][j - neighbor:j]) / neighbor

    #improve2
    (r,c) = x_train.shape
    x_train_var = []
    for i in xrange(c):
        x_train_var.append(np.var(x_train[:,i]))
    x_train_var = np.array(x_train_var)
    x_train_tem = np.sort(x_train_var)[0:int(noise_factor*len(x_train_var))]

    x_train_noise = x_train
    for i in x_train_tem:
        for j in range(len(x_train_var)):
            if i == x_train_var[j]:
                noise = noise_factor * np.random.normal(loc=0.5, scale=1.0, size=x_train[:,j].shape)
                noise[noise>0] = 0
                noise[noise<0] = -2
                x_train_noise[:,j] = x_train_noise[:,j] + noise

    (r, c) = x_test.shape
    x_test_var = []
    for i in xrange(c):
        x_test_var.append(np.var(x_test[:,i]))
    x_test_var = np.array(x_test_var)
    x_test_tem = np.sort(x_test_var)[0:int(noise_factor*len(x_test_var))]

    x_test_noise = x_test
    for i in x_test_tem:
        for j in range(len(x_test_var)):
            if i== x_test_var[j]:
                noise = noise_factor * np.random.normal(loc=0.5, scale=1.0, size=x_test[:,j].shape)
                noise[noise>0] = 0
                noise[noise<0] = -2
                x_test_noise[:,j] = x_test_noise[:,j] + noise


    x_train_noise = np.clip(x_train_noise,0.,1.)
    x_test_noise = np.clip(x_test_noise, 0.,1.)

    print "Loading data sucess"

#    y_train = to_categorical(y_train, nb_class)
#    y_test = to_categorical(y_test, nb_class)

    input = Input(shape=(41,))

    encoded = Dense(30, activation='relu')(input)
    encoded = Dense(20, activation='relu')(encoded)
    encoded = Dense(10, activation='relu')(encoded)
    encoded_output = Dense(encoding_dim)(encoded)

    decoded = Dense(10, activation='relu')(encoded_output)
    decoded = Dense(20, activation='relu')(decoded)
    decoded = Dense(30, activation='relu')(decoded)
    decoded = Dense(41, activation='tanh')(decoded)

    autoencoder = Model(inputs=input, outputs=decoded)

    encoder = Model(inputs=input, outputs=encoded_output)

    autoencoder.compile(optimizer='adam', loss='mse')

    autoencoder.fit(x_train_noise, x_train, epochs=nb_epoch, batch_size=batch_size,shuffle=True, validation_data=(x_test_noise,x_test))

    x_train = encoder.predict(x_train, batch_size=batch_size, verbose=0)

    x_test = encoder.predict(x_test, batch_size=batch_size, verbose=0)

    K.clear_session()

    clf = SVC(C=0.01,decision_function_shape = "ovo")
    clf.fit(x_train,y_train.ravel())
    y_pre = clf.predict(x_test)

    return y_test, y_pre



if __name__ == '__main__':
    y_test, y_pre =  idae()
    print accuracy_score(y_test,y_pre)
    print f1_score(y_test, y_pre, average=None)
    print f1_score(y_test, y_pre, average='macro')
