#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
#检验正太分布

path4 = '/Users/chenwuji/Documents/苏州出租车/resultReduced2/'
outputPath = '/Users/chenwuji/Documents/苏州出租车/NormalDisResult/'
fileList = []
from scipy.stats import kstest
import numpy as np
import glob
import os
def fileListAll():

    f = glob.glob(path4 + '*')
    for eachFile in f:
        fileBaseName = os.path.basename(eachFile)
        fileList.append(fileBaseName)

def writeToFile(fileName,data):
    f = file(outputPath+fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()

def readData(currentFile):
    f = open(path4 + currentFile)
    speedInfo = {}
    for eachline in f:
        list = eachline.split(';')
        basicInfo = list[0]
        currentPri = int(basicInfo.split(',')[0])
        currentLater = int(basicInfo.split(',')[1])
        nextPri = int(basicInfo.split(',')[2])
        roadDetailInfo = list[3]
        otherRoadIntersection = roadDetailInfo.split('[')[1].split(']')[0].split(',')
        if len(otherRoadIntersection)>0:
            for eachPointIndex in range(1,len(otherRoadIntersection)):
                nextPri = int(otherRoadIntersection[eachPointIndex].split('\'')[1])
                if nextPri != currentPri and nextPri != currentLater:
                    break
        basicInfo = str(currentPri)+','+str(currentLater)+','+str(nextPri)

        from datetime import datetime
        ddd = datetime.strptime((list[2].split(',')[1]), "%Y-%m-%d %H:%M:%S").hour
        print ddd
        mmm = datetime.strptime((list[2].split(',')[1]), "%Y-%m-%d %H:%M:%S").minute
        # print mmm
        if int(mmm) < 30:
            mmm = 0
        else:
            mmm = 1
        basicInfo = basicInfo + ',' + str(ddd)+'-'+str(mmm)
        # print basicInfo




        # basicInfo = basicInfo.split(',')[0]+',' + basicInfo.split(',')[1] +','+ basicInfo.split(',')[3]
        speed = int(list[1])
        if (speedInfo.__contains__(basicInfo)):
            currentList = speedInfo.get(basicInfo)
            currentList.append(speed)
            speedInfo.update({basicInfo: currentList})
        else:
            speed0 = []
            speed0.append(speed)
            speedInfo.setdefault(basicInfo, speed0)
    return speedInfo


if __name__ =='__main__':
    fileListAll()
    for eachFile in fileList:
        # print eachFile
        dataDict = readData(eachFile)
        for eachModel in dataDict:
            currentKey = eachModel
            eachPointList = dataDict.get(currentKey)
            listMean = np.mean(eachPointList)
            liststd = np.std(eachPointList)
            floorList = listMean * 0.5
            ceilList = listMean *1.5
            x = []
            for eachE in eachPointList:
                if eachE > floorList and eachE < ceilList:
                    x.append((eachE-listMean)/liststd)
                    # x.append(eachE)#((x-x.mean())/x.std(), 'norm')
            try:
                test_stat = kstest(x,'norm')
                writeToFile(eachFile, str(currentKey) + ':' + str(test_stat))
            except:
                pass
            print eachPointList
            print currentKey
            print test_stat
    # x = np.random.normal(23,3,1000)
    # x = x * 1000
    # print x
    # list1 = [16,22,14,27,12,35,18,40,16,29,40]
    # list2 = [40, 77, 11, 7, 22, 38, 35, 16, 14, 46, 42, 25, 7, 20, 24, 40, 24, 18, 38, 42, 44, 24, 38, 42, 18, 33, 42, 22, 31, 38, 29, 38, 44, 18, 7, 14, 29, 24, 62, 37, 37, 29, 16, 42]
    # test_stat = kstest(list1,'norm')
    # print test_stat
