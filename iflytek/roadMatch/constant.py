#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''
#根目录路径
rootPath = '/Users/chenwuji/Documents/RoadMatch/'

#基站的静态表
cellIDInfoStatic = 'RoadData/cellIdSheetOnlyXiaoQU.txt'
#候选点的生成路径  该路径只在候选点生成的程序中使用
houxuanOutPath = 'HouXuanPointInfo/HouxuanPP'
#新的候选点生成路径  下面这个路径是使用的新的候选点的生成规则进行的
houxuanOutPathWithNewMethod = "HouXuanPointInfo/HouxuanNew"

#小区的静态表的读取
cellIDSheet = 'RoadData/cellIdSheetOnlyXiaoQU.txt'
#路口的基本信息
lukouInfo = 'RoadData/lukou.txt'
#路网邻接矩阵的数据
adjInfo = 'RoadData/adj.txt'
#经过预处理的原始序列的读取目录
luceProcessed = '经过翌晨处理的数据/'
#未经过处理的原始序列的读取路径
luceYuanshi = 'NotProcessed/szf.data'
#候选点的载入目录
houxuanPointPath = 'HouXuanPointInfo/HouxuanNew200-50.txt'
#路口距离缓冲区的路径
roadIntersectionDisCache = 'RoadData/LukouDisStatic.txt'
#静态矩阵的输出路径
staticMatrixOutPath = 'MidTermData/staticMatrix/'  #静态矩阵的输出结果

#临时任务路径
resultDataOutpathWithNoProcess = 'zyc/result/'
tempResultOutPath = 'zyc/result_out.js'

#输出最终经过投票的结果的路径
luceResultOut = 'result/result_luceyuanshi.txt'
resultDataOutpathLuce = 'result/result/'