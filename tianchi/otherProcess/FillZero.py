#-*- coding: UTF-8 -*-
'''
@author: chenwuji
读取一个文件夹下面所有的数据  依据日期  针对下面的日期集合  对于没有数据的项目 收听的次数加上0
输入的是一个文件夹 文件名为歌曲名称
输出的也是一个文件夹  文件名为歌曲名称
'''
import glob
import os
import tools
outputPath = '/Users/chenwuji/Documents/skypool/集群原始数据/歌曲收听次数filled/'

dateList = []
def readRootPath():
    f2 = glob.glob('/Users/chenwuji/Documents/skypool/集群原始数据/歌曲收听次数/*')
    for file2 in f2:
        readToBeFilled(file2)


def readToBeFilled(filePath):
    songList = {}
    f = open(filePath)
    for eachline in f:
        eachline = eachline.split('\n')[0]
        list1 = eachline.split(',')
        listenTime = str(list1[0])
        date = str(list1[1])
        songList.setdefault(date,listenTime)
    f.close()
    fillZero(os.path.basename(filePath),songList)

def genernateDateList():
    for i in range(20150301, 20150332):
        dateList.append(i)
    for i in range(20150401, 20150431):
        dateList.append(i)
    for i in range(20150501, 20150532):
        dateList.append(i)
    for i in range(20150601, 20150631):
        dateList.append(i)
    for i in range(20150701, 20150732):
        dateList.append(i)
    for i in range(20150801, 20150831):
        dateList.append(i)

def fillZero(currentSong,songList):
    for eachDay in dateList:
        eachDay = str(eachDay)
        if songList.__contains__(eachDay):
            pass
        else:
            songList.setdefault(eachDay,0)
    dict1 = sorted(songList.iteritems(), key=lambda d: d[0])
    for eachE in dict1:
        writeToFile(outputPath+currentSong,str(eachE[1])+','+str(eachE[0]))


def writeToFile(fileName,data):

    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()


if __name__ == '__main__':
    tools.makeDir(outputPath)
    genernateDateList()
    readRootPath()