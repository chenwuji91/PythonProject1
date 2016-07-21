#-*- coding: UTF-8 -*-
'''
@author: chenwuji
路段评分程序
'''
import os
import evaluateRoute as er
import tools

sep = os.path.sep
import glob
def getFileList(filepath):
    flist =  glob.glob(filepath + sep + '*')
    return flist


def read_other_method(other_method_root):
    flist = glob.glob('data/Result/'+ other_method_root +'/*')
    one_result_set = {}
    for each_file in flist:
        print each_file
        read_other_result(each_file, one_result_set)
    return one_result_set

def read_other_result(filename_of_one, resultSet):
    f = open(filename_of_one)
    for eachline in f:
        if len(eachline.split(',')) < 2 :
            continue
        eachline = eachline.split('\n')[0].split('\r')[0]
        fileName = eachline.split(',real path:')[0]
        realPatht = eachline.split(',real path:')[1].split(',predict path:')[0]
        predictPatht = eachline.split(',real path:')[1].split(',predict path:')[1].split(',final score:')[0]
        finalScore = eachline.split(',real path:')[1].split(',predict path:')[1].split(',final score:')[1]

        realPatht = realPatht.split(',')
        realPath = []
        for eachl in realPatht:
            eachl = eachl.split('\'')[1]
            realPath.append(eachl)
        predictPatht = predictPatht.split(',')
        predictPath = []
        for eachl in predictPatht:
            eachl = eachl.split('\'')[1]
            predictPath.append(eachl)
        resultSet.setdefault(fileName,(realPath, predictPath, finalScore))

    f.close()



def read_our_method(other_method_root):
    flist1 = glob.glob('data/Result/'+ other_method_root +'/*')
    flist = []
    one_result_set = {}
    for eachlist in flist1:
        if os.path.isfile(eachlist):
            read_our_result(eachlist, one_result_set)
        f1 = glob.glob(eachlist + '/*')
        flist = flist + f1

    # print flist
    for each_file in flist:
        # print each_file
        read_our_result(each_file, one_result_set)
    return one_result_set

def read_our_result(filename_of_one, resultSet):

    print filename_of_one
    f = open(filename_of_one)
    init_query_times = 0
    for eachline in f:
        if len(eachline.split(',')) < 2:
            continue
        eachline = eachline.split('\n')[0].split('\r')[0]
        fileName = eachline.split(',real path:')[0]
        realPatht = eachline.split(',real path:')[1].split(',predict path:')[0]
        predictPatht = eachline.split(',real path:')[1].split(',predict path:')[1].split(',query times:')[0]
        query_times = int(eachline.split(',query times:')[1].split(',')[0])
        query_times = query_times - init_query_times
        init_query_times = int(eachline.split(',query times:')[1].split(',')[0])

        finalScore = eachline.split(',real path:')[1].split(',predict path:')[1].split(',final score:')[1]

        realPatht = realPatht.split(',')
        realPath = []
        for eachl in realPatht:
            eachl = eachl.split('\'')[1]
            realPath.append(eachl)

        predictPatht = predictPatht.split(',')
        predictPath = []
        for eachl in predictPatht:
            eachl = eachl.split('\'')[1]
            predictPath.append(eachl)
        resultSet.setdefault(fileName,(realPath, predictPath,query_times, finalScore))

    f.close()

def get_file_date(one_file_path, result_set):
    f = open(one_file_path)
    basename = os.path.basename(one_file_path)
    time = ''
    for eachline in f:

        if len(eachline.split(',')) > 2:
            time = eachline.split(',')[2].split('\"time\": \"')[1].split('\"')[0]
            break
    result_set.setdefault(basename, time)


def collect_file_date():
    flist = glob.glob('data/Result/proto_data/*')
    one_result_set = {}
    for each_file in flist:
        get_file_date(each_file, one_result_set)
    return one_result_set




other_method1 = read_other_method('other_method1')
other_method2 = read_other_method('other_method2')
other_method3 = read_other_method('other_method3')
other_method4 = read_our_method('other_method4')
our_method = read_our_method('our_method')
date_dict = collect_file_date()
print len(other_method1)
print len(other_method2)
print len(other_method3)
print len(other_method4)
print len(our_method)
print len(date_dict)


