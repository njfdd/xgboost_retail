# coding=utf-8
import threading
from exporter.day_sale_exporter import print_evaluation, plt_draw, gen_predicts, corr_evaluation, write_corr
from feature_engine import f_binning
import pandas as pd

from global_sources.top_goods import top_goodsn_list_561
from job.xg_cv import get_best_paras

lock = threading.Lock()
from global_sources import file_operation
from job import xg_regression,sk_gdbt,xg_multi_classifier


def get_paras(train_dt_end, df_simple, df_label):
    train_simple = df_simple[(df_simple['rundate'] < train_dt_end)].drop('rundate', 1)
    train_label = df_label[(df_label['rundate'] < train_dt_end)].drop('rundate', 1)
    return get_best_paras(train_simple, train_label)

# sale predict job
def sale_job(paras, dt, df_simple, df_label):
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

def interval_regression(df_feature_full, train_begin, test_day):
    # make label as int
    df_feature_full['result'] = df_feature_full['result'].astype(int)

    storeid_list = df_feature_full['storeid'].unique()
    goodsn_list = df_feature_full['goodscode'].unique()

    df_results_out = pd.DataFrame()
    df_corr = pd.DataFrame()
    for store_id in storeid_list:
        for goodsn in goodsn_list:
            # filter data
            df_goods_full = df_feature_full[
                (df_feature_full['goodscode'] == goodsn)
                & (df_feature_full['storeid'] == store_id)
                & (df_feature_full['rundate'] >= train_begin)
                & (df_feature_full['rundate'] <= test_day)
            ].drop('goodscode', 1).drop('storeid', 1)
            if len(df_goods_full) == 0:
                continue

            # binning
            df_goods_full = f_binning.binner_engine(df_goods_full)

            # get feature and label
            df_feature = df_goods_full.drop('result', 1)
            df_label = df_goods_full[['result', 'rundate']]

            # get best parameters
            # paras = get_paras(pred_dts[0], df_feature, df_label)
            paras = {}

            # single process predict
            res_stock_list = []
            res_sale_list = []
            res_sale_list.append(sale_job(paras, test_day, df_feature, df_label))
            res_stock_list.append(stock_job(test_day, df_feature, df_label))


            # # generate plt draw data
            # df_draw = df_goods_full
            # df_draw = df_draw[df_draw['rundate'] >
            #                   (datetime.strptime(test_begin, "%Y-%m-%d") - timedelta(days=20)).strftime('%Y-%m-%d')]
            # # exporter
            # if not print_evaluation(goodsn, res_list):
            #     continue
            # if not plt_draw(store_id, goodsn, df_draw, res_list):
            #     continue
            succ, result = gen_predicts(store_id, goodsn, res_sale_list, res_stock_list)
            if not succ:
                continue

            #result
            df_results_out = pd.concat([df_results_out, result], ignore_index=True)
            #feature corr output
            df_corr = corr_evaluation(df_corr, store_id, goodsn, df_goods_full)


    write_corr(df_corr)
    return df_results_out

if __name__ == '__main__':
    train_begin = '2017-02-01'
    test_day = '2018-06-14'
    df_feature_full = file_operation.read_feature_full()
    df_predict_result = interval_regression(df_feature_full, train_begin, test_day)
    file_operation.write_predicts(df_predict_result, test_day)
