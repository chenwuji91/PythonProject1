#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
#重新产生移动序列 产生的移动序列是标准的格式  可以直接读取为tuple的
#将路测的数据读取  并进行序列化存储

import glob
import os
dictAllData = {}
fileOutPath = '/Users/chenwuji/Documents/RoadMatch/NotProcessed/'

def readFile():

    f2 = glob.glob('/Users/chenwuji/Documents/RoadMatch/原始数据及变种/移动序列处理原始数据/szfDate/*')
    for file2 in f2:
        dataOneFile = []
        filename2 = os.path.basename(file2)
        print '当前正在处理文件:' +  filename2
        f3 = open(file2)
        for eachline in f3:
            list1 = eachline.split('\n')[0].split(',')
            date1 = list1[0]
            jizhan = list1[2]
            dataOneFile.append((jizhan,date1))
        f3.close()
        dictAllData.setdefault(date1[0:8], dataOneFile)
    toFileWithPickle('szf',dictAllData)
    for eachF in dictAllData:
        eachS = dictAllData.get(eachF)
        for eachL in eachS:
             writeToFile(fileOutPath + eachF,eachL[0]+','+eachL[1])

import pickle as p
def toFileWithPickle(filename, obj1):
    rootpath = fileOutPath
    f = file(rootpath + filename + '.data', "w")
    p.dump(obj1,f)
    f.close()

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()

if __name__ == '__main__':
    readFile()