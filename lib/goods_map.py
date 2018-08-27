# coding=utf-8

# Digitization
def lifetype(row):
    if row['lifetype'] == '淘汰中' :
        return 1
    if row['lifetype'] == '已淘汰' :
        return 2
    if row['lifetype'] == '正常品' :
        return 3
    if row['lifetype'] == '新品' :
        return 4
    return 0

def storagetype(row):
    if row['storagetype'] == '20.常温整箱':
        return 1
    if row['storagetype'] == '1.休闲食品':
        return 2
    if row['storagetype'] == '3.酒':
        return 3
    if row['storagetype'] == '11.冷冻品':
        return 4
    if row['storagetype'] == '10.日配':
        return 5
    if row['storagetype'] == '9.休闲充饥':
        return 6
    if row['storagetype'] == '12.副食/冲饮':
        return 7
    if row['storagetype'] == '6.烟草':
        return 8
    if row['storagetype'] == '2.百货':
        return 9
    if row['storagetype'] == '7.社区商品':
        return 10
    if row['storagetype'] == '5.食品服务':
        return 11
    if row['storagetype'] == '4.自用':
        return 12
    if row['storagetype'] == '8.赠品':
        return 13
    return 0

