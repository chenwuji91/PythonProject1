#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
import numpy as np
import sys
import glob
import os
#给出基站点周围所有道路上面的候选点
#基于基站半径范围300米的数据集  数据集表示了在基站半径范围内有多少的候选点
#目的就是找出所有候选点之间的关系  所有的基站点之间要两两迭代  这个计算量很大

cellIdDict={}
lukouDict={}
roadAdjDict={}
luceDict={}
houxuanPointDict={}
class JiZhanPoint:
    def __init__(self,x,y,range):
#         print 'NewObject'
        self.x = x
        self.y = y
        self.range = range
class RoadIntersectionPoint:
    def __init__(self,x,y):
#         print 'NewObject'
        self.x = x
        self.y = y
class HouxuanPoint:
    def __init__(self, x, y, roadIntersection1, roadIntersection2):
        self.x = x
        self.y = y
        self.roadIntersection1 = roadIntersection1
        self.roadIntersection2 = roadIntersection2
        self.voteCount = int(0)  # 获得的票数  票数是对象本身的属性
        self.voteDict = {}


class HouXuanPath:#注意这个类和上一个类会保存
    def __init__(self, path, length, dis_similarity,time, time_similarity, point1 ,point2):
        self.path = path  #List类型  保存的是从下一个行驶的路口到下下个点的路口中间的完整的路径
        self.length = length
        self.dis_similarity = dis_similarity
        self.time_similarity = time_similarity
        self.time = time
        self.similarity = dis_similarity * time_similarity
        self.point1 = point1  #父节点1  1默认为主节点
        self.point2 = point2    #父节点2
        self.dSimilarity = self.similarity
    def setDSimilarity(self,sim):
        self.dSimilarity = sim * 100  #人为的放大一个倍数
    def __cmp__(self, other):
        if self.dSimilarity > other.dSimilarity:
            return 1
        elif self.dSimilarity < other.dSimilarity:
            return -1
        else:
            return 0
def readcellIdSheet():
        f =open('/Users/chenwuji/Documents/RoadMatch/cellIdSheet.txt')
        for eachline in f:
            list1 = eachline.split('\t')
            cellId = list1[0]
            cellIdDict.setdefault(cellId,JiZhanPoint(float(list1[1]),float(list1[2]),float(list1[3])))
        f.close()
def readLukou():
        f =open('/Users/chenwuji/Documents/RoadMatch/lukou.txt')
        for eachline in f:
            list1 = eachline.split()
            cellId = list1[0]
            position = list1[1].split(",")
            lukouDict.setdefault(cellId,RoadIntersectionPoint(float(position[0]),float(position[1])))
        f.close()
def readAdj():
        f =open('/Users/chenwuji/Documents/RoadMatch/adj.txt')
        for eachline in f:
            list1 = eachline.split()
            roadAdjDict.setdefault(list1[0],list1[1:len(list1)])
        f.close()
def readLuce():
    dir = '/Users/chenwuji/Documents/RoadMatch/szfOut04144WithDate/'  # 要访问文件夹路径
    f = glob.glob(dir + '//*')
    for file in f:
        filename = os.path.basename(file)
        # print filename
        f = open(dir + '//' + filename, 'r')
        for eachline in f:
            # print eachline,  # 后面跟 ',' 将忽略换行符
            # print eachline.__len__()
            list1 = eachline[1:(eachline.__len__()-2)]
            # print list1
            list1 = list1.split(',CompactBuffer')
            date = list1[0]
            xulie = list1[1]
            # print xulie
            list2 = xulie[1:(xulie.__len__()-1)].split(', ')
            # print list2
            listPoint = []
            for singleP in list2:
                singleP = singleP[1:(len(singleP) - 1)]
                list1 = singleP.split(",")
                # print list1[0]#候选点1 基站
                # print list1[1]#候选点2 时间
                listPoint.append((list1[0], list1[1]))  # 将序列点变成元组的形式
                # 在下面进行单个序列的最佳相似度的求解#
            luceDict.setdefault(date,listPoint)
        f.close()
   # pass
