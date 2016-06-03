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
orderDir = 'order_data\\'
trafficDir = 'traffic_data\\'
weatherDir = 'weather_data\\'
clusterFile = 'cluster_map\\cluster_map'
poiFile = 'poi_data\\poi_data'
outRoot = 'E:\\didi\\citydata\\season_1\\processedData2\\'
weekend = ['2016-01-01','2016-01-02','2016-01-03','2016-01-09','2016-01-10','2016-01-16','2016-01-17','2016-01-23','2016-01-24','2016-01-31','2016-01-30']



clusterMap = {}
poiMap = {}
def loadCluster():
    list = IOUtil.getDataFromFile(trainingRoot + clusterFile)
    for eachL in list:
        clusterMap.setdefault(eachL[0], eachL[1])

def loadPOI():
    list = IOUtil.getDataFromFile(trainingRoot + poiFile)
    for eachL in list:
        poiHashValue = eachL[0]
        poiValue = clusterMap.get(poiHashValue)
        poiList = eachL[1:len(eachL)]
        poiMap.setdefault(poiValue, poiList)

def dataInit():
    loadCluster()
    loadPOI()

def loadOrder(date):
    dataDict = {}
    oneDayData = IOUtil.getDataFromFile(trainingRoot + orderDir + 'order_data_' + date)
    for eachline in oneDayData:
        driverID = eachline[1]
        start_districtID = clusterMap.get(eachline[3])
        time = str(util.timeTranslate(eachline[6]))
        if driverID == 'NULL':
            if dataDict.__contains__((time, start_districtID)):
                currentGap = dataDict.get((time, start_districtID))
                dataDict.update({(time, start_districtID):(currentGap + 1)})
            else:
                dataDict.setdefault((time, start_districtID),1)
    return dataDict


def loadTraffic(date):
    dataDict = {}
    oneDayData = IOUtil.getDataFromFile(trainingRoot + trafficDir + 'traffic_data_' + date)

    for eachline in oneDayData:
        start_districtID = clusterMap.get(eachline[0])
        time = str(util.timeTranslate(eachline[5]))
        trafficList = eachline[1:5]
        if dataDict.__contains__((time, start_districtID)):
            pass
        else:
            dataDict.setdefault((time, start_districtID),trafficList)

    for i in range(1, 145):
        for j in range(1,67):
            if dataDict.__contains__((str(i),str(j))):
                pass
            else:
                if dataDict.__contains__((str(i-1),str(j))):
                    dataSupply = dataDict.get((str(i-1),str(j)))
                    dataDict.setdefault((str(i),str(j)), dataSupply)
                else:
                    dataSupply = dataDict.get((str(i + 1),str(j)))
                    dataDict.setdefault((str(i),str(j)), dataSupply)
    return dataDict


def loadWeather(date):
    dataDict = {}
    oneDayData = IOUtil.getDataFromFile(trainingRoot + weatherDir + 'weather_data_' + date)
    for eachline in oneDayData:
        time = str(util.timeTranslate(eachline[0]))
        weather = eachline[1]
        temperature = eachline[2]
        pm = eachline[3]
        if dataDict.__contains__(time):
            pass
        else:
            dataDict.setdefault(time, [weather, temperature, pm])
    for i in range(1,145):
        if dataDict.__contains__(str(i)):
            pass
        else:
            if dataDict.__contains__(str(i-1)):
                dataSupply = dataDict.get(str(i-1))
                dataDict.setdefault(str(i), dataSupply)
            else:
                dataSupply = dataDict.get(str(i+1))
                dataDict.setdefault(str(i), dataSupply)
    return dataDict


def dataProcess(eachFile):
    basename = os.path.basename(eachFile)
    dateInfo = basename[11:21]
    if dateInfo in weekend:
        weekMark = 1
    else:
        weekMark = 0
    orderInfo = loadOrder(dateInfo)
    trafficInfo = loadTraffic(dateInfo)
    weatherInfo = loadWeather(dateInfo)
    for i in range(1, 145):
        for j in range(1, 67):
            time = str(i)
            place = str(j)
            currentOutRecord = dateInfo +  ',' + time + ',' + place +',' + str(weekMark) +\
                               ',' + str(orderInfo.get((time,place))) + ','  + str(trafficInfo.get((time, place))) \
                               + ',' + str(weatherInfo.get(time)) + \
                               ',' +  str(poiMap.get(place))
            IOUtil.makeDir(outRoot)
            IOUtil.writeToFile(outRoot + time + '_' + place + '.csv', currentOutRecord)



if __name__ == '__main__':
    dataInit()
    fileList = IOUtil.getFileList(trainingRoot + orderDir)
    for eachFile in fileList:
        print eachFile
        dataProcess(eachFile)


