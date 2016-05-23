#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
import sys
import glob
import os
#传入两个点  计算时间和空间相似度
rootPath = '/Users/chenwuji/Documents/RoadMatch/'
# rootPath = '~/PythonScript/data/'
lukouDict={}
roadAdjDict={}

cellNearestDisDict = {}

class RoadIntersectionPoint:
    def __init__(self,x,y):
#         print 'NewObject'
        self.x = x
        self.y = y



def readLukou():
        f =open(rootPath + 'lukou.txt')
        for eachline in f:
            list1 = eachline.split()
            cellId = list1[0]
            position = list1[1].split(",")
            lukouDict.setdefault(cellId,RoadIntersectionPoint(float(position[0]),float(position[1])))
        f.close()
def readAdj():
        f =open(rootPath + 'adj.txt')
        for eachline in f:
            list1 = eachline.split()
            roadAdjDict.setdefault(list1[0],list1[1:len(list1)])
        f.close()

import pickle as p
def loadDict():

    dataFileP = rootPath + 'cellCloestRoad2.data'
    dataFile = file(dataFileP)
    global cellNearestDisDict
    cellNearestDisDict = p.load(dataFile)


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

import networkx as nx
def graphGenerate():
    G = nx.DiGraph()
    for eachPointPair in roadAdjDict:
        for anotherPoint in roadAdjDict.get(eachPointPair):
            point1 = lukouDict.get(eachPointPair)
            point2 = lukouDict.get(anotherPoint)
            x1 = point1.x
            y1 = point1.y
            x2 = point2.x
            y2 = point2.y
            dis = calculate(x1,y1,x2,y2)
            G.add_edge(eachPointPair,anotherPoint,weight = dis)
    print "有向带权图加载完成"
    return G
def nearestPath(point1,point2, G):
    return nx.dijkstra_path(G, point1 , point2)
def nearestPathLen(point1,point2, G):
    return nx.dijkstra_path_length(G, point1, point2)
#传入的参数类型  point1 point2 类型为HouxuanPoint 类型 为真实点的候选点  distance为真实点之间的距离  time_point为时间差  volicity为内置的速度值

def generateNearestCellDis():
    G = graphGenerate()
    for eachP1 in cellNearestDisDict:
        for eachP2 in cellNearestDisDict:
            eachV1 = cellNearestDisDict.get(eachP1)
            eachV2 = cellNearestDisDict.get(eachP2)
            try:
                pToRoadDis = eachV1[0] + eachV2[0]
                dis1 = nearestPathLen(eachV1[1][0], eachV2[1][0],G)
                dis2 = nearestPathLen(eachV1[1][0], eachV2[1][1],G)
                dis3 = nearestPathLen(eachV1[1][1], eachV2[1][0],G)
                dis4 = nearestPathLen(eachV1[1][1], eachV2[1][1],G)
                disAll = min(dis1,dis2,dis3,dis4) + pToRoadDis
                writeToFile(rootPath + 'cellDisTable.txt',eachP1 + ',' + eachP2+',' + str(disAll))
            except:
                print 'CurrentPoint:',
                print eachP1,
                print ',',
                print eachP2,
                print ',',
                print type(eachV1),
                print ',',
                print type(eachV2)




def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()



if __name__ == '__main__':
     # 基本数据加载

     readLukou()
     readAdj()
     loadDict()
     generateNearestCellDis()







