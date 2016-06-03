#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''

import glob
import os
import pickle
import constant
import math
#传入两个点  计算时间和空间相似度
rootDir = constant.rootPath
cellIdDict={}
lukouDict={}
roadAdjDict={}
# luceDict={}
houxuanPointDict={}
lukouCache = {}

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
    def setDisToJizhan(self, JizhanPoint):
        self.distanceToJizhan = calculate(self.x, self.y, JizhanPoint.x, JizhanPoint.y)
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
        self.dSimilarity = sim * 10000  #人为的放大一个倍数
    def __cmp__(self, other):
        if self.dSimilarity > other.dSimilarity:
            return 1
        elif self.dSimilarity < other.dSimilarity:
            return -1
        else:
            return 0
def readcellIdSheet():
        f =open(rootDir + constant.cellIDSheet)
        for eachline in f:
            list1 = eachline.split('\t')
            cellId = list1[0]
            cellIdDict.setdefault(cellId,JiZhanPoint(float(list1[1]),float(list1[2]),float(list1[3])))
        f.close()
def readLukou():
        f =open(rootDir + constant.lukouInfo)
        for eachline in f:
            list1 = eachline.split()
            cellId = list1[0]
            position = list1[1].split(",")
            lukouDict.setdefault(cellId,RoadIntersectionPoint(float(position[0]),float(position[1])))
        f.close()
def readAdj():
        f =open(rootDir + constant.adjInfo)
        for eachline in f:
            list1 = eachline.split()
            roadAdjDict.setdefault(list1[0],list1[1:len(list1)])
        f.close()
def readLuce():
    dir = rootDir + constant.luceProcessed # 要访问文件夹路径
    f = glob.glob(dir + '//*')
    for file in f:
        filename = os.path.basename(file)
        # print filename
        f = open(dir + '//' + filename, 'r')
        for eachline in f:
            list1 = eachline[1:(eachline.__len__()-2)]
            list1 = list1.split(',CompactBuffer')
            date = list1[0]
            xulie = list1[1]
            list2 = xulie[1:(xulie.__len__()-1)].split(', ')
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
def readLuceYuanshi():
    # dataFile = file(rootDir+'MovingSeq/szf.data')
    dataFile = file(rootDir+ constant.luceYuanshi)
    global luceDict
    luceDict = pickle.load(dataFile)
def readHouXuanPoint():
    f = open(rootDir + constant.houxuanPointPath)
    for eachline in f:
        list1 = eachline.split(':')
        point0 = list1[0]
        pointn = list1[1]
        list2 = pointn[0:(pointn.__len__()-1)].split(';')
        list3 = []
        for eachHouxuan in list2:
            list4 = eachHouxuan[1:(eachHouxuan.__len__()-1)].split(',')
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
# def readRoadIntersectionCache():
#     dataFile1 = file(rootDir+'LukouDisStatic.data','r')
#     global lukouCache
#     lukouCache = pickle.load(dataFile1)
#     print 'finish'
def readRoadIntersectionCacheFromTxt():
    f = open(rootDir + constant.roadIntersectionDisCache)
    for eachLine in f:
        eachLine = eachLine.split('\n')[0]
        list1 = eachLine.split(';')
        road1 = list1[0]
        road2 = list1[1]
        dis = float(list1[2])
        roadL = list1[3][2:len(list1[3])-2].split('\', \'')
        lukouCache.setdefault((road1,road2),(dis,roadL))
    print len(lukouCache)
    pass
def nearestPath(point1, point2, G):
    if lukouCache.__contains__((point1,point2)):
        return lukouCache.get((point1, point2))[1]
    elif lukouCache.__contains__((point2, point1)):
        return lukouCache.get((point2, point1))[1]
    else:
        print "Call External Dijkstra"
        return nearestPathWithDijkstra(point1, point2, G)
def nearestPathLen(point1, point2, G):
    if lukouCache.__contains__((point1,point2)):
        return lukouCache.get((point1, point2))[0]
    elif lukouCache.__contains__((point2, point1)):
        return lukouCache.get((point2, point1))[0]
    else:
        # print "Call External Dijkstra"
        return nearestPathLenWithDijkstra(point1, point2, G)
def nearestPathWithDijkstra(point1,point2, G):
    return nx.dijkstra_path(G, point1 , point2)
def nearestPathLenWithDijkstra(point1,point2, G):
    return nx.dijkstra_path_length(G, point1, point2)




