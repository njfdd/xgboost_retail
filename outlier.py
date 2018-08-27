import pandas as pd
import sys

sys.path.append('../')
from global_sources import file_operation

"""
def outlier_processing(df_feature_full,column):
    #goodsn_list = df_feature_full['goodscode'].unique()
    goodsn_list = [2005413,2018241]
    for goodsn in goodsn_list:
        df_goods = df_feature_full[(df_feature_full['goodscode'] == goodsn)]
        df_goods = df_goods.sort_values(by=['rundate'])

        mean_result = df_goods[column].mean()
        std_result = df_goods[column].std()
        for k in range(3,df_goods[column].shape[0]):
            i = df_goods.index[k]
            if (df_feature_full[column][i] > mean_result + std_result) or (df_feature_full[column][i] < mean_result - std_result):
                df_feature_full[column][i] = round(df_goods[column][df_goods.index[k-3:k]].mean())
    return df_feature_full
"""


def outlier_processing(df_feature_full,column):
    df_feature_full = df_feature_full.sort_values(by=['rundate'])
    #df_goods = df_feature_full
    mean_result = df_feature_full[column].mean()
    std_result = df_feature_full[column].std()
    for k in range(3,df_feature_full[column].shape[0]):
        i = df_feature_full.index[k]
        if (df_feature_full[column][i] > mean_result + 5*std_result) or (df_feature_full[column][i] < mean_result - 5*std_result):
            df_feature_full[column][i] = mean_result + std_result#round(df_feature_full[column][df_feature_full.index[k-3:k]].mean())
    return df_feature_full



if __name__ == '__main__':
    df_feature_full = file_operation.read_feature_full()
    df_processed = outlier_processing(df_feature_full)
    file_operation.write_feature_full(df_processed)