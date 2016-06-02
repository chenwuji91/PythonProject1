#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
import constant
lukouDict = {}
lukouCache = {}
cellIdDict={}
roadAdjDict={}
luceDict={}
houxuanPointDict={}
rootDir = constant.rootPath

import glob
import os
class JiZhanPoint:
    def __init__(self,x,y,range):
        self.x = x
        self.y = y
        self.range = range
class RoadIntersectionPoint:
    def __init__(self,x,y):
        self.x = x
        self.y = y
class HouxuanPoint:
    def __init__(self, x, y, roadIntersection1, roadIntersection2):
        self.x = x
        self.y = y
        self.roadIntersection1 = roadIntersection1
        self.roadIntersection2 = roadIntersection2


from math import radians, cos, sin, asin, sqrt
def calculate(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000




def readLukou():
    f = open(rootDir + constant.lukouInfo)
    for eachline in f:
        list1 = eachline.split()
        cellId = list1[0]
        position = list1[1].split(",")
        lukouDict.setdefault(cellId, RoadIntersectionPoint(float(position[0]), float(position[1])))
    f.close()


def readAdj():
    f = open(rootDir + constant.adjInfo)
    for eachline in f:
        list1 = eachline.split()
        roadAdjDict.setdefault(list1[0], list1[1:len(list1)])
    f.close()





def readRoadIntersectionCacheFromTxt():
    f = open(rootDir + constant.roadIntersectionDisCache)
    for eachLine in f:
        eachLine = eachLine.split('\n')[0]
        list1 = eachLine.split(';')
        road1 = list1[0]
        road2 = list1[1]
        dis = float(list1[2])
        roadL = list1[3][2:len(list1[3]) - 2].split('\', \'')
        lukouCache.setdefault((road1, road2), (dis, roadL))

def nearestPath(point1, point2, G):
    if lukouCache.__contains__((point1,point2)):
        return lukouCache.get((point1, point2))[1]
    elif lukouCache.__contains__((point2, point1)):
        return lukouCache.get((point2, point1))[1]
    else:
        return []


def nearestPathLen(point1, point2, G):
    if lukouCache.__contains__((point1,point2)):
        return lukouCache.get((point1, point2))[0]
    elif lukouCache.__contains__((point2, point1)):
        return lukouCache.get((point2, point1))[0]
    else:
        return 10000
def init():
    readRoadIntersectionCacheFromTxt()
    readLukou()
    readAdj()


class NearestPathInfo:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.calculateShortest()



    def currentPointToNeighbourDis(point, neighbourIndex):  # 当前点的信息  返回到邻居的距离 传入参数为1或者2  1为第一个邻居 2为第二个邻居
        if neighbourIndex == 1:
            neighbourC = lukouDict.get(point.roadIntersection1)
            # 获得当前点到第一个邻居的距离
        elif neighbourIndex == 2:
            neighbourC = lukouDict.get(point.roadIntersection2)
            # 获得当前点到第二个邻居的距离
        return calculate(point.x, point.y, neighbourC.x, neighbourC.y)

    def calculateShortest(self):
        minP1 = min(self.point1.roadIntersection1, self.point1.roadIntersection2)
        minP2 = min(self.point2.roadIntersection1, self.point2.roadIntersection2)
        maxP1 = max(self.point1.roadIntersection1, self.point1.roadIntersection2)
        maxP2 = max(self.point2.roadIntersection1, self.point2.roadIntersection2)
        if minP1 == minP2 and maxP1 == maxP2:
            self.sameRoad()
        else:
            self.diffRoad()

    def sameRoad(self):
        self.nearestPath = []
        self.nearestPathLen = calculate(self.point1.x, self.point1.y, self.point2.x, self.point2.y)

    def diffRoad(self):
        self.point11_21_length = nearestPathLen(self.point1.roadIntersection1, self.point2.roadIntersection1, self.G)
        self.point11_22_length = nearestPathLen(self.point1.roadIntersection1, self.point2.roadIntersection2, self.G)
        self.point12_21_length = nearestPathLen(self.point1.roadIntersection2, self.point2.roadIntersection1, self.G)
        self.point12_22_length = nearestPathLen(self.point1.roadIntersection2, self.point2.roadIntersection2, self.G)

        self.point11_21_length += (
        self.currentPointToNeighbourDis(self.point1, 1) + self.currentPointToNeighbourDis(self.point2, 1))
        self.point11_22_length += (
        self.currentPointToNeighbourDis(self.point1, 1) + self.currentPointToNeighbourDis(self.point2, 2))
        self.point12_21_length += (
        self.currentPointToNeighbourDis(self.point1, 2) + self.currentPointToNeighbourDis(self.point2, 1))
        self.point12_22_length += (
        self.currentPointToNeighbourDis(self.point1, 2) + self.currentPointToNeighbourDis(self.point2, 2))
        self.list1 = [self.point11_21_length, self.point11_22_length, self.point12_21_length, self.point12_22_length]
        self.index_min = self.list1.index(min(self.list1))

        if self.index_min == 0:
            self.nearestPath = nearestPath(self.point1.roadIntersection1, self.point2.roadIntersection1, self.G)
            self.nearestPathLen = self.point11_21_length
        if self.index_min == 1:
            self.nearestPath = nearestPath(self.point1.roadIntersection1, self.point2.roadIntersection2, self.G)
            self.nearestPathLen = self.point11_22_length
        if self.index_min == 2:
            self.nearestPath = nearestPath(self.point1.roadIntersection2, self.point2.roadIntersection1, self.G)
            self.nearestPathLen = self.point12_21_length
        if self.index_min == 3:
            self.nearestPath = nearestPath(self.point1.roadIntersection2, self.point2.roadIntersection2, self.G)
            self.nearestPathLen = self.point12_22_length
