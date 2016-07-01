#-*- coding: UTF-8 -*-
'''
@author: chenwuji
生成sql语句
'''
dateList = []
basicInfo = []
result_a = []


def readData():


    f = open('dateList_submit.txt')
    for eachL in f:
        eachL = eachL.split('\n')[0]
        dateList.append(eachL)
    f.close()

    f = open('basicInfo3')
    for eachL in f:
        eachL = eachL.split('\n')[0]
        basicInfo.append(eachL)
    f.close()


def generateOneSinger(singer):
        print basicInfo[0],
        print '\''+singer+'\'',
        print basicInfo[2],
        s = basicInfo[0] + '\''+singer+'\''+ basicInfo[2]
        result_a.append(s)



def generateAll():
    for eachS in dateList:
        generateOneSinger(eachS)

def w():
    for eachW in result_a:
        writeToFile('allr3', eachW)

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