#-*- coding: UTF-8 -*-
'''
@author: chenwuji
读入原始数据 按照天来分类
'''

dataIn = '/Users/chenwuji/Documents/skypool/集群原始数据/原始数据按天分文件/*'
outpath = '/Users/chenwuji/Documents/skypool/集群原始数据/HotAndCold歌曲收听人数/'
import glob
import os

def readTestList():
    f = glob.glob(dataIn)
    for eachFile in f:
        process(eachFile)


def process(filename):
    dict = set()
    f = open(filename)
    for eachline in f:
        eachline = eachline.split('\n')[0]
        list1 = eachline.split(',')
        listUser = list1[0]
        song = list1[1]
        actionType = int(list1[3])
        date = list1[4]
        if actionType == 1:
            dict.add((listUser,song,date))
    dict2 = {}
    for eachD in dict:
        song2 = eachD[1]
        date2 = eachD[2]
        if dict2.__contains__((song2, date2)):
            currentListenTime = dict2.get((song2, date2))
            dict2.update({(song2, date2): (currentListenTime + 1)})
        else:
            dict2.setdefault((song2, date2), 1)
    for eachRecord in dict2:
        writeToFile(outpath+'歌曲收听人数'+'.csv',eachRecord[0] + ',' + str(dict2.get(eachRecord))+','+eachRecord[1])
        # writeToFile(outpath + eachRecord[0] + '.csv', str(dict2.get(eachRecord)) + ',' + eachRecord[1])
    f.close()

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()


if __name__ == '__main__':

    readTestList()

