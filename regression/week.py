# coding=utf-8
import pandas as pd

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from datetime import datetime
from xgboost import XGBRegressor
import multiprocessing as mp

from lib.evaluation import *

# Global Variable
SHOP_NUMBER = 166
DT_GAP = 400
TOP_GOODSN = 10


df_goods_original = pd.read_csv("../sources/dim_goods.csv")
df_order_detail = pd.read_csv("../sources/df_order_detail.csv")
df_xgboost_full = pd.read_csv("../sources/df_xgboost_full.csv", index_col=0)

# get sum sales
df_sales_sum = df_order_detail[df_order_detail['store_id'] == SHOP_NUMBER].groupby(['goodsn']).agg({'sales': 'sum'})
# 按周单品预测

dt_full_min = df_xgboost_full['dt'].min()
dt_full_max = df_xgboost_full['dt'].max()
# top goodsn
# goodsn_list = [2004083, 2025696, 2017999, 2026253, 2032689, 2018602, 2032282, 2032104, 2004092, 2021667, 2033631,
#                2031883, 2004476, 2022441, 2029939, 2028359, 2032385, 2023289, 2032589, 2032587, 2032590, 2035177,
#                2031026, 2009767, 2036842, 2021662, 2003293, 2033373, 2025102, 2026853, 2034543, 2006304, 2017307,
#                2026686, 2004353, 2035864, 2032586, 2032284, 2021116, 2032921, 2018134, 2017997, 2003228, 2032361,
#                2034633, 2035707, 2004326, 2017286, 2034082, 2032588]
goodsn_list = df_xgboost_full[df_xgboost_full['store_id'] == SHOP_NUMBER]['goodsn'].unique()
print(len(goodsn_list))


def job(dt_min):
    y_tests = {}
    y_preds = {}
    dts = {}
    for dt in range(dt_min, dt_min + 1):
        # 取训练集
        train = df_xgboost_full[(df_xgboost_full['dt'] < dt) & (df_xgboost_full['goodsn'].isin(goodsn_list))]\
            .drop('dt', 1).drop('goodsn', 1)
        if len(train) == 0:
            continue
        x_train = train.iloc[:, 1:]
        y_train = train.iloc[:, 0]
        # 构建模型，调参方法为固定其他参数，使用数组定义需要调节的参数，不断逼近
        model = LGBMRegressor()
        # 训练
        model.fit(x_train, y_train)
        for goodsn in goodsn_list:
            # 取测试集
            test = df_xgboost_full[(df_xgboost_full['store_id'] == SHOP_NUMBER) \
                                   & (df_xgboost_full['goodsn'] == goodsn) \
                                   & (df_xgboost_full['dt'] == dt)].drop('dt', 1).drop('goodsn', 1)
            x_test = test.iloc[:, 1:]
            y_test = test.iloc[:, 0]
            if len(x_test) == 0 or len(y_test) == 0:
                continue
            y_pred = model.predict(x_test)
            y_tests.setdefault(goodsn, []).append(y_test.values[0])
            y_preds.setdefault(goodsn, []).append(y_pred[0])
            dts.setdefault(goodsn, []).append(dt)

            # feature importance
            # plt.figure(1, figsize=(20, 10))
            # plt.subplot(1,1,1)
            # feat_imp = pd.Series(model._Booster.get_fscore()).sort_values(ascending=False)
            # feat_imp.plot(kind='bar', title='Feature Importances', ax=plt.gca())
    return {'y_tests': y_tests, 'y_preds': y_preds, 'dts': dts}

# regression
pred_dts = []
for dt in range(dt_full_max - 30, dt_full_max):
    pred_dts.append(dt)
pool = mp.Pool()
res_list = pool.map(job, pred_dts)
pool.close()
pool.join()

