# -*- coding: UTF-8 -*-
"""
@author: lbx
获取当前时间、指定路段上的,所有出租车信息
date，from, to =>[taxi1, taxi2, taxi3,...],taxi=(id,x,y,距离from)
"""
import os
# import roadBasic as rd
import tools
rd = None

carFiles = {}   # 所有出租车读入的详细信息
carNames = []   # 所有出租车的名字，即ID


def initCarFiles(rd1):
    """
    读入全部车辆基础数据
    :return: 写入全局变量 carFiles中
    """
    if rd != None:
        return
    global rd
    global carFiles
    global carNames
    rd = rd1
    # rd.initRoadData()
    car_path_files = rd.getCarDataList()
    # [详细信息[（fro,to,距离）,（fro,to,距离）...]，该段区间平均速度，开始时间，结束时间，unknown，导航距离，直线距离]
    print("start init car files...")
    for eachL in car_path_files:
        car_name = os.path.basename(eachL).split('.data')[0]  # 文件名  车Id
        carNames.append(car_name)
        eachObj = rd.getCarObj(eachL)  # 一辆车一天的数据
        carFiles[car_name] = eachObj
    print("init car files done")

def int2str0(n):
    if n >= 10:
        return str(n)
    return '0' + str(n)

def str2int(s):
    """
    :param s='2012-03-02 10:22:23':
    :return: 当天从0时起经过的秒数
    """
    s1 = s.split(' ')[1].split(':')
    return int(s1[0]) * 3600 + int(s1[1]) * 60 + int(s1[2])
def int2str(n):
    hour = n / 3600
    minute = (n % 3600) / 60
    second = n % 60
    return int2str0(hour) + ':' + int2str0(minute) + ':' + int2str0(second)
def getCarInfo(time, fro, to):
    time = '2012-03-02' + time[10:19]
    fro = fro.split('\r')[0].split('\n')[0]
    to = to.split('\r')[0].split('\n')[0]
    # print '&&&&&&&&&',
    # print fro,
    # print ',',
    # print to,
    # print ',',
    # print time,
    # print ',',

    matched_car = []
    for car in carNames:
        for period in carFiles[car]:
            if period[2] <= time <= period[3]:  # 匹配时间区段成功
                index = 0
                d = 0.0
                t = str2int(time) - str2int(period[2])  # 查询时刻在当前区间段过去的时间
                avg_speed = period[1] / 3.6  # speed= m/s
                dis = avg_speed * t  # 从该区间起始位置走过的一系列距离和
                for dat in period[0]:   # 查阅该时间段内的记录
                    if d + dat[2] >= dis >= d:  # 根据走过的距离，看落在哪个路段上
                        if dat[0] == fro and dat[1] == to:  # 匹配到完全吻合的路段                           
                            fro_xy = rd.getRoadPointLocation(fro)   # 获取from路口的坐标
                            to_xy  = rd.getRoadPointLocation(to)
                            length = rd.getRoadLen(fro, to)  # from-》to路段总长度
                            dto = d + dat[2] - dis  # 求当前位置离to的距离
                            if index == len(period[0]) - 1:  # 边界特殊处理
                                dto += length - dat[2]
                            dfrom = length - dto
                            percent  = dto / length    # 根据当前距离from的距离计算出比重
                            x0  =   fro_xy[0] + (to_xy[0] - fro_xy[0]) * percent
                            y0  =   fro_xy[1] + (to_xy[1] - to_xy[1]) * percent
                            matched_car.append((car, x0, y0, dfrom))
                            break   # 成功匹配到，压入list后退出
                    d += dat[2]
                    index += 1
                break   # 时间段匹配成功，但无需求数据，跳出，进行下一辆车查找
    # print 'Successfully asked the car and return:',
    # print matched_car
    return matched_car

def car_route(carname):
    """
    根据车辆名称得到该车辆一天的轨迹
    :param carname: 车辆名，即文件名
    :return: [(路口id，时间，平均速度)]
    """
    route = []
    #pre_to = -1
    for period in carFiles[carname]:
        d = 0.0
        t = str2int(period[3]) - str2int(period[2])
        left = len(period[0])
        for dat in period[0]:
            if left <= 1:   # 长度为1，则扔掉
                break
            left -= 1
            d += dat[2]
            if rd.judgeBounds(dat[1]):
                #dat[1] != pre_to and
                percent = d / period[5]
                t0 = period[2].split(' ')[0] + ' ' + int2str(str2int(period[2]) + int(t * percent))
                route.append((dat[1], t0, period[1]))

    return route

def getCarRoutes():
    """
    输出格式如下：
    [{"num": "865", "speed": 20, "time": "2016-10-1-12:00"},
    {"num": "1180", "speed": 20, "time": "2016-10-1-12:00"},
    ...
    {"num": "1180", "speed": 20, "time": "2016-10-1-12:00"}]
    :return:
    """
    tools.makeDir('car_route')
    for car in carNames:        # 遍历所有车辆
        r = car_route(car)  # 获得路径
        if len(r) <= 0:
            print("empty route file:%s"%car)
            continue
        with open('car_route' + os.path.sep + car, 'w') as f:   # 写输出文件
            print("write file %s"%car)
            f.write('[')
            for i in range(len(r) - 1):
                f.write("""{"num": "%s", "speed": %d, "time": "%s"},\n"""%(r[i][0], r[i][2], r[i][1]))
            try:
                f.write("""{"num": "%s", "speed": %d, "time": "%s"}]""" % (r[len(r)-1][0], r[len(r)-1][2], r[len(r)-1][1]))
            except:
                print("error:%s" % str(r[i]))

  # 读入所有车辆信息
# getCarRoutes()  # 生成所有车辆路径信息，并写入文本
# print("all task done")

if "__main__" == __name__:
    import  roadBasic as rd1
    rd1.initRoadData()

    initCarFiles(rd1)
    while True:

        s = raw_input("please input: time,from,to;format like:2012-03-07 07:18:09,1027,887\n")
        s = s.split(',')
        print getCarInfo(s[0], s[1], s[2])
