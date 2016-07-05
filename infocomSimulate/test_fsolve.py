#-*- coding: UTF-8 -*-
'''
@author: chenwuji
测试fsolve
'''


import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
# fig, ax = plt.subplots(1, 1)
# norm1 = norm
# print norm
# print norm.cdf(2)
#
# from scipy import stats
# import matplotlib.pyplot as plt
# x = np.linspace(stats.norm.ppf(0.01,30,3.56), stats.norm.ppf(0.99,30,3.56), 100)
# # x = np.linspace(-1, 1, 100)
# plt.plot(x, stats.norm.pdf(x,30,3.56), 'r-', alpha=0.6, label='norm pdf')
# plt.show()

# x = np.linspace(norm.ppf(0.01),norm.ppf(0.99), 100)
# # ax.plot(x, norm.pdf(x),'r-', lw=5, alpha=0.6, label='norm pdf')
# print 'x'
# print x
#
# from scipy import stats
# import matplotlib.pyplot as plt
# x = np.linspace(stats.norm.ppf(0.01), stats.norm.ppf(0.99), 100)
# plt.plot(x, stats.norm.pdf(x), 'r-', alpha=0.6, label='norm pdf')
# plt.show()


from scipy.optimize import fsolve
from math import cos



def f(x):
    d = 140
    l = 156
    a = float(x[0])
    r = float(x[1])
    return [
        cos(a) - 1 + (d*d)/(2*r*r),
        l - r * a
    ]
result = fsolve(f, [1, 1])
print result