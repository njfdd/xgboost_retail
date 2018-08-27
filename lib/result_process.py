from global_sources.file_operation import read_goods,read_predicts,read_stock,read_goods_list
import pandas as pd
from datetime import datetime, timedelta, date
from definitions import ROOT_DIR
from global_sources import file_operation

def day_shift(dt, gap):
    tmp = datetime.strptime(dt, "%Y-%m-%d")
    n_time = tmp + timedelta(days=gap)
    n_nyr = n_time.strftime('%Y-%m-%d')
    return n_nyr


def run(dt):
    #read predict_result
    df_predict_result = read_predicts(dt)
    #read goods.csv
    df_goods = read_goods()
    goods_moqs_dict = dict(zip(df_goods['goodscode'], df_goods['dc_moq']))

    #read stock.csv
    yesterday = day_shift(dt, -2)
    df_stock = read_stock()
    df_stock = df_stock[df_stock['rundate'] == yesterday]
    df_stock = df_stock.rename(index=str, columns={'goodscode':'goodsn'})
    df_stock = df_stock[['storeid', 'goodsn', 'endqty']]

    #read_goods list
    df_goods_list = read_goods_list()
    df_goods_list.columns = ['storeid', 'goodsn', 'interval']

    df_predict_result = df_predict_result[['storeid','goodsn','rundate','pred_sale','pred_stock']]

    #generate result for users:
    #1. predict sale and predict_stock are n-days result. n is the supply period of each good
    #2. suggest inqty = pred_stock - stock qty at the end of yesterday. if suggest inqty < 0, then suggest_inqty = 0
    #3. if moq(minimum order quantity) > suggest inqty, then suggest inqty = moq
    df_tmp = pd.merge(df_predict_result,df_stock,how='left',on=['storeid', 'goodsn'])
    df_tmp = pd.merge(df_tmp, df_goods_list, how='left', on=['storeid', 'goodsn'])
    df_tmp['pred_sale'] = df_tmp['pred_sale'] * df_tmp['interval']
    df_tmp['pred_stock'] = df_tmp['pred_stock'] * df_tmp['interval']
    df_tmp['suggest_inqty'] = df_tmp['pred_stock'] - df_tmp['endqty']

    for i in range(0,df_tmp.shape[0]):
        moq = goods_moqs_dict[df_tmp['goodsn'][i]]
        if df_tmp['suggest_inqty'][i] < 0:
            df_tmp['suggest_inqty'][i] = 0
        elif df_tmp['suggest_inqty'][i] > 0 and moq > df_tmp['suggest_inqty'][i]:
            df_tmp['suggest_inqty'][i] = moq


    return df_tmp[['storeid','goodsn','interval','pred_sale','pred_stock','suggest_inqty']].round(0)

if __name__ == '__main__':
    dt = '2018-06-14'
    df_result = run(dt)
    file_operation.write_results(df_result, dt)
