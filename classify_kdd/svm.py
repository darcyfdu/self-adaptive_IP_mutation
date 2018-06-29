import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from kdd_input import kdd_test,kdd_train
from sklearn.decomposition  import PCA, TruncatedSVD

def svm():
    print 'Loading data ...'
    x_train, y_train = kdd_train()
    x_test, y_test = kdd_test()

    pca = PCA(n_components=15)
    x_train = pca.fit_transform(x_train)
    x_test = pca.fit_transform(x_test)

    clf = SVC(C=0.01)
    clf.fit(x_train,y_train.ravel())
    y_pre = clf.predict(x_test)

    return y_test, y_pre

if __name__ == '__main__':
    y_test, y_pre = svm()
    print accuracy_score(y_test,y_pre)
    print f1_score(y_test, y_pre, average=None)
    print f1_score(y_test, y_pre, average='macro')