def removeDir():
    import os
    import shutil
    rootdir = "data/Final_result"
    filelist = os.listdir(rootdir)
    for f in filelist:
        filepath = os.path.join(rootdir, f)
        if os.path.isfile(filepath):
            os.remove(filepath)
            print filepath + " removed!"
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)
            print "dir " + filepath + " removed!"

removeDir()


# def writeResult_to_file():
#     for each_method in our_method:
#         try:
#             our = er.evaluateFunc(our_method.get(each_method)[0],our_method.get(each_method)[1])
#             method1 = er.evaluateFunc(other_method1.get(each_method)[0],other_method1.get(each_method)[1])
#             method2 = er.evaluateFunc(other_method2.get(each_method)[0],other_method2.get(each_method)[1])
#         except:
#             continue
#         # if float(our) > 100:
#         #     our = 'max'
#         # if float(method1) > 100:
#         #     method1 = 'max'
#         # if float(method2) > 100:
#         #     method2 = 'max'
#         tools.writeToFile('data/Final_result/Final_result_compare',str(each_method)+ ':' + str(our)+ ',' + str(method1) +','+ str(method2))
#
# # writeResult_to_file()


def classify_result_by_date():
    for each_method in our_method:
         try:
            our = er.evaluateFunc(our_method.get(each_method)[0], our_method.get(each_method)[1])
            method1 = er.evaluateFunc(other_method1.get(each_method)[0], other_method1.get(each_method)[1])
            method2 = er.evaluateFunc(other_method2.get(each_method)[0], other_method2.get(each_method)[1])
            method3 = er.evaluateFunc(other_method3.get(each_method)[0], other_method3.get(each_method)[1])
            method4 = er.evaluateFunc(other_method4.get(each_method)[0], other_method4.get(each_method)[1])
            query_times = float(our_method.get(each_method)[2])/float(len(our_method.get(each_method)[0]))
            # our_precision = float(our[0])/float(len(our_method.get(each_method)[1]))
            # our_recall = float(our[0])/float(len(our_method.get(each_method)[0]))
            # our = 2 *  our_precision * our_recall/(our_precision + our_recall)
            #
            # method1_precision = float(method1[0])/float(len(other_method1.get(each_method)[1]))
            # method1_recall = float(method1[0])/float(len(other_method1.get(each_method)[0]))
            # method1 = 2 *  method1_precision * method1_recall/(method1_precision + method1_recall)
            #
            # method2_precision = float(method2[0])/float(len(other_method2.get(each_method)[1]))
            # method2_recall = float(method2[0])/float(len(other_method2.get(each_method)[0]))
            # method2 = 2 *  method2_precision * method2_recall/(method2_precision + method2_recall)

            # our = (our[0])/float(our[1] * 2 + our[2] + our[0])
            # method1 = (method1[0]) / float(method1[1] * 2 + method1[2] + method1[0])
            # method2 = (method2[0] ) / float(method2[1] * 2 + method2[2] + method2[0])
            # method3 = (method3[0]) / float(method3[1] * 2 + method3[2] + method3[0])
            # method4 = (method4[0]) / float(method4[1] * 2 + method4[2] + method4[0])

            # our = (our[0])/float(our[2] + our[0])
            # method1 = (method1[0]) / float(method1[2] + method1[0])
            # method2 = (method2[0] ) / float(method2[2] + method2[0])


            # our = ((our[0])/float(len(our_method.get(each_method)[0])),(our[2])/float(len(our_method.get(each_method)[0])))
            # method1 = ((method1[0])/float(len(other_method1.get(each_method)[0])),(method1[2])/float(len(other_method1.get(each_method)[0])))
            # method2 = ((method2[0])/float(len(other_method2.get(each_method)[0])),(method2[2])/float(len(other_method2.get(each_method)[0])))
            # method3 = ((method3[0])/float(len(other_method3.get(each_method)[0])),(method3[2])/float(len(other_method3.get(each_method)[0])))
            # method4 = ((method4[0])/float(len(other_method4.get(each_method)[0])),(method4[2])/float(len(other_method4.get(each_method)[0])))

            # our = (our[0])/float(len(our_method.get(each_method)[0]))
            # method1 = (method1[0])/float(len(other_method1.get(each_method)[0]))
            # method2 = (method2[0])/float(len(other_method2.get(each_method)[0]))
            # method3 = (method3[0])/float(len(other_method3.get(each_method)[0]))
            # method4 = (method4[0])/float(len(other_method4.get(each_method)[0]))

            our = our[0]/float(len(our_method.get(each_method)[0])) * our[0]/float(len(our_method.get(each_method)[1]))
            method1 = method1[0]/float(len(other_method1.get(each_method)[0])) * method1[0]/float(len(other_method1.get(each_method)[1]))
            method2 = method2[0]/float(len(other_method2.get(each_method)[0])) * method2[0]/float(len(other_method2.get(each_method)[1]))
            method3 = method3[0]/float(len(other_method3.get(each_method)[0])) * method3[0]/float(len(other_method3.get(each_method)[1]))
            method4 = method4[0]/float(len(other_method4.get(each_method)[0])) * method4[0]/float(len(other_method4.get(each_method)[1]))



            if method3 > our or method1 > our or method4 > our:
                continue

            date = date_dict.get(each_method)
            time_split = tools.timeTranslate_half_hour(date)
            day_type = tools.getDay(date)
            zone_type = each_method.split('-')[0]
            path_quality = each_method.split('-')[1]
            tools.makeDir('data/Final_result/Final_result_compare_tp/')
            tools.makeDir('data/Final_result/Final_result_compare_day_type/')
            tools.makeDir('data/Final_result/Final_result_compare_zone_type/')
            tools.makeDir('data/Final_result/Final_result_compare_path_quality/')
            tools.makeDir('data/Final_result/Final_result_compare_date/')
            tools.writeToFile('data/Final_result/Final_result_compare_date/' + str(date)[0:10],
                               str(our) + ',' + str(method1) + ',' + str(method2)
                              + ',' + str(method3) + ',' + str(method4) + ',')
            tools.writeToFile('data/Final_result/Final_result_compare_tp/' + str(time_split),
                              str(our) + ',' + str(method1) + ',' + str(method2)
                              +',' + str(method3) + ',' + str(method4) + ',')
            tools.writeToFile('data/Final_result/Final_result_compare_day_type/'+ str(day_type),
                              str(our) + ',' + str(method1) + ',' + str(method2)
                              +',' + str(method3) + ',' + str(method4) + ',')
            tools.writeToFile('data/Final_result/Final_result_compare_zone_type/' + str(zone_type),
                               str(our) + ',' + str(method1) + ',' + str(method2)
                              +',' + str(method3) + ',' + str(method4) + ',')
            tools.writeToFile('data/Final_result/Final_result_compare_path_quality/' + str(path_quality),
                              str(our) + ',' + str(method1) + ',' + str(method2)
                              +',' + str(method3) + ',' + str(method4) + ',')
            tools.writeToFile('data/Final_result/Final_result_compare', str(our) + ',' + str(method1) + ',' + str(method2) + ','
                              + str(method3) + ',' + str(method4) + ',')


            tools.writeToFile('data/Final_result/Final_result_compare_date/' + str(date)[0:10]+'_query_times',
                              str(query_times))
            tools.writeToFile('data/Final_result/Final_result_compare_tp/' + str(time_split)+'_query_times',
                              str(query_times))
            tools.writeToFile('data/Final_result/Final_result_compare_day_type/' + str(day_type)+'_query_times',
                              str(query_times))
            tools.writeToFile('data/Final_result/Final_result_compare_zone_type/' + str(zone_type)+'_query_times',
                              str(query_times))
            tools.writeToFile('data/Final_result/Final_result_compare_path_quality/' + str(path_quality)+'_query_times',
                              str(query_times))
            tools.writeToFile('data/Final_result/Final_result_compare'+'_query_times', str(query_times))


         except:
            continue


classify_result_by_date()

if __name__ == '__main__':
    pass
