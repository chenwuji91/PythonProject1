#-*- coding: UTF-8 -*-
'''
@author: chenwuji
fsolve解决对数正态叠加的问题
'''
import math
from scipy import stats
from scipy.optimize import fsolve
current_para0_12 = 0.0

current_para3 = 0.0

def f(x):


    para12 = current_para0_12
    para3 = current_para3

    print '越界检查: '
    print 'x:',
    print x
    print 'para3:',
    print para3
    print 'para12:',
    print para12
    print 'math.pow(math.e,(1 + x ** 2)/para3):',
    print long(math.pow(math.e,long(1 + x ** 2)/para3))
    print '(stats.norm.cdf(2 * x / (para3)):',
    print stats.norm.cdf(2 * x / (para3))
    print '(2 * math.pow(stats.norm.cdf(x/(para3)),2)):',
    print (2 * math.pow(stats.norm.cdf(x/(para3)),2))

    return para12 - math.pow(math.e,(1 + x ** 2)/para3) * \
                 (stats.norm.cdf(2 * x / math.sqrt(para3))/(2 * math.pow(stats.norm.cdf(x/math.sqrt(para3)),2))) + 1


def lognorm_together(list):#传入的参数是一系列路段的均值和标准差  返回是是最后一个函数表达式
    mean_list = []
    std_list = []
    std_list_3 = []
    para0_list = []
    para1_list = []
    for each_e in list:
        mean_list.append(each_e[0])
        std_list.append(each_e[1])
        std_list_3.append(1/(each_e[1] ** 2))
        para0_list.append(math.pow(math.e,2 * each_e[0]) * math.pow(math.e,each_e[1] ** 2) * (math.pow(math.e,each_e[1] **2 )-1))
        para1_list.append(math.pow(math.e,each_e[0]) * math.pow(math.e, 0.5 * math.pow(each_e[1],2)))


    global current_para0_12,current_para3
    current_para0_12 = sum(para0_list)/(sum(para1_list) ** 2)
    current_para3 = sum(std_list_3)

    lam0 = math.sqrt(max(std_list) ** 2 + sum(std_list_3) - 1)  #初始值
    print lam0


    result = fsolve(f, lam0)
    print 'The Result is:',
    print result
    pass




if __name__ == '__main__':
    # list1 = [(15.4917964029,9.56449200606),(6.23520584451,1.76698180473),(13.0138494961,15.2115357424),(55.23,1.21),(40.23,0.21),(80.23,0.21),\
    #          (53.23, 3.231), (32.23, 1.21), (67.23, 0.71), (55.23, 0.21), (40.23, 0.21), (80.23, 0.21),\
    #          (53.23, 3.21), (32.23, 4.21), (67.23, 3.71), (55.23, 1.21), (40.23, 0.21), (80.23, 0.21)]
    # list1 = [(32.23,4.21),(67.23,3.71),(55.23,6.21)]  #The Result is: [ 2.21945729]
    list1 = [(15.4917964029,9.56449200606),(6.23520584451,1.76698180473),(13.0138494961,15.2115357424), \
             (5.28634405453,1.97354017235),(11.9316260856,2.34496399376),(6.95264124673,3.24797882694),\
             (7.24977271634,4.105039055),(12.3885333696,4.98853101919),(13.2465241129,6.54005441778),\
             (9.38593382001,5.16847622414),(6.68359389297,2.32071881279),(30.9760940609,9.47560323993), \
             (9.17911893004,3.25901281406),(13.5129791325,4.33189533705)]
    # list1 = [(15.4917964029, 9.56449200606), (6.23520584451, 1.76698180473), (13.0138494961, 15.2115357424), \
    #          (5.28634405453, 1.97354017235), (11.9316260856, 2.34496399376), (6.95264124673, 3.24797882694),\
    #          (7.24977271634, 4.105039055), (12.3885333696, 4.98853101919), (13.2465241129, 6.54005441778)]
    lognorm_together(list1)
    # list =  [1.0,4.0,9.0,16.0]
    # print sum(math.sqrt(list))
