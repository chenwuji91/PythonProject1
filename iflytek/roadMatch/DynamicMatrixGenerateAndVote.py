#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
import numpy as np
import sys
import glob
import os
import pickle
#传入两个点  计算时间和空间相似度
pathdate = '20160330'
voteMatrix = []
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
        self.dSimilarity = sim * 10000  #人为的放大一个倍数

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
        f =open('/Users/chenwuji/Documents/RoadMatch/RoadData/lukou.txt')
        for eachline in f:
            list1 = eachline.split()
            cellId = list1[0]
            position = list1[1].split(",")
            lukouDict.setdefault(cellId,RoadIntersectionPoint(float(position[0]),float(position[1])))
        f.close()
def readAdj():
        f =open('/Users/chenwuji/Documents/RoadMatch/RoadData/adj.txt')
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
    f = open('/Users/chenwuji/Documents/RoadMatch/HouXuanPointInfo/HouXuanP100.txt')
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
        return [point1,point1]
def nearestPathLen(point1,point2, G):
    try:
        return nx.dijkstra_path_length(G, point1, point2)
    except:
        return 9


#这个函数是整个程序的最后一个步骤  统计当前轨迹所有的票数 恢复出用户实际经过的所有的点   输入参数 smallMatrix的点   输出参数 轨迹[]  初期考虑输出的就是List的集合的叠加  表示出来一条完整的轨迹
def generateBestPath(smallMatrix,trace):
    bestPathIndex = []
    bestpath = []
    for i in range(len(trace)):
        currentHouxuanList = houxuanPointDict.get(trace[i][0])  #所有的候选点
        currentVote = {}
        for j in range(len(currentHouxuanList)):
            singleHouxuanPointVote = currentHouxuanList[j].getVote(i)
            currentVote.setdefault(j,singleHouxuanPointVote)
        voteSorted  = sorted(currentVote.iteritems(), key=lambda d: d[1],reverse=True) #从大到小排序
        bestXiaBiao = voteSorted[0][0]  #当前trace最好的一个下标
        bestPathIndex.append(bestXiaBiao)
    for i in range(len(bestPathIndex)-1):
        bestindex1 = bestPathIndex[i]
        bestindex2 = bestPathIndex[i+1]
        currentCycle = i
        bestPathSingle = smallMatrix[currentCycle][bestindex1][bestindex2].path
        bestpath.append(bestPathSingle)
    return bestpath

def gengerateBestPathWithMatrix(smallMatrix,trace):
    bestList = []
    for m in range(len(trace)):
        currentList = voteMatrix[m]
        # try:
        maxValue = max(currentList)
        bestIndex = currentList.index(maxValue)
        bestList.append(bestIndex)
        # except:
        #     print 'Empty Set'
        #     pass
    # print bestList
    bestpath = []
    s = ''
    for i in range(len(bestList)-1):
        bestpath.append(smallMatrix[i][bestList[i]][bestList[i+1]].path)
    for eachP1 in bestpath:
        for eachPP1 in eachP1:
            print eachPP1+',',
            s = s + str(eachPP1) + ','
    print ''
    # print bestpath
    print '!'
    process(s)


def process(StringToBeProcess):
    listall = str(StringToBeProcess).split(',')
    listnew = []
    for eachP in listall:
        if listnew.__contains__(eachP):
            index1 = listnew.index(eachP)
            listnew = listnew[0:index1]
            listnew.append(eachP)
            pass
        else:
            listnew.append(eachP)
    print listnew
    for eachNo in listnew:
        print eachNo+',',


def traceDis(trace, k):
    traceLength = []
    for i in range(0,len(trace[0:k])):
        print str(k)+'和' +str(i)+'的距离'+ str(calculate(cellIdDict.get(trace[k][0]).x, cellIdDict.get(trace[k][0]).y, cellIdDict.get(trace[i][0]).x, cellIdDict.get(trace[i][0]).y))
        traceLength.append(calculate(cellIdDict.get(trace[k][0]).x, cellIdDict.get(trace[k][0]).y, cellIdDict.get(trace[i][0]).x, cellIdDict.get(trace[i][0]).y))
    for j in range(len(trace[0:k+1]),len(trace)):
        print str(k)+'和' +str(j)+'的距离'+ str(calculate(cellIdDict.get(trace[k][0]).x, cellIdDict.get(trace[k][0]).y, cellIdDict.get(trace[j][0]).x, cellIdDict.get(trace[j][0]).y))
        traceLength.append(calculate(cellIdDict.get(trace[k][0]).x, cellIdDict.get(trace[k][0]).y, cellIdDict.get(trace[j][0]).x, cellIdDict.get(trace[j][0]).y))
    if len(traceLength)==len(trace)-1:
        print '矩阵点之间的距离加权是'
        print traceLength
        return traceLength
    else:
        print 'Error'
        sys.exit(-1)

