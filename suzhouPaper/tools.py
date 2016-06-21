
#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''


from datetime import datetime
def timeTranslate(date):
    h = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").hour
    m = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").minute
    timeSplit = int((h * 60 + m)/6) + 1
    return timeSplit

def timeRetranslate(time):
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

if __name__ == '__main__':
    print intervalofSeconds('2015-02-03 08:19:01','2015-02-04 18:09:09')#96
    print calculate(120.698959,31.3425903,120.693153,31.330349)

