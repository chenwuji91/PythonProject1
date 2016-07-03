#-*- coding: UTF-8 -*-
'''
@author: chenwuji
测试demo
'''

import roadBasic as rd
import tools

if __name__ == '__main__':

    #下面是路网基本数据的相关参数  注意使用的时候需要调用初始化函数
    rd.initRoadData()
    print rd.getRoadLen('1099','1157')  #计算道路长度
    print tools.calculate(120.640319889,31.2916944701,120.639999, 31.29039)   #  计算距离
    print rd.getRoadPointLocation('1099')  #获取路口位置经纬度
    print rd.getNeighbourList('1099')  #获取相邻的路口
    print rd.judgeBounds('1099')  #判断是否超出边界



    #下面是获取车辆数据的相关demo
    print rd.getCarDataList()
    list1 = rd.getCarDataList()
    import os
    for eachL in list1:
        # print eachL
        # print os.path.basename(eachL).split('.data')[0] #文件名  车Id
        # eachObj = rd.getCarObj(eachL)  #一辆车一天的数据
        pass
        #处理一辆车
    sep = os.path.sep
    print rd.getCarObj('data'+sep+'carMoving'+sep+'0004855e-37a3-11e6-9dba-84383566f30c.data')   #读取一辆车的相关数据


    #下面测试道路参数获取相关函数
    #说明 调用相关部分需要先调用初始化参数  传入的前两个参数为路口  第三个参数为时间段 时间段需要用timeTranslate函数将标准日期转换成时间段\
    #具体demo如下所示  最后一个参数是是否为周末 1代表周末    返回的是标准差
    rd.initTimeData()
    print rd.getRoadTimeAvg('1007','1186','72',1)
    print rd.getRoadTimeAvg('1016','895','74',1)
    print rd.getRoadTimeVariance('1016','895','74',1)

    rd.initSpeedData()
    print rd.getRoadSpeedAvg('1007','1186','72',1)
    print rd.getRoadSpeedAvg('1016','895','74',1)
    print rd.getRoadSpeedVariance('1016','895','74',1)
    print rd.getRoadTimeAvg('1016','895',str(tools.timeTranslate('2012-03-02 09:58:23')),1)  #传入的参数需要转换为时间段
    print tools.timeRetranslate('74')

    import networkx as nx
    #demo of networkx
    def graphGenerate():
        G = nx.DiGraph()
        G.add_edge('291', '214', weight = 21)
        return G

    def nearestPath(point1, point2, G):
        try:
            return nx.dijkstra_path(G, point1, point2)
        except:
            return [point1, point2]



