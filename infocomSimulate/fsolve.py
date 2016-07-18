#-*- coding: UTF-8 -*-
'''
@author: chenwuji
fsolve解决对数正态叠加的问题
'''
import math
from scipy import stats
from scipy.optimize import fsolve
import numpy as np
current_para0_12 = 0.0
current_para3 = 0.0

def f(x):#需要求解的函数表达式
    para12 = current_para0_12
    para3 = current_para3
    # print '越界检查: '
    # print 'x:',
    # print x
    # print 'para3:',
    # print para3
    # print 'para12:',
    # print para12
    # print 'math.pow(math.e,(1 + x ** 2)/para3):',
    # print long(math.pow(math.e,long(1 + x ** 2)/para3))
    # print '(stats.norm.cdf(2 * x / (para3)):',
    # print stats.norm.cdf(2 * x / (para3))
    # print '(2 * math.pow(stats.norm.cdf(x/(para3)),2)):',
    # print (2 * math.pow(stats.norm.cdf(x/(para3)),2))
    return para12 - math.pow(math.e,(1 + x ** 2)/para3) * \
                 (stats.norm.cdf(2 * x / math.sqrt(para3))/(2 * math.pow(stats.norm.cdf(x/math.sqrt(para3)),2))) + 1


def fsolve_main(list):#传入的参数是一系列路段的均值和标准差  返回是是最后一个函数表达式
    mean_list = []
    std_list = []
    std_list_3 = []
    para0_list = []
    para1_list = []
    for each_e in list:
        mean_list.append(each_e[0])
        std_list.append(each_e[1])
        std_list_3.append(1/(each_e[1] ** 2))
        # print math.pow(math.e, each_e[0]) * math.pow(math.e, 0.5 * math.pow(each_e[1], 2))
        para1_list.append(math.pow(math.e, each_e[0]) * math.pow(math.e, 0.5 * math.pow(each_e[1], 2)))
        # para0_list.append(math.pow(math.e,2 * each_e[0]) * math.pow(math.e,each_e[1] ** 2) * (math.pow(math.e,each_e[1] **2 )-1))
    para12_list =[]
    sum_para1 = sum(para1_list) #** 2
    # print sum_para1
    for each_e in list:
        para12_list.append(math.pow(math.e,2 * each_e[0])/sum_para1 * math.pow(math.e,0.5 * math.pow(each_e[1], 2))/sum_para1 * math.pow(math.e,0.5 * math.pow(each_e[1], 2)) * (math.pow(math.e,each_e[1] **2 )-1))

    global current_para0_12,current_para3
    # current_para0_12 = sum(para0_list)/(sum(para1_list) ** 2)
    current_para0_12 = sum(para12_list)
    current_para3 = sum(std_list_3)
    import copy
    std_list_3_3 = copy.deepcopy(std_list_3)
    del std_list_3_3[std_list.index(max(std_list))]

    # if ((max(std_list) ** 2 * sum(std_list_3_3)))<= 0:
    #     print 'Error!@',
    #     print (max(std_list) ** 2 * sum(std_list_3_3))
    #     print std_list
    #     print std_list_3

    lam0_0 = (max(std_list) ** 2 * sum(std_list_3_3))
    # lam0_0 = max(lam0_0,0)
    # lam0 = math.sqrt(max(std_list) ** 2 * sum(std_list_3) - 1)  #初始值
    lam0 = math.sqrt(lam0_0)  # 初始值
    # print lam0

    result = fsolve(f, lam0)
    # print 'The Result of fsolve is:',
    # print result[0]
    return result[0]





def lognorm_together(list2):
    list3 = list2

    lamx = fsolve_main(list3)
    w = math.sqrt((1+lamx**2)/current_para3)
    para4_list = []
    for eache in list3:
        para4_list.append(math.pow(math.e,eache[0]) * math.pow(math.e, eache[1]**2 / 2))
    kesai = math.log(sum(para4_list)) - 0.5 * math.pow(w,2) - math.log(stats.norm.cdf(lamx/math.sqrt(current_para3)))

    # print (lamx,w,kesai)
    # def f_all(x):
    #     return 2/w * stats.norm.cdf(lamx * (x - kesai) / w) * stats.norm.pdf((x-kesai)/w)

    def f_all(x):
        return 2/(w * x) * stats.norm.cdf(lamx * (math.log(x,math.e) - kesai) / w) * stats.norm.pdf((math.log(x,math.e)-kesai)/w)

    return f_all

import tools
def potential_path_to_fsolve(each_s, query_date, rd):

    ifweekend = tools.getDay(query_date)  # 需要查询的日期是否为周末
    current_s_para = []
    for i in range(len(each_s) - 1):  # 总共应该是有这么多的路径数量  这里有时候会有数据取不到  要处理数据娶不到的情况
        current_variance = rd.getRoadTimeVariance(each_s[i], each_s[i + 1], str(tools.timeTranslate(query_date)),ifweekend)
        current_mean = rd.getRoadTimeAvg(each_s[i], each_s[i + 1], str(tools.timeTranslate(query_date)), ifweekend)
        current_s_para.append((current_mean, current_variance))
        current_s_fun = lognorm_together(current_s_para)
    return current_s_fun



if __name__ == '__main__':
    # list1 = [(15.4917964029,9.56449200606),(6.23520584451,1.76698180473),(13.0138494961,15.2115357424),(55.23,1.21),(40.23,0.21),(80.23,0.21),\
    #          (53.23, 3.231), (32.23, 1.21), (67.23, 0.71), (55.23, 0.21), (40.23, 0.21), (80.23, 0.21),\
    #          (53.23, 3.21), (32.23, 4.21), (67.23, 3.71), (55.23, 1.21), (40.23, 0.21), (80.23, 0.21)]
    # list1 = [(32.23,4.21),(67.23,3.71),(55.23,6.21)]  #The Result is: [ 2.21945729]
    # list1 = [(15.4917964029,9.56449200606),(6.23520584451,1.76698180473),(13.0138494961,15.2115357424), \
    #          (5.28634405453,1.97354017235),(11.9316260856,2.34496399376),(6.95264124673,3.24797882694),\
    #          (52.3885333696,21.98853101919),(63.2465241129,26.54005441778),\
    #          (9.38593382001,5.16847622414),(6.68359389297,2.32071881279),(30.9760940609,9.47560323993), \
    #          (9.17911893004,3.25901281406),(13.5129791325,4.33189533705),(60.8518612079,16.4789071949),(6.68359389297,2.32071881279),(30.9760940609,9.47560323993), \
    #          (9.17911893004,3.25901281406),(13.5129791325,4.33189533705)]
    list1 = [(15.4917964029, 9.56449200606), (6.23520584451, 1.76698180473), (13.0138494961, 15.2115357424), \
             (5.28634405453, 1.97354017235), (11.9316260856, 2.34496399376), (6.95264124673, 3.24797882694),\
             (7.24977271634, 4.105039055), (12.3885333696, 4.98853101919), (13.2465241129, 6.54005441778)]
    function = lognorm_together(list1)
    # print f
    x = np.linspace(-1000,1000)
    print function(53.28)
    # plt.plot(x, function(x), 'r-', alpha=0.6, label='norm pdf')
    # plt.show()
    print function(99)
    print function(1)
    print function(95)
    print function(85)
    print function(75)
    print function(88)
    print function(1000)
    print function(60)
    print function(70)
    print function(100)

    print function(200)
    print function(300)
    print function(400)
    # list =  [1.0,4.0,9.0,16.0]
    # print sum(math.sqrt(list))