# Arrangement data
y_tests = {}
y_preds = {}
y_sales = {}
dts = {}
full_dts = {}
# 补充更早数据
for goodsn in goodsn_list:
    y_past = df_xgboost_full[(df_xgboost_full['store_id'] == SHOP_NUMBER) & (df_xgboost_full['goodsn'] == goodsn) \
                             & (df_xgboost_full['dt'] < dt_full_max - 30)]
    for sales in y_past['sales'].values:
        y_sales.setdefault(goodsn, []).append(sales)
    for dt in y_past['dt'].values:
        full_dts.setdefault(goodsn, []).append(datetime.fromtimestamp(dt * (7 * 24 * 60 * 60)).date())

for res in res_list:
    for (goodsn, goodsn_y_tests) in res['y_tests'].items():
        for y_test in goodsn_y_tests:
            y_tests.setdefault(goodsn, []).append(y_test)
    for (goodsn, goodsn_y_preds) in res['y_preds'].items():
        for y_pred in goodsn_y_preds:
            y_preds.setdefault(goodsn, []).append(y_pred)
    for (goodsn, goodsn_y_tests) in res['y_tests'].items():
        for y_test in goodsn_y_tests:
            y_sales.setdefault(goodsn, []).append(y_test)
    for (goodsn, goodsn_dts) in res['dts'].items():
        for dt in goodsn_dts:
            dts.setdefault(goodsn, []).append(datetime.fromtimestamp(dt * (7 * 24 * 60 * 60)).date())
    for (goodsn, goodsn_dts) in res['dts'].items():
        for dt in goodsn_dts:
            full_dts.setdefault(goodsn, []).append(datetime.fromtimestamp(dt * (7 * 24 * 60 * 60)).date())

for goodsn in goodsn_list:
    if goodsn not in y_tests or len(y_tests.get(goodsn)) == 0:
        continue
    goods_name = df_goods_original[df_goods_original['goodsn'] == goodsn]['name']
    if len(goods_name) > 0:
        print('\tgoodsn: ' + str(goodsn))
        print('\tgoods_name: ' + str(goods_name.iloc[0]))
        print('\tsum(abs(r-p)/(r+1))/n: ' + str(rmsp_avg_1(y_tests.get(goodsn), y_preds.get(goodsn))))
        print('\tsum(abs(r-p))/sum(p): ' + str(rmsp_avg_5(y_tests.get(goodsn), y_preds.get(goodsn))))
        print('\tsum(abs(r-p))/sum(r): ' + str(rmsp_avg_5_2(y_tests.get(goodsn), y_preds.get(goodsn))))
        print('\tsum(abs(r-p)/max(r,p))/n: ' + str(rmsp_avg_6(y_tests.get(goodsn), y_preds.get(goodsn))))
        print('\tsum(min(abs(r-p)/(r+1),1))/n: ' + str(rmsp_avg_7(y_tests.get(goodsn), y_preds.get(goodsn))))
        print('\tsum(min(abs(r-p)/(p+1),1))/n: ' + str(rmsp_avg_8(y_tests.get(goodsn), y_preds.get(goodsn))))
        print('\tabs(r-p)/(r+1)>1 count: ' + str(rmsp_avg_9(y_tests.get(goodsn), y_preds.get(goodsn))))
        print('\tabs(r-p)/(p+1)>1 count: ' + str(rmsp_avg_10(y_tests.get(goodsn), y_preds.get(goodsn))))
        print('\tnot equal 0 count: ' + str(rmsp_avg_11(y_tests.get(goodsn), y_preds.get(goodsn))))
        print('\tgoods sales sum: ' + str(df_sales_sum.loc[goodsn].values[0]))
        print('\tgoods volatility: ' + str(get_volatility(y_tests.get(goodsn))))

        # draw sales chart
        plt.figure(1, figsize=(20, 7))
        plt.plot(full_dts.get(goodsn), y_sales.get(goodsn), color='grey', marker='o')
        plt.plot(dts.get(goodsn), y_preds.get(goodsn), color='red', marker='o')
        plt.savefig('../sources/imgs/' + str(goodsn) + '.png')
        plt.close('all')

