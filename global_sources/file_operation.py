import pandas as pd
import os
import glob
import re

from definitions import ROOT_DIR

def union_file(input_path, dir_name = None):
    all_files = glob.glob(os.path.join(input_path, '*'))
    all_data_frames = pd.DataFrame()
    for file in all_files:
        df = pd.read_csv(file, index_col=False)
        all_data_frames = pd.concat([all_data_frames, df], ignore_index=True)
    if dir_name == 'saledata':
        all_data_frames.drop_duplicates(subset=['storeid','buytime','ord','goodscode'], inplace=True)
    elif dir_name == 'stock':
        all_data_frames.drop_duplicates(subset=['storeid','rundate','goodscode'], inplace=True)
    else:
        all_data_frames.drop_duplicates(inplace=True)
    return all_data_frames

def read_origin_full():
    return pd.read_csv('../test/input/origin_full.csv', parse_dates=['rundate'])

def write_origin_full(df_origin_full):
    df_origin_full.to_csv('../test/input/origin_full.csv', index=False)

def read_sale_feature():
    return pd.read_csv('../test/output/sale_feature.csv', parse_dates=['rundate'])

def write_sale_feature(df_origin_full):
    df_origin_full.to_csv('../test/output/sale_feature.csv', index=False)

def read_future_feature():
    return pd.read_csv('../test/output/future_feature.csv', parse_dates=['rundate'])

def write_future_feature(df_origin_full):
    df_origin_full.to_csv('../test/output/future_feature.csv', index=False)

def read_result():
    return pd.read_csv('../test/output/result.csv', parse_dates=['rundate'])

def write_result(df_result):
    df_result.to_csv('../test/output/result.csv', index=False)

def read_feature_full():
    return pd.read_csv('%s/%s' % (ROOT_DIR, 'sources/output/feature_full.csv'), parse_dates=['rundate'])

def write_feature_full(df_feature):
    df_feature.to_csv('%s/%s' % (ROOT_DIR, 'sources/output/feature_full.csv'), index=False)

def read_temp_full():
    return pd.read_csv('../test/input/temp.csv', parse_dates=['rundate'])

def write_temp_full(df_feature):
    df_feature.to_csv('../test/input/temp.csv', index=False)

def read_predicts(dt):
    return pd.read_csv('%s/%s%s' % (ROOT_DIR, 'sources/output/predict/', dt + '_predict.csv'), parse_dates=['rundate'])

def write_predicts(df_feature, dt):
    df_feature.to_csv('%s/%s%s' % (ROOT_DIR, 'sources/output/predict/', dt + '_predict.csv'), index=False)

def read_goods():
    return pd.read_csv('%s/%s' % (ROOT_DIR, 'sources/goods/goods.csv'))

def read_results(dt):
    return pd.read_csv('%s/%s%s' % (ROOT_DIR, 'sources/output/result/', dt + '_predict.csv'), parse_dates=['rundate'])

def read_stock():
    return pd.read_csv('%s/%s' % (ROOT_DIR, 'sources/input/stock.csv'), parse_dates=["rundate"])

def read_goods_list():
    goods_lists = []
    paths = '%s/%s' % (ROOT_DIR, 'sources/goods_list/*')
    for path in glob.glob(paths):
        goods_lists.append(pd.read_csv(path))
    df_goods_list = pd.concat(goods_lists)
    return df_goods_list

def write_results(df_predict_processed, dt):
    df_predict_processed.to_csv('%s/%s%s' % (ROOT_DIR, 'sources/output/result/', dt + '_result.csv'), index=False)