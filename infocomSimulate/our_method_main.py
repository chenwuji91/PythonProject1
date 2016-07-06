#-*- coding: UTF-8 -*-
'''
@author: chenwuji
实验主类   控制整个实验流程 调用相关的方法得到相关的结果
'''
import roadBasic as rd
import tools

#产生道路的所有候选路段的集合
def generate_potential_path_set(begin_time, end_time, begin_road_intersection, end_road_intersection):
    #调用张文的程序  根据时间生成一个有穷的集合 以List的形式保存
    # potential_set = [('256','425','593','214'), ('256','4235','5923','214'), ('256','4235','5493','214'),
    #                  ('256', '4225', '5793', '214'), ('256','4525','5393','214'), ('256','4625','5963','2714'),
    #                  ('256', '4425', '513', '214'), ('256','4275','6593','214'), ('256','4275','5933','214')]
    import roadDFS
    print '开始搜索潜在路径'
    potential_set = roadDFS.searchAllRoad('1000', '947', 80)
    return potential_set

def generate_s_pdf_function_list(potential_path):
    s_pdf_function_list = []
    import fsolve
    for i in len(len(potential_path)):
        rd.getRoadTimeVariance(potential_path[i],
                               rd.getRoadTimeAvg('1016','895',str(tools.timeTranslate('2012-03-02 09:58:23')),1)))




#根据初始信息生成按照概率密度排序的一个List集合  路段查询的概率从大到小
def generate_query_point_position_with_order(potential_path_set):
    #首先获得每一段概率密度的参数


    pass


#根据查询路段求积分生成最佳的查询时间   返回一个t  这个t最佳的查询时间
def generate_best_query_point_time(begin_time, end_time, begin_road_intersection, end_road_intersection):
    pass


#询问出租车车辆是不是在这个地方   输入一辆车在的路口以及需要查询的时间
#需要调用出租车位置的相关接口  然后返回true or false 判断车辆是不是在那里
def ask_taxi_if_exist(road_intersection1, road_intersection2, query_time):
    return True
    pass

stop_prob = 0.5

#主要流程控制及调用
def main_flow(begin_time, end_time, begin_road_intersection, end_road_intersection):
    current_prob = 0
    # 生成所有候选路段的一个集合
    potential_path_set = generate_potential_path_set()
    # 生成所有潜在路径组合的pdf函数  需要传入当前可能的路径集合以及需要生成的时间段
    s_pdf_function_list = generate_s_pdf_function_list(potential_path_set,




    road_link_prob = generate_query_point_position_with_order(potential_path_set)  #生成一个按照概率从高到低的一个查询路段的排序  并且里面应至少包含有link的概率数据
    for each_link_prob in road_link_prob:  #对每一个路段确定一个查询时间  针对这个查询时间来询问出租车 得到一组正确或者错误的值 可以是最后某个link的组合的s达到一个概率的阀值之后  就输出这个序列
        query_time = generate_best_query_point_time(each_link_prob)   #在什么时间查这一段路获得的概率最大
        ask_result = ask_taxi_if_exist(each_link_prob,query_time)  #each_link_prob可以是一个元组 保存了多个信息
        if ask_result == True:  #随便写的 就是判断查询到了多少个正确之后  就终止
            current_prob = current_prob + 0.1   #查询到某一条路会把整个的概率提高多少
        if current_prob > stop_prob:
            break
    result_set = potential_path_set[0]  #返回第几条结果作为最后的结果值
    # result_set = []  #结果集   是一个路段的集合
    return result_set  #返回查询结果







