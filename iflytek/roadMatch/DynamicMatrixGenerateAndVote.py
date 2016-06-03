#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
import numpy as np
import sys
import glob
import os
import pickle
import constant
import tools
#传入两个点  计算时间和空间相似度

voteMatrix = []
cellIdDict={}
lukouDict={}
roadAdjDict={}
luceDict={}
houxuanPointDict={}
rootDir = constant.rootPath
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
        self.voteCount = int(0)  # 获得的票数  票数是对象本身的属性
        self.voteDict = {}
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

def readLuceYuanshi():
    dataFile = file(rootDir + constant.luceYuanshi)
    global luceDict
    luceDict = pickle.load(dataFile)

def readLuce():
    dir = rootDir + constant.luceProcessed  # 要访问文件夹路径
    f = glob.glob(dir + '//*')
    for file in f:
        filename = os.path.basename(file)
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
            luceDict.setdefault(date,listPoint)
        f.close()

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

def nearestPath(point1,point2, G):
    try:
        return nx.dijkstra_path(G, point1 , point2)
    except:
        print 'No Path!!!'

def nearestPathLen(point1,point2, G):
    try:
        return nx.dijkstra_path_length(G, point1, point2)
    except:
        print 'No Path!!!'


def voteMatrixInit(trace):
    for m in range(len(trace)):
        pointEachLine = []
        for n in range(len(houxuanPointDict.get(trace[m][0]))):
            pointEachLine.append(0)
        voteMatrix.append(pointEachLine)

def traceDis(trace, k):
    traceLength = []
    for i in range(0,len(trace[0:k])):
        # print str(k)+'和' +str(i)+'的距离'+ str(calculate(cellIdDict.get(trace[k][0]).x, cellIdDict.get(trace[k][0]).y, cellIdDict.get(trace[i][0]).x, cellIdDict.get(trace[i][0]).y))
        traceLength.append(calculate(cellIdDict.get(trace[k][0]).x, cellIdDict.get(trace[k][0]).y, cellIdDict.get(trace[i][0]).x, cellIdDict.get(trace[i][0]).y))
    for j in range(len(trace[0:k+1]),len(trace)):
        # print str(k)+'和' +str(j)+'的距离'+ str(calculate(cellIdDict.get(trace[k][0]).x, cellIdDict.get(trace[k][0]).y, cellIdDict.get(trace[j][0]).x, cellIdDict.get(trace[j][0]).y))
        traceLength.append(calculate(cellIdDict.get(trace[k][0]).x, cellIdDict.get(trace[k][0]).y, cellIdDict.get(trace[j][0]).x, cellIdDict.get(trace[j][0]).y))
    if len(traceLength)==len(trace)-1:
        # print '矩阵点之间的距离加权是'
        # print traceLength
        return traceLength
    else:
        print 'Error'
        sys.exit(-1)

def weightMatrix(smallMatrix,k):
    traceLen = traceDis(trace, k)  # 可以得到当前点和其他点的一个依次距离
    for s in range(len(smallMatrix)):  # (len(trace)-1):
        # 对于单独一个矩阵进行处理 先改变权值 再进行排序 找最优路径 计算票数
        for i in range(len(smallMatrix[s])):  # (len(Houxuan1List)):#smallMatrix[s]
            for j in range(len(smallMatrix[s][i])):  # (len(Houxuan2List)):
                if traceLen[s] == 0.0:
                    traceLen[s] = traceLen[s] + 0.000001
                smallMatrix[s][i][j].setDSimilarity(smallMatrix[s][i][j].similarity / traceLen[s])

