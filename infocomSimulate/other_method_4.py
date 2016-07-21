#-*- coding: UTF-8 -*-
'''
@author: chenwuji
对比实验4  直接返回概率最大的路径作为实验结果
'''
# import roadBasic as rd
# rd.initRoadData()
# rd.initTimeData()
import tools
import pick_from_route
import glob
import random
import roadDFS
import math
import getcarinfo
import os
import roadBasic as rd
import evaluateRoute
rd.initRoadData()
rd.initTimeData()
count_query = 0

#产生道路的所有候选路段的集合
def generate_potential_path_set(begin_time, end_time, begin_road_intersection, end_road_intersection):
    #调用张文的程序  根据时间生成一个有穷的集合 以List的形式保存
    # potential_set = [('256','425','593','214'), ('256','4235','5923','214'), ('256','4235','5493','214'),
    #                  ('256', '4225', '5793', '214'), ('256','4525','5393','214'), ('256','4625','5963','2714'),
    #                  ('256', '4425', '513', '214'), ('256','4275','6593','214'), ('256','4275','5933','214')]

    # print '开始搜索潜在路径'

    potential_set = roadDFS.searchAllRoad(begin_road_intersection, end_road_intersection , tools.intervalofSeconds(begin_time, end_time),rd)
    return potential_set

def generate_s_pdf_function_list(potential_path, query_date):   # potential_path 接收的是点的保存信息
    s_pdf_function_list = []
    import fsolve
    # ifweekend = tools.getDay(query_date)  #需要查询的日期是否为周末
    for each_s in potential_path:
        # current_s_para = []
        # for i in range(len(each_s)-1):  #总共应该是有这么多的路径数量  这里有时候会有数据取不到  要处理数据娶不到的情况
        #     current_variance = rd.getRoadTimeVariance(each_s[i], each_s[i + 1],str(tools.timeTranslate(query_date)),ifweekend)
        #     current_mean = rd.getRoadTimeAvg(each_s[i], each_s[i + 1],str(tools.timeTranslate(query_date)),ifweekend)
        #     current_s_para.append((current_mean,current_variance))
        # current_s_fun = fsolve.lognorm_together(current_s_para)
        current_s_fun = fsolve.potential_path_to_fsolve(each_s, query_date, rd)
        s_pdf_function_list.append(current_s_fun)
    return s_pdf_function_list


#根据初始信息生成按照概率密度排序的一个List集合  路段查询的概率从大到小
def generate_query_point_position_with_order(potential_path_set, s_pdf_function_list, begin_time, end_time):
    #首先获得每一段概率密度的参数
    probility_list_with_time_interval1 = []
    time_interval = tools.intervalofSeconds(begin_time, end_time)
    for each_f in s_pdf_function_list:
        probility_list_with_time_interval1.append(each_f(time_interval))  #计算每一个路径的概率
    #将这个路径的概率转换一下
    probility_list_with_time_interval = []
    for each_f in probility_list_with_time_interval1:
        probility_list_with_time_interval.append(each_f/sum(probility_list_with_time_interval1))



    #将计算出来的概率值 返回一个已经排序的list
    return  probility_list_with_time_interval