# def tupleTranslate(t):
#     a = int(t[0])
#     b = int(t[1])
#     c = a * 1000000 + b
#     return c
# def tupleRegenerate(c):
#     a = int(c/1000000)
#     b = int(c%1000000)
#     t = (a,b)
#     return t

#这个函数需要好好做测试

def voteMatrixInit(trace):

    for m in range(len(trace)):
        pointEachLine = []
        for n in range(len(houxuanPointDict.get(trace[m][0]))):
            pointEachLine.append(0)
        voteMatrix.append(pointEachLine)
    # print len(voteMatrix)
    # print len(voteMatrix[0])
    # print 's'

#未测试
def vote(smallMatrix , trace , k):  #k表示是第k轮投票  每一轮投票都需要调用一次这个函数  其中k值表示确定的这个值是属于哪一层的  所以,在定义投票层数的时候需要定义全局的
    #但是在建立图的时候  是在完成加权之后  就需要建立一个图 并作为参数进行传递   smallMatrix实际上保存的是边的信息  注意:在循环的时候 是traceLength-1次的循环 最后一次要单独处理
    #注意::在处理完一个轨迹之后,需要对票数全部重新清0
    traceLen = traceDis(trace, k)  # 可以得到当前点和其他点的一个依次距离
    for s in range(len(smallMatrix)):  # (len(trace)-1):
        # 对于单独一个矩阵进行处理 先改变权值 再进行排序 找最优路径 计算票数
        for i in range(len(smallMatrix[s])):  # (len(Houxuan1List)):#smallMatrix[s]
            for j in range(len(smallMatrix[s][i])):  # (len(Houxuan2List)):
                if traceLen[s]== 0.0:
                    traceLen[s] = traceLen[s] + 0.000001
                smallMatrix[s][i][j].setDSimilarity(smallMatrix[s][i][j].similarity/traceLen[s])
    votePoint = []
    for m in range(len(trace)):
        pointEachLine = []
        for n in range(len(houxuanPointDict.get(trace[m][0]))):
            pointEachLine.append((m,n))
        votePoint.append(pointEachLine)
    for m in range(len(votePoint)):
        for n in range(len(votePoint[m])):
            print votePoint[m][n]
    #后面开始建立
    G = nx.DiGraph()
    #开始建立 从当前层数k向上建立 并且同时从层数k向下进行建立
    for i in range(k,len(votePoint)-1):  #向下
        layer1 = votePoint[i]
        layer2 = votePoint[i+1]
        for l1 in layer1:
            for l2 in layer2:
                G.add_edge(l1,l2,weight = (1.0/(smallMatrix[l1[0]][l1[1]][l2[1]].dSimilarity+0.0000001)))     #前面的加上后面的后缀1.0/
    #向下的边全部添加完成  开始添加向上的边
    for i in range(0,k):  #从0到k-1的循环  实际形成的图是从k(包含)到0的所有的路径
        layer1 = votePoint[i]  #下面的节点
        layer2 = votePoint[i+1]   #上面面的节点  还是从1到2
        for l1 in layer1:
            for l2 in layer2:
                # try:
                    G.add_edge(l2,l1,weight = (1.0/(smallMatrix[l1[0]][l1[1]][l2[1]].dSimilarity+0.0000001))) #修复bug  1.0/
                # except:
                #     pass

    #建立有向图的一个边界处理点  即第一层到起点的路径   和最后一层归一到终点的路径
    layerFirst = votePoint[0]
    layerEnd = votePoint[len(trace)-1]
    for l1 in layerFirst:
        G.add_edge(l1,(-1,-1), weight = 1)  #最终到达-1点
    for l2 in layerEnd:
        G.add_edge(l2,(999999,999999), weight = 1)  #最终到达999999点

    print '单个有向图建立完成'
    #至此有向图建立完成  现在需要尝试在这一轮所有的点依次向上向下寻找最短路径

    # try:
    for nthVote in range(len(smallMatrix[k])):#对k层的每一个节点依次开始进行投票
            bestVotePath1 = nearestPath((k, nthVote), (999999, 999999), G)
            bestVotePath2 = nearestPath((k, nthVote), (-1, -1), G)
            smallMatrix = increaseVoteForEverySingleHouXuanPointOnEveryPath(bestVotePath1,k,smallMatrix,0)#对最佳路径下面的点进行投票
            smallMatrix = increaseVoteForEverySingleHouXuanPointOnEveryPath(bestVotePath2,k,smallMatrix,1)#对最佳路径上面的点进行投票
    # except:
    #     pass #IndexError: list index out of range
    # smallMatrix[0][1][1].point1.printVote(0)
    return smallMatrix
    pass

