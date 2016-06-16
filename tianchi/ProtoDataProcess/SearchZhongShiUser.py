#-*- coding: UTF-8 -*-
'''
@author: chenwuji
读入原始数据 按照天来分类
'''
import tools
import glob
import os
inputPath = '/Users/chenwuji/Documents/skypool/集群原始数据/原始数据按天对应歌手数据按照周/'
songToSinger = {}
outputPath = '/Users/chenwuji/Documents/skypool/集群原始数据/忠实用户按周/'

def readSingerSong():
    f = open('/Users/chenwuji/Documents/skypool/p2_mars_tianchi_songs.csv')
    for eachline in f:
        list1 = eachline.split(',')
        song = str(list1[0])
        singer = str(list1[1])
        songToSinger.setdefault(song,singer)
    f.close()

def readFileList():
    f = glob.glob(inputPath + '*')
    return f

def transferFileToDict(inpath1):
    dict = {}
    f1 = open(inpath1)
    for eachLine in f1:
        user = eachLine.split(',')[0]
        singer = eachLine.split(',')[1]
        if dict.__contains__(singer):
            currentSinger = dict.get(singer)
            currentSinger.add(user)
            dict.update({singer:currentSinger})
        else:
            l = set()
            l.add(user)
            dict.setdefault(singer, l)
    f1.close()
    return dict



def process(inpath1, inpath2):
    dict1 = transferFileToDict(inpath1)
    dict2 = transferFileToDict(inpath2)
    fileName1 = os.path.basename(inpath1)
    fileName2 = os.path.basename(inpath2)
    for eachSinger in dict1:
        oneDay = dict1.get(eachSinger)
        nextDay = dict2.get(eachSinger)
        if not isinstance(nextDay,set):
            writeToFile(outputPath + eachSinger + '.csv',
                        str(fileName1) + ',' + str(beforeCount1) + ',' + '0' + ',' + '0')
            continue
        if not isinstance(oneDay,set):
            writeToFile(outputPath + eachSinger + '.csv',
                        str(fileName1) + ',' + '0' + ',' + str(beforeCount2) + ',' + '0')

            continue
        beforeCount1 = len(oneDay)
        beforeCount2 = len(nextDay)
        intersection = oneDay & nextDay
        afterCount = len(intersection)
        writeToFile(outputPath + eachSinger + '.csv', str(fileName1) + ',' + str(beforeCount1) + ',' +str(beforeCount2) + ',' + str(afterCount))



def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()


if __name__ == '__main__':
    fileList = readFileList()
    tools.makeDir(outputPath)
    readSingerSong()
    for i in range(len(fileList) - 1):
        process(fileList[i], fileList[i + 1])

