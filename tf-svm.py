#!/usr/bin/python
# -*- coding: UTF-8 -*-
#参考
#特征工程全流程 https://www.cnblogs.com/peizhe123/p/7412364.html
#svm svc参数解释  https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
#非数值特征编码问题 https://blog.csdn.net/luguanyou/article/details/80598122
#独热编码 https://blog.csdn.net/dongyanwen6036/article/details/78555163
#原始输入数据归一化 https://blog.csdn.net/Datapad/article/details/80174775

from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.svm import SVC
from sklearn import metrics
from sklearn import preprocessing
from sklearn.decomposition import PCA
import pandas as pd
import time
import logging
import os
from sklearn.ensemble import ExtraTreesClassifier

def test_svm(random_state):
    logging.basicConfig(filename=os.path.join(os.getcwd(),'log_12w.txt'),level=logging.DEBUG)
    logging.info('=============================================================')
    logging.info('Begin...')
    logging.info('Random_state='+ str(random_state))
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


    #加载特征数据集
    logging.info('Load features...')
    X=[]
    columnName = ['featReqRate','openKinds','openUins','openTotalPrice','period','spoa','price','prov','channel']
    #columnName = ['featReqRate','openKinds','openUins','openTotalPrice']
    with open('features_X_12w.txt','r') as f:
        for line in f:
            line=line.strip('\n')
            line=line.strip('\r')
            columns=line.split('|')
            line = [0]*9
            line[0] = int(columns[0])
            line[1] = int(columns[1])
            line[2] = int(columns[2])
            line[3] = int(columns[3])
            line[4] = columns[4]
            line[5] = columns[5]
            line[6] = int(columns[6])
            line[7] = columns[7]
            line[8] = columns[8]
            X.append(line)
    logging.info('Load features finished')

    #加载标签数据集
    logging.info('Load tag...')
    f=open('tag_y_12w.txt','r')
    sourceInLine=f.readlines()
    y=[]
    for line in sourceInLine:
        line=line.strip('\n')
        line=line.strip('\r')
        line=line.split(' ')
        line=map(int,line)
        y.extend(line)
    #logging.info(y)
    logging.info('Load tag finished')
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


    #非数值部分独热编码
    logging.info('One hot encode...')
    df = pd.DataFrame(X,columns = columnName)
    X = []
    df = pd.get_dummies(df[columnName]) #实际只作用于字符类型的列，对数值型是不处理的
    #logging.info(df)
    logging.info('One hot encode finished')
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    #归一化
    logging.info('Begin normalization...')
    min_max_scaler = preprocessing.MinMaxScaler()  
    X = min_max_scaler.fit_transform(df)
    #logging.info(X)
    print(X)
    logging.info('Begin normalization finished')
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    #pca降维
    logging.info('Begin pca...')
    pca = PCA(n_components=0.9)# 保证降维后的数据保持90%的信息
    pca.fit(X)
    X = pca.transform(X)
    print(X)
    logging.info(pca.explained_variance_ratio_)
    logging.info('Pca finished')


    # 将数据集拆分为训练集和测试集 
    logging.info('Data divide...')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=random_state)
    # logging.info('xtr',X_train)
    # logging.info('xtest',X_test)
    # print('ytr',y_train)
    # print('ytest',y_test)
    logging.info('Data divide finished')
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    #训练
    logging.info('training...')
    clf = SVC()
    clf.fit(X_train, y_train) 
    SVC(C=1.0, cache_size=200, class_weight=None, coef0=0.0,
    decision_function_shape='ovr', degree=3, gamma='auto', kernel='rbf',
    max_iter=-1, probability=False, random_state=None, shrinking=True,
    tol=0.001, verbose=False)
    logging.info('training finished')
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    #预测
    logging.info('predicting...')
    y_pred = clf.predict(X_test)
    #logging.info(y_pred)    
    logging.info(metrics.accuracy_score(y_test, y_pred))
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    logging.info('predict finished')

    logging.info('All finished')
    logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    logging.info('')
    logging.info('')

def cross_validate():
    for i in range(10):
        test_svm(i) 

if __name__=='__main__':
    #test_svm(1)
    cross_validate()
