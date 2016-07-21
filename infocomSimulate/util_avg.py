#-*- coding: UTF-8 -*-
'''
@author: chenwuji
常用工具类
'''

def get_data(path):
    avg_our = []
    avg_method1 = []
    avg_method2 = []
    avg_method3 = []
    avg_method4 = []

    f = open(path)
    for eachline in f:
        list = eachline.split('\r')[0].split('\n')[0].split(':')[1].split(';')
        avg_our.append(float(list[0]))
        avg_method1.append(float(list[1]))
        # avg_method2.append(float(list[2]))
        avg_method3.append(float(list[3]))
        # avg_method4.append(float(list[4]))
    import numpy as np
    # print np.mean(avg_our),
    # print np.mean(avg_method1),
    # print np.mean(avg_method2),
    # print np.mean(avg_method3),
    # print np.mean(avg_method4)
    np.std(avg_our)
    return np.mean(avg_our),np.mean(avg_method1),np.mean(avg_method2),\
           np.mean(avg_method3),np.mean(avg_method4)


import glob
import os
def file_list():
    flist = []
    f = glob.glob('data/Final_result/*')
    for f1 in f:
        if os.path.isfile(f1):
            flist.append(f1)
        else:
            f2 = glob.glob(f1 + '/*')
            for f3 in f2:
                flist.append(f3)
    return flist
import tools
flist = file_list()
for eachf in flist:
    # print eachf,
    # print get_data(eachf)
    result = str(get_data(eachf))
    tools.writeToFile('data/Final_result/final.csv', str(eachf)+ ',' + result[1:len(result)-1])