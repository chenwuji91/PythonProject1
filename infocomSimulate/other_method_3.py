#-*- coding: UTF-8 -*-
'''
@author: 丁文建
对比实验3  最少转弯
'''
import evaluateRoute
import roadBasic as rd
import tools
import math
import os
import glob
import roadDFS


def other_mehod_3(potential_path_set):
    #给定一个起始终点的路劲list，遍历，找出其中转弯次数最少的一个路径
    # potential_path_set = [('21','213','31','827'),('21','213','31','827'),('21','213','31','827')]

    min_angle = 60   #定义最小转弯角度为60，可修改
    for path in potential_path_set:
        if len(path)<3:     # 如果有相邻的一种可能性，直接返回这种可能路径
            return path

    list_len = len(potential_path_set)  #list长度
    road_turn = [0 for x in range(0,list_len)]  #路径列表中每一可能性的转弯次数列表
    num = 0   #list起点
    for path in potential_path_set:  #path为同一起止点
        turn_num = 0  #每一path初始转向次数为0
        for i in range(len(path)-2):   #遍历每一path中所有的路口
            inter1 = rd.getRoadPointLocation(path[i])
            inter2 = rd.getRoadPointLocation(path[i+1])
            inter3 = rd.getRoadPointLocation(path[i+2])        #依次取三个路口

            #用向量方法计算，计算值与真实值比较过，误差不超过8度
            a1 = [inter2[0]-inter1[0],inter2[1]-inter1[1]]   #向量1
            a2 = [inter3[0]-inter2[0],inter3[1]-inter2[1]]   #向量2
            res = (a1[0]*a2[0]+a1[1]*a2[1])/((a1[0]**2+a1[1]**2)**0.5*(a2[0]**2+a2[1]**2)**0.5)  #计算向量夹角
            if res<=-1.0:
                res = -0.99
            if res>=1.0:
                res = 0.99
            angle = math.acos(res)
            angle = angle*180/3.1415
            if angle>min_angle:   #夹角大于最小角，转向次数加1
                turn_num +=1
        road_turn[num] = turn_num  #转向次数存入数组中
        # print turn_num
        num +=1    #存下一种可能路径

    min_turn = 100 #初始最少转向次数为100
    min_turn_path = -1 #转向最少路径初始标号为-1
    for i in range(0,len(road_turn)):       #找到转向次数最少的那一条路径
        if road_turn[i]<min_turn:
            min_turn = road_turn[i]
            min_turn_path = i

    return potential_path_set[min_turn_path]


# if __name__ == '__main__':
#
#     #下面是路网基本数据的相关参数  注意使用的时候需要调用初始化函数
#     rd.initRoadData()
#     print rd.getRoadLen('1099','1157')  #计算道路长度
#     print tools.calculate(120.640319889,31.2916944701,120.639999, 31.29039)   #  计算距离
#     print rd.getRoadPointLocation('1099')  #获取路口位置经纬度
#     print rd.getNeighbourList('1099')  #获取相邻的路口
#     print rd.judgeBounds('1099')  #判断是否超出边界
#
#     potential_path_set =[['1108', '892', '878', '892', '878', '781', '1088', '964', '953'],
# ['1108', '1019', '1108', '1019', '1108', '892', '878', '781', '1088', '781', '1088', '964', '953']]
#     print other_mehod_3(potential_path_set)


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
        rd.initRoadData()
        roadDFS.level = len(each_carmera_path)
        roadDFS.firstCall = False
        path_list_one = roadDFS.searchAllRoad(each_carmera_path[0][0],
                                              each_carmera_path[len(each_carmera_path)-1][0],
                                              tools.intervalofSeconds(each_carmera_path[0][2]
                                                                      , each_carmera_path[len(each_carmera_path)-1][2]),
                                              rd)
        print path_list_one
        currentResult = list(other_mehod_3(path_list_one))  #当前的处理结果  传进去的参数要进行过DFS搜索的  是list里面有list的
        print currentResult
        all_result_list = all_result_list + currentResult

    print all_result_list
    if len(all_result_list) == 0:
        return
    print evaluateRoute.evaluateFunc(real_path, all_result_list)
    tools.writeToFile('data_result_other_method_3', str(os.path.basename(path_name)) + ',real path:' +
                      str(real_path) + ',predict path:' + str(all_result_list) +
                       ',final score:' + str(evaluateRoute.evaluateFunc(real_path, all_result_list)))


if __name__ == '__main__':
    flist = glob.glob('data_for_run' + os.path.sep + '*')
    for each_path in flist:
        # try:
            print 'BEGIN A NEW FILE  @WJCHEN'
            do_main_by_loop(each_path)