import tools
#传入的参数类型  point1 point2 类型为HouxuanPoint 类型 为 候选点  distance为真实点之间的距离  time_point为时间差  volicity为内置的速度值
def disSimilarity(point1,point2,distance,G, time_point, volicity): #传入的是两个点的信息 以及两个实际点之间的距离 点的定义如上个HouxuanPoint类所示  返回的是距离的相似度的值(以及当前相似度下面的道路路径)  相似度的值计算需要两个点的直线距离 以及点在道路上面的最短距离

    def currentPointToNeighbourDis(point,neighbourIndex):  #当前点的信息  返回到邻居的距离 传入参数为1或者2  1为第一个邻居 2为第二个邻居
        if neighbourIndex == 1:
            neighbourC = lukouDict.get(point.roadIntersection1)
            # 获得当前点到第一个邻居的距离
        elif neighbourIndex == 2:
            neighbourC = lukouDict.get(point.roadIntersection2)
            # 获得当前点到第二个邻居的距离
        return  calculate(point.x, point.y, neighbourC.x, neighbourC.y)

    def timeSimilarity(volicity, road_distance):
        return road_distance/volicity

    def calSimilarity(shijiP ,HouxuanP ):
        value1 = 1 - abs(shijiP-HouxuanP)/(shijiP+0.0000001)
        return max(0,value1)

    def spaceSimilarityNew(point1,point2):
        p2pDis = calculate(point1.x, point1.y, point2.x, point2.y)
        p2ToJizhanDis = point2.distanceToJizhan
        return math.exp(-p2pDis * 0.1) + 1/math.log10(p2ToJizhanDis)



    class NearestPathInfo:
        def __init__(self, point1, point2, G):
            self.point1 = point1
            self.point2 = point2
            self.G = G
            self.calculateShortest()

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
            self.nearestPathLen = calculate(self.point1.x,self.point1.y,self.point2.x,self.point2.y)

        def diffRoad(self):
            self.point11_21_length = nearestPathLen(self.point1.roadIntersection1, self.point2.roadIntersection1, self.G)
            self.point11_22_length = nearestPathLen(self.point1.roadIntersection1, self.point2.roadIntersection2, self.G)
            self.point12_21_length = nearestPathLen(self.point1.roadIntersection2, self.point2.roadIntersection1, self.G)
            self.point12_22_length = nearestPathLen(self.point1.roadIntersection2, self.point2.roadIntersection2, self.G)

            self.point11_21_length += (currentPointToNeighbourDis(self.point1, 1) + currentPointToNeighbourDis(self.point2, 1))
            self.point11_22_length += (currentPointToNeighbourDis(self.point1, 1) + currentPointToNeighbourDis(self.point2, 2))
            self.point12_21_length += (currentPointToNeighbourDis(self.point1, 2) + currentPointToNeighbourDis(self.point2, 1))
            self.point12_22_length += (currentPointToNeighbourDis(self.point1, 2) + currentPointToNeighbourDis(self.point2, 2))
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

    nf = NearestPathInfo(point1, point2, G)
    # print nf.nearestPathLen
    # print nf.nearestPath
    len1 = nf.nearestPathLen
    time1 = timeSimilarity(volicity,len1)
    # shortestPath = HouXuanPath(nf.nearestPath,len1 ,空间近似度  ,time1,时间近似度  ,point1 ,point2)
    shortestPath = HouXuanPath(nf.nearestPath, len1, spaceSimilarityNew(point1, point2), time1, 1, point1, point2)

    # (self, path, length, dis_similarity, time, time_similarity, point1, point2):
    return shortestPath  #返回的是一个类  包含节点中间最短路径 以及该候选路径的相似度
def roadMatch(pathdate):
    def timetranslate(HouxuanTime):
        sss = int(HouxuanTime[len(HouxuanTime) - 2:len(HouxuanTime)])
        mmm = int(HouxuanTime[len(HouxuanTime) - 4:len(HouxuanTime) - 2])
        hhh = int(HouxuanTime[len(HouxuanTime) - 6:len(HouxuanTime) - 4])
        return sss + mmm * 60 + hhh * 3600
    trace2 = luceDict.get(pathdate)  # 开始进行一条移动序列的匹配工作  这个移动序列可以看成是有序的
    trace = tools.traceLegalCheck(trace2,cellIdDict,JiZhanPoint,houxuanPointDict)
    G = graphGenerate()
    print trace   #开始处理一条轨迹
    smallMatrix = []  # 数组的最外层  即该维度表示的是是第几个小数组    索引为0到len(trace)-1的索引  表示的是两个实际点之间的小矩阵的复杂关系    最后这个smallMatrix保存饿的是这个整个序列的全局矩阵
    for pointPair in range(len(trace)-1):  #对于一个点而言
        Houxuan1List = houxuanPointDict.get(trace[pointPair][0])  #当前的点的所有候选点集  trace保存的是一个元组  [0]号下标表示基站点信息  [1]号下标表示时间戳
        Houxuan2List = houxuanPointDict.get(trace[pointPair+1][0])  #下一个点所有的候选点集
        point1 = cellIdDict.get(trace[pointPair][0])  #point1代表点的详细信息 HouxuanPoint的点的详细信息  类型为JiZhanPoint
        point2 = cellIdDict.get(trace[pointPair+1][0])  #point点的详细信息

        point12Dis = calculate(point1.x, point1.y, point2.x, point2.y)  #两个点的实际距离
        timeHouxuan1 = timetranslate(trace[pointPair][1])
        timeHouxuan2 = timetranslate(trace[pointPair+1][1])
        time12 = timeHouxuan2 - timeHouxuan1  #两个点的时间差

        point1Matrix = []  # 和第pointPair个实际点的第i个候选点相关的 所有候选点之间的关系
        for i in range(len(Houxuan1List)):              # for eachPoint1 in Houxuan1List:
            eachPoint1 = Houxuan1List[i]
            eachPoint1.setDisToJizhan(cellIdDict.get(trace[pointPair][0]))  #设置点到基站的距离字段
            point2Matrix = []  #和第pointPair个实际点的第i个候选点相关的 第j个点 之间的关系    对于HouxuanList可以认为每个基站点的候选点是唯一的  但是 如果一段移动序列出现两个连续的基站 这个基站会获得重复的票数叠加
            for j in range(len(Houxuan2List)):    #for eachPoint2 in Houxuan2List:
                eachPoint2 = Houxuan2List[j]
                eachPoint2.setDisToJizhan(cellIdDict.get(trace[pointPair+1][0]))  #设置点到基站的距离字段
                sPath = disSimilarity(eachPoint1, eachPoint2, point12Dis, G, time12, 12)   #传入的是两个原始点的两个候选点 返回的可以看作是一条边  保存的是两个点之间的关系
                point2Matrix.append(sPath)
            point1Matrix.append(point2Matrix)
        smallMatrix.append(point1Matrix)

        # print '中间的结果是'20202037
        # for i in range(len(Houxuan1List)):
        #     for j in range(len(Houxuan2List)):
        #         print str(i)+"  "+ str(j)+"  "+str(point1Matrix[i][j].dSimilarity)
    smallMatrixToFile(pathdate, smallMatrix)  # 保存矩阵的文件
    smallMatrixToFileWithPickle(pathdate, smallMatrix)  # 保存矩阵的文件

