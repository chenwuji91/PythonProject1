#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
import os
from datetime import datetime
def timetranslate(datetime1):
    hhh = datetime.strptime(datetime1, "%Y-%m-%d %H:%M:%S").hour
    mmm = datetime.strptime(datetime1, "%Y-%m-%d %H:%M:%S").minute
    sss = datetime.strptime(datetime1, "%Y-%m-%d %H:%M:%S").second
    return sss + mmm * 60 + hhh * 3600

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()

def makeDir(outpathDir):
    if os.path.exists(outpathDir)==False:
        print 'Create DIr'
        os.makedirs(outpathDir)

import pickle as p
def toFileWithPickle(filename, obj1):
    f = file(filename + '.data', "w")
    p.dump(obj1,f)
    f.close()