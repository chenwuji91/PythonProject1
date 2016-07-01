#-*- coding: UTF-8 -*-
'''
@author: chenwuji
生成sql语句
'''
singerList = []
basicInfo = []
result_a = []


def readData():


    f = open('singerList')
    for eachL in f:
        eachL = eachL.split('\n')[0]
        singerList.append(eachL)
    f.close()

    f = open('basicInfo2')
    for eachL in f:
        eachL = eachL.split('\n')[0]
        basicInfo.append(eachL)
    f.close()


def generateOneSinger(singer):
        print basicInfo[0],
        print '\''+singer+'\'',
        print basicInfo[2],
        print '\'' + singer + '\'',
        print basicInfo[4],
        print '\''+singer+'\'',
        print basicInfo[6],

        s = basicInfo[0] + '\''+singer+'\''+ basicInfo[2]+ '\''+singer+'\''+basicInfo[4] + '\''+singer+'\''+ basicInfo[6]
        result_a.append(s)



def generateAll():
    for eachS in singerList:
        generateOneSinger(eachS)

def w():
    for eachW in result_a:
        writeToFile('allr2', eachW)

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