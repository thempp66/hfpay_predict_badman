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
    print('Begin...')
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

    # 配置
    gapTime = 5*60 # 用户行为加测间隔时间
    saveSpace = 1451577600 # 2016-01-01 00:00:00 的时间戳
    newSpace = 1577808000 # 2020-01-01 00:00:00 的时间戳
    kFileLine = 1000 #86628214

    #初始化
    fin = open('flow_1000.txt','r')
    fout = open('features_1000.txt','wb+')
    sameMobile = []
    maxFeat = ['',0,0,0,0,'','','','','']
    for i in range(kFileLine):
        #进度报告
        print('Process line ('+ str(i) + '/' + str(kFileLine) + ') ' + str(int(i * 100 / kFileLine)) + '%')

        line = fin.readline()
        line=line.strip('\n')
        line=line.strip('\r')
        line=line.split('\t')
        if i == 0:
            lastOrderid = line[0]

        orderid = line[0]
        mobile = line[1]
        uin = line[2]
        spoa = line[3]
        price = int(line[4]) / 100
        prov = line[5]
        channel = line[6] if line[6]!='' else 'NULL'
        cmd = line[7]
        timestamp = int(line[8])
        datetime = line[9]
        #统计实时数据，测试先采用遍历

        if i != 0 and mobile == sameMobile[0][1]:
            j = len(sameMobile)
            reqRate = 1
            openKindsSet = set()
            openUinsSet = set()
            openTotalPrice = (int(price) if cmd == '6' else 0)
            for j in range(len(sameMobile)):
                if timestamp - int(sameMobile[-j][8]) <= gapTime:
                    #单位时间请求量计算
                    reqRate += 1

                    #单位时间开通种类数计算
                    openKindsSet.add(sameMobile[j][3])

                    #单位时间开通QQ个数计算
                    openUinsSet.add(sameMobile[j][2])

                    #单位时间成功开通总金额
                    openTotalPrice += (price if sameMobile[j][7] == '6' else 0)

                    j -= 1
                else:
                    break
            featReqRate = reqRate
            featOpenKinds = len(openKindsSet)
            featOpenUins = len(openUinsSet)
            featOpenTotalPrice = openTotalPrice

            #更新最大值
            if orderid == lastOrderid:
                maxFeat[0] = orderid
                maxFeat[1] = max(maxFeat[1],featReqRate)
                maxFeat[2] = max(maxFeat[2],featOpenKinds)
                maxFeat[3] = max(maxFeat[3],featOpenUins)
                maxFeat[4] = max(maxFeat[4],featOpenTotalPrice)
                maxFeat[5] = datetime[11:13] #period
                maxFeat[6] = spoa
                maxFeat[7] = price
                maxFeat[8] = prov
                maxFeat[9] = channel
            else:
                #换orderid了，此时应当输出当前orderid的features
                writeLine = maxFeat[0] + "|" + str(maxFeat[1]) + "|" + str(maxFeat[2]) + "|" + str(maxFeat[3]) + "|" + str(maxFeat[4]) + "|" + maxFeat[5] + "|" + maxFeat[6] + "|" + str(maxFeat[7]) + "|" + maxFeat[8] + "|" + maxFeat[9] + "\n"
                #print(writeLine)
                fout.write(writeLine)
                maxFeat = [orderid,1,1,1,featOpenTotalPrice,datetime[11:13],spoa,price,prov,channel]
                lastOrderid = orderid

        else:
            #换手机了
            sameMobile = [] #换手机需要清空
            featReqRate = 1
            featOpenKinds = 1
            featOpenUins = 1
            featOpenTotalPrice = (price if cmd == '6' else 0)

        sameMobile.append(line)#不管换不换手机都要加上历史行

    #打印最后一条
    writeLine = maxFeat[0] + "|" + str(maxFeat[1]) + "|" + str(maxFeat[2]) + "|" + str(maxFeat[3]) + "|" + str(maxFeat[4]) + "|" + maxFeat[5] + "|" + maxFeat[6] + "|" + str(maxFeat[7]) + "|" + maxFeat[8] + "|" + maxFeat[9] + "\n"
    #print(writeLine)
    fout.write(writeLine)
    print('All finished')
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    fin.close()
    fout.close()


if __name__=='__main__':
    process() 

