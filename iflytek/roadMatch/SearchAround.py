#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
#本程序主要是生成静态的基站映射表,根据基站的位置信息,生成该基站在道路上面的映射点.最后输出备选点集
cellIdDict={}
lukouDict={}
roadAdjDict={}
extraDis = 300

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

def houxuanPoint(): #寻找附近的点  讲当前基站的路口点按照距离进行一个排序
        allHouxuanPoint={}
        for eachCell in cellIdDict:
            listCurrentCell = {}
            currentCellPoint = cellIdDict.get(eachCell)
            nearByPointSet = set()
            for roadIntersection in lukouDict:
                currentLukouPoint = lukouDict.get(roadIntersection)#RoadIntersection是当前路口的ID号  得到的是当前ID对应的经纬度
                currentDis = calculate(float(currentCellPoint.x),float(currentCellPoint.y),float(currentLukouPoint.x),float(currentLukouPoint.y)) #得到的是当前路口离当前基站的距离
                if(currentDis<3000):#只找周围5KM的路口
                    #当前路口点和当前基站的距离加入字典集合
                    nearByPointSet.add(roadIntersection) #找到所有小于3km的点 放到集合里面去   15:40测试的没有问题

            HouxuanPoint = generateHouxuanPoint(eachCell,nearByPointSet)  #返回值需要为List类型  保存这里的每一个基站点对应的所有候选点集合
            allHouxuanPoint.setdefault(eachCell,HouxuanPoint)#将当前的点和当前点的候选点集加入到allHouxuanPoint字典里面去
            print '当前已处理节点数量'+str(allHouxuanPoint.__len__())


        print '候选点集合加载完毕'
        return allHouxuanPoint

def generateHouxuanPoint(point,nearbyPointSet):   #原始基站点   基站点周围的临近路口点的集合     返回候选点段集  点集定义的是 经纬度 属于的道路(第一个编号 第二个编号)
        listHouxuan = []
        class HouxuanPoint:
            def __init__(self,x,y,roadIntersection1,roadIntersection2):
                self.x = x
                self.y = y
                self.roadIntersection1 = roadIntersection1
                self.roadIntersection2 = roadIntersection2

        class HouxuanLine:
            def __init__(self,x1,y1,x2,y2):
                self.x1 = x1
                self.x2 = x2
                self.y1 = y1
                self.y2 = y2
                if(x2-x1==0):
                    x2+=0.000001
                self.k = (y2-y1)/(x2-x1)
                self.b = (x2*y1-x1*y2)/(x2-x1)
            def getK(self):
                return self.k
            def getB(self):
                return self.b

        point0 = cellIdDict.get(point)#基站点的基本信息
        x0 = point0.x
        y0 = point0.y
        range0 = point0.range + extraDis    #改参数的地方

        for eachRoadIntersectionPoint in nearbyPointSet:
            point1 = eachRoadIntersectionPoint #第一个满足条件的点的编号
            point2 = roadAdjDict.get(point1)  #找到这个点的临界点的list集合 的编号
            point1_2 = lukouDict.get(point1) #第一个满足点的坐标信息
            x1 = point1_2.x
            y1 = point1_2.y

            for point2_2_2 in point2:#处理第一个点的邻接点 并获得位置信息   point2_2_2为第二个节点的编号
                point2_2 = lukouDict.get(point2_2_2)
                x2 = point2_2.x
                y2 = point2_2.y

                line = HouxuanLine(x1,y1,x2,y2) #将每一个点转换为一个线段了
                k1 = line.getK()
                b1 = line.getB()

                k0 = -1/k1
                b0 = y0 - k0*x0
                if(k1-k0==0):
                    k1+=0.000001
                x_intersect = (b0-b1)/(k1-k0)  #点和垂线的交点的坐标
                y_intersect = k0*x_intersect+b0
                #print x_intersect
                distance0n = calculate(x0,y0,x_intersect,y_intersect)
                if(distance0n<range0):  #距离如果小于中心点到直线距离的话 暂时作为候选点
                    if(x_intersect<x1 or x_intersect>x2):
                        #交点在直线外  继续判断两个端点,如果是候选点  那么这个就是候选点
                        disPoint01 = calculate(x0,y0,x1,y1)
                        disPoint02 = calculate(x0,y0,x2,y2)
                        if(disPoint01 < range0 and disPoint02<range0):#在设置参数的时候,把距离的2倍作为候选点  可以搜索到更多的候选点,这个后期可以做改变
                            if disPoint01<disPoint02:
                                listHouxuan.append(HouxuanPoint(x1,y1,point1,point2_2_2))
                            else:
                                listHouxuan.append(HouxuanPoint(x2, y2, point1, point2_2_2))
                        elif(disPoint01<range0):
                            listHouxuan.append(HouxuanPoint(x1, y1, point1, point2_2_2))
                        elif(disPoint02<range0):
                            listHouxuan.append(HouxuanPoint(x2, y2, point1, point2_2_2))
                    else:
                        if(distance0n<range0):
                            listHouxuan.append(HouxuanPoint(x_intersect,y_intersect,point1, point2_2_2))
        return listHouxuan



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







if __name__ == '__main__':
     readcellIdSheet()
     readLukou()
     readAdj()

     print lukouDict

     allHouxuanPoint = houxuanPoint()
     f = file("/Users/chenwuji/Documents/RoadMatch/HouXuanPointDis300MoreMeters.txt", "a+")
     for eachCellTable in allHouxuanPoint:
         li = eachCellTable + ":"
         f.writelines(li)
         for eachPoint in allHouxuanPoint.get(eachCellTable):
             li = "[" + str(eachPoint.x) + "," + str(eachPoint.y) + "," + str(eachPoint.roadIntersection1) + "," + str(
                 eachPoint.roadIntersection2) + "]" + ";"
             f.writelines(li)
         f.writelines("\n")
     f.close()
        

        