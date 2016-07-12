
#-*- coding: UTF-8 -*-
'''
@author: chenwuji
常用工具类
'''

#时间处理的相关工具
from datetime import datetime
def timeTranslate(date):
    h = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").hour
    m = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").minute
    timeSplit = int((h * 60 + m)/6) + 1
    return timeSplit

def timeRetranslate(time):
    time = int(time)
    hour = int(time/10)
    minute = int(time%10) * 6
    return str(hour) + ':' + str(minute)

weekend = [3,4,10,11,18,17,25,24,31,1]
def getDay(date):
    d = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").day
    if d in weekend:
        return 1
    else:
        return 0

def intervalofSeconds(d1, d2):
    dd1 = datetime.strptime(d1, "%Y-%m-%d %H:%M:%S")
    dd2 = datetime.strptime(d2, "%Y-%m-%d %H:%M:%S")
    return (dd2-dd1).seconds


#计算类
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


#IO类
import pickle as p
def toFileWithPickle(filename, obj1):
    f = file(filename + '.data', "w")
    p.dump(obj1,f)
    f.close()

import os
# 创建目录,如果路径不存在创建文件夹
def makeDir(outpathDir):
    if os.path.exists(outpathDir)==False:
        print 'Create DIr'
        os.makedirs(outpathDir)

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()

def translate_potential_path(potential_list):#将点的表示转换成为边的一个表示
    translated_set = []
    for eachS in potential_list:
        each_translated_path = []
        for i in range(len(eachS)-1):
            each_translated_path.append((eachS[i],eachS[i + 1]))
        translated_set.append(each_translated_path)
    return translated_set

def re_translate_potential_path(potential_list):#将边的表示转换成为点的表示
    translated_set = []
    for eachS in potential_list:
        each_translated_path = []
        for i in range(len(eachS)-1):
            each_translated_path.append(eachS[i][0])
        each_translated_path.append(eachS[len(eachS)-1][0])
        each_translated_path.append(eachS[len(eachS)-1][1])
        translated_set.append(each_translated_path)
    return translated_set

def re_translate_one_potential_path(potential_list):#将边的表示转换成为点的表示
    translated_set = []
    for eachS in potential_list:
        translated_set.append(eachS[0])
    translated_set.append(eachS[1])
    return translated_set

from datetime import datetime
from datetime import timedelta
def increase_several_seconds(ds, increase_seconds):
    incre = timedelta(seconds = increase_seconds)
    ds2 = datetime.strptime(ds, "%Y-%m-%d %H:%M:%S") + incre
    return str(ds2)

def decrease_several_seconds(ds, increase_seconds):
    incre = timedelta(seconds = increase_seconds)
    ds2 = datetime.strptime(ds, "%Y-%m-%d %H:%M:%S") - incre
    return str(ds2)

if __name__ == '__main__':
    print increase_several_seconds('2015-02-03 12:21:21', 100)
    # print timeRetranslate(73)
    # print re_translate_one_potential_path([('1007', '1009'), ('1009', '1122')])
