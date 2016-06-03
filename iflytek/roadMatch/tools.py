#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
import os
from datetime import datetime

def traceLegalCheck(trace,cellIdDict,JiZhanPoint,houxuanPointDict):
    tracenew = []
    for pointPair in range(len(trace)):
        point = cellIdDict.get(trace[pointPair][0])

        if isinstance(point,JiZhanPoint):
                Houxuan1List = houxuanPointDict.get(trace[pointPair][0])  # 当前的点的所有候选点集  trace保存的是一个元组  [0]号下标表示基站点信息  [1]号下标表示时间戳
                if(len(Houxuan1List)>0):
                    # if len(tracenew) > 0:  # 从第二个点开始 如果现在点和满足条件的前一个点的距离超过 2 km 则不添加这个点
                    #     # if calculate(point.x, point.y, cellIdDict.get(tracenew[len(tracenew) - 1][0]).x,
                    #     #              cellIdDict.get(tracenew[len(tracenew) - 1][0]).y) > 2000:
                    #     #     break
                    tracenew.append(trace[pointPair])
    return tracenew

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


def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.close()

def process(listall):
    listnew = []
    for eachP in listall:
        if listnew.__contains__(eachP):
            index1 = listnew.index(eachP)
            listnew = listnew[0:index1]
            listnew.append(eachP)
            pass
        else:
            listnew.append(eachP)
    return listnew

from math import radians, cos, sin, asin, sqrt
def calculate(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000