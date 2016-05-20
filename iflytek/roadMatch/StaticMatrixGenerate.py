#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
import numpy as np
import sys
import glob
import os
#传入两个点  计算时间和空间相似度
pathdate = '20160823'
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
    # def increaseVote(self,index1):
    #     self.voteCount = self.voteCount + 1
    def getVote(self,index1):
        return self.voteDict.get(index1)
    def increaseVote(self,index1):#这个在增加的时候需要增加索引 这个设定是为了防止一条序列里面可能出现相同的两个序列 造成值引用的异常
        if (self.voteDict.__contains__(index1)):
            current = self.voteDict.get(index1)
            self.voteDict.update({index1: current + 1})
        else:
            self.voteDict.setdefault(index1, 1)

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
    def vote(self,matrixCount):
        self.point1.increaseVote(matrixCount)
    def voteTwo(self,matrixCount):

        self.point2.increaseVote(matrixCount)  #当是矩阵中最后一个节点的时候 需要调用这个方法增加票数

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
def disSimilarity(point1,point2,distance,G, time_point, volicity): #传入的是两个点的信息 以及两个实际点之间的距离 点的定义如上个HouxuanPoint类所示  返回的是距离的相似度的值(以及当前相似度下面的道路路径)  相似度的值计算需要两个点的直线距离 以及点在道路上面的最短距离
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
    def timeSimilarity(volicity, road_distance):
        return road_distance/volicity

    def calSimilarity(shijiP ,HouxuanP ):
        value1 = 1 - abs(shijiP-HouxuanP)/shijiP
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


    if index_min == 0:
        time1 = timeSimilarity(volicity,point11_21_length)
        shortestPath = HouXuanPath(nearestPath(point1.roadIntersection1,point2.roadIntersection1, G),
                                   point11_21_length,calSimilarity(distance,point11_21_length),time1,calSimilarity(time_point,time1),point1 ,point2)
    if index_min == 1:
        time2 = timeSimilarity(volicity, point11_22_length)
        shortestPath = HouXuanPath(nearestPath(point1.roadIntersection1, point2.roadIntersection2, G),
                                   point11_22_length,calSimilarity(distance,point11_22_length),time2,calSimilarity(time_point,time2),point1 ,point2)
    if index_min == 2:
        time3 = timeSimilarity(volicity, point12_21_length)
        shortestPath = HouXuanPath(nearestPath(point1.roadIntersection2, point2.roadIntersection1, G),
                                   point12_21_length,calSimilarity(distance,point12_21_length),time3,calSimilarity(time_point,time3),point1 ,point2)
    if index_min == 3:
        time4 = timeSimilarity(volicity, point12_22_length)
        shortestPath = HouXuanPath(nearestPath(point1.roadIntersection2, point2.roadIntersection2, G),
                                   point12_22_length,calSimilarity(distance,point12_22_length),time4,calSimilarity(time_point,time4),point1 ,point2)
    return shortestPath  #返回的是一个类  包含节点中间最短路径 以及该候选路径的相似度
def roadMatch():
    def timetranslate(HouxuanTime):
        # print '时间转换测试'

        sss = int(HouxuanTime[len(HouxuanTime) - 2:len(HouxuanTime)])
        mmm = int(HouxuanTime[len(HouxuanTime) - 4:len(HouxuanTime) - 2])
        hhh = int(HouxuanTime[len(HouxuanTime) - 6:len(HouxuanTime) - 4])
        return sss + mmm * 60 + hhh * 3600
    #每一条序列需要重新加载候选点的信息  因为引用改变值的问题
    readHouXuanPoint()
    trace = luceDict.get(pathdate)  # 开始进行一条移动序列的匹配工作  这个移动序列可以看成是有序的
    G = graphGenerate()
    print trace   #开始处理一条轨迹
    smallMatrix = []  # 数组的最外层  即该维度表示的是是第几个小数组    索引为0到len(trace)-1的索引  表示的是两个实际点之间的小矩阵的复杂关系    最后这个smallMatrix保存饿的是这个整个序列的全局矩阵
    for pointPair in range(len(trace)-1):  #对于一个点而言
        Houxuan1List = houxuanPointDict.get(trace[pointPair][0])  #当前的点的所有候选点集  trace保存的是一个元组  [0]号下标表示基站点信息  [1]号下标表示时间戳
        Houxuan2List = houxuanPointDict.get(trace[pointPair+1][0])  #下一个点所有的候选点集
        point1 = cellIdDict.get(trace[pointPair][0])  #point1代表点的详细信息 HouxuanPoint的点的详细信息  类型为JiZhanPoint
        point2 = cellIdDict.get(trace[pointPair+1][0])  #point点的详细信息
        try:
            point12Dis = calculate(point1.x, point1.y, point2.x, point2.y)  #两个点的实际距离
        except:
            print point1
            print point2
        timeHouxuan1 = timetranslate(trace[pointPair][1])
        timeHouxuan2 = timetranslate(trace[pointPair+1][1])
        time12 = timeHouxuan2 - timeHouxuan1  #两个点的时间差
        rSimilarity = 0  #当前下面最大的静态相似度
        rPath = []  #当前静态相似度的中间路径
        point1Matrix = []  # 和第pointPair个实际点的第i个候选点相关的 所有候选点之间的关系
        for i in range(len(Houxuan1List)):              # for eachPoint1 in Houxuan1List:
            eachPoint1 = Houxuan1List[i]
            point2Matrix = []  #和第pointPair个实际点的第i个候选点相关的 第j个点 之间的关系    对于HouxuanList可以认为每个基站点的候选点是唯一的  但是 如果一段移动序列出现两个连续的基站 这个基站会获得重复的票数叠加
            for j in range(len(Houxuan2List)):    #for eachPoint2 in Houxuan2List:
                eachPoint2 = Houxuan2List[j]
                sPath = disSimilarity(eachPoint1, eachPoint2, point12Dis, G, time12, 12)   #传入的是两个原始点的两个候选点 返回的可以看作是一条边  保存的是两个点之间的关系
                point2Matrix.append(sPath)
                if(sPath.dis_similarity*sPath.time_similarity > rSimilarity):
                    rSimilarity = sPath.dis_similarity*sPath.time_similarity
                    rPath = sPath.path

            point1Matrix.append(point2Matrix)
        # print '__________________最佳相似路径_________________________'
        # print rPath
        smallMatrix.append(point1Matrix)
        print '中间的结果是'
        for i in range(len(Houxuan1List)):
            for j in range(len(Houxuan2List)):
                print str(i)+"  "+ str(j)+"  "+str(point1Matrix[i][j].dSimilarity)
        # smallMatrixToFile('20160816', smallMatrix)  # 保存矩阵的文件
        # smallMatrixToFileWithPickle('20160816', smallMatrix)  # 保存矩阵的文件
    print '最终的结果是'
    # smallMatrixToFile('20160816',smallMatrix)#保存矩阵的文件
    for s in range(len(smallMatrix)):  #(len(trace)-1):
        for i in range(len(smallMatrix[s])): #(len(Houxuan1List)):#smallMatrix[s]
            for j in range(len(smallMatrix[s][i])): #(len(Houxuan2List)):
                print str(i)+"  "+ str(j)+"  "+str(smallMatrix[s][i][j].dSimilarity)
    smallMatrixToFile(pathdate, smallMatrix)  # 保存矩阵的文件
    smallMatrixToFileWithPickle(pathdate, smallMatrix)  # 保存矩阵的文件

    #下面开始动态矩阵和投票系统  在动态矩阵部分处理剩下的内容   本程序重构之后只负责将当前路径的静态矩阵内容存储
    # for vetoCycle in len(trace):   #对每一轮进行一个投票
    #     vote(smallMatrix,trace,vetoCycle)   #开始对所有的点进行加权  trace是一个元组  smallMatrix表示图的边  保存的有HouXuanPath的相关信息
    # BestPath = generateBestPath(smallMatrix,trace)
    # print '最佳路径是'+ str(BestPath)

