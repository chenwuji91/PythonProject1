#-*- coding: UTF-8 -*-
'''
@author: chenwuji
处理数据的主函数
'''
import IOUtil
import util
import os
trainingRoot = 'E:\\didi\\citydata\\season_1\\training_data\\'
testingRoot = 'E:\didi\citydata\season_1\test_set_1\\'
orderData = 'order_data\\'
clusterDir = 'cluster_map\\cluster_map'
outRoot = 'E:\\didi\\citydata\\season_1\\processedData\\'

clusterMap = {}

def dataInit():
    list = IOUtil.getDataFromFile(trainingRoot + clusterDir)
    for eachL in list:
        clusterMap.setdefault(eachL[0],eachL[1])

def dataProcess(eachFile):
    oneDayData = IOUtil.getDataFromFile(eachFile)
    basename = os.path.basename(eachFile)
    IOUtil.makeDir(outRoot + basename+'\\')
    for eachline in oneDayData:
        orderID = eachline[0]
        driverID = eachline[1]
        passengerID = eachline[2]
        start_districtID = clusterMap.get(eachline[3])
        dest_districeID = str(clusterMap.get(eachline[4]))
        price = eachline[5]
        time = str(util.timeTranslate(eachline[6]))
        IOUtil.makeDir(outRoot + basename +'\\'+start_districtID+'\\')
        IOUtil.writeToFile(outRoot + basename +'\\'+start_districtID+'\\'+ time,
                           orderID +','+ driverID +',' + passengerID  +','+ start_districtID  +','+dest_districeID +',' + price +',' + time)

if __name__ == '__main__':
    dataInit()
    fileList = IOUtil.getFileList(trainingRoot + orderData)
    for eachFile in fileList:
        dataProcess(eachFile)
        print ''

