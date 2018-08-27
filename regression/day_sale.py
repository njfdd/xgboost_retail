# coding=utf-8
import threading
from exporter.day_sale_exporter import print_evaluation, plt_draw, gen_predicts, corr_evaluation, write_corr
from feature_engine import f_binning
import pandas as pd

from global_sources.top_goods import *
from job.xg_cv import get_best_paras

lock = threading.Lock()
from datetime import datetime, timedelta
from global_sources import file_operation
from job import xg_regression,sk_gdbt


def get_paras(dt, df_simple, df_label):
    train_simple = df_simple[(df_simple['rundate'] < dt)].drop('rundate', 1)
    train_label = df_label[(df_label['rundate'] < dt)].drop('rundate', 1)
    return get_best_paras(train_simple, train_label)

# predict job
def proba_job(paras, dt, df_simple, df_label):
    train_simple = df_simple[(df_simple['rundate'] < dt)].drop('rundate', 1)
    train_label = df_label[(df_label['rundate'] < dt)].drop('rundate', 1)
    test_simple = df_simple[(df_simple['rundate'] == dt)].drop('rundate', 1)
    test_label = df_label[(df_label['rundate'] == dt)].drop('rundate', 1)
    result = {}
    if len(train_label) > 0 and len(test_label) > 0:
        result = xg_regression.predict(paras, train_simple, train_label.iloc[:,0], test_simple, test_label.iloc[:,0])
    if result:
        result['rundate'] = dt
    return result

def day_regression(store_id, goodsn_list, df_feature_full, date_max, gap=30):
    # make label as int
    df_feature_full['result'] = df_feature_full['result'].astype(int)

    df_results = pd.DataFrame()
    df_corr = pd.DataFrame()
    for goodsn in goodsn_list:
        df_goods_full = df_feature_full[(df_feature_full['goodscode']==goodsn) &
                                  (df_feature_full['storeid']==store_id)].drop('goodscode', 1).drop('storeid', 1)
        if len(df_goods_full) == 0:
            continue
        # binning
        df_goods_full = f_binning.binner_engine(df_goods_full)
        # feature and label
        df_feature = df_goods_full.drop('result', 1)
        df_label = df_goods_full[['result', 'rundate']]
        # get date range
        pred_dts = [x.strftime('%Y-%m-%d') for x in pd.date_range(end=date_max, periods=gap).tolist()]
        # get best parameters
        dt_min = pred_dts[0]
        paras = get_paras(dt_min, df_feature, df_label)
        # paras = {}
        # single process predict
        res_list = []
        for pred_dt in pred_dts:
            res_list.append(proba_job(paras, pred_dt, df_feature, df_label))
        # generate plt draw data
        df_draw = df_feature
        df_draw['rundate'] = df_draw['rundate'] + timedelta(days=-2)
        df_draw = df_draw[df_draw['rundate'] >
                          (datetime.strptime(date_max, "%Y-%m-%d") - timedelta(days=gap+20)).strftime('%Y-%m-%d')]
        #exporter
        if not print_evaluation(goodsn, res_list):
            continue
        if not plt_draw(store_id, goodsn, df_draw, res_list):
            continue
        succ, result = gen_predicts(goodsn, res_list)
        if not succ:
            continue
        df_results = pd.concat([df_results, result], ignore_index=True)
        #feature corr output
        df_corr = corr_evaluation(df_corr, store_id, goodsn, df_goods_full)
    write_corr(df_corr)
    return df_results

if __name__ == '__main__':
    store_list = [561]
    df_feature_full = file_operation.read_feature_full()
    for store_id in store_list:
        print(store_id)
        # all goodsn
        # goodsn_list = df_feature_full[df_feature_full['storeid']==store_id]['goodscode'].unique()
        goodsn_list = [
            2026507
        ]
        df_predict_result = day_regression(store_id, top_goodsn_list_561, df_feature_full, '2018-07-15', gap=60)
        file_operation.write_predicts(df_predict_result, store_id)