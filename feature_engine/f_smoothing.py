import pandas as pd
import warnings

from global_sources import file_operation

warnings.filterwarnings('ignore')
from lib.holt_winters import *


def smoothing(df_feature_full):
    goodsn_list = df_feature_full['goodscode'].unique()
    store_ids = df_feature_full['storeid'].unique()

    # add smoothing feature
    s1_result = pd.Series([])
    s2_result = pd.Series([])
    s3_result = pd.Series([])
    for goodsn in goodsn_list:
        for store_id in store_ids:
            df_goods = df_feature_full[(df_feature_full['storeid'] == store_id) & (df_feature_full['goodscode'] == goodsn)]
            if len(df_goods.index) < 2 * 7:
                continue
            y = [v for i, v in df_goods['saleqty'].items()]
            s1 = holt_winters_first_order_ewma(y, 0.3)
            s2 = holt_winters_second_order_ewma(y, 0.3, 0.3)
            s3 = triple_exponential_smoothing(y, 7, 0.3, 0.3, 0.1)
            s1_result = pd.concat([s1_result, pd.Series(s1, index=df_goods.index)])
            s2_result = pd.concat([s2_result,pd.Series(s2, index=df_goods.index)])
            s3_result = pd.concat([s3_result,pd.Series(s3, index=df_goods.index)])
    df_feature_full['smoothing1'] = s1_result
    df_feature_full['smoothing2'] = s2_result
    df_feature_full['smoothing3'] = s3_result
    return df_feature_full

if __name__ == '__main__':
    df_sale_feature = file_operation.read_feature_full()
    df_sale_feature = smoothing(df_sale_feature)
    file_operation.write_feature_full(df_sale_feature)
