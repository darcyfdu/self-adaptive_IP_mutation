from sklearn.metrics import accuracy_score, f1_score
from svm import svm
from ae import ae
from DAE import dae
from idae import idae

noise = [0.05, 0.1, 0.2, 0.3, 0.4, 0.5]
output = open('result', 'w')
output.write('models    '+'acc      '+'f1'+'\n')

for i in noise:
    y_test, y_pre = svm(i)
    print "svm"
    print accuracy_score(y_test, y_pre)
    print f1_score(y_test, y_pre, average=None)
    print f1_score(y_test, y_pre, average='macro')

    y_test, y_pre = ae(i)
    print "AE"
    print accuracy_score(y_test, y_pre)
    print f1_score(y_test, y_pre, average=None)
    print f1_score(y_test, y_pre, average='macro')

    y_test, y_pre = dae(i)
    print "DAE"
    print accuracy_score(y_test, y_pre)
    print f1_score(y_test, y_pre, average=None)
    print f1_score(y_test, y_pre, average='macro')

    y_test, y_pre = idae(i)
    print "IDAE"
    print accuracy_score(y_test, y_pre)
    print f1_score(y_test, y_pre, average=None)
    print f1_score(y_test, y_pre, average='macro')