#-*- coding: UTF-8 -*-
'''
@author: chenwuji
对比实验2  最短时间
'''

import roadBasic as rd
rd.initRoadData()
rd.initTimeData()
roadAdjDict = {}
import tools
import os
import math
import glob
import evaluateRoute
import networkx as nx
import os
sep = os.path.sep

def readAdj():
    f =open('data'+sep+'roadnet_newid')
    for eachline in f:
        list1 = eachline.split(':')
        list2 = list1[1].split()
        roadAdjDict.setdefault(list1[0],list2)
    f.close()

readAdj()

def graphGenerate():
    G = nx.DiGraph()
    for eachPointPair in roadAdjDict:
        for anotherPoint in roadAdjDict.get(eachPointPair):

            dis = math.pow(math.e, rd.getRoadTimeAvg(eachPointPair, anotherPoint, '120', 0))
            G.add_edge(eachPointPair,anotherPoint,weight = dis)
    print "有向带权图加载完成"
    return G

G  = graphGenerate()

def nearestPath(point1,point2, G):
    # try:
        return nx.dijkstra_path(G, point1 , point2)
    # except:
    #     return [point1,point2]

def other_mehod_2(potential_path_set):
    return nearestPath(potential_path_set[0][0],potential_path_set[len(potential_path_set)-1][0],G)

def do_main_by_loop(path_name):
    cam_list = []
    f = open('data' + os.path.sep + 'camera.txt.tempremove')
    for eachline in f:
        eachline = eachline.split('\n')[0].split('\r')[0]
        cam_list.append(eachline)
    f.close()

    all_path_list = []

    f = open(path_name)
    onepath = []
    for eachline in f:
        if len(eachline.split(',')) > 2:
            rd_intersection = eachline.split(',')[0].split('\"num\": \"')[1].split('\"')[0]
            speed = int(eachline.split(',')[1].split('\"speed\": ')[1])
            time = eachline.split(',')[2].split('\"time\": \"')[1].split('\"')[0]
            if rd_intersection in cam_list and len(onepath) > 0:
                onepath.append((rd_intersection, speed, time, os.path.basename(path_name)))
                all_path_list.append(onepath)
                onepath = []
            else:
                onepath.append((rd_intersection, speed, time, os.path.basename(path_name)))


    real_path = []
    for each_path in all_path_list:
        temp_p = []
        for each_p in each_path:
            temp_p.append(each_p[0])
        real_path = real_path + temp_p


    print real_path
    print 'Now searching.. :',
    print all_path_list

    all_result_list = []
    for each_carmera_path in all_path_list:

        rd.readCamera()
        currentResult = other_mehod_2(each_carmera_path)  #当前的处理结果
        all_result_list = all_result_list + currentResult

    print all_result_list
    if len(all_result_list) == 0:
        return
    print evaluateRoute.evaluateFunc(real_path, all_result_list)
    tools.writeToFile('data_result_other_method_2', str(os.path.basename(path_name)) + ',real path:' +
                      str(real_path) + ',predict path:' + str(all_result_list) +
                       ',final score:' + str(evaluateRoute.evaluateFunc(real_path, all_result_list)))


if __name__ == '__main__':
    flist = glob.glob('data_for_run' + os.path.sep + '*')
    for each_path in flist:
        # try:
            print 'BEGIN A NEW FILE  @WJCHEN'
            do_main_by_loop(each_path)
        # except:
        #     tools.writeToFile('data_result', str(each_path))