#主要流程控制及调用
def main_flow(begin_time, end_time, begin_road_intersection, end_road_intersection, queryFile):
    print 'Searching potential path...'
    potential_path_set = generate_potential_path_set(begin_time, end_time, begin_road_intersection, end_road_intersection)   #List(('12','32'),('12','45'),('22','63'))
    print potential_path_set
    # potential_path_set = [('406', '463', '1303', '451', '1402', '1345', '1330', '1389', '1330', '1345', '1330', '1326'), ('406', '463', '128', '268', '451', '1402', '1264', '1402', '1264', '1402', '1264', '1344', '1264', '1330', '1326'), ('406', '463', '128', '172', '128', '268', '451', '99', '250', '1329', '1326'), ('406', '463', '25', '1137', '1303', '1284', '1402', '1264', '1330', '1345', '1330', '1326'), ('406', '463', '1303', '451', '268', '451', '1402', '1264', '1330', '1389', '1310', '1389', '1330', '1326'), ('406', '463', '1303', '451', '1402', '451', '1402', '1264', '1330', '1345', '1330', '1389', '1330', '1326'), ('406', '463', '128', '268', '451', '268', '451', '268', '451', '1402', '1284', '1382', '1264', '1330', '1326'), ('406', '463', '128', '172', '99', '451', '1402', '1264', '1330', '1326'), ('406', '463', '1303', '451', '99', '1345', '99', '1345', '1329', '250', '1329', '1326'), ('406', '463', '1303', '1284', '1402', '451', '1402', '1264', '1402', '451', '99', '1345', '1330', '1326'), ('406', '463', '1303', '1284', '1303', '451', '1402', '1264', '1402', '1345', '99', '250', '1329', '1326'), ('406', '463', '1303', '1284', '1402', '1345', '1330', '1389', '1310', '1389', '1282', '1333', '1396', '1326'), ('406', '463', '1303', '1284', '1382', '1384', '1382', '1384', '1336', '1268', '1388', '1268', '1344', '1264', '1330', '1326'), ('406', '463', '1303', '451', '268', '451', '268', '451', '268', '451', '1402', '1264', '1402', '1345', '1329', '1326'), ('406', '463', '1303', '1284', '1303', '1284', '1402', '1345', '99', '250', '1329', '1326'), ('406', '463', '1303', '1284', '1402', '1264', '1382', '1264', '1330', '1345', '1330', '1345', '1329', '1326'), ('406', '463', '128', '268', '451', '268', '451', '1303', '1284', '1402', '1345', '1330', '1345', '1330', '1326')]
    print 'Generating pdf...'
    # 生成S={s1,s2...sn}的pdf函数  需要传入当前可能的路径集合以及需要生成的时间段  这个时间是这个时段的起始时刻就好了
    s_pdf_function_list = generate_s_pdf_function_list(potential_path_set, begin_time)

    potential_path_set = tools.translate_potential_path(potential_path_set)  #将候选集合的数据格式进行转换 将点的表示转换成边的表示
    # print 'Generating road link probility order by prob desc...'#前面一个参数是按照概率排序的link的东西  后面是有几条序列 按照概率排序的那个东西
    probility_list_with_time_interval = generate_query_point_position_with_order(potential_path_set,s_pdf_function_list, begin_time, end_time)  #生成一个按照概率从高到低的一个查询路段的排序  并且里面应至少包含有link的概率数据
    print 'Max Probility Path:', #开始循环来对每个路段询问出租车

    print tools.re_translate_one_potential_path(potential_path_set[probility_list_with_time_interval.index(max(probility_list_with_time_interval))])
    return  tools.re_translate_one_potential_path(potential_path_set[probility_list_with_time_interval.index(max(probility_list_with_time_interval))])
  #如果循环做完  这一段没得查 就直接返回概率最大的路段


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
        print 'BEGIN A NEW LIST,THE LIST IS :',
        print each_carmera_path
        print 'setLevel:',
        print len(each_carmera_path)
        rd.readCamera()
        roadDFS.level = len(each_carmera_path) - 1
        roadDFS.firstCall = False
        currentResult = main_flow(each_carmera_path[0][2], each_carmera_path[len(each_carmera_path) - 1][2],
                                  each_carmera_path[0][0], each_carmera_path[len(each_carmera_path) - 1][0],
                                  each_carmera_path[0][3])
        all_result_list = all_result_list + currentResult

    print all_result_list
    print count_query
    print evaluateRoute.evaluateFunc(real_path, all_result_list)
    tools.writeToFile('data_result_other_result_4',str(os.path.basename(path_name)) + ',real path:' +
                      str(real_path) + ',predict path:' + str(all_result_list) +
                      ',query times:' + str(count_query) + ',final score:' + str(evaluateRoute.evaluateFunc(real_path, all_result_list)))



if __name__ == '__main__':
    flist = glob.glob('data_for_run' + os.path.sep + '*')
    for each_path in flist:
        # try:
            print 'BEGIN A NEW FILE  @WJCHEN'
            do_main_by_loop(each_path)
        # except:
        #     tools.writeToFile('data_result', str(each_path))
