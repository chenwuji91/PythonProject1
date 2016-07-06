#-*- coding: UTF-8 -*-
'''
@author: 张文
搜索所有潜在的可能路径
'''

import roadBasic as rd

rd.initRoadData()

#路网的最高限速m/s
MAX_VELOCITY = 20

# 允许的搜索深度
level = 20

# 一条路径
route = []

# 所有的路径列表
routeList = []

#返回路口在规定区域内的相邻路口
def adjionInter(roadIntersection) :
    adjionList = rd.getNeighbourList(roadIntersection)
    for roadInter in adjionList :
        if (rd.judgeBounds(roadInter)) :
            adjionList.remove(roadInter)

    return adjionList

#返回一个路口到其相邻路口的最快通行时间
def minRunTime(roadIntersection, adjionList) :
    times = []
    for roadIter in adjionList :
        times.append(rd.getRoadLen(roadIntersection, roadIter) / MAX_VELOCITY)

    return times

#路径遍历函数
def rDFS(roadIntersection1, roadIntersection2, Time, level) :

    if (Time < 0 or level < 0):  #T耗完，或者搜索深度耗完
        return
    if (roadIntersection1 == roadIntersection2):
        # 找到了一条路径
        tempRoute = route[:]
        tempRoute.append(roadIntersection1)
        print '路径搜索状态:'
        print(tempRoute)
        routeList.append(tuple(tempRoute))
        return

    route.append(roadIntersection1)

    # 递归遍历相邻路口
    adjionList = adjionInter(roadIntersection1)
    times = minRunTime(roadIntersection1, adjionList)
    for roadInter in adjionList:
        rDFS(roadInter, roadIntersection2, Time - times[adjionList.index(roadInter)], level - 1)
    route.pop()


#给出两个路口以及通行时间，查询所有可能的路径
def searchAllRoad(roadIntersection1, roadIntersection2, Time) :

    rDFS(roadIntersection1, roadIntersection2, Time, level)

    routeSet = set(routeList)

    return list(routeSet)


if __name__ == '__main__':
    print rd.judgeBounds('1000')  #找的是园区外的  在处理的时候 要改一下底层函数或者改进一下相关的判断
    print rd.judgeBounds('947')
    print searchAllRoad('1000', '947', 80)