#这个函数是整个程序的最后一个步骤  统计当前轨迹所有的票数 恢复出用户实际经过的所有的点   输入参数 smallMatrix的点   输出参数 轨迹[]  初期考虑输出的就是List的集合的叠加  表示出来一条完整的轨迹
def smallMatrixToFile(filename, smallMatrix):
    rootpath = rootDir+ constant.staticMatrixOutPath
    f = file(rootpath + filename + '.txt', "a+")
    for s in range(len(smallMatrix)):  # (len(trace)-1):
        for i in range(len(smallMatrix[s])):  # (len(Houxuan1List)):#smallMatrix[s]
            for j in range(len(smallMatrix[s][i])):  # (len(Houxuan2List)):
                # print str(s) + ";" + str(i) + ";" + str(j) + ";" + str(smallMatrix[s][i][j].path) + ';' + \
                #       str(smallMatrix[s][i][j].length) + ';' + str(smallMatrix[s][i][j].dis_similarity) + ';' + str(
                #     smallMatrix[s][i][j].time_similarity) + ';' + \
                #       str(smallMatrix[s][i][j].time) + ';' + str(smallMatrix[s][i][j].similarity) + ';' + \
                #       str(str(smallMatrix[s][i][j].point1.x) + ',' + str(smallMatrix[s][i][j].point1.y) + ',' + str(
                #           smallMatrix[s][i][j].point1.roadIntersection1) + ',' + str(
                #           smallMatrix[s][i][j].point1.roadIntersection2)) + ';' + \
                #       str(str(smallMatrix[s][i][j].point2.x) + ',' + str(smallMatrix[s][i][j].point2.y) + ',' + str(
                #           smallMatrix[s][i][j].point2.roadIntersection1) + ',' + str(
                #           smallMatrix[s][i][j].point2.roadIntersection2)) + ';'
                f.writelines(str(s) + ";" + str(i) + ";" + str(j) + ";" + str(smallMatrix[s][i][j].path)+';'+ \
                      str(smallMatrix[s][i][j].length) +';' + str(smallMatrix[s][i][j].dis_similarity)+';'+ str(smallMatrix[s][i][j].time_similarity)+';'+ \
                      str(smallMatrix[s][i][j].time)+ ';' +str(smallMatrix[s][i][j].similarity)+ ';'+\
                      str(str(smallMatrix[s][i][j].point1.x) + ',' + str(smallMatrix[s][i][j].point1.y) + ',' + str(smallMatrix[s][i][j].point1.roadIntersection1) + ',' + str(smallMatrix[s][i][j].point1.roadIntersection2)) + ';'+ \
                      str(str(smallMatrix[s][i][j].point2.x) + ',' + str(smallMatrix[s][i][j].point2.y) + ',' + str(smallMatrix[s][i][j].point2.roadIntersection1) + ',' + str(smallMatrix[s][i][j].point2.roadIntersection2)) + ';')
                f.writelines("\n")
    f.close()
import pickle as p
def smallMatrixToFileWithPickle(filename, smallMatrix):
    rootpath = rootDir + constant.staticMatrixOutPath
    f = file(rootpath + filename + '.data', "w")
    p.dump(smallMatrix,f)
    f.close()

if __name__ == '__main__':
     # 基本数据加载
     # readLuce()
     readLuceYuanshi()
     readcellIdSheet()
     readLukou()
     readAdj()
     readHouXuanPoint()
     readRoadIntersectionCacheFromTxt()
     for eachD in luceDict:
        # try:
            roadMatch(eachD)
        # except:
        #     print 'Fail',
        #     print eachD







