#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time

def process():
    #初始化
    fout_y_pos = open('tag_y_pos.txt','wb')
    fout_y_neg = open('tag_y_neg.txt','wb')
    fout_X_pos = open('features_X_pos.txt','wb')
    fout_X_neg = open('features_X_neg.txt','wb')
    # 配置
    kFileLine = 36845343

    print('Begin...')
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

    print('start divide...')
    fin_X = open('features_X.txt','r')
    fin_y = open('tag_y.txt','r')
    for i in range(kFileLine):
        print('Progress bar ('+ str(i) + '/' + str(kFileLine) + ') ' + str(int(i * 100 / kFileLine)) + '%') #进度条
        line_X=fin_X.readline()
        line_y=fin_y.readline()
        if (line_y == '1\n'):
            fout_y_neg.write(line_y)
            fout_X_neg.write(line_X)
        elif (line_y == '0\n'):
            fout_y_pos.write(line_y)
            fout_X_pos.write(line_X)
        else:
            print(line_y)

    print('All finished')
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    fin_X.close()
    fin_y.cloee()
    fout_y_pos.close()
    fout_y_neg.close()
    fout_X_pos.close()
    fout_X_neg.close()


if __name__=='__main__':
    process() 

