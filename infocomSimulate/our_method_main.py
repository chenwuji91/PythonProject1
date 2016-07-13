#-*- coding: UTF-8 -*-
'''
@author: chenwuji
实验主类   控制整个实验流程 调用相关的方法得到相关的结果
'''
import roadBasic as rd
rd.initRoadData()
rd.initTimeData()
import tools
import pick_from_route
# import getcarinfo
import random



#产生道路的所有候选路段的集合
def generate_potential_path_set(begin_time, end_time, begin_road_intersection, end_road_intersection):
    #调用张文的程序  根据时间生成一个有穷的集合 以List的形式保存
    # potential_set = [('256','425','593','214'), ('256','4235','5923','214'), ('256','4235','5493','214'),
    #                  ('256', '4225', '5793', '214'), ('256','4525','5393','214'), ('256','4625','5963','2714'),
    #                  ('256', '4425', '513', '214'), ('256','4275','6593','214'), ('256','4275','5933','214')]
    import roadDFS
    # print '开始搜索潜在路径'
    potential_set = roadDFS.searchAllRoad(begin_road_intersection, end_road_intersection , 300)
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
    return sorted(link_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True), probility_list_with_time_interval



#根据查询路段求积分生成最佳的查询时间   返回一个t  这个t最佳的查询时间 以及最佳的一个查询路段
def generate_best_query_point_time(most_likely_road_link, potential_path_set, s_pdf_function_list, begin_time, end_time, prob_of_s):
    init_time = 1
    delta_t = 6   #求解定积分的时候 时间的变化率
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

    prob_list_all = []
    #下面开始对包含这个link的所有路段开始求解积分的问题
    for each_path_contains_link in list_s_index_contains_most_likely_road_link: #对于每一个包含这个link的路段来求解时间
        #正常的情况是分成这几段   考虑边界情况呢?
        prob_list_of_one_link = []
        path_sb = potential_path_set[each_path_contains_link[0]][0:each_path_contains_link[1]]
        path_r = potential_path_set[each_path_contains_link[0]][each_path_contains_link[1]]
        path_r = [path_r]
        path_sa = potential_path_set[each_path_contains_link[0]][each_path_contains_link[1]+1:len(potential_path_set[each_path_contains_link[0]])]

        # print path_sb
        # print len(path_r)
        # print len(path_sb)
        fun1 = None
        fun3 = None
        if len(path_sb) > 0:
            fun1 = fsolve.potential_path_to_fsolve(tools.re_translate_one_potential_path(path_sb), begin_time, rd)
        # print path_r
        # print tools.re_translate_one_potential_path(path_r)
        # print begin_time
        fun2 = fsolve.potential_path_to_fsolve(tools.re_translate_one_potential_path(path_r), begin_time, rd)
        if len(path_sa) > 0:
            # print '!!'
            # print tools.re_translate_one_potential_path(path_sa)
            fun3 = fsolve.potential_path_to_fsolve(tools.re_translate_one_potential_path(path_sa), begin_time, rd)

        for i in range(init_time, delta_time, delta_t):  #对于每一个分块的时间间隔 时间离散化操作

            if fun1 and fun3:
                prob1 = dblquad.fun_2d(fun1, fun2, fun3, i, delta_time)  # 求解积分
            elif fun1:

                prob1 = dblquad.fun_1d_1(fun1, fun2, i, delta_time)

            elif fun3:

                prob1 = dblquad.fun_1d_2(fun2, fun3, i, delta_time)
            else:

                prob1 = dblquad.fun_1d_3(fun2, delta_time)

            prob_of_one_list_of_one_time_split = prob1[0]/s_pdf_function_list[each_path_contains_link[0]](delta_time) * prob_of_s[each_path_contains_link[0]]       #计算 P(trs|T)
            # print '输出一个概率:',
            # print prob1
            # print prob_of_one_list_of_one_time_split  # prob1
            prob_list_of_one_link.append(prob_of_one_list_of_one_time_split)  #计算 P(trs|T)
        prob_list_all.append(prob_list_of_one_link)


    prob_of_all_time_split = []
    for eachT in range(len(prob_list_all[0])):
        currentProb = 0.0
        for each_time_prob in prob_list_all:
            currentProb = currentProb + each_time_prob[eachT]
        prob_of_all_time_split.append(currentProb)

    print 'Final result :',
    print prob_of_all_time_split
    best_query_prob = max(prob_of_all_time_split)
    best_query_time_index = prob_of_all_time_split.index(best_query_prob)
    best_query_time = init_time + best_query_time_index * delta_t

    return best_query_time,best_query_prob #返回一个排序过的带概率的list



