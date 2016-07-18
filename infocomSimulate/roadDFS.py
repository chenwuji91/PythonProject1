#-*- coding: UTF-8 -*-
'''
@author: 张文
搜索所有潜在的可能路径
'''

#import roadBasic as rd

#rd.initRoadData()

#路网的最高限速m/s
MAX_VELOCITY = 30

# 允许的搜索深度
level = 8

rd = None

firstCall = False
firstResult = []



#返回路口在规定区域内的相邻路口
def adjionInter(roadIntersection) :
    adjionList = rd.getNeighbourList(roadIntersection)
    for roadInter in adjionList :
        if (rd.judgeBounds(roadInter)==False) :
            adjionList.remove(roadInter)

        #去掉摄像头路口
        if (rd.judgeCamera(roadInter)):
            if (roadInter in adjionList):
                adjionList.remove(roadInter)

    return adjionList

#返回一个路口到其相邻路口的最快通行时间
def minRunTime(roadIntersection, adjionList) :
    times = []
    for roadIter in adjionList :
        times.append(rd.getRoadLen(roadIntersection, roadIter) / MAX_VELOCITY)

    return times

#路径遍历函数
def rDFS(roadIntersection1, roadIntersection2, Time, level,route, routeList) :
    route.append(roadIntersection1)

    if (Time < 0 or level < 0):  #T耗完，或者搜索深度耗完
        route.pop()
        return


    # 递归遍历相邻路口
    adjionList = adjionInter(roadIntersection1)
    times = minRunTime(roadIntersection1, adjionList)
    for roadInter in adjionList:
        if (roadInter == roadIntersection2):
            # 找到了一条路径
            tempRoute = route[:]
            tempRoute.append(roadInter)
            # print '路径搜索状态:'
            # print(tempRoute)
            routeList.append(tuple(tempRoute))
            #route.pop()
            #return
        elif route.count(roadInter)<=2:
            #tempRoute = route[:]
            rDFS(roadInter, roadIntersection2, Time - times[adjionList.index(roadInter)], level - 1,route, routeList)
            #route.pop()
    route.pop()

def search_exist_list(roadIntersection1, roadIntersection2):
    result0 = set()
    for eachl in firstResult:
        temp1 = []
        temp2 = []
        eachl = list(eachl)
        for i in range(len(eachl)):
            if eachl[i] == roadIntersection1:
                temp1.append(i)

            if eachl[i] == roadIntersection2:
                temp2.append(i)
        for i in temp1:
            for j in temp2:
                if i < j:
                    result0.add(tuple(eachl[i:j+1]))
    return list(result0)


#给出两个路口以及通行时间，查询所有可能的路径
def searchAllRoad(roadIntersection1, roadIntersection2, Time, rd2) :
    global firstCall
    if firstCall == True:
        return search_exist_list(roadIntersection1, roadIntersection2)
    else:
        firstCall = True
        global rd
        rd = rd2

        if rd.cameraList.__contains__(roadIntersection2):
            rd.cameraList.remove(roadIntersection2)
        # 一条路径
        route = []

        # 所有的路径列表
        routeList = []

        rDFS(roadIntersection1, roadIntersection2, Time, level, route, routeList)

        routeSet = set(routeList)

        rd.cameraList.append(roadIntersection1)
        rd.cameraList.append(roadIntersection2)
        global firstResult
        firstResult = list(routeSet)
        return list(routeSet)


if __name__ == '__main__':

    import roadBasic as rd

    rd.initRoadData()
    print searchAllRoad('406', '1239', 300, rd)
    print rd.judgeBounds('128')
    print rd.judgeBounds('1402')
    # print searchAllRoad('1335', '1237', 260, rd)
    # print searchAllRoad('1248', '1246', 260, rd)
    # print searchAllRoad('1335', '1246', 260, rd)
    # print searchAllRoad('1335', '1249', 260, rd)