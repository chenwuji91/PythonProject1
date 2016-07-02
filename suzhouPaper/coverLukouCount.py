#-*- coding: UTF-8 -*-
'''
计算范围内的路口的个数
@author: chenwuji
'''

lukouDict = {}
roadAdjDict = {}
carDataDict = []
rootpath = '/Users/chenwuji/Documents/苏州出租车/'

zuoshangjiao = 120.6354828592534, 31.376368052001823
zuoxiajiao = 120.63549057996597, 31.253756666173818
youshangjiao = 120.85634919819948, 31.376015656647887
youxiajiao = 120.85635657413037, 31.253404335545934

class RoadIntersectionPoint:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def ifInRange(x,y):
    if x > zuoshangjiao[0] and x < youshangjiao[0]:
        if y > zuoxiajiao[1] and y < zuoshangjiao[1]:
            return 1
        else:
            return 0
    else:
        return 0


def readLukou():
    f = open(rootpath + '道路等相关数据/intersection_newid.txt')
    for eachline in f:
        list1 = eachline.split(',')
        lukouId = list1[0]
        position1 = list1[2]
        position2 = list1[3]
        lukouDict.setdefault(lukouId, RoadIntersectionPoint(float(position1), float(position2)))
    f.close()


def readAdj():
    f = open(rootpath + '道路等相关数据/roadnet_newid')
    for eachline in f:
        list1 = eachline.split(':')
        list2 = list1[1].split()
        roadAdjDict.setdefault(list1[0], list2)
    f.close()

if __name__ == '__main__':
    readLukou()
    readAdj()
    count = 0
    for eachL in lukouDict:
        count = count + ifInRange(lukouDict.get(eachL).x, lukouDict.get(eachL).y)
    print count

    count = 0
    for eachL in lukouDict:
        theotherPoint = roadAdjDict.get(eachL)
        for eachO in theotherPoint:
            if ifInRange(lukouDict.get(eachL).x, lukouDict.get(eachL).y) == 1:
                if ifInRange(lukouDict.get(eachO).x, lukouDict.get(eachO).y) == 1:
                    count = count + 1
    print count

