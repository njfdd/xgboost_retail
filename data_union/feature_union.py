import glob

import pandas as pd
import numpy as np
import warnings
from datetime import timedelta

from definitions import ROOT_DIR
from global_sources import file_operation
from lib.interval_group import interval_group_from_past, interval_group_from_future

warnings.filterwarnings('ignore')


def union_dfs_day(weather_daily_path, weather_hour_path, holiday_path, stock_path,
                  user_count_path, purchase_feature_path, goods_list_paths, test_day):
    # read goodsn to predict
    goods_lists = []
    for goods_list_path in glob.glob(goods_list_paths):
        goods_lists.append(pd.read_csv(goods_list_path))
    df_goods_list = pd.concat(goods_lists)

    # future feature, to future
    df_weather_hourly = pd.read_csv(weather_hour_path, parse_dates=['dt'])
    df_weather_hourly.rename(columns={'dt': 'rundate'}, inplace=True)
    df_weather_daily = pd.read_csv(weather_daily_path, parse_dates=['dt'])
    df_weather_daily.rename(columns={'dt': 'rundate'}, inplace=True)
    df_holiday = pd.read_csv(holiday_path, parse_dates=["dt"])
    df_holiday.rename(columns={'dt': 'rundate'}, inplace=True)

    # past feature, until yesterday
    df_user_count = pd.read_csv(user_count_path, parse_dates=['rundate'])
    df_purchase_feature = pd.read_csv(purchase_feature_path, parse_dates=['rundate'])
    df_stock = pd.read_csv(stock_path, parse_dates=["rundate"])

    # past feature union
    df_past = df_goods_list
    df_past = pd.merge(df_past, df_stock, how='inner', on=['storeid', 'goodscode'])
    df_past = pd.merge(df_past, df_purchase_feature, how='left', on=['rundate', 'storeid', 'goodscode'])
    df_past = pd.merge(df_past, df_user_count, how='left', on=['rundate', 'storeid'])

    # shift two days ago, 'use yesterday data predict tomorrow value'
    df_past['rundate'] = df_past['rundate'] + timedelta(days=2)

    # get result, future feature
    df_result = df_stock[['rundate', 'storeid', 'goodscode', 'saleqty']]
    df_result.columns = ['rundate', 'storeid', 'goodscode', 'result']
    df_result = pd.merge(df_result, df_goods_list, how='inner', on=['storeid', 'goodscode'])

    # fill future result default value for union future feature
    # df_result_future = df_result.copy(deep=True)
    # df_result_future['rundate'] = df_result_future['rundate'] + timedelta(days=MAX_PREDICT_INTERVAL)

    # df_result_temp = df_result.copy(deep=True)
    # df_result_temp = df_result_temp.drop('interval', 1)
    # df_result_temp.columns = ['rundate', 'storeid', 'goodscode', 'temp_result']
    # df_result_future = pd.merge(df_result_future, df_result_temp, how='left', on=['rundate', 'storeid', 'goodscode'])
    # df_result_future = df_result_future[df_result_future['temp_result'].isnull()]
    # df_result_future = df_result_future.drop('temp_result', 1)
    # df_result = pd.concat([df_result, df_result_future])

    # past feature group from past
    df_past = interval_group_from_past(df_past)
    df_past = df_past.drop('interval', 1)

    # future feature group from future
    df_result = interval_group_from_future(df_result)

    # generate feature result columns=['rundate', 'storeid', 'goodscode', 'result']
    for index, row in df_goods_list.iterrows():
        for i in range(0, row['interval']):
            df_result.loc[len(df_result.index)] = {
                'rundate': np.datetime64(test_day) + np.timedelta64(i, 'D'),
                'storeid': row['storeid'],
                'goodscode': row['goodscode'],
                'result': 0,
                'interval': row['interval'],
            }
    df_result = df_result.drop('interval', 1)

    # union all
    df_feature_full = pd.merge(df_result, df_holiday, how='left', on=['rundate'])
    df_feature_full = pd.merge(df_feature_full, df_weather_daily, how='left', on=['rundate'])
    df_feature_full = pd.merge(df_feature_full, df_weather_hourly, how='left', on=['rundate'])
    df_feature_full = pd.merge(df_past, df_feature_full, how='inner', on=['rundate', 'storeid', 'goodscode'])

    # put result column first
    cols = list(df_feature_full)
    cols.insert(0, cols.pop(cols.index('result')))
    df_feature_full = df_feature_full.loc[:, cols]

    return df_feature_full


if __name__ == '__main__':
    df_origin_full = union_dfs_day(
        '%s/%s' % (ROOT_DIR, 'sources/output/weather_day_feature.csv'),
        '%s/%s' % (ROOT_DIR, 'sources/output/weather_hour_feature.csv'),
        '%s/%s' % (ROOT_DIR, 'sources/output/df_holiday_feature.csv'),
        '%s/%s' % (ROOT_DIR, 'sources/input/stock.csv'),
        '%s/%s' % (ROOT_DIR, 'sources/output/user_count_feature.csv'),
        '%s/%s' % (ROOT_DIR, 'sources/output/purchase_feature.csv'),
        '%s/%s' % (ROOT_DIR, 'sources/goods_list/*'),
    )
    file_operation.write_feature_full(df_origin_full)
