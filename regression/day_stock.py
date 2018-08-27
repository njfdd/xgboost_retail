# coding=utf-8
import threading

from feature_engine import f_binning

lock = threading.Lock()

import pandas as pd
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from global_sources import file_operation
from job import xg_multi_classifier


from lib.evaluation import *

# Global Variable
DT_GAP = 400
TOP_GOODSN = 10


def proba_job(dt, df_simple, df_label):
    train_simple = df_simple[(df_simple['rundate'] < dt)].drop('rundate', 1)
    train_label = df_label[(df_label['rundate'] < dt)].drop('rundate', 1)
    test_simple = df_simple[(df_simple['rundate'] == dt)].drop('rundate', 1)
    test_label = df_label[(df_label['rundate'] == dt)].drop('rundate', 1)
    result = {}
    if len(train_label) > 0 and len(test_label) > 0:
        result = xg_multi_classifier.predict(train_simple, train_label.iloc[:,0], test_simple, test_label.iloc[:,0])
    if result:
        result['rundate'] = dt
    return result

def day_regression(store_id, goodsn_list, df_feature_full, gap=30):
    df_feature_full['result'] = df_feature_full['result'].astype(int)

    df_results = []
    for goodsn in goodsn_list:
        df_data = df_feature_full[(df_feature_full['goodscode']==goodsn) & (df_feature_full['storeid']==store_id)]\
            .drop('goodscode', 1).drop('storeid', 1)
        df_simple = df_data.drop('result', 1)
        df_label = df_data[['result', 'rundate']]

        # get date range
        rundate_max = df_simple['rundate'].max()
        if rundate_max == 'nan' or str(rundate_max) == 'NaT':
            continue
        df_simple = f_binning.binner_engine(df_simple)
        df_max = rundate_max.strftime('%Y-%m-%d')
        pred_dts = [x.strftime('%Y-%m-%d') for x in pd.date_range(end=df_max, periods=gap).tolist()]

        # single process
        res_list = []
        for pred_dt in pred_dts:
            res_list.append(proba_job(pred_dt, df_simple, df_label))

        # Arrangement data
        df_draw = df_simple
        df_draw['rundate'] = df_draw['rundate'] + timedelta(days=-2)
        df_draw = df_draw[df_draw['rundate'] > (rundate_max - timedelta(days=gap)).strftime('%Y-%m-%d')]
        y_tests = []
        y_preds = []
        dts = []
        for res in res_list:
            if not res:
                continue
            y_tests.append(res['y_test'])
            y_preds.append(res['y_pred'])
            dts.append(res['rundate'])
        if len(y_preds) == 0:
            continue
        y_preds = np.array(y_preds)
        y_tests = np.array(y_tests)
        print('goodsn: ' + str(goodsn))
        print('\tmean(stock): ' + str(df_draw['endqty'].mean()))
        print('\tmean(sales): ' + str(y_tests.mean()))
        print('\tmean(predict_stock): ' + str(y_preds.mean()))
        print('\tcount(stock<0): ' + str(len(df_draw[df_draw['endqty']<0])))
        print('\tpredict_stock<sales: ' + str(np.sum(y_preds < y_tests)))
        print('\tcount(sales): ' + str(len(y_tests)))

        # draw sales chart
        plt.figure(1, figsize=(20, 7))
        plt.plot(df_draw['rundate'], df_draw['saleqty'], color='#6aa84f', marker='o')
        # plt.plot(df_draw['rundate'], df_draw['stockqty'], color='black', marker='o')
        plt.plot([datetime.strptime(d, '%Y-%m-%d').date() for d in dts], y_preds, color='red', marker='o')
        plt.savefig('../sources/' + str(store_id) + '_' + str(goodsn) + '.png')
        plt.close('all')

        df_result = pd.DataFrame(dts, columns=['rundate'])
        df_result['pred'] = y_preds
        df_result['sales'] = y_tests
        df_result['goodsn'] = goodsn
        df_results.append(df_result)
    df_results_detail = pd.concat(df_results, ignore_index=True)
    return df_results_detail

if __name__ == '__main__':
    store_list = [561]
    df_feature_full = file_operation.read_feature_full()
    for store_id in store_list:
        # all goodsn
        # goodsn_list = df_feature_full[df_feature_full['storeid']==store_id]['goodscode'].unique()
        goodsn_list = [
            2025696, 2032587, 2032590, 2004083, 2032589, 2032104, 2033631, 2035865, 2031883, 2032586, 2031175, 2026253,
            2021667, 2028679, 2020075, 2035864, 2034082, 2028698, 2034078, 2026686, 2004476, 2034286, 2006304, 2028680,
            2004326, 2032085, 2003228, 2032284, 2009767, 2035834, 2004353, 2035061, 2005364, 2021116, 2004092, 2005413,
            2034844, 2017307, 2034280, 2021927, 2036297, 2025105, 2021928, 2023591, 2032282, 2018241, 2034279, 2035037,
            2024836, 2023289, 2005812, 2025102, 2025107, 2008982, 2032385, 2024892, 2035740, 2004482, 2021662, 2025535,
            2026210, 2026853, 2035517, 2030994, 2027203, 2025106, 2032722, 2025103, 2013791, 2013793, 2032659, 2031364,
            2017286, 2034520, 2018124, 2017293, 2013136, 2003239, 2006293, 2033756, 2026625, 2034543, 2025104, 2029939,
            2034697, 2026473, 2017999, 2036717, 2036842, 2026471, 2029398, 2015440, 2035554, 2027020, 2013789, 2003354,
            2036298, 2027021, 2022531, 2027818,
        ]
        print(str(datetime.now()))
        df_predict_result = day_regression(store_id, goodsn_list, df_feature_full, gap=60)
        print(str(datetime.now()))
        file_operation.write_predicts(df_predict_result, store_id)