#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
#检验正太分布
#实验步骤  先依次读取每一条道路的车速的信息 (当前路段,下一个路口,半个小时的时间段,周末还是工作日)--> 判断这个数据集是否大于50个
# -->对于大于50个的样本做KS检验-->统计这个时段内正太分布的比例

#读取文件的时候  先读取suzhou1——10的列表  然后在另外一个目录下做正则匹配 读取相关的所有文件  一个路口存到一个集合中进行操作
#操作包括周末的判断 时间段元组的划分 等
import tools
path1 = '/Users/chenwuji/Documents/苏州出租车/newMethod/'
path2 = '/Users/chenwuji/Documents/苏州出租车/newMethod2/newMethod1/'
outputPathSingleRsult = '/Users/chenwuji/Documents/苏州出租车/按照平均速度检测标准正态时间结果/检验平均速度的/'
outpathResultDate = '/Users/chenwuji/Documents/苏州出租车/按照平均速度检测标准正态时间结果/按照日期的检验平均速度/'
tools.makeDir(outpathResultDate)
tools.makeDir(outputPathSingleRsult)

fileList = []

from scipy.stats import kstest
import numpy as np
import glob
import os
import tools
rootpath = '/Users/chenwuji/Documents/苏州出租车/'
lukouDict = {}
class RoadIntersectionPoint:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def readLukou():
    f = open(rootpath + '道路等相关数据/intersection_newid.txt')
    for eachline in f:
        list1 = eachline.split(',')
        lukouId = list1[0]
        position1 = list1[2]
        position2 = list1[3]
        lukouDict.setdefault(lukouId, RoadIntersectionPoint(float(position1), float(position2)))
    f.close()


def fileListAll():
    f = glob.glob(path1 + '*')
    for eachFile in f:
        fileBaseName = os.path.basename(eachFile)
        fileList.append(fileBaseName)

def readData(currentFile):
    currentRoad = []
    f1 = open(path1 + currentFile)
    for eachline in f1:
        currentRoad.append(eachline)
    f1.close()
    f2List = glob.glob(path2 + currentFile +'*')
    for eachF in f2List:
        f = open(eachF)
        for eachline in f:
            currentRoad.append(eachline)
        f.close()
    return currentRoad

def dataFilter(oneFileDataList):
    currentRoadDict = {}
    for eachline in oneFileDataList:
        list = eachline.split(';')
        currentPri = list[0]  #当前路的前一个点
        currentLater = list[1]  #当前路的后一个点
        speed = float(list[2])
        date1 = list[3]
        date2 = list[4]
        time_interval = tools.intervalofSeconds(date1, date2)
        ifweekend = tools.getDay(date1)
        timeInfo = tools.timeTranslate(date1)
        dis = tools.calculate(lukouDict.get(currentPri).x, lukouDict.get(currentPri).y,
                              lukouDict.get(currentLater).x, lukouDict.get(currentLater).y)
        if speed > 5.0 and time_interval < 200 and speed < 100:
            time1 = dis/speed
            basicInfo = (currentPri, currentLater, timeInfo, ifweekend)
            if currentRoadDict.__contains__(basicInfo):
                speedList = currentRoadDict.get(basicInfo)
                speedList.append(time1)
                currentRoadDict.update({basicInfo:speedList})
            else:
                speedList = []
                speedList.append(time1)
                currentRoadDict.setdefault(basicInfo, speedList)
    speedDictAC = {}
    for eachD in currentRoadDict:
        l = currentRoadDict.get(eachD)
        if len(l) > 6:
            speedDictAC.setdefault(eachD, l)
    return speedDictAC

def KSTest(dataDict):
    print 'Done:' + str(dataDict)
    for eachRecord in dataDict:
        currentKey = eachRecord
        eachPointList = dataDict.get(currentKey)
        listMean = np.mean(eachPointList)
        liststd = np.std(eachPointList)
        floorList = listMean * 0.5
        ceilList = listMean * 1.5
        x = []
        x1 = []
        for eachE in eachPointList:
            # if eachE > floorList and eachE < ceilList:
                x.append((eachE - listMean) / liststd)
                x1.append(eachE)
        test_stat = kstest(x, 'norm')
        tools.makeDir(outputPathSingleRsult)
        tools.writeToFile(outputPathSingleRsult + str(eachRecord[0]) + '_' + str(eachRecord[1]) + '_' +str(eachRecord[3]),
                          str(eachRecord) + ':' + str(test_stat)+';' + str(x1) +';'+ str(listMean) + ';' + str(liststd))
        tools.writeToFile(outpathResultDate + str(eachRecord[2]) +'_'+ str(eachRecord[3]) +'.csv' ,str(test_stat[1])+ ',' + str(eachRecord[0]) + ',' + str(eachRecord[1]) + ',' +str(listMean) + ',' + str(liststd))


if __name__ =='__main__':
    fileListAll()
    readLukou()
    print len(fileList)
    for eachFile in fileList:
        try:
            dataList = readData(eachFile)
            dataDict = dataFilter(dataList)
            KSTest(dataDict)
        except:
            continue


    # x = np.random.normal(23,3,1000)
    # x = x * 1000
    # print x
    # list1 = [16,22,14,27,12,35,18,40,16,29,40]
    # list2 = [40, 77, 11, 7, 22, 38, 35, 16, 14, 46, 42, 25, 7, 20, 24, 40, 24, 18, 38, 42, 44, 24, 38, 42, 18, 33, 42, 22, 31, 38, 29, 38, 44, 18, 7, 14, 29, 24, 62, 37, 37, 29, 16, 42]
    # test_stat = kstest(list1,'norm')
    # print test_stat