def voteNetworkGen(smallMatrix,trace,k):
    votePoint = []
    for m in range(len(trace)):
        pointEachLine = []
        for n in range(len(houxuanPointDict.get(trace[m][0]))):
            pointEachLine.append((m, n))
        votePoint.append(pointEachLine)
    # for m in range(len(votePoint)):
    #     for n in range(len(votePoint[m])):
            # print votePoint[m][n]
    # 后面开始建立
    G = nx.DiGraph()
    # 开始建立 从当前层数k向上建立 并且同时从层数k向下进行建立
    for i in range(k, len(votePoint) - 1):  # 向下
        layer1 = votePoint[i]
        layer2 = votePoint[i + 1]
        for l1 in layer1:
            for l2 in layer2:
                G.add_edge(l1, l2,
                    weight=(1.0 / (smallMatrix[l1[0]][l1[1]][l2[1]].dSimilarity + 0.0000001)))  # 前面的加上后面的后缀1.0/
    # 向下的边全部添加完成  开始添加向上的边
    for i in range(0, k):  # 从0到k-1的循环  实际形成的图是从k(包含)到0的所有的路径
        layer1 = votePoint[i]  # 下面的节点
        layer2 = votePoint[i + 1]  # 上面面的节点  还是从1到2
        for l1 in layer1:
            for l2 in layer2:
                G.add_edge(l2, l1,
                    weight=(1.0 / (smallMatrix[l1[0]][l1[1]][l2[1]].dSimilarity + 0.0000001)))  # 修复bug  1.0/
    # 建立有向图的一个边界处理点  即第一层到起点的路径   和最后一层归一到终点的路径
    layerFirst = votePoint[0]
    layerEnd = votePoint[len(trace) - 1]
    for l1 in layerFirst:
        G.add_edge(l1, (-1, -1), weight=1)  # 最终到达-1点
    for l2 in layerEnd:
        G.add_edge(l2, (999999, 999999), weight=1)  # 最终到达999999点
    return G

def increaseVoteForEverySingleHouXuanPointOnEveryPath(bestVotePath, direction):  # 通过建立有向图的形式搜索最优解 即每一个当成是一个节点是最优点 然后投票其他的点
        if direction == 0:  # 向下  #先处理的是只投一票的情况
            for i in range(0, len(bestVotePath) - 2):
                # 这里注意了 对于两个路径来说  处理的时候传入的参数还不一样 向上和向下的方向上面 在做smallMatrix下标的时候指向是不一样的
                everySinglePointInBestPath1 = bestVotePath[i]  # 除去了最后的(99999,99999)的点
                everySinglePointInBestPath2 = bestVotePath[i + 1]
                voteMatrix[everySinglePointInBestPath1[0]][everySinglePointInBestPath1[1]] = \
                voteMatrix[everySinglePointInBestPath1[0]][everySinglePointInBestPath1[1]] + 1
                if i == (len(bestVotePath) - 3):  ##Test#测试的时候最好检查一下k这个值到底投了几票
                    voteMatrix[everySinglePointInBestPath2[0]][everySinglePointInBestPath2[1]] = \
                    voteMatrix[everySinglePointInBestPath2[0]][everySinglePointInBestPath2[1]] + 1
        elif direction == 1:  # 向上
            for i in range(0, len(bestVotePath) - 2):
                # 这里注意了 对于两个路径来说  处理的时候传入的参数还不一样 向上和向下的方向上面 在做smallMatrix下标的时候指向是不一样的
                everySinglePointInBestPath2 = bestVotePath[i]  # 除去了最后的(-1,-1)的点
                everySinglePointInBestPath1 = bestVotePath[i + 1]

                voteMatrix[everySinglePointInBestPath1[0]][everySinglePointInBestPath1[1]] = \
                voteMatrix[everySinglePointInBestPath1[0]][everySinglePointInBestPath1[1]] + 1
        pass

def vote(smallMatrix , trace , k):  #k表示是第k轮投票  每一轮投票都需要调用一次这个函数  其中k值表示确定的这个值是属于哪一层的  所以,在定义投票层数的时候需要定义全局的

    weightMatrix(smallMatrix,k)  #加权  对当前的轮数所有的点进行投票
    G = voteNetworkGen(smallMatrix, trace, k)   #建立投票的矩阵
    for nthVote in range(len(smallMatrix[k])):#对k层的每一个节点依次开始进行投票
            bestVotePath1 = nearestPath((k, nthVote), (999999, 999999), G)
            bestVotePath2 = nearestPath((k, nthVote), (-1, -1), G)
            increaseVoteForEverySingleHouXuanPointOnEveryPath(bestVotePath1,0)#对最佳路径下面的点进行投票
            increaseVoteForEverySingleHouXuanPointOnEveryPath(bestVotePath2,1)#对最佳路径上面的点进行投票