#询问出租车车辆是不是在这个地方   输入一辆车在的路口以及需要查询的时间
#需要调用出租车位置的相关接口  然后返回true or false 判断车辆是不是在那里
# def ask_taxi_if_exist(road_intersection1, road_intersection2, query_time):
#     # return True
#
#     # import pick_from_route
#     # import getcarinfo
#     # import random
#     taxi_car_location_list = getcarinfo.getCarInfo(query_time.split('\r')[0].split('\n')[0],road_intersection1,road_intersection2)
#     real_car_position = pick_from_route.getinfo(query_time.split('\r')[0].split('\n')[0]+'\n', '1')  #待检测的车辆的位置
#     if real_car_position[0] != road_intersection1 or real_car_position[1]!= road_intersection2:
#         print 'Query Fail...'
#         return False
#     for each_taxi in taxi_car_location_list:
#         taxi_position = each_taxi[3]
#         real_car_position = real_car_position[2]
#         if real_car_position - taxi_position < 150:
#             if random.uniform(0,100) < 80.0:
#                 print 'Query Successfully!'
#                 return True
#     print 'Query Fail...'
#     return False


def ask_taxi(road_intersection1, road_intersection2, query_time):

    real_car_position = pick_from_route.getinfo(query_time.split('\r')[0].split('\n')[0] + '\n', '1')  # 待检测的车辆的位置
    if real_car_position[0] == road_intersection1 and real_car_position[1] == road_intersection2:
        print 'Query Success...'
        return True
    else:
        print 'Query Fail...'
        return False





