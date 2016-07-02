#-*- coding: UTF-8 -*-
'''
@author: chenwuji
测试demo
'''

import roadBasic as rd
import tools

if __name__ == '__main__':
    rd.initRoadData()
    print rd.getRoadLen('1099','1157')  #计算道路长度
    print tools.calculate(120.640319889,31.2916944701,120.639999, 31.29039)   #  计算距离
    print rd.getRoadPointLocation('1099')  #获取路口位置经纬度
    print rd.getNeighbourList('1099')  #获取相邻的路口
    print rd.judgeBounds('1099')  #判断是否超出边界

