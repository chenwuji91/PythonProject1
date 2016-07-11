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


def fun_1d_1(fun1, fun2,t, T):
    def f(x):

        return fun1(x) * fun2(T-x)
    return integrate.quad(f, 0, t, epsabs=1.49e-05, epsrel=1.49e-05)



def fun_1d_2(fun2, fun3,t, T):
    def f(x):

        return fun2(x) * fun3(T-x)
    return integrate.quad(f, t, T, epsabs=1.49e-05, epsrel=1.49e-05)


def fun_1d_3(fun2, T):
    def f(x):

        return fun2(x)
    return integrate.quad(f, 0, T, epsabs=1.49e-05, epsrel=1.49e-05)



#注意 这个norm到后面换成新的那个整体的概率密度函数  现在暂时用标准正态分布函数做一个代替  到时候具体的函数可以作为一个参数传入这里
def fun_2d(fun1, fun2, fun3, t, T):
    def f(a1, a2):
        # return fun1(a1) * stats.lognorm.pdf(a2, 1,fun2[0], fun2[1]) * fun3(T - a1 -a2)
        return fun1(a1) * fun2(a2) * fun3(T - a1 - a2)

    return integrate.dblquad(f, 0, t, lambda ax:t - ax, lambda ax: T-ax, epsabs=1.49e-05, epsrel=1.49e-05)


if __name__ == '__main__':
    pass
    # result1 = integrate.dblquad(half_sphere, -1, 1,
    #               lambda x: -half_circle(x),
    #               lambda x: half_circle(x))
    # print result1
    #     dblquad(func2d, a, b, gfun, hfun)
    # 对于func2d(x,y)函数进行二重积分，其中a,b为变量x的积分区间，而gfun(x)到hfun(x)为变量y的积分区间


    # import matplotlib.pyplot as plt
    # x = np.linspace(-100, 200)
    # plt.plot(x, stats.lognorm.pdf(x, 1,fun2[0], fun2[1]), 'r-', alpha=0.6, label='norm pdf')
    # plt.show()
    # print 'Notice warning!!'
    # print stats.lognorm.pdf(2.91179910784, 1,fun2[0], fun2[1])
    # pass
