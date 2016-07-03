#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
#本程序做道路映射
from math import radians, cos, sin, asin, sqrt
import numpy as np
import networkx as nx
import glob
import os
from datetime import datetime
import tools
import uuid
lukouDict = {}
roadAdjDict = {}
carDataDict = []
current_date1 = ''
current_car = ''

import os
sep = os.sep
rootpath = sep+ 'Users'+sep+'chenwuji'+sep+'Documents'+sep+'苏州出租车'+sep+''


class RoadIntersectionPoint:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class CarPoint:
    def __init__(self,carId,x,y,speed,angle,time):
        self.carId = carId
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.time = time
def readLukou():
        f =open(rootpath+'道路等相关数据'+sep+'intersection_newid.txt')
        for eachline in f:
            list1 = eachline.split(',')
            lukouId = list1[0]
            position1 = list1[2]
            position2 = list1[3]
            lukouDict.setdefault(lukouId,RoadIntersectionPoint(float(position1),float(position2)))
        f.close()
def readAdj():
        f =open(rootpath+'道路等相关数据'+sep+'roadnet_newid.txt')
        for eachline in f:
            list1 = eachline.split(':')
            list2 = list1[1].split()
            roadAdjDict.setdefault(list1[0],list2)
        f.close()
def readCar(pathToRead):
    zuoshangjiao = 120.6354828592534, 31.376368052001823
    zuoxiajiao = 120.63549057996597, 31.253756666173818
    youshangjiao = 120.85634919819948, 31.376015656647887
    youxiajiao = 120.85635657413037, 31.253404335545934
    f = open(pathToRead)
    for eachline in f:
        list1 = eachline.split(',')
        if(list1.__len__()>5) and float(list1[1]) > zuoshangjiao[0] \
                and float(list1[1]) < youxiajiao[0] and float(list1[2]) < zuoshangjiao[1] \
                and float(list1[2]) > youxiajiao[1]:
            carDataDict.append(CarPoint(list1[0],float(list1[1]),float(list1[2]),int(list1[3]),int(list1[4]),list1[5]))
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
    try:
        return nx.dijkstra_path(G, point1 , point2)
    except:
        return [point1,point2]


