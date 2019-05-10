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
    #文件入内存
    print('Load file to memory...')
    lines = []
    with open('flow_orderid_ten.txt','r') as fin:
        for line in fin:
            line=line.strip('\n')
            line=line.strip('\r')
            line=line.split('\t')
            lines.append(line)
    print('Load file to memory finished')
    
    #初始化
    sameBeginIndex = 0
    featReqRate = [0]*len(lines)
    featOpenKinds = [0]*len(lines)
    featOpenUins = [0]*len(lines)
    featOpenTotalPrice = [0]*len(lines)

    for i in range(len(lines)):
        if int(i * 100 / len(lines)) % 5 == 0:
            print('Process line ('+ str(i) + '/' + str(len(lines)) + ') ' + str(int(i * 100 / len(lines))) + '%')
        line = lines[i]
        orderid = line[0]
        mobile = line[1]
        uin = line[2]
        spoa = line[3]
        price = line[4]
        prov = line[5]
        channel = line[6]
        cmd = line[7]
        timestamp = int(line[8])
        datetime = line[9]
        #统计实时数据，测试先采用遍历
        if mobile == lines[sameBeginIndex][1]:
            j = i-1
            reqRate = 1
            openKindsSet = set()
            openUinsSet = set()
            openTotalPrice = (int(price) if cmd == '6' else 0)
            while (j >= sameBeginIndex):
                if timestamp - int(lines[j][8]) <= gapTime:
                    #单位时间请求量计算
                    reqRate += 1

                    #单位时间开通种类数计算
                    openKindsSet.add(lines[j][3])

                    #单位时间开通QQ个数计算
                    openUinsSet.add(lines[j][2])

                    #单位时间成功开通总金额
                    openTotalPrice += (int(price) if lines[j][7] == '6' else 0)

                    j -= 1
                else:
                    break
            featReqRate[i] = reqRate
            featOpenKinds[i] = len(openKindsSet)
            featOpenUins[i] = len(openUinsSet)
            featOpenTotalPrice[i] = openTotalPrice / 100
        else:
            #换手机了
            sameBeginIndex = i
            featReqRate[i] = 1
            featOpenKinds[i] = 1
            featOpenUins[i] = 1
            featOpenTotalPrice[i] = (int(price) if cmd == '6' else 0) / 100
        
    print('Output to file..')
    fout = open('order_fetures.txt', 'wb+')
    for i in range (len(lines)):
        line = lines[i]
        if line[7] == '2' or line[7] == '1':
            #只分析下单行为，因为只有下单阶段才做风控,短验下单的时候订单不落库，可以以2-获取验证码当做下单
            orderid = line[0] #订单号
            peroid = line[9][11:13]
            spoa = line[3]
            price = line[4]
            prov = line[5]
            channel = line[6] if line[6] != '' else 'NULL'
            writeLine = orderid + "|" + str(featReqRate[i]) + "|" + str(featOpenKinds[i]) + "|" + str(featOpenUins[i]) + "|" + str(featOpenTotalPrice[i]) + "|" + peroid + "|" + spoa + "|" + price + "|" + prov + "|" + channel + "\n"
            #print(writeLine)
            fout.write(writeLine)

    print('All finished')
    print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 


if __name__=='__main__':
    process() 

