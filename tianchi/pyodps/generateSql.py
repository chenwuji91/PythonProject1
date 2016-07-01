#-*- coding: UTF-8 -*-
'''
@author: chenwuji
生成sql语句
'''
dateList = []
singerList = []
basicInfo = []
result_a = []


def readData():
    f = open('dateList')
    for eachL in f:
        eachL = eachL.split('\n')[0]
        dateList.append(eachL)
    f.close()

    f = open('singerList')
    for eachL in f:
        eachL = eachL.split('\n')[0]
        if eachL != '2dc8d3a917b12e65d4695e2277dd4943':
            singerList.append(eachL)
    f.close()

    f = open('basicInfo')
    for eachL in f:
        eachL = eachL.split('\n')[0]
        basicInfo.append(eachL)
    f.close()


def generateOneSingerOneDate(singer,ddd):
        print basicInfo[0],
        print '\''+singer+'\'',
        print basicInfo[2],
        print ddd,
        print basicInfo[4],
        print '\''+singer+'\'',
        print basicInfo[6],
        print ddd,
        print basicInfo[8],
        print '\''+singer+'\'',
        print basicInfo[10]
        s = basicInfo[0] + '\''+singer+'\''+ basicInfo[2]+ ddd+ basicInfo[4] + '\''+singer+'\''+ basicInfo[6] + ddd+ basicInfo[8]+ '\''+singer+'\''+ basicInfo[10]
        result_a.append(s)


def generateOneSinger(singer):
    for eachD in dateList:
        generateOneSingerOneDate(singer,eachD)

def generateAll():
    for eachS in singerList:
        generateOneSinger(eachS)

def w():
    for eachW in result_a:
        writeToFile('allr', eachW)

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()


if __name__ == '__main__':
    readData()
    # generateOneSinger('2dc8d3a917b12e65d4695e2277dd4943')
    generateAll()
    w()