def roadMatch():  #需要做的是 输入连续的两个CarPoint类型点,且 ID一致    输出一个道路上面的道路行驶情况的集合  [(当前路段,下一路段),车辆ID,时间段,速度]
    # count1 = 0
    G = graphGenerate()
    allHouxuanPoint = houxuanPoint()  #就是一个文件的全部点集
    # print nearestPath('26','328',G)
    pointPairInfo = []
    for i in range(len(allHouxuanPoint)-1):
        currentBeforeLukou = allHouxuanPoint[i][1].roadIntersection1  # 当前路口的上一个路口
        currentNextLukou = allHouxuanPoint[i][1].roadIntersection2 #当前路口的下一个路口
        nextBeforLukou = allHouxuanPoint[i+1][1].roadIntersection1  #下一个点的上一次路口   这个距离实际上是包含方向的 因为带有方向角 所以这个总是从一端到另外一端
        nextNextLukou = allHouxuanPoint[i + 1][1].roadIntersection2
        nextLukou = nearestPath(currentNextLukou,nextBeforLukou,G)  #保存的是中间的所有的路径
        dddInfo1 = str(allHouxuanPoint[i][0].time)
        dddInfo2 = str(allHouxuanPoint[i+1][0].time)
        currentTotalDis = 0
        currentTotalTime = 0
        currentSpeed = 0
        speedInfoList = []
        if currentBeforeLukou == nextBeforLukou and currentNextLukou == nextNextLukou:
            currentTotalDis = calculate(allHouxuanPoint[i][1].x, allHouxuanPoint[i][1].y, allHouxuanPoint[i+1][1].x, allHouxuanPoint[i+1][1].y)
            currentTotalTime = tools.intervalofSeconds(dddInfo1,dddInfo2)
            if currentTotalTime == 0:
                currentTotalTime = currentTotalTime + 0.000001
            currentSpeed = float(currentTotalDis)/float(currentTotalTime) * 3.6
            speedInfoList.append((currentBeforeLukou,nextBeforLukou,calculate(lukouDict.get(currentBeforeLukou).x,lukouDict.get(currentBeforeLukou).y,
                                                                              lukouDict.get(nextBeforLukou).x,lukouDict.get(nextBeforLukou).y)))
        else:
            for j in range(len(nextLukou)-1):
                currentTotalDis = currentTotalDis + calculate(lukouDict.get(nextLukou[j]).x,lukouDict.get(nextLukou[j]).y,
                                            lukouDict.get(nextLukou[j+1]).x,lukouDict.get(nextLukou[j+1]).y)
            dis00 = calculate(allHouxuanPoint[i][1].x,allHouxuanPoint[i][1].y,
                                                          lukouDict.get(nextLukou[0]).x, lukouDict.get(nextLukou[0]).y)
            currentTotalDis = currentTotalDis + dis00
            disnn = calculate(allHouxuanPoint[i+1][1].x,allHouxuanPoint[i+1][1].y,
                                                          lukouDict.get(nextLukou[len(nextLukou)-1]).x, lukouDict.get(nextLukou[len(nextLukou)-1]).y)
            currentTotalDis = currentTotalDis + disnn
            currentTotalTime = tools.intervalofSeconds(dddInfo1,dddInfo2)
            currentSpeed = float(currentTotalDis)/float(currentTotalTime) * 3.6
            # if currentSpeed > 100.0:
                # print '+++++++++++++++++'
                # count1 = count1 + 1
            speedInfoList.append((currentBeforeLukou,nextLukou[0],dis00))
            for j in range(len(nextLukou) - 1):
                speedInfoList.append((nextLukou[j],nextLukou[j+1],calculate(lukouDict.get(nextLukou[j]).x,lukouDict.get(nextLukou[j]).y,
                                                                            lukouDict.get(nextLukou[j+1]).x,lukouDict.get(nextLukou[j+1]).y)))
            speedInfoList.append((nextLukou[len(nextLukou)-1],nextNextLukou,disnn))
        pointPairInfo.append((speedInfoList,currentSpeed,dddInfo1,dddInfo2,allHouxuanPoint[i][0].speed,
                              currentTotalDis,calculate(allHouxuanPoint[i+1][0].x,allHouxuanPoint[i+1][0].y,
                                                        allHouxuanPoint[i ][0].x,allHouxuanPoint[i][0].y)))
        # temp = nextLukou[0]
        # if len(nextLukou) > 1:
        #     temp = nextLukou[1]
        # else:
        #     temp = nextLukou[0]
        # ddd = datetime.strptime(dddInfo1, "%Y-%m-%d %H:%M:%S").hour
    # fileName = str(currentBeforeLukou)+'_'+ str(currentNextLukou)+'_'+str(temp)+'_'+str(ddd)
    # dataWrite = str(currentBeforeLukou)+','+ str(currentNextLukou)+','+str(temp) +','+str(ddd) + ';' +str(allHouxuanPoint[i][0].speed)+ ';'+ str(allHouxuanPoint[i][0].carId) +','+ str(allHouxuanPoint[i][0].time)+";"+str(nextLukou)
    # # print fileName
    # # print dataWrite
    # writeToFile(fileName,dataWrite)
    # print 'co!'
    # print count1
    for oneSpeed in pointPairInfo[0][0]:
        filename = str(oneSpeed[0]) + '_' + str(oneSpeed[1])
        dateWrite = str(oneSpeed[0]) + ';' + str(oneSpeed[1]) + ';' + str(pointPairInfo[0][1]) + ';' \
                    + str(pointPairInfo[0][2]) +';'+ str(pointPairInfo[0][3]) + ';' + str(pointPairInfo[0][4])
        writeToFile(filename,dateWrite)

    for i in range(1,len(pointPairInfo)-1):
        filename = str(pointPairInfo[i][0][0][0]) + '_' + str(pointPairInfo[i][0][0][1])
        try:
            speed = (pointPairInfo[i-1][0][len(pointPairInfo[i-1][0])-1][2] + pointPairInfo[i][0][0][2])/\
                    (pointPairInfo[i-1][0][len(pointPairInfo[i-1][0])-1][2]/pointPairInfo[i-1][1] +
                     pointPairInfo[i][0][0][2]/pointPairInfo[i][1])
        except:
            speed = str(pointPairInfo[i][1])
        dateWrite = str(pointPairInfo[i][0][0][0]) + ';' + str(pointPairInfo[i][0][0][1]) + ';' + str(speed) + ';' \
                    + str(pointPairInfo[i][2]) + ';' + str(pointPairInfo[i][3]) + ';' + str(pointPairInfo[i][4])
        writeToFile(filename, dateWrite)
        for j in range(1,len(pointPairInfo[i][0])-1):
            filename = str(pointPairInfo[i][0][j][0]) + '_' + str(pointPairInfo[i][0][j][1])
            dateWrite = str(pointPairInfo[i][0][j][0]) + ';' + str(pointPairInfo[i][0][j][1]) + ';' + str(pointPairInfo[i][1]) + ';' \
                        + str(pointPairInfo[i][2]) + ';' + str(pointPairInfo[i][3]) + ';' + str(pointPairInfo[i][4])
            writeToFile(filename, dateWrite)
    pName = str(current_date1) +'_'+str(current_car)+'_'+str(uuid.uuid1())
    tools.makeDir(rootpath+sep+'newMethod'+sep+'obj'+sep+'')
    tools.toFileWithPickle(rootpath+''+sep+'newMethod'+sep+'obj'+sep+''+ str(pName), pointPairInfo)