def readHouXuanPoint():
    f = open('/Users/chenwuji/Documents/RoadMatch/HouXuanPointDis300MoreMeters.txt')
    for eachline in f:
        list1 = eachline.split(':')
        point0 = list1[0]
        pointn = list1[1]
        list2 = pointn[0:(pointn.__len__()-1)].split(';')
        list3 = []
        for eachHouxuan in list2:
            list4 = eachHouxuan[1:(eachHouxuan.__len__()-1)].split(',')
            # print list4
            if list4.__len__()>1:
                list3.append(HouxuanPoint(float(list4[0]),float(list4[1]),list4[2],list4[3]))
        houxuanPointDict.setdefault(point0,list3)
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
def disSimilarity(point1,point2, G): #传入的是两个点的信息 以及两个实际点之间的距离 点的定义如上个HouxuanPoint类所示  返回的是距离的相似度的值(以及当前相似度下面的道路路径)  相似度的值计算需要两个点的直线距离 以及点在道路上面的最短距离
    def currentPointToNeighbourDis(point,neighbourIndex):  #当前点的信息  返回到邻居的距离 传入参数为1或者2  1为第一个邻居 2为第二个邻居
        if neighbourIndex == 1:
            neighbourC = lukouDict.get(point.roadIntersection1)
            # point1_neighbour1_dis = calculate(point.x, point.y, neighbourC.x, neighbourC.y)  # 获得当前点到第一个邻居的距离
        elif neighbourIndex == 2:
            neighbourC = lukouDict.get(point.roadIntersection2)
            # point1_neighbour2_dis = calculate(point1.x, point1.y, neighbour2.x, neighbour2.y)  # 获得当前点到第二个邻居的距离
        # else:
        #     return null
        return  calculate(point.x, point.y, neighbourC.x, neighbourC.y)

    def calSimilarity(shijiP ,HouxuanP ):
        value1 = 1 - abs(shijiP-HouxuanP)/shijiP
        # print value1
        return max(0,value1)
    point11_21_length = nearestPathLen(point1.roadIntersection1,point2.roadIntersection1,G)
    point11_22_length = nearestPathLen(point1.roadIntersection1, point2.roadIntersection2, G)
    point12_21_length = nearestPathLen(point1.roadIntersection2, point2.roadIntersection1, G)
    point12_22_length = nearestPathLen(point1.roadIntersection2, point2.roadIntersection2, G)

    point11_21_length += (currentPointToNeighbourDis(point1,1)+currentPointToNeighbourDis(point2,1))
    point11_22_length += (currentPointToNeighbourDis(point1,1)+currentPointToNeighbourDis(point2,2))
    point12_21_length += (currentPointToNeighbourDis(point1,2)+currentPointToNeighbourDis(point2,1))
    point12_22_length += (currentPointToNeighbourDis(point1,2)+currentPointToNeighbourDis(point2,2))

    list1 = [point11_21_length,point11_22_length,point12_21_length,point12_22_length]

    # print list1

    index_min = list1.index(min(list1))
    return list1[index_min]



def everyJizhanDis():
    readHouXuanPoint()
    G = graphGenerate()
    for eachP1 in cellIdDict:
        for eachP2 in cellIdDict:
            PPDis = []
            houxuan1 = houxuanPointDict.get(eachP1)
            houxuan2 = houxuanPointDict.get(eachP2)
            for eachP1_1 in houxuan1:
                for eachP2_2 in houxuan2:
                    dis = disSimilarity(eachP1_1, eachP2_2, G)
                    PPDis.append(dis)
            currentMin = min(PPDis)
            print str(eachP1) + ' ' + str(eachP2) + ':' + currentMin





if __name__ == '__main__':
     # 基本数据加载
     readLuce()
     readcellIdSheet()
     readLukou()
     readAdj()
     everyJizhanDis()







