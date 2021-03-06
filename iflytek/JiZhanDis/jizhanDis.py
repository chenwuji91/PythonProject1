#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
#本程序主要是生成静态的基站映射表,根据基站的位置信息,生成该基站在道路上面的映射点.最后输出备选点集
cellIdDict={}
lukouDict={}
roadAdjDict={}
extraDis = 0

class JiZhanPoint:
    def __init__(self,x,y,range):
#         print 'NewObject'
        self.x = x
        self.y = y
        self.range = range + extraDis
class RoadIntersectionPoint:
    def __init__(self,x,y):
#         print 'NewObject'
        self.x = x
        self.y = y
def readcellIdSheet():
        f =open('/Users/chenwuji/Documents/RoadMatch/cellIdSheetOnlyXiaoQU.txt')
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

def houxuanPoint(): #寻找附近的点  讲当前基站的路口点按照距离进行一个排序
        allHouxuanPoint={}
        for eachCell in cellIdDict:
            currentCellPoint = cellIdDict.get(eachCell)
            nearByPointSet = set()
            for roadIntersection in lukouDict:
                currentLukouPoint = lukouDict.get(roadIntersection)#RoadIntersection是当前路口的ID号  得到的是当前ID对应的经纬度
                currentDis = calculate(float(currentCellPoint.x),float(currentCellPoint.y),float(currentLukouPoint.x),float(currentLukouPoint.y)) #得到的是当前路口离当前基站的距离
                if(currentDis<5000):#只找周围5KM的路口
                    #当前路口点和当前基站的距离加入字典集合
                    nearByPointSet.add(roadIntersection) #找到所有小于3km的点 放到集合里面去   15:40测试的没有问题
            HouxuanPoint = generateHouxuanPoint(eachCell,nearByPointSet)  #得到eachCell的最近的道路信息
            allHouxuanPoint.setdefault(eachCell,HouxuanPoint)#将当前的点和当前点的候选点集加入到allHouxuanPoint字典里面去
            print '当前已处理节点数量'+str(allHouxuanPoint.__len__())
        print '候选点集合加载完毕'
        toFileWithPickle('',allHouxuanPoint)

def generateHouxuanPoint(point,nearbyPointSet):   #原始基站点   基站点周围的临近路口点的集合     返回候选点段集  点集定义的是 经纬度 属于的道路(第一个编号 第二个编号)

        dictHouxuan = {}
        class HouxuanPoint:
            def __init__(self,x,y,roadIntersection1,roadIntersection2):
                self.x = x
                self.y = y
                self.roadIntersection1 = roadIntersection1
                self.roadIntersection2 = roadIntersection2


        def lineToPointDis(cellID, roadPoint1, roadPoint2):
            class RoadLine:
                def __init__(self, x1, y1, x2, y2):
                    self.x1 = x1
                    self.x2 = x2
                    self.y1 = y1
                    self.y2 = y2
                    if (x2 - x1 == 0):
                        x2 += 0.0000001
                    self.k = (y2 - y1) / (x2 - x1)
                    self.b = y1 - (self.k) * x1

            class Chuixian:
                def __init__(self, x0, y0, k):
                    self.x0 = x0
                    self.y0 = y0
                    self.k = k
                    self.b = y0 - (self.k) * x0
            point1 = lukouDict.get(roadPoint1)
            x1 = point1.x
            y1 = point1.y
            point2 = lukouDict.get(roadPoint2)
            x2 = point2.x
            y2 = point2.y
            pointCell = cellIdDict.get(cellID)
            x0 = pointCell.x
            y0 = pointCell.y
            line12 = RoadLine(x1, y1, x2, y2)
            k1 = line12.k
            b1 = line12.b
            chuixian = Chuixian(x0,y0,-1.0/k1)
            k0 = chuixian.k
            b0 = chuixian.b
            if k1-k0==0:
                k1 = k1 + 0.000000001
            x_i =  (b0 - b1) / (k1 -k0)
            y_i = k0 * x_i + b0
            disPoint01 = calculate(x0, y0, x1, y1)
            disPoint02 = calculate(x0, y0, x2, y2)
            return min(disPoint01,disPoint02)

        for eachP1 in nearbyPointSet:
            listP2 = roadAdjDict.get(eachP1)
            for eachP2 in listP2:
                singlePointDis = lineToPointDis(point, eachP1, eachP2)
                dictHouxuan.setdefault(singlePointDis,(eachP1,eachP2))

        dictHouxuan = sorted(dictHouxuan.iteritems(), key=lambda d: d[0])
        if len(dictHouxuan) > 0:
            return dictHouxuan[0]



from math import radians, cos, sin, asin, sqrt
def calculate(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # 地球平均半径，单位为公里
    return c * r * 1000

import pickle as p
def toFileWithPickle(filename, smallMatrix):
    rootpath = '/Users/chenwuji/Documents/RoadMatch/cellCloestRoad2'
    f = file(rootpath + filename + '.data', "w")
    p.dump(smallMatrix,f)
    f.close()



if __name__ == '__main__':
     readcellIdSheet()
     readLukou()
     readAdj()
     houxuanPoint()



        

        