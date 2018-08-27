# coding=utf-8

# Digitization
def week(row):
    if row['week'] == '星期一' :
        return 1
    if row['week'] == '星期二' :
        return 2
    if row['week'] == '星期三' :
        return 3
    if row['week'] == '星期四' :
        return 4
    if row['week'] == '星期五' :
        return 5
    if row['week'] == '星期六' :
        return 6
    if row['week'] == '星期日' :
        return 7
    return 0
def workday(row):
    if row['workday'] == 'no' :
        return 0
    if row['workday'] == 'yes' :
        return 1
    return 0
def weather(row):
    if row['weather'] == '霾~晴':
        return 1
    if row['weather'] == '晴~霾':
        return 2
    if row['weather'] == '霾':
        return 3
    if row['weather'] == '小雪':
        return 4
    if row['weather'] == '阴~晴':
        return 5
    if row['weather'] == '晴':
        return 6
    if row['weather'] == '多云~小雪':
        return 7
    if row['weather'] == '晴~多云':
        return 8
    if row['weather'] == '多云~晴':
        return 9
    if row['weather'] == '多云':
        return 10
    if row['weather'] == '晴~阴':
        return 11
    if row['weather'] == '多云~阴':
        return 12
    if row['weather'] == '小雪~阴':
        return 13
    if row['weather'] == '阴~多云':
        return 14
    if row['weather'] == '小雨~阴':
        return 15
    if row['weather'] == '阴~小雨':
        return 16
    if row['weather'] == '小雨':
        return 17
    if row['weather'] == '雨夹雪~阴':
        return 18
    if row['weather'] == '阴':
        return 19
    if row['weather'] == '扬沙~晴':
        return 20
    if row['weather'] == '晴~阵雨':
        return 21
    if row['weather'] == '阴~阵雨':
        return 22
    if row['weather'] == '小到中雨~阴':
        return 23
    if row['weather'] == '阵雨~晴':
        return 24
    if row['weather'] == '阵雨~多云':
        return 25
    if row['weather'] == '小雨~晴':
        return 26
    if row['weather'] == '阴~雷阵雨':
        return 27
    if row['weather'] == '雷阵雨~阴':
        return 28
    if row['weather'] == '阵雨~小到中雨':
        return 29
    if row['weather'] == '大雨':
        return 30
    if row['weather'] == '雷阵雨':
        return 31
    if row['weather'] == '阵雨~阴':
        return 32
    if row['weather'] == '雷阵雨~多云':
        return 33
    if row['weather'] == '多云~雷阵雨':
        return 34
    if row['weather'] == '阵雨':
        return 35
    if row['weather'] == '雷阵雨~中到大雨':
        return 36
    if row['weather'] == '小雨~阵雨':
        return 37
    if row['weather'] == '中雨~阵雨':
        return 38
    if row['weather'] == '中雨~小到中雨':
        return 39
    if row['weather'] == '雷阵雨~晴':
        return 40
    if row['weather'] == '雷阵雨~中雨':
        return 41
    if row['weather'] == '多云~阵雨':
        return 42
    if row['weather'] == '小雨~多云':
        return 43
    if row['weather'] == '多云~雾':
        return 44
    if row['weather'] == '阴~小雪':
        return 45
    if row['weather'] == '小雪~多云':
        return 46
    return 0
def holiday(row):
    if row['holiday'] == '元旦':
        return 0
    if row['holiday'] == 'Na':
        return 1
    if row['holiday'] == '腊八':
        return 2
    if row['holiday'] == '小年':
        return 3
    if row['holiday'] == '春节':
        return 4
    if row['holiday'] == '元宵节':
        return 5
    if row['holiday'] == '情人节':
        return 6
    if row['holiday'] == '妇女节':
        return 7
    if row['holiday'] == '清明节':
        return 8
    if row['holiday'] == '劳动节':
        return 9
    if row['holiday'] == '青年节':
        return 10
    if row['holiday'] == '立夏':
        return 11
    if row['holiday'] == '母亲节':
        return 12
    if row['holiday'] == '端午节':
        return 13
    if row['holiday'] == '儿童节':
        return 14
    if row['holiday'] == '父亲节':
        return 15
    if row['holiday'] == '夏至':
        return 16
    if row['holiday'] == '立秋':
        return 17
    if row['holiday'] == '七夕':
        return 18
    if row['holiday'] == '教师节':
        return 19
    if row['holiday'] == '国庆节':
        return 20
    if row['holiday'] == '中秋节':
        return 21
    if row['holiday'] == '立冬':
        return 22
    if row['holiday'] == '感恩节':
        return 23
    if row['holiday'] == '冬至':
        return 24
    if row['holiday'] == '圣诞节':
        return 25
    if row['holiday'] == '立春':
        return 26
    return 0
def wind(row):
    if row['wind'] == '南风1-2级':
        return 0
    if row['wind'] == '北风1-2级':
        return 1
    if row['wind'] == '无持续风向微风':
        return 2
    if row['wind'] == '北风3-4级':
        return 3
    if row['wind'] == '东南风1-2级':
        return 4
    if row['wind'] == '北风5-6级':
        return 5
    if row['wind'] == '西南风1-2级':
        return 6
    if row['wind'] == '东北风4-5级':
        return 7
    if row['wind'] == '北风4-5级':
        return 8
    if row['wind'] == '西南风3-4级':
        return 9
    if row['wind'] == '南风3-4级':
        return 10
    if row['wind'] == '东风1-2级':
        return 11
    if row['wind'] == '西北风1-2级':
        return 12
    if row['wind'] == '西北风4-5级':
        return 13
    if row['wind'] == '东北风3-4级':
        return 14
    if row['wind'] == '东北风1-2级':
        return 15
    if row['wind'] == '西风1-2级':
        return 16
    if row['wind'] == '西北风3-4级':
        return 17
    if row['wind'] == '西北风5-6级':
        return 18
    if row['wind'] == '东南风3-4级':
        return 19
    return 0

def wind_level(wind_level):
    if wind_level == '微风':
        return 1
    if wind_level == '1-2级':
        return 2
    if wind_level == '微风~3-4级':
        return 3
    if wind_level == '3-4级~微风':
        return 4
    if wind_level == '3-4级':
        return 5
    if wind_level == '3-4级~4-5级':
        return 6
    if wind_level == '微风~4-5级':
        return 7
    if wind_level == '4-5级~微风':
        return 8
    if wind_level == '3-4级~4-5级':
        return 9
    if wind_level == '3-4级~5-6级':
        return 10
    if wind_level == '4-5级~3-4级':
        return 11
    if wind_level == '4-5级':
        return 12
    if wind_level == '4-5级~5-6级':
        return 13
    if wind_level == '5-6级~3-4级':
        return 14
    if wind_level == '5-6级~4-5级':
        return 15
    if wind_level == '5-6级~微风':
        return 16
    if wind_level == '5-6级':
        return 17
    if wind_level == '6-7级~5-6级':
        return 18
    if wind_level == '6-7级':
        return 19
    return 0

def week_day(week_day):
    if week_day == '星期一' :
        return 1
    if week_day == '星期二' :
        return 2
    if week_day == '星期三' :
        return 3
    if week_day == '星期四' :
        return 4
    if week_day == '星期五' :
        return 5
    if week_day == '星期六' :
        return 6
    if week_day == '星期日' :
        return 7
    return 0