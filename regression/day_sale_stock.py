# coding=utf-8
import threading

from feature_engine import f_binning

lock = threading.Lock()

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

from global_sources import file_operation
from job import xg_multi_classifier, xg_regression

from lib.evaluation import *

# Global Variable
DT_GAP = 400
TOP_GOODSN = 10


def stock_job(dt, df_simple, df_label):
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

def sale_job(dt, df_simple, df_label):
    train_simple = df_simple[(df_simple['rundate'] < dt)].drop('rundate', 1)
    train_label = df_label[(df_label['rundate'] < dt)].drop('rundate', 1)
    test_simple = df_simple[(df_simple['rundate'] == dt)].drop('rundate', 1)
    test_label = df_label[(df_label['rundate'] == dt)].drop('rundate', 1)
    result = {}
    if len(train_label) > 0 and len(test_label) > 0:
        result = xg_regression.predict(train_simple, train_label.iloc[:,0], test_simple, test_label.iloc[:,0])
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
        res_stock_list = []
        res_sale_list = []
        for pred_dt in pred_dts:
            res_stock_list.append(stock_job(pred_dt, df_simple, df_label))
            res_sale_list.append(sale_job(pred_dt, df_simple, df_label))

        # Arrangement data
        df_draw = df_simple
        df_draw['rundate'] = df_draw['rundate'] + timedelta(days=-2)
        df_draw = df_draw[df_draw['rundate'] > (rundate_max - timedelta(days=gap)).strftime('%Y-%m-%d')]
        y_tests = []
        y_stock_preds = []
        y_sale_preds = []
        stock_dts = []
        sale_dts = []
        for res in res_stock_list:
            if not res:
                continue
            y_tests.append(res['y_test'])
            y_stock_preds.append(res['y_pred'])
            stock_dts.append(res['rundate'])
        for res in res_sale_list:
            if not res:
                continue
            y_sale_preds.append(res['y_pred'])
            sale_dts.append(res['rundate'])
        if len(y_stock_preds) == 0 or len(y_sale_preds) == 0:
            continue
        y_tests = np.array(y_tests)
        y_stock_preds = np.array(y_stock_preds)
        y_sale_preds = np.array(y_sale_preds)
        print('goodsn: ' + str(goodsn))
        print('\tmean(stock): ' + str(df_draw['stockqty'].mean()))
        print('\tmean(sales): ' + str(y_tests.mean()))
        print('\tmean(predict_stock): ' + str(y_stock_preds.mean()))
        print('\tcount(stock<0): ' + str(len(df_draw[df_draw['stockqty']<0])))
        print('\tpredict_stock<sales: ' + str(np.sum(y_stock_preds < y_tests)))
        print('\tcount(sales): ' + str(len(y_tests)))
        print('\tmape: ' + str(mape(y_tests, y_sale_preds)))

        # draw sales chart
        plt.figure(1, figsize=(20, 7))
        plt.plot(df_draw['rundate'], df_draw['saleqty'], color='#6aa84f', marker='o')
        plt.plot(df_draw['rundate'], df_draw['stockqty']+df_draw['saleqty'], color='black', marker='o')
        plt.plot([datetime.strptime(d, '%Y-%m-%d').date() for d in stock_dts], y_stock_preds, color='red', marker='o')
        plt.plot([datetime.strptime(d, '%Y-%m-%d').date() for d in sale_dts], y_sale_preds, color='#FFA500', marker='o')
        plt.savefig('../sources/' + str(store_id) + '_' + str(goodsn) + '.png')
        plt.close('all')

        df_result = pd.DataFrame(stock_dts, columns=['rundate'])
        df_result['stock_pred'] = y_stock_preds
        df_result['sale_pred'] = y_sale_preds
        df_result['sales'] = y_tests
        df_result['goodsn'] = goodsn
        df_results.append(df_result)
    df_results_detail = pd.concat(df_results, ignore_index=True)
    return df_results_detail

if __name__ == '__main__':
    store_list = [166]
    df_feature_full = file_operation.read_feature_full()
    for store_id in store_list:
        # all goodsn
        # goodsn_list = df_feature_full[df_feature_full['storeid']==store_id]['goodscode'].unique()
        goodsn_list = [
            2004083,
            2005413,
            2036844,
            2035864,
            2026210,
        ]
        print(str(datetime.now()))
        df_predict_result = day_regression(store_id, goodsn_list, df_feature_full, gap=60)
        print(str(datetime.now()))
        file_operation.write_predicts(df_predict_result, store_id)