def writeToFile(fileName,data):
    tools.makeDir(rootpath+sep+'newMethod'+sep+'')
    f = file(rootpath+''+sep+'newMethod'+sep+''+fileName, "a+")
    # f = file(rootpath + "/路段分时段车速信息/" + '20120301', "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()

def houxuanPoint():  # 寻找附近的点  讲当前基站的路口点按照距离进行一个排序
        allHouxuanPoint = []
        for eachCell in carDataDict: #carDataDict存储的是整个轨迹
            nearByPointSet = set()
            for roadIntersection in lukouDict:
                currentLukouPoint = lukouDict.get(roadIntersection)  # RoadIntersection是当前路口的ID号  得到的是当前ID对应的经纬度
                currentDis = calculate(float(eachCell.x), float(eachCell.y), float(currentLukouPoint.x),
                                       float(currentLukouPoint.y))  # 得到的是当前路口离当前基站的距离
                if (currentDis < 500):  # 只找周围5KM的路口
                    # listCurrentCell.setdefault(roadIntersection,int(currentDis))#当前路口点和当前基站的距离加入字典集合
                    nearByPointSet.add(roadIntersection)  # 找到所有小于3km的点 放到集合里面去   15:40测试的没有问题
            # print nearByPointSet
            HouxuanP = generateHouxuanLuduan(eachCell, nearByPointSet)  # 返回值HouxuanPoint  保存的是当前GPS点对应的道路点的信息  class为 CarPoint
            if HouxuanP:
                allHouxuanPoint.append((eachCell,HouxuanP))
        return allHouxuanPoint

#返回的数据类型  返回一个点 即intersection1表示上一个路段  intersection2表示下一个路段 xy表示当前具体在道路上面点的位置,这个仅供参考即可
class HouxuanPoint:
    def __init__(self, x, y, roadIntersection1, roadIntersection2,dis,angle):
        self.x = x
        self.y = y
        self.roadIntersection1 = roadIntersection1
        self.roadIntersection2 = roadIntersection2
        self.dis = dis  #这里表示距离和角度的相似度
        self.angle = angle
        self.sim = dis  #*angle+dis+angle
    def __cmp__(self, other):
        if self.sim > other.sim:
            return 1
        elif self.sim <other.sim:
            return -1
        else:
            return 0

