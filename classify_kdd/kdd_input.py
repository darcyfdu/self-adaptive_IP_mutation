# -*- coding:utf-8 -*-
import os
import sys
import numpy as np
import random
path1 = ''

noise = 0.4

def kdd_train():
    input_train = np.loadtxt(path1+'train_new.csv', delimiter=',', dtype=np.float)
    (r,c) = input_train.shape
    #print input_train.shape
    x = [random.randint(0,r-1) for _ in range(int(r*noise))]
    x_train = input_train[:,0:c-1]
    x_test = input_train[:,c-1]-1
#    print noise
#    for i in x:
#        if x_test[i] == 1:
#            x_test[i] = random.randint(2,3)
#        if x_test[i] == 2:
#            x_test[i] = random.randint(1, 3)
#        if x_test[i] == 3:
#            x_test[i] = random.randint(1, 2)

#    print x_test.tolist().count(2)

    return x_train,  x_test

def kdd_test():
    input_test = np.loadtxt(path1+'test_new.csv',delimiter=',', dtype=np.float)
    (r,c) = input_test.shape
    return input_test[:,0:c-1],input_test[:,c-1]-1

if __name__ == '__main__':
    x_train, y_train = kdd_train()
    x_test, y_test = kdd_test()
    print x_train.shape
    print y_train[1:50]

