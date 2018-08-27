# coding=utf-8
import threading
from exporter.day_sale_exporter import print_evaluation, plt_draw, gen_predicts
from feature_engine import f_binning
import pandas as pd
lock = threading.Lock()
from datetime import datetime, timedelta
from global_sources import file_operation

def get_n_day_ago(dt, n):
    tmp=datetime.strptime(dt, "%Y-%m-%d")
    n_time = tmp + timedelta(days=-n)
    n_nyr = n_time.strftime('%Y-%m-%d')
    return n_nyr

# predict job
def proba_job(dt, df_simple, df_label):
    train_label = df_label[(df_label['rundate'] < dt)].drop('rundate', 1)
    test_label = df_label[(df_label['rundate'] == dt)].drop('rundate', 1)
    result = {}
    if len(train_label) > 0 and len(test_label) > 0:
        result = {'y_test': test_label.values[0], 'y_pred': train_label['result'].mean()}
    if result:
        result['rundate'] = dt
    return result

def day_regression(store_id, goodsn_list, df_feature_full, date_max, gap=30):
    # make label as int
    df_feature_full['result'] = df_feature_full['result'].astype(int)

    df_results = pd.DataFrame()
    for goodsn in goodsn_list:
        df_goods_full = df_feature_full[(df_feature_full['goodscode']==goodsn) &
                                  (df_feature_full['storeid']==store_id)].drop('goodscode', 1).drop('storeid', 1)
        if len(df_goods_full) == 0:
            continue
        # binning
        df_goods_full = f_binning.binner_engine(df_goods_full)
        # get date range
        pred_dts = [x.strftime('%Y-%m-%d') for x in pd.date_range(end=date_max, periods=gap).tolist()]
        # single process predict
        res_list = []
        for pred_dt in pred_dts:
            day_ago = get_n_day_ago(pred_dt, 7)
            df_goods_full = df_goods_full[df_goods_full['rundate'] > day_ago]
            # feature and label
            df_feature = df_goods_full.drop('result', 1)
            df_label = df_goods_full[['result', 'rundate']]
            res_list.append(proba_job(pred_dt, df_feature, df_label))
        #exporter
        if not print_evaluation(goodsn, res_list):
            continue
        succ, result = gen_predicts(goodsn, res_list)
        if not succ:
            continue
        df_results = pd.concat([df_results, result], ignore_index=True)
    return df_results

if __name__ == '__main__':
    store_list = [605]
    df_feature_full = file_operation.read_feature_full()
    for store_id in store_list:
        print(store_id)
        # all goodsn
        # goodsn_list = df_feature_full[df_feature_full['storeid']==store_id]['goodscode'].unique()
        goodsn_list = [
            2034504, 2034848, 2004083, 2017999, 2026253, 2006304, 2035740, 2034849, 2026686, 2006293, 2003293,
            2012607, 2027203, 2035517, 2025102, 2009767, 2018602, 2032085, 2013793, 2009198, 2017307, 2003280,
            2005738, 2021116, 2032010, 2032507, 2004092, 2036328, 2013789, 2015440, 2031681, 2029744, 2040199,
            2005812, 2025103, 2007020, 2004476, 2013791, 2025104, 2030543, 2025106, 2004326, 2029099, 2003228,
            2005831, 2019198, 2004120, 2005855, 2005773, 2026207, 2038324, 2025107, 2018124, 2003286, 2036137,
            2032508, 2038325, 2035797, 2036136, 2026679, 2032689, 2036937, 2036333, 2036276, 2034566, 2036846,
            2025105, 2040198, 2035555, 2029635, 2038250, 2025398, 2038689, 2017286, 2040732, 2036135, 2036277,
            2005800, 2021612, 2026473, 2026646, 2033868, 2026470, 2035552, 2032334, 2004998, 2032284, 2033601,
            2022117, 2037993, 2034554, 2033796, 2026471, 2031364, 2022457, 2035544, 2027020, 2040123, 2032361,
            2037523
        ]
        df_predict_result = day_regression(store_id, goodsn_list, df_feature_full, '2018-06-12', gap=60)
        file_operation.write_predicts(df_predict_result, store_id)