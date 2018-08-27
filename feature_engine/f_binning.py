import pandas as pd
import numpy as np
from datetime import datetime
from global_sources import file_operation
from lib.date_map import week_day
from lib.woe_binning import mono_bin


def binner_engine(df_feature_full):
    # print iv and woe
    # df_binning = df_feature_full[['result', 'saleqty', 'inqty', 'stockqty']]
    # d4, iv, cut, woe = mono_bin(df_binning['result'].astype(int), df_feature_full['saleqty'], 5)
    # print(iv)

    df_feature_full['hightemp'] = pd.qcut(df_feature_full['hightemp'],
                                          min(10, len(df_feature_full['hightemp'].unique())), duplicates='drop').cat.codes
    df_feature_full['lowtemp'] = pd.qcut(df_feature_full['lowtemp'],
                                         min(10, len(df_feature_full['lowtemp'].unique())), duplicates='drop').cat.codes
    df_feature_full['beginqty_binning'] = pd.qcut(np.log10(df_feature_full['beginqty'].abs() + 1),
                                              min(10, len(df_feature_full['beginqty'].unique())), duplicates='drop').cat.codes
    df_feature_full['endqty_binning'] = pd.qcut(np.log10(df_feature_full['endqty'].abs() + 1),
                                                  min(10, len(df_feature_full['endqty'].unique())),
                                                  duplicates='drop').cat.codes
    df_feature_full['inqty_binning'] = pd.qcut(np.log10(df_feature_full['inqty'].abs() + 1),
                                      min(10, len(df_feature_full['inqty'].unique())), duplicates='drop').cat.codes
    df_feature_full['saleqty_binning'] = pd.qcut(np.log10(df_feature_full['saleqty'].abs() + 1),
                                                min(10, len(df_feature_full['saleqty'].unique())), duplicates='drop').cat.codes
    df_feature_full['total_amount'] = pd.qcut(df_feature_full['total_amount'],
                                                min(10, len(df_feature_full['total_amount'].unique())), duplicates='drop').cat.codes
    df_feature_full['total_discount'] = pd.qcut(df_feature_full['total_discount'],
                                                min(10, len(df_feature_full['total_discount'].unique())), duplicates='drop').cat.codes
    df_feature_full['user_count'] = pd.qcut(df_feature_full['user_count'],
                                            min(5, len(df_feature_full['user_count'].unique())), duplicates='drop').cat.codes
    df_feature_full['min_60'] = pd.qcut(df_feature_full['min_60'],
                                         min(10, len(df_feature_full['min_60'].unique())), duplicates='drop').cat.codes
    df_feature_full['std_60'] = pd.qcut(df_feature_full['std_60'],
                                        min(10, len(df_feature_full['std_60'].unique())), duplicates='drop').cat.codes
    df_feature_full['var_60'] = pd.qcut(df_feature_full['var_60'],
                                        min(10, len(df_feature_full['var_60'].unique())), duplicates='drop').cat.codes
    df_feature_full['max_60'] = pd.qcut(df_feature_full['max_60'],
                                        min(10, len(df_feature_full['max_60'].unique())), duplicates='drop').cat.codes
    df_feature_full['sum_60'] = pd.qcut(df_feature_full['sum_60'],
                                        min(10, len(df_feature_full['sum_60'].unique())), duplicates='drop').cat.codes
    df_feature_full['min_15'] = pd.qcut(df_feature_full['min_15'],
                                        min(10, len(df_feature_full['min_15'].unique())), duplicates='drop').cat.codes
    df_feature_full['std_15'] = pd.qcut(df_feature_full['std_15'],
                                        min(10, len(df_feature_full['std_15'].unique())), duplicates='drop').cat.codes
    df_feature_full['var_15'] = pd.qcut(df_feature_full['var_15'],
                                        min(10, len(df_feature_full['var_15'].unique())), duplicates='drop').cat.codes
    df_feature_full['max_15'] = pd.qcut(df_feature_full['max_15'],
                                        min(10, len(df_feature_full['max_15'].unique())), duplicates='drop').cat.codes
    df_feature_full['sum_15'] = pd.qcut(df_feature_full['sum_15'],
                                        min(10, len(df_feature_full['sum_15'].unique())), duplicates='drop').cat.codes
    df_feature_full['min_7'] = pd.qcut(df_feature_full['min_7'],
                                        min(10, len(df_feature_full['min_7'].unique())), duplicates='drop').cat.codes
    df_feature_full['std_7'] = pd.qcut(df_feature_full['std_7'],
                                        min(10, len(df_feature_full['std_7'].unique())), duplicates='drop').cat.codes
    df_feature_full['var_7'] = pd.qcut(df_feature_full['var_7'],
                                        min(10, len(df_feature_full['var_7'].unique())), duplicates='drop').cat.codes
    df_feature_full['max_7'] = pd.qcut(df_feature_full['max_7'],
                                        min(10, len(df_feature_full['max_7'].unique())), duplicates='drop').cat.codes
    df_feature_full['sum_7'] = pd.qcut(df_feature_full['sum_7'],
                                        min(10, len(df_feature_full['sum_7'].unique())), duplicates='drop').cat.codes
    df_feature_full['min_3'] = pd.qcut(df_feature_full['min_3'],
                                        min(10, len(df_feature_full['min_3'].unique())), duplicates='drop').cat.codes
    df_feature_full['std_3'] = pd.qcut(df_feature_full['std_3'],
                                        min(10, len(df_feature_full['std_3'].unique())), duplicates='drop').cat.codes
    df_feature_full['var_3'] = pd.qcut(df_feature_full['var_3'],
                                        min(10, len(df_feature_full['var_3'].unique())), duplicates='drop').cat.codes
    df_feature_full['max_3'] = pd.qcut(df_feature_full['max_3'],
                                        min(10, len(df_feature_full['max_3'].unique())), duplicates='drop').cat.codes
    df_feature_full['sum_3'] = pd.qcut(df_feature_full['sum_3'],
                                        min(10, len(df_feature_full['sum_3'].unique())), duplicates='drop').cat.codes
    # print(df_feature_full.head)
    return df_feature_full

if __name__ == '__main__':
    df_feature_full = file_operation.read_feature_full()
    df_feature_full = binner_engine(df_feature_full)
    file_operation.write_feature_full(df_feature_full)