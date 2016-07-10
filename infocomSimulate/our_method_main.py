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
    probility_list_with_time_interval = []
    time_interval = tools.intervalofSeconds(begin_time, end_time)
    for each_f in s_pdf_function_list:
        probility_list_with_time_interval.append(each_f(time_interval))  #计算每一个路径的概率

    #下面开始将所有道路的集合进行统一的存储以及排序
    link_dict = {}
    for i in range(len(potential_path_set)):
        for j in range(len(potential_path_set[i])):
            if link_dict.__contains__(potential_path_set[i][j]):
                currentP = link_dict.get(potential_path_set[i][j])
                currentP = currentP + probility_list_with_time_interval[i]
                link_dict.update({potential_path_set[i][j]:currentP})  #更新当前的概率值
            else:   #每一个dict包含两项   dict={((道路编号),概率值}
                link_dict.setdefault(potential_path_set[i][j], probility_list_with_time_interval[i])

    #将计算出来的概率值 返回一个已经排序的list
    return sorted(link_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)



#根据查询路段求积分生成最佳的查询时间   返回一个t  这个t最佳的查询时间 以及最佳的一个查询路段
def generate_best_query_point_time(most_likely_road_link, potential_path_set, s_pdf_function_list, begin_time, end_time):
    init_time = 1
    delta_t = 3   #求解定积分的时候 时间的变化率
    delta_time = int(tools.intervalofSeconds(begin_time, end_time))
    dict_result = {}
    import fsolve
    from scipy import stats
    import dblquad
    list_s_index_contains_most_likely_road_link = []
    for i in range(len(potential_path_set)):
        for j in range(len(potential_path_set[i])):
            if most_likely_road_link[0] == potential_path_set[i][j]:
                list_s_index_contains_most_likely_road_link.append((i,j))  #如果这个路段里面包含这个link  把这个路段的索引加入到这个里面
    #下面开始对包含这个link的所有路段开始求解积分的问题
    for each_path_contains_link in list_s_index_contains_most_likely_road_link: #对于每一个包含这个link的路段来求解时间
        #正常的情况是分成这几段   考虑边界情况呢?
        path_sb = potential_path_set[each_path_contains_link[0]][0:each_path_contains_link[1]]
        path_r = potential_path_set[each_path_contains_link[0]][each_path_contains_link[1]]
        path_sa = potential_path_set[each_path_contains_link[0]][each_path_contains_link[1]+1:len(potential_path_set[each_path_contains_link[0]])]
        prob_list = []
        fun1 = fsolve.potential_path_to_fsolve(tools.re_translate_one_potential_path(path_sb), begin_time, rd)
        fun2 = stats.lognorm.pdf  # x,s,mean,variance
        fun2_mean = rd.getRoadTimeAvg(path_r[0], path_r[1], str(tools.timeTranslate(begin_time)),
                                      tools.getDay(begin_time))
        fun2_variance = rd.getRoadTimeVariance(path_r[0], path_r[1], str(tools.timeTranslate(begin_time)),
                                               tools.getDay(begin_time))
        fun3 = fsolve.potential_path_to_fsolve(tools.re_translate_one_potential_path(path_sa), begin_time, rd)
        for i in range(init_time, delta_time, delta_t):  #对于每一个分块的时间间隔 时间离散化操作
            # def fun4(a1):
            #     return i - a1
            # def fun5(a1):
            #     return delta_t - a1
            prob1 = dblquad.fun_2d(fun1, (fun2,fun2_mean,fun2_variance), fun3, i, delta_time)  #求解积分
            print '输出一个概率:',
            print prob1
            prob_list.append(prob1[0]/)
            pass

        print prob_list #跑完这个link属于一个路段的情况
        max_prob = max(prob_list)   #最大的这个概率
        max_index = prob_list.index(max_prob)  #取到最大概率的索引
        best_query_time = init_time + max_index * delta_t  #这个概率对应的最佳查询点
        list_link_pro_belongs_to_s = each_path_contains_link[0]    #查看这个路径概率对应的外面的s是什么
        query_prob = max_prob * s_pdf_function_list[list_link_pro_belongs_to_s](delta_time)    #某个路段s对应的后验概率的最大值
        dict_result.setdefault(query_prob,(best_query_time,potential_path_set[each_path_contains_link[0]][each_path_contains_link[1]]
                                            ,potential_path_set[each_path_contains_link[0]]))   #保存字典,key为概率值,value为(最佳查询时间,最佳查询路段,该查询路段属于哪个路径)

    return sorted(dict_result.items(), lambda x, y: cmp(x[0], y[0]), reverse=True)  #返回一个排序过的带概率的list



