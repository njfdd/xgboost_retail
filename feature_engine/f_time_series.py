import pandas as pd

from global_sources import file_operation
from lib.time_series import *

gap_list = [3, 7, 15, 60]


def gen_time_series_features(df_feature_full):
    goodsn_list = df_feature_full['goodscode'].unique()
    store_ids = df_feature_full['storeid'].unique()
    gap_results = []
    for _ in gap_list:
        gap_results.append({'max': pd.Series([]), 'min': pd.Series([]),
                            'var': pd.Series([]), 'std': pd.Series([]),
                            'sum': pd.Series([]), })
    for goodsn in goodsn_list:
        for store_id in store_ids:
            df_goods = df_feature_full[
                (df_feature_full['storeid'] == store_id) & (df_feature_full['goodscode'] == goodsn)]
            y = [v for i, v in df_goods['saleqty'].items()]
            for gap in gap_list:
                gap_max = time_series_max(y, gap)
                gap_min = time_series_min(y, gap)
                gap_var = time_series_var(y, gap)
                gap_std = time_series_std(y, gap)
                gap_sum = time_series_sum(y, gap)
                gap_result = gap_results[gap_list.index(gap)]
                gap_result['max'] = pd.concat([gap_result['max'], pd.Series(gap_max, index=df_goods.index)])
                gap_result['min'] = pd.concat([gap_result['min'], pd.Series(gap_min, index=df_goods.index)])
                gap_result['var'] = pd.concat([gap_result['var'], pd.Series(gap_var, index=df_goods.index)])
                gap_result['std'] = pd.concat([gap_result['std'], pd.Series(gap_std, index=df_goods.index)])
                gap_result['sum'] = pd.concat([gap_result['sum'], pd.Series(gap_sum, index=df_goods.index)])
    for gap in gap_list:
        gap_result = gap_results[gap_list.index(gap)]
        df_feature_full["max_%d" % gap] = gap_result['max']
        df_feature_full["min_%d" % gap] = gap_result['min']
        df_feature_full["var_%d" % gap] = gap_result['var']
        df_feature_full["std_%d" % gap] = gap_result['std']
        df_feature_full["sum_%d" % gap] = gap_result['sum']
    return df_feature_full


if __name__ == '__main__':
    df_future_feature = file_operation.read_feature_full()
    df_future_feature = gen_time_series_features(df_future_feature)
    file_operation.write_feature_full(df_future_feature)