#这个函数是整个程序的最后一个步骤  统计当前轨迹所有的票数 恢复出用户实际经过的所有的点   输入参数 smallMatrix的点   输出参数 轨迹[]  初期考虑输出的就是List的集合的叠加  表示出来一条完整的轨迹
def smallMatrixToFile(filename, smallMatrix):
    rootpath = '/Users/chenwuji/Documents/RoadMatch/staticMatrix/'
    f = file(rootpath + filename + '.txt', "a+")
    for s in range(len(smallMatrix)):  # (len(trace)-1):
        for i in range(len(smallMatrix[s])):  # (len(Houxuan1List)):#smallMatrix[s]
            for j in range(len(smallMatrix[s][i])):  # (len(Houxuan2List)):
                print str(s) + ";" + str(i) + ";" + str(j) + ";" + str(smallMatrix[s][i][j].path) + ';' + \
                      str(smallMatrix[s][i][j].length) + ';' + str(smallMatrix[s][i][j].dis_similarity) + ';' + str(
                    smallMatrix[s][i][j].time_similarity) + ';' + \
                      str(smallMatrix[s][i][j].time) + ';' + str(smallMatrix[s][i][j].similarity) + ';' + \
                      str(str(smallMatrix[s][i][j].point1.x) + ',' + str(smallMatrix[s][i][j].point1.y) + ',' + str(
                          smallMatrix[s][i][j].point1.roadIntersection1) + ',' + str(
                          smallMatrix[s][i][j].point1.roadIntersection2)) + ';' + \
                      str(str(smallMatrix[s][i][j].point2.x) + ',' + str(smallMatrix[s][i][j].point2.y) + ',' + str(
                          smallMatrix[s][i][j].point2.roadIntersection1) + ',' + str(
                          smallMatrix[s][i][j].point2.roadIntersection2)) + ';'
                f.writelines(str(s) + ";" + str(i) + ";" + str(j) + ";" + str(smallMatrix[s][i][j].path)+';'+ \
                      str(smallMatrix[s][i][j].length) +';' + str(smallMatrix[s][i][j].dis_similarity)+';'+ str(smallMatrix[s][i][j].time_similarity)+';'+ \
                      str(smallMatrix[s][i][j].time)+ ';' +str(smallMatrix[s][i][j].similarity)+ ';'+\
                      str(str(smallMatrix[s][i][j].point1.x) + ',' + str(smallMatrix[s][i][j].point1.y) + ',' + str(smallMatrix[s][i][j].point1.roadIntersection1) + ',' + str(smallMatrix[s][i][j].point1.roadIntersection2)) + ';'+ \
                      str(str(smallMatrix[s][i][j].point2.x) + ',' + str(smallMatrix[s][i][j].point2.y) + ',' + str(smallMatrix[s][i][j].point2.roadIntersection1) + ',' + str(smallMatrix[s][i][j].point2.roadIntersection2)) + ';')
                f.writelines("\n")
    f.close()

import pickle as p
def smallMatrixToFileWithPickle(filename, smallMatrix):
    rootpath = '/Users/chenwuji/Documents/RoadMatch/staticMatrix/'
    f = file(rootpath + filename + '.data', "w")
    p.dump(smallMatrix,f)
    f.close()


if __name__ == '__main__':
     # 基本数据加载
     readLuce()
     readcellIdSheet()
     readLukou()
     readAdj()
     roadMatch()






