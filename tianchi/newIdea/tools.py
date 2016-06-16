
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