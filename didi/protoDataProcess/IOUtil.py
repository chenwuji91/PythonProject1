#-*- coding: UTF-8 -*-
'''
@author: chenwuji
读入基本的数据集  返回相关的值
'''

import glob
import os

def getDataFromDir(rootpath):
    dataDict = {}
    filelist = getFileList(rootpath)
    for eachFile in filelist:
        eachFiledata = getDataFromFile(eachFile)
        filename2 = os.path.basename(eachFile)
        dataDict.setdefault(filename2, eachFiledata)
    return dataDict

def getDataFromFile(file):
    eachFiledata = []
    f = open(file)
    for eachline in f:
        eachline = eachline.split('\n')[0]
        list = eachline.split('\t')
        eachFiledata.append(list)
    f.close()
    return eachFiledata

def getFileList(rootpath):
    f2 = glob.glob(rootpath+'/*')
    return f2

def writeToFile(fileName,data):
    f = file(fileName+ '.csv', "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()

def makeDir(outpathDir):
    if os.path.exists(outpathDir)==False:
        print 'Create DIr'
        os.makedirs(outpathDir)


