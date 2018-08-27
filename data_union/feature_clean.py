import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta
from global_sources import file_operation

def remove_nan(df_origin_full):
    df_cleaned = df_origin_full
    df_cleaned = df_cleaned.dropna(subset=[
        'rundate',
        'price',
        'total_amount',
        'total_discount'
    ])
    return df_cleaned

def remove_illegal(df_cleaned):
    # df_cleaned = df_cleaned[(df_cleaned['saleqty'] > 0) & (df_cleaned['result'] > 0)]
    return df_cleaned

def remove_useless(df_cleaned):
    # df_cleaned = df_cleaned.drop('goodsn', 1)
    # df_cleaned = df_cleaned.drop('name', 1)
    # df_cleaned = df_cleaned.drop('barcode', 1)
    # df_cleaned = df_cleaned.drop('daleicode', 1)
    # df_cleaned = df_cleaned.drop('zhongleicode', 1)
    # df_cleaned = df_cleaned.drop('xiaoleicode', 1)
    # df_cleaned = df_cleaned.drop('storageattr', 1)
    # df_cleaned = df_cleaned.drop('vendorid', 1)
    # df_cleaned = df_cleaned.drop('specification', 1)
    # df_cleaned = df_cleaned.drop('dt_x', 1)
    # df_cleaned = df_cleaned.drop('dt_y', 1)
    return df_cleaned

def data_clean(df_origin_full):
    df_cleaned = remove_nan(df_origin_full)
    df_cleaned = remove_illegal(df_cleaned)
    df_cleaned = remove_useless(df_cleaned)
    pd.set_option('display.max_columns', None)
    # print(df_cleaned[df_cleaned.isnull().any(axis=1)])
    print('df_cleaned contains invalid value:')
    print(np.count_nonzero(df_cleaned.isnull()))
    return df_cleaned

if __name__ == '__main__':
    df_origin_full = file_operation.read_feature_full()
    df_cleaned = data_clean(df_origin_full)
    file_operation.write_feature_full(df_cleaned)