# 首先在这里需要训练一个network   在这里  对于每一次循环生成的smallMatrix的动态矩阵之后 需要对于每次这个第k轮投票的 实际要投的票数是这一轮所选候选点的个数
# 也就是有几个候选点就要投几次票  因此这个投票的起点是这个候选点的每一个点  然后依次向上或者向下建立这样的有向网络
# 现在考虑传入的参数  建立有向图的时候传入五个参数  投票轮数k  smallMatrix的三个参数  以及矩阵的权值
# 在调用HouXuanPoint里面的投票函数的时候  传入的index值应该是层数  即smallMatrix矩阵的第一个下标  主要是为了区别不同层 投票看作是不同的投票
# 20160511日志:现在下面这个函数主要处理  传入的参数为list类型   这个函数对list类型进行解析  并增加这个list上面的票数
#未测试
def increaseVoteForEverySingleHouXuanPointOnEveryPath(bestVotePath, k, smallMatrix, direction):#通过建立有向图的形式搜索最优解 即每一个当成是一个节点是最优点 然后投票其他的点
    if direction == 0:#向下  #先处理的是只投一票的情况
        for i in range(0, len(bestVotePath)-2):#这里注意了 对于两个路径来说  处理的时候传入的参数还不一样 向上和向下的方向上面 在做smallMatrix下标的时候指向是不一样的
            everySinglePointInBestPath1 = bestVotePath[i]  #除去了最后的(99999,99999)的点
            everySinglePointInBestPath2 = bestVotePath[i+1]

            voteMatrix[everySinglePointInBestPath1[0]][everySinglePointInBestPath1[1]] = voteMatrix[everySinglePointInBestPath1[0]][everySinglePointInBestPath1[1]] + 1
            if i == (len(bestVotePath)-3):##Test#测试的时候最好检查一下k这个值到底投了几票
                voteMatrix[everySinglePointInBestPath2[0]][everySinglePointInBestPath2[1]] = voteMatrix[everySinglePointInBestPath2[0]][everySinglePointInBestPath2[1]] + 1
    elif direction == 1:#向上
        for i in range(0, len(bestVotePath) - 2):  # 这里注意了 对于两个路径来说  处理的时候传入的参数还不一样 向上和向下的方向上面 在做smallMatrix下标的时候指向是不一样的
            everySinglePointInBestPath2 = bestVotePath[i]  # 除去了最后的(-1,-1)的点
            everySinglePointInBestPath1 = bestVotePath[i + 1]
            print '当前投票信息2' + str(everySinglePointInBestPath1[0]) + ' ' + str(
                everySinglePointInBestPath1[1]) + ' ' + str(everySinglePointInBestPath2[1]) + ' '
            voteMatrix[everySinglePointInBestPath1[0]][everySinglePointInBestPath1[1]] = voteMatrix[everySinglePointInBestPath1[0]][everySinglePointInBestPath1[1]] + 1
            # if i == (len(bestVotePath) - 2):   #这个投的票实际上是倒着进行的  所以实际上少的是k这个票点  实际这个在前面一个已经投票过了

    else:
        pass
    return smallMatrix


if __name__ == '__main__':

     readLuce()
     readcellIdSheet()
     readLukou()
     readAdj()
     # roadMatch()
         #下面开始动态矩阵和投票系统
     trace = luceDict.get(pathdate)
     readHouXuanPoint()  #加载候选点的数据
     rootpath = '/Users/chenwuji/Documents/RoadMatch/staticMatrix/'
     dataFile = file(rootpath+pathdate+'.data')
     smallMatrix = pickle.load(dataFile)
     voteMatrixInit(trace)
     for vetoCycle in range(len(trace)-1):#len(trace):   #对每一轮进行一个投票
        smallMatrix = vote(smallMatrix,trace,vetoCycle)   #开始对所有的点进行加权  trace是一个元组  smallMatrix表示图的边  保存的有HouXuanPath的相关信息
     print '开始计算票数'

     gengerateBestPathWithMatrix(smallMatrix,trace)





