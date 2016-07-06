#-*- coding: UTF-8 -*-
'''
@author: chenwuji
实验主类   控制整个实验流程 调用相关的方法得到相关的结果
'''
import roadBasic as rd
rd.initRoadData()
rd.initTimeData()
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

def generate_s_pdf_function_list(potential_path, query_date):   # potential_path 接收的是点的保存信息
    s_pdf_function_list = []
    import fsolve
    ifweekend = tools.getDay(query_date)  #需要查询的日期是否为周末
    for each_s in potential_path:
        current_s_para = []
        for i in range(len(each_s)-1):  #总共应该是有这么多的路径数量  这里有时候会有数据取不到  要处理数据娶不到的情况
            current_variance = rd.getRoadTimeVariance(each_s[i], each_s[i + 1],str(tools.timeTranslate(query_date)),ifweekend)
            current_mean = rd.getRoadTimeAvg(each_s[i], each_s[i + 1],str(tools.timeTranslate(query_date)),ifweekend)
            current_s_para.append((current_mean,current_variance))
        current_s_fun = fsolve.lognorm_together(current_s_para)
        s_pdf_function_list.append(current_s_fun)
    return s_pdf_function_list


#根据初始信息生成按照概率密度排序的一个List集合  路段查询的概率从大到小
def generate_query_point_position_with_order(potential_path_set, s_pdf_function_list, begin_time, end_time):
    #首先获得每一段概率密度的参数
    probility_list_with_time_interval = []
    time_interval = tools.intervalofSeconds(begin_time, end_time)
    for each_f in s_pdf_function_list:
        probility_list_with_time_interval.append(each_f(time_interval))  #计算每一个路径的概率

    #先建立道路link的一个集合:



    pass


#根据查询路段求积分生成最佳的查询时间   返回一个t  这个t最佳的查询时间
def generate_best_query_point_time(begin_time, end_time, begin_road_intersection, end_road_intersection):
    pass


#询问出租车车辆是不是在这个地方   输入一辆车在的路口以及需要查询的时间
#需要调用出租车位置的相关接口  然后返回true or false 判断车辆是不是在那里
def ask_taxi_if_exist(road_intersection1, road_intersection2, query_time):
    return True
    pass


def translate_potential_path(potential_list):#将点的表示转换成为边的一个表示
    translated_set = []
    for eachS in potential_list:
        each_translated_path = []
        for i in range(len(eachS)-1):
            each_translated_path.append((eachS[i],eachS[i + 1]))
        translated_set.append(each_translated_path)
    return translated_set

def re_translate_potential_path(potential_list):#将边的表示转换成为点的表示
    translated_set = []
    for eachS in potential_list:
        each_translated_path = []
        for i in range(len(eachS)-1):
            each_translated_path.append(eachS[i][0])
        each_translated_path.append(eachS[len(eachS)-1][0])
        each_translated_path.append(eachS[len(eachS)-1][1])
        translated_set.append(each_translated_path)
    return translated_set



#主要流程控制及调用
def main_flow(begin_time, end_time, begin_road_intersection, end_road_intersection):
    # 生成所有候选路段的一个集合
    potential_path_set = generate_potential_path_set(begin_time, end_time, begin_road_intersection, end_road_intersection)   #List(('12','32'),('12','45'),('22','63'))
    #下面的是测试数据
    potential_path_set = [('1007', '1009', '1122', '1186', '792', '814'),('1007', '1009', '1122', '1186', '792', '814','994')]

    # 生成所有潜在路径组合的pdf函数  需要传入当前可能的路径集合以及需要生成的时间段
    s_pdf_function_list = generate_s_pdf_function_list(potential_path_set,'2012-03-05 07:18:18')
    # print s_pdf_function_list[0](70)    #输入任意的时间  是可以返回这个时间对应的概率
    print 'pdf函数生成完毕1 '

    potential_path_set = translate_potential_path(potential_path_set)  #将候选集合的数据格式进行转换 将点的表示转换成边的表示

    road_link_prob = generate_query_point_position_with_order(potential_path_set,s_pdf_function_list, begin_time, end_time)  #生成一个按照概率从高到低的一个查询路段的排序  并且里面应至少包含有link的概率数据


    for each_link_prob in road_link_prob:  #对每一个路段确定一个查询时间  针对这个查询时间来询问出租车 得到一组正确或者错误的值 可以是最后某个link的组合的s达到一个概率的阀值之后  就输出这个序列
        query_time = generate_best_query_point_time(each_link_prob)   #在什么时间查这一段路获得的概率最大
        ask_result = ask_taxi_if_exist(each_link_prob,query_time)  #each_link_prob可以是一个元组 保存了多个信息

    result_set = potential_path_set[0]  #返回第几条结果作为最后的结果值
    # result_set = []  #结果集   是一个路段的集合
    return result_set  #返回查询结果





if __name__ == '__main__':
    # main_flow('2012-03-03 19:21,18','2012-03-03 19:24,18','1000','947')
    potential_path_set = [('1007', '1009', '1122', '1186', '792', '814'),
                          ('1007', '1009', '1122', '1186', '792', '814', '994')]
    print translate_potential_path(potential_path_set)
    print re_translate_potential_path(translate_potential_path(potential_path_set))