#询问出租车车辆是不是在这个地方   输入一辆车在的路口以及需要查询的时间
#需要调用出租车位置的相关接口  然后返回true or false 判断车辆是不是在那里
def ask_taxi_if_exist(road_intersection1, road_intersection2, query_time):
    return True
    pass






#主要流程控制及调用
def main_flow(begin_time, end_time, begin_road_intersection, end_road_intersection):
    # 生成所有候选路段的一个集合
    potential_path_set = generate_potential_path_set(begin_time, end_time, begin_road_intersection, end_road_intersection)   #List(('12','32'),('12','45'),('22','63'))
    #下面的是测试数据
    potential_path_set = [('1007', '1009', '1122', '1186', '792', '814'),('1007', '1009', '1122', '1186', '792', '814','994')]

    # 生成S={s1,s2...sn}的pdf函数  需要传入当前可能的路径集合以及需要生成的时间段  这个时间是这个时段的起始时刻就好了
    s_pdf_function_list = generate_s_pdf_function_list(potential_path_set, begin_time)

    print 'pdf函数生成完毕1 '       # print s_pdf_function_list[0](70)    #输入任意的时间  是可以返回这个时间对应的概率

    potential_path_set = tools.translate_potential_path(potential_path_set)  #将候选集合的数据格式进行转换 将点的表示转换成边的表示

    road_link_prob = generate_query_point_position_with_order(potential_path_set,s_pdf_function_list, begin_time, end_time)  #生成一个按照概率从高到低的一个查询路段的排序  并且里面应至少包含有link的概率数据

    print '已经生成按照概率排序的link的集合 下面按照link概率的大小依次进行查询'

    #确定最佳的查询时间点  传入的参数:需要确定时间的路段(最佳的路段编号,最佳路段的概率),所有潜在路段的集合s,所有s的pdf函数集合.

    #返回的是 具有最大的概率的查询点,包括被查询路段  查询时间  查询路段的序列等
    best_query_time = generate_best_query_point_time(road_link_prob[0],potential_path_set,s_pdf_function_list, begin_time, end_time)
    print 'Best_query_result:',
    print best_query_time



    for each_link_prob in road_link_prob:  #对每一个路段确定一个查询时间  针对这个查询时间来询问出租车 得到一组正确或者错误的值 可以是最后某个link的组合的s达到一个概率的阀值之后  就输出这个序列
        query_time = generate_best_query_point_time(each_link_prob)   #在什么时间查这一段路获得的概率最大
        ask_result = ask_taxi_if_exist(each_link_prob,query_time)   #each_link_prob可以是一个元组 保存了多个信息

    result_set = potential_path_set[0]  #返回第几条结果作为最后的结果值
    # result_set = []  #结果集   是一个路段的集合
    return result_set  #返回查询结果





if __name__ == '__main__':
    main_flow('2012-03-05 07:18:18','2012-03-05 07:19:18','1000','947')
    potential_path_set = [('1007', '1009', '1122', '1186', '792', '814'),
                          ('1007', '1009', '1122', '1186', '792', '814', '994')]
    print tools.translate_potential_path(potential_path_set)
    print tools.re_translate_potential_path(tools.translate_potential_path(potential_path_set))

    dict = {}
    dict.setdefault('as',0.8)
    dict.setdefault('a1s', 0.5)
    dict.setdefault('a2s', 0.9)
    sorted1 = sorted(dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    print sorted1
    print type(sorted1)