def timetranslate(HouxuanTime):
    sss = int(HouxuanTime[len(HouxuanTime) - 2:len(HouxuanTime)])
    mmm = int(HouxuanTime[len(HouxuanTime) - 4:len(HouxuanTime) - 2])
    hhh = int(HouxuanTime[len(HouxuanTime) - 6:len(HouxuanTime) - 4])
    return sss + mmm * 60 + hhh * 3600

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines('\n')
    f.close()

def gengerateBestPathWithMatrix(smallMatrix,trace):
    bestList = []
    for m in range(len(trace)):
        currentList = voteMatrix[m]
        maxValue = max(currentList)
        bestIndex = currentList.index(maxValue)
        bestList.append(bestIndex)

    bestpath = []

    for i in range(len(trace)-1):
        dis = (smallMatrix[i][bestList[i]][bestList[i + 1]].length)
        timeHouxuan1 = timetranslate(trace[i][1])
        timeHouxuan2 = timetranslate(trace[i + 1][1])
        if(timeHouxuan2-timeHouxuan1==0):
            timeHouxuan2 = timeHouxuan2 + 0.0000001
        speed = dis/(timeHouxuan2-timeHouxuan1)
        houxuanP1 = smallMatrix[i][bestList[i]][bestList[i + 1]].point1
        houxuanP2 = smallMatrix[i][bestList[i]][bestList[i + 1]].point2
        bestpath.append((trace[i][0], smallMatrix[i][bestList[i]][bestList[i+1]].path,dis,(timeHouxuan2 - timeHouxuan1),speed,houxuanP1,houxuanP2))
    return bestpath

import pointToPointDis as pointCal
def processAgain(ListToBeProcess):
    pointCal.init()
    listOnlyContainLukou = []
    listContainsAll = []
    for eachP in ListToBeProcess:
        if listOnlyContainLukou.__contains__(eachP[0]):
            index1 = listnew.index(eachP)
            listnew = listnew[0:index1]
            listnew.append(eachP)
            pass
        else:
            listnew.append(eachP)
    print listnew
    for eachNo in listnew:
        print eachNo+',',
        sProcessed = sProcessed +',' +str(eachNo)
    return sProcessed



if __name__ == '__main__':

     readLuceYuanshi()
     readcellIdSheet()

     readLukou()
     readAdj()
     readHouXuanPoint()  # 加载候选点的数据

     fileList = glob.glob(rootDir + constant.staticMatrixOutPath + '*.data')
     print fileList
     for eachF in fileList:
          try:
             global voteMatrix
             voteMatrix = []
             filename = os.path.basename(eachF)
             pathdate = filename.split('.')[0]
             trace = luceDict.get(pathdate)
             trace = tools.traceLegalCheck(trace,cellIdDict,JiZhanPoint,houxuanPointDict)

             rootpath = rootDir + constant.staticMatrixOutPath
             dataFile = file(rootpath+pathdate+'.data')
             smallMatrix = pickle.load(dataFile)
             voteMatrixInit(trace)
             for vetoCycle in range(len(trace)-1):#len(trace):   #对每一轮进行一个投票
                vote(smallMatrix,trace,vetoCycle)   #开始对所有的点进行加权  trace是一个元组  smallMatrix表示图的边  保存的有HouXuanPath的相关信息
             print '开始计算票数'
             resultListWithNoProcess = gengerateBestPathWithMatrix(smallMatrix,trace)
             # sProcessed = processAgain(s)
             datatemp = []
             for eachL in resultListWithNoProcess:
                 import tools
                 tools.makeDir(rootDir + constant.resultDataOutpathLuce)
                 writeToFile(rootDir+ constant.resultDataOutpathLuce + pathdate +'.txt',str(eachL[0])+';'+
                             str(eachL[1]) + ';' +str(eachL[2])+';'+str(eachL[3])+';'+str(eachL[4]))
                 datatemp.extend(eachL[1])

             import tempTask
             tempTask.writeToMapLuce(pathdate, rootDir + constant.luceResultOut,datatemp)
             # tempTask.writeToMapForm(lukouDict,rootDir + constant.tempResultOutPath,datatemp)

          except:
              print 'FailDate' + eachF





