#-*- coding: UTF-8 -*-
'''
@author: chenwuji
测试demo
'''

import roadBasic as rd
import tools
import math

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
        print turn_num
        num +=1    #存下一种可能路径

    min_turn = 100 #初始最少转向次数为100
    min_turn_path = -1 #转向最少路径初始标号为-1
    for i in range(0,len(road_turn)):       #找到转向次数最少的那一条路径
        if road_turn[i]<min_turn:
            min_turn = road_turn[i]
            min_turn_path = i

    return potential_path_set[min_turn_path]


if __name__ == '__main__':

    #下面是路网基本数据的相关参数  注意使用的时候需要调用初始化函数
    rd.initRoadData()
    print rd.getRoadLen('1099','1157')  #计算道路长度
    print tools.calculate(120.640319889,31.2916944701,120.639999, 31.29039)   #  计算距离
    print rd.getRoadPointLocation('1099')  #获取路口位置经纬度
    print rd.getNeighbourList('1099')  #获取相邻的路口
    print rd.judgeBounds('1099')  #判断是否超出边界

    potential_path_set =[['1108', '892', '878', '892', '878', '781', '1088', '964', '953'],
['1108', '1019', '1108', '1019', '1108', '892', '878', '781', '1088', '781', '1088', '964', '953']]
    print other_mehod_3(potential_path_set)