#主要流程控制及调用
def main_flow(begin_time, end_time, begin_road_intersection, end_road_intersection):
    print 'Searching potential path...'
    potential_path_set = generate_potential_path_set(begin_time, end_time, begin_road_intersection, end_road_intersection)   #List(('12','32'),('12','45'),('22','63'))
    print potential_path_set
    # potential_path_set = [('406', '463', '1303', '451', '1402', '1345', '1330', '1389', '1330', '1345', '1330', '1326'), ('406', '463', '128', '268', '451', '1402', '1264', '1402', '1264', '1402', '1264', '1344', '1264', '1330', '1326'), ('406', '463', '128', '172', '128', '268', '451', '99', '250', '1329', '1326'), ('406', '463', '25', '1137', '1303', '1284', '1402', '1264', '1330', '1345', '1330', '1326'), ('406', '463', '1303', '451', '268', '451', '1402', '1264', '1330', '1389', '1310', '1389', '1330', '1326'), ('406', '463', '1303', '451', '1402', '451', '1402', '1264', '1330', '1345', '1330', '1389', '1330', '1326'), ('406', '463', '128', '268', '451', '268', '451', '268', '451', '1402', '1284', '1382', '1264', '1330', '1326'), ('406', '463', '128', '172', '99', '451', '1402', '1264', '1330', '1326'), ('406', '463', '1303', '451', '99', '1345', '99', '1345', '1329', '250', '1329', '1326'), ('406', '463', '1303', '1284', '1402', '451', '1402', '1264', '1402', '451', '99', '1345', '1330', '1326'), ('406', '463', '1303', '1284', '1303', '451', '1402', '1264', '1402', '1345', '99', '250', '1329', '1326'), ('406', '463', '1303', '1284', '1402', '1345', '1330', '1389', '1310', '1389', '1282', '1333', '1396', '1326'), ('406', '463', '1303', '1284', '1382', '1384', '1382', '1384', '1336', '1268', '1388', '1268', '1344', '1264', '1330', '1326'), ('406', '463', '1303', '451', '268', '451', '268', '451', '268', '451', '1402', '1264', '1402', '1345', '1329', '1326'), ('406', '463', '1303', '1284', '1303', '1284', '1402', '1345', '99', '250', '1329', '1326'), ('406', '463', '1303', '1284', '1402', '1264', '1382', '1264', '1330', '1345', '1330', '1345', '1329', '1326'), ('406', '463', '128', '268', '451', '268', '451', '1303', '1284', '1402', '1345', '1330', '1345', '1330', '1326')]
    print 'Generating pdf...'
    # 生成S={s1,s2...sn}的pdf函数  需要传入当前可能的路径集合以及需要生成的时间段  这个时间是这个时段的起始时刻就好了
    s_pdf_function_list = generate_s_pdf_function_list(potential_path_set, begin_time)

    potential_path_set = tools.translate_potential_path(potential_path_set)  #将候选集合的数据格式进行转换 将点的表示转换成边的表示
    # print 'Generating road link probility order by prob desc...'#前面一个参数是按照概率排序的link的东西  后面是有几条序列 按照概率排序的那个东西
    road_link_prob,probility_list_with_time_interval = generate_query_point_position_with_order(potential_path_set,s_pdf_function_list, begin_time, end_time)  #生成一个按照概率从高到低的一个查询路段的排序  并且里面应至少包含有link的概率数据
    print 'Max Probility Path:', #开始循环来对每个路段询问出租车

    print tools.re_translate_one_potential_path(potential_path_set[probility_list_with_time_interval.index(max(probility_list_with_time_interval))])

    for i in range(len(road_link_prob)):
    #返回的是 具有最大的概率的查询点,包括被查询路段  查询时间  查询路段的序列等  还包括s的概率
        print 'Best_query_prob:',
        print road_link_prob[i]
        # print 'Generateing best query time...'
        best_query_time = generate_best_query_point_time(road_link_prob[i],potential_path_set,s_pdf_function_list, begin_time, end_time, probility_list_with_time_interval)
        print 'Best_query_time:',
        print best_query_time
        query_time = best_query_time   #在什么时间查这一段路获得的概率最大
        # ask_result = ask_taxi_if_exist(road_link_prob[i][0][0],road_link_prob[i][0][1],tools.increase_several_seconds(begin_time,query_time[0]))   #each_link_prob可以是一个元组 保存了多个信息
        ask_result = ask_taxi(road_link_prob[i][0][0],road_link_prob[i][0][1],tools.increase_several_seconds(begin_time,query_time[0]))   #each_link_prob可以是一个元组 保存了多个信息
        if ask_result == True:
            print 'Query recursive...'
            print 'From:'+str(begin_road_intersection)+',To:'+str(road_link_prob[i][0][0])
            print 'From:'+str(road_link_prob[i][0][1]) + ',To:' + str(end_road_intersection)
            if begin_road_intersection != str(road_link_prob[i][0][0]):
                result1 = main_flow(begin_time, tools.increase_several_seconds(begin_time,int(best_query_time[0])), begin_road_intersection,road_link_prob[i][0][0])
            else:
                result1 = [begin_road_intersection]
            if str(end_road_intersection) != str(road_link_prob[i][0][1]):
                result2 = main_flow(tools.increase_several_seconds(begin_time,int(best_query_time[0])), end_time, road_link_prob[i][0][1],end_road_intersection)
            else:
                result2 = [end_road_intersection]
            return  result1 + result2
    print 'Returning current query result...'
    return  tools.re_translate_one_potential_path(potential_path_set[probility_list_with_time_interval.index(max(probility_list_with_time_interval))])
  #如果循环做完  这一段没得查 就直接返回概率最大的路段





if __name__ == '__main__':
    print main_flow('2012-03-12 16:41:12','2012-03-12 16:45:00','1335','1378')
    # potential_path_set = [('1007', '1009', '1122', '1186', '792', '814'),
    #                       ('1007', '1009', '1122', '1186', '792', '814', '994')]
    # print tools.translate_potential_path(potential_path_set)
    # print tools.re_translate_potential_path(tools.translate_potential_path(potential_path_set))



