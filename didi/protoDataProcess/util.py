#-*- coding: UTF-8 -*-
'''
@author: chenwuji
工具类  保存常用的函数  无状态组件 每个函数单独作用
'''

from datetime import datetime

def timeTranslate(date):
    h = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").hour
    m = datetime.strptime(date, "%Y-%m-%d %H:%M:%S").minute
    timeSplit = int((h * 60 + m)/10) + 1
    return timeSplit
