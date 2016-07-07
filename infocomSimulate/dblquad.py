#-*- coding: UTF-8 -*-
'''
@author: chenwuji
求解二重积分的demo
'''

import numpy as np
from scipy import integrate
from scipy import stats

def half_sphere(x, y):
    return (1-x**2-y**2)**0.5

def half_circle(x):
    return (1-x**2)**0.5


#注意 这个norm到后面换成新的那个整体的概率密度函数  现在暂时用标准正态分布函数做一个代替  到时候具体的函数可以作为一个参数传入这里
def fun_2d(fun1, fun2, fun3, t, T, fun4, fun5 ):
    print t
    print fun1(30)
    print fun2[0](5, 1,fun2[1], fun2[2])
    print fun3(20)

    def f(a1, a2):
        print a1
        print a2
        print T - a1 - a2
        return fun1(a1) * fun2[0](a2, 1,fun2[1], fun2[2]) * fun3(T - a1 -a2)

    return integrate.dblquad(f, 0, t, fun4, fun5)


if __name__ == '__main__':
    pass
    # result1 = integrate.dblquad(half_sphere, -1, 1,
    #               lambda x: -half_circle(x),
    #               lambda x: half_circle(x))
    # print result1
    #     dblquad(func2d, a, b, gfun, hfun)
    # 对于func2d(x,y)函数进行二重积分，其中a,b为变量x的积分区间，而gfun(x)到hfun(x)为变量y的积分区间
