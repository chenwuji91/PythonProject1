#-*- coding: UTF-8 -*-
'''
@author: chenwuji
本类为道路的基本类  保存道路相关的基本数据
'''


import tools

zuoshangjiao = 120.6354828592534, 31.376368052001823
zuoxiajiao = 120.63549057996597, 31.253756666173818
youshangjiao = 120.85634919819948, 31.376015656647887
youxiajiao = 120.85635657413037, 31.253404335545934

lukouDict = {}
roadAdjDict = {}
carDataDict = []
rootpath = '/Users/chenwuji/Documents/苏州出租车/'

def getRoadSpeedAvg(roadIntersection1, roadIntersection2, time1, ifweekend):#返回float类型
    pass

def getRoadSpeedVariance(roadIntersection1, roadIntersection2,time1, ifweekend):#返回float类型 方差
    pass

def getRoadTimeAvg(roadIntersection1, roadIntersection2, time1, ifweekend):
    pass

def getRoadTimeVariance(roadIntersection1, roadIntersection2, time1, ifweekend):
    pass

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
        f =open('data/intersection_newid')
        for eachline in f:
            list1 = eachline.split(',')
            lukouId = list1[0]
            position1 = list1[2]
            position2 = list1[3]
            lukouDict.setdefault(lukouId,RoadIntersectionPoint(float(position1),float(position2)))
        f.close()
def readAdj():
        f =open('data/roadnet_newid')
        for eachline in f:
            list1 = eachline.split(':')
            list2 = list1[1].split()
            roadAdjDict.setdefault(list1[0],list2)
        f.close()


def initRoadData():
    readAdj()
    readLukou()


def initSpeedData():
    pass

