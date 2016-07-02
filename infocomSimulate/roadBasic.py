#-*- coding: UTF-8 -*-
'''
@author: chenwuji
本类为道路的基本类  保存道路相关的基本数据
'''


import tools
import os

zuoshangjiao = 120.6354828592534, 31.376368052001823
zuoxiajiao = 120.63549057996597, 31.253756666173818
youshangjiao = 120.85634919819948, 31.376015656647887
youxiajiao = 120.85635657413037, 31.253404335545934
sep = os.path.sep

lukouDict = {}
roadAdjDict = {}
carDataDict = []
weekend_speed_avg_varivace_para = {}
weekday_speed_avg_varivace_para = {}
weekend_time_avg_varivace_para = {}
weekday_time_avg_varivace_para = {}


rootpath = sep + 'Users'+sep+'chenwuji'+sep+'Documents'+sep+'苏州出租车'+sep

def getRoadSpeedAvg(roadIntersection1, roadIntersection2, time1, ifweekend):#返回float类型
    if ifweekend == 1:
        allLukou = weekend_speed_avg_varivace_para.get(time1)
        if allLukou.__contains__((roadIntersection1, roadIntersection2)):
            return allLukou.get((roadIntersection1,roadIntersection2))[0]
    else:
        allLukou = weekday_speed_avg_varivace_para.get(time1)
        if allLukou.__contains__((roadIntersection1, roadIntersection2)):
            return allLukou.get((roadIntersection1, roadIntersection2))[0]


def getRoadSpeedVariance(roadIntersection1, roadIntersection2,time1, ifweekend):#返回float类型 方差
    if ifweekend == 1:
        allLukou = weekend_speed_avg_varivace_para.get(time1)
        if allLukou.__contains__((roadIntersection1, roadIntersection2)):
            return allLukou.get((roadIntersection1, roadIntersection2))[1]
        else:
            print 'No info'

    else:
        allLukou = weekday_speed_avg_varivace_para.get(time1)
        if allLukou.__contains__((roadIntersection1, roadIntersection2)):
            return allLukou.get((roadIntersection1, roadIntersection2))[1]
        else:
            print 'No info'

def getRoadTimeAvg(roadIntersection1, roadIntersection2, time1, ifweekend):
    if ifweekend == 1:
        allLukou = weekend_time_avg_varivace_para.get(time1)
        if allLukou.__contains__((roadIntersection1,roadIntersection2)):
            return allLukou.get((roadIntersection1,roadIntersection2))[0]
        else:
            print 'No info'
    else:
        allLukou = weekday_time_avg_varivace_para.get(time1)
        if allLukou.__contains__((roadIntersection1, roadIntersection2)):
            return allLukou.get((roadIntersection1, roadIntersection2))[0]
        else:
            print 'No info'


def getRoadTimeVariance(roadIntersection1, roadIntersection2, time1, ifweekend):
    if ifweekend == 1:
        allLukou = weekend_time_avg_varivace_para.get(time1)
        return allLukou.get((roadIntersection1,roadIntersection2))[1]
    else:
        allLukou = weekday_time_avg_varivace_para.get(time1)
        return allLukou.get((roadIntersection1, roadIntersection2))[1]



def judgeBounds(roadIntersection):
    position = getRoadPointLocation(roadIntersection)
    if position[0] > zuoxiajiao[0] and position[0] < youshangjiao[0] and \
                position[1] > zuoxiajiao[1] and position[1] < youshangjiao[1]:
        return True
    else:
        return False


def getRoadLen(roadIntersection1, roadIntersection2):#返回float类型
    neighbour = roadAdjDict.get(roadIntersection1)
    if roadIntersection2 in neighbour:
        dis = tools.calculate(lukouDict.get(roadIntersection1).x, lukouDict.get(roadIntersection1).y,
                          lukouDict.get(roadIntersection2).x, lukouDict.get(roadIntersection2).y)
    else:
        print 'Illegal parameter! Check the adj relation!'
        dis = -1
    return dis


def getRoadPointLocation(roadIntersection1):#返回tuple类型 ((),())嵌套形式
    position1 = (lukouDict.get(roadIntersection1).x, lukouDict.get(roadIntersection1).y)
    return position1

def getNeighbourList(roadIntersection1):
    return roadAdjDict.get(roadIntersection1)


class RoadIntersectionPoint:
    def __init__(self,x,y):
        self.x = x
        self.y = y


def readLukou():
        f =open('data'+sep+'intersection_newid')
        for eachline in f:
            list1 = eachline.split(',')
            lukouId = list1[0]
            position1 = list1[2]
            position2 = list1[3]
            lukouDict.setdefault(lukouId,RoadIntersectionPoint(float(position1),float(position2)))
        f.close()

def readAdj():
        f =open('data'+sep+'roadnet_newid')
        for eachline in f:
            list1 = eachline.split(':')
            list2 = list1[1].split()
            roadAdjDict.setdefault(list1[0],list2)
        f.close()

import glob
def getCarDataList():
    fList = glob.glob('data'+sep+'carMoving'+sep+'*')
    return fList

import pickle
def getCarObj(path):
    dataFile = file(path)
    obj = pickle.load(dataFile)
    return obj


def initRoadData():
    readAdj()
    readLukou()


def initSpeedData():
    readAvg_variance('avgSpeedValue',weekend_speed_avg_varivace_para,weekday_speed_avg_varivace_para)

def initTimeData():
    readAvg_variance('avgTimeValue', weekend_time_avg_varivace_para, weekday_time_avg_varivace_para)

def readAvg_variance(path, dict_weekend, dict_weekday):
    fList = glob.glob('data'+sep+path+sep+'*')
    for eachF in fList:
        basename = os.path.basename(eachF)
        timeInterval = basename.split('.csv')[0].split('_')[0]
        ifweekend1 = basename.split('.csv')[0].split('_')[1]
        f = open(eachF)
        dict_avg_one_time = {}
        for eachL in f:
            eachL = eachL.split('\n')[0]
            roadNo = (eachL.split(',')[1], eachL.split(',')[2])
            avgSpeed = float(eachL.split(',')[3])
            variance = float(eachL.split(',')[4])
            dict_avg_one_time.setdefault(roadNo, (avgSpeed, variance))
        if ifweekend1 == '1':
            dict_weekend.setdefault(timeInterval, dict_avg_one_time)
        else:
            dict_weekday.setdefault(timeInterval, dict_avg_one_time)