def generateHouxuanLuduan(point, nearbyPointSet):  # 原始点   点周围的临近路口点的集合     返回当前路段即可    point的定义见CarPoint

    listHouxuan = []
    class HouxuanLine:
        def __init__(self, x1, y1, x2, y2):
            self.x1 = x1
            self.x2 = x2
            self.y1 = y1
            self.y2 = y2
            if (x2 - x1 == 0):
                x2 += 0.000001
            self.k = (y2 - y1) / (x2 - x1)
            self.b = (x2 * y1 - x1 * y2) / (x2 - x1)

        def getK(self):
            return self.k

        def getB(self):
            return self.b

    x0 = point.x
    y0 = point.y


    for eachRoadIntersectionPoint in nearbyPointSet:
        point1 = eachRoadIntersectionPoint  # 第一个满足条件的点的编号
        point2 = roadAdjDict.get(point1)  # 找到这个点的临界点的list集合 的编号
        point1_2 = lukouDict.get(point1)  # 第一个满足点的坐标信息
        x1 = point1_2.x
        y1 = point1_2.y

        for point2_2_2 in point2:  # 处理第一个点的邻接点 并获得位置信息   point2_2_2为第二个节点的编号
            point2_2 = lukouDict.get(point2_2_2)
            x2 = point2_2.x
            y2 = point2_2.y

            line = HouxuanLine(x1, y1, x2, y2)  # 将每一个点转换为一个线段了
            k1 = line.getK()
            b1 = line.getB()
            k0 = -1 / k1
            b0 = y0 - k0 * x0
            if (k1 - k0 == 0):
                k1 += 0.000001

            x_intersect = (b0 - b1) / (k1 - k0)  # 点和垂线的交点的坐标
            y_intersect = k0 * x_intersect + b0

            if x_intersect < min(x1, x2) or x_intersect > max(x1, x2) or y_intersect < min(y1, y2) or y_intersect > max(y1, y2):
                x_intersect = (x1 + x2)/2
                y_intersect = (y1 + y2)/2
            else:
                pass

            # print x_intersect
            temp1 = np.arctan(k1) / np.pi * 180
            if y2 > y1:
                if temp1 > 0:
                    temp1 = 90 - temp1
                else:
                    temp1 = 360 - (90 + temp1)
            else:
                if temp1 < 0:
                    temp1 = 90 - temp1
                else:
                    temp1 = 180 + (90 - temp1)
            angleSimilarity = np.abs((float(point.angle)-temp1))
            distance0n = calculate(x0, y0, x_intersect, y_intersect)  #实际GPS点到当前道路的距离
            # if angleSimilarity < 60 and distance0n < 2000:
            if angleSimilarity < 60:
                listHouxuan.append(HouxuanPoint(x_intersect,y_intersect,eachRoadIntersectionPoint,point2_2_2,angleSimilarity,distance0n))

    listHouxuan.sort()
    # print '最好的相似度'
    # print listHouxuan[0].angle
    # print listHouxuan[0].dis
    # print listHouxuan[0].sim
    # print '下一个路口'
    # print listHouxuan[0].roadIntersection2
    # print len(listHouxuan)
    if len(listHouxuan) < 1:
        # print 'null'
        return
    else:
        return listHouxuan[0]
    # return listHouxuan


def printEouLaDis():
    for i in range(1,len(carDataDict)-1):
        print calculate(carDataDict[i-1].x,carDataDict[i-1].y,carDataDict[i].x,carDataDict[i].y)



if __name__ == '__main__':
    readLukou()
    readAdj()
    dir = rootpath+'原始数据和中间结果'+sep+'20120301-20120310_navigate'+sep+''  # 要访问文件夹路径
    fffff = glob.glob(dir + ''+sep+'*')
    print 'begin'
    for file1 in fffff:
        filename1 = os.path.basename(file1)
        print filename1
        current_date1 = filename1
        oneDay = dir+filename1+''+sep+''
        f2 = glob.glob(oneDay + ''+sep+'*')
        for file2 in f2:
            try:
                filename2 = os.path.basename(file2)
                current_car = filename2
                print '当前正在处理文件:'+oneDay+filename2
                carDataDict = []
                readCar(oneDay+filename2)
                # printEouLaDis()
                # pass
                roadMatch()
            except:
                print 'Fail File:',
                print oneDay + filename2
