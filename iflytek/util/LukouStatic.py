#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
#本程序主要是生成静态的基站映射表,根据基站的位置信息,生成该基站在道路上面的映射点.最后输出备选点集
cellIdDict={}
lukouDict={}
roadAdjDict={}
extraDis = 0
outPath = '/Users/chenwuji/Documents/RoadMatch/staticPara1/'

class RoadIntersectionPoint:
    def __init__(self,x,y):
        self.x = x
        self.y = y

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
def objToFile(filename, obj1):
    rootpath = outPath
    f = file(rootpath + filename + '.data', "w")
    p.dump(obj1,f)
    f.close()

def writeToFile(fileName,data):
    f = file(fileName, "a+")
    f.writelines(data)
    f.writelines("\n")
    f.close()

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
    try:
        return nx.dijkstra_path(G, point1 , point2)
    except:
        return [point1,point2]
def nearestPathLen(point1,point2, G):
    try:
        return nx.dijkstra_path_length(G, point1, point2)
    except:
        print 'Illegal Path:',
        print point1,
        print ' ',
        print point2
        return 999999999

def generateAllLukouDis():
    resultDict = {}
    G = graphGenerate()
    for eachLukou1 in lukouDict:
        for eachLukou2 in lukouDict:
            length = nearestPathLen(eachLukou1,eachLukou2,G)
            path = nearestPath(eachLukou1, eachLukou2, G)
            writeToFile(outPath + 'LukouDisStatic.txt',str(eachLukou1) + ';' + str(eachLukou2) + ";" + str(length) + ";" + str(path))
            resultDict.setdefault((eachLukou1,eachLukou2),(length, path))
    objToFile('LukouDisStatic',resultDict)



if __name__ == '__main__':
    readAdj()
    readLukou()
    generateAllLukouDis()






