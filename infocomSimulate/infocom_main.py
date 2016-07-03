#-*- coding: UTF-8 -*-
'''
@author: chenwuji
实验程序  调用真实路测结果,并调用相关的函数进行测评
'''

import our_method_main as our
import other_method_result as other
import evaluate_function as evalute

begin_time = '2012-03-02 17:28:35'
end_time = '2012-03-02 17:31:35'
begin_road_intersection = '287'
end_road_intersection = '365'
real_path = ['11','22','33','44']


result_our = our.main_flow(begin_time, end_time, begin_road_intersection, end_road_intersection)
result_other1 = other.shortest_path_in_distance(begin_time, end_time, begin_road_intersection, end_road_intersection)
result_other2 = other.shortest_path_in_time(begin_time, end_time, begin_road_intersection, end_road_intersection)
result_other3 = other.path_with_minimum_turning(begin_time, end_time, begin_road_intersection, end_road_intersection)
result_other4 = other.path_with_max_prob(begin_time, end_time, begin_road_intersection, end_road_intersection)


score_our = evalute(real_path, result_our)
score_other1 = evalute(real_path, result_other1)
score_other2 = evalute(real_path, result_other2)
score_other3 = evalute(real_path, result_other3)
score_other4 = evalute(real_path, result_other4)


