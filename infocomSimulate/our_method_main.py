#-*- coding: UTF-8 -*-
'''
@author: chenwuji
实验主类   控制整个实验流程 调用相关的方法得到相关的结果
'''

#产生道路的所有候选路段的集合
def generate_potential_path_set(begin_time, end_time, begin_road_intersection, end_road_intersection):
    #调用张文的程序  根据时间生成一个有穷的集合 以List的形式保存
    potential_set = []
    return potential_set


#根据初始信息生成按照概率密度排序的一个List集合  路段查询的概率从大到小
def generate_query_point_position_with_order(potential_path_set):
    pass


#根据查询路段求积分生成最佳的查询时间   返回一个t  这个t最佳的查询时间
def generate_best_query_point_time(begin_time, end_time, begin_road_intersection, end_road_intersection):
    pass

#询问出租车车辆是不是在这个地方   输入一辆车在的路口以及需要查询的时间
#需要调用出租车位置的相关接口  然后返回true or false 判断车辆是不是在那里
def ask_taxi_if_exist(road_intersection1, road_intersection2, query_time):
    pass


#主要流程控制及调用
def main_flow(begin_time, end_time, begin_road_intersection, end_road_intersection):
    potential_path_set = generate_potential_path_set()
    road_link_prob_desc = generate_query_point_position_with_order()
    result_set = []
    return result_set




# if __name__ == '__main__':
#     real_path = []  #保存实际行驶的一个真实的路径
#     our_query_result_path = main_flow('2012-03-02 17:28:35','2012-03-02 17:28:35','287','365')
#     accuracy = evaluate_result([1,3,5,7,9],[2,4,5,7,9])



