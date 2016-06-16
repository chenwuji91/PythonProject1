
#-*- coding: UTF-8 -*-
'''
@author: chenwuji
计算歌曲的收听人数
'''
import os
import shutil

def removeDir(path):
    if os.path.exists(path) == True:
        print 'Remove DIr'
        shutil.rmtree(path)


# 创建目录,如果路径不存在创建文件夹
def makeDir(outpathDir):
    if os.path.exists(outpathDir)==False:
        print 'Create DIr'
        os.makedirs(outpathDir)

from datetime import datetime
def twoDateInterval(date1, date2):
    d1 = datetime.strptime(date1, "%Y%m%d")
    d2 = datetime.strptime(date2, "%Y%m%d")
    return (d2-d1).days


if __name__ == '__main__':
    print twoDateInterval('20160905','20140902')