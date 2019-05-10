#!/usr/bin/python
# -*- coding: UTF-8 -*-

import time

spoaDict={}
def spoa2Int(spoa):
    if (spoaDict.has_key(spoa)==False):
        spoaDict[spoa] = len(spoaDict)
    return spoaDict[spoa]

provDict={}
def prov2Int(prov):
    if (provDict.has_key(prov)==False):
        provDict[prov] = len(provDict)
    return provDict[prov]

def process():
    #初始化
    fout_y = open('tag_y.txt','wb')
    fout_X = open('features_X.txt','wb')
    # 配置
    kFileLine = 36845343

    print('Begin...')
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

    #导入核减订单清单
    print('Begin load hj orderid...')
    hj_orderid_set = set() 
    with open('hj_orderid.txt','r') as fin:
        for line in fin:
            line=line.strip('\n')
            line=line.strip('\r')
            hj_orderid_set.add(line)
    print('End load hj orderid...')

    print('start tagging...')
    fin = open('features_orderid_ten_sort.txt','r')
    for i in range(kFileLine):
        print('Progress bar ('+ str(i) + '/' + str(kFileLine) + ') ' + str(int(i * 100 / kFileLine)) + '%') #进度条
        line=fin.readline()
        line=line.strip('\n')
        line=line.strip('\r')
        line=line.split('|')
        writeline = line[1] + "|" + line[2] + "|" + line[3] + "|" + line[4] + "|" + line[5] + "|" + line[6] + "|" + line[7] + "|" + line[8] + "|" + line[9] + "\n"
        #print(writeline)
        fout_X.write(writeline)
        if line[0] in hj_orderid_set:
            fout_y.write("1\n")
        else:
            fout_y.write("0\n")


    print('All finished')
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    fin.close()
    fout_y.close()
    fout_X.close()


if __name__=='__main__':
    process() 

