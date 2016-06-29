#-*- coding: UTF-8 -*-
'''
@author: chenwuji
'''

import numpy as np
from scipy import stats
logsample = stats.norm.rvs(loc=10, scale=3, size=1000) # logsample ~ N(mu=10, sigma=3)
sample = np.exp(logsample) # sample ~ lognormal(10, 3)
shape, loc, scale = stats.lognorm.fit(sample, floc=0) # hold location to 0 while fitting
print shape, loc, scale
# Out[61]: (2.9212650122639419, 0, 21318.029350592606)
print np.log(scale), shape # mu, sigma
# Out[62]: (9.9673084420467362, 2.9212650122639419)