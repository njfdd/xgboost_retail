from definitions import ROOT_DIR
from lib.evaluation import mape, rmsp_avg_5, corr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

def print_evaluation(goodsn, res_list):
    y_tests = []
    y_preds = []
    dts = []
    for res in res_list:
        if not res:
            continue
        y_tests.append(res['y_test'])
        y_preds.append(res['y_pred'])
        dts.append(res['rundate'])
    if len(y_preds) == 0:
        return False
    print('goodsn: ' + str(goodsn))
    print('\tmape: ' + str(mape(y_tests, y_preds)))
    print('\tsum(abs(r-p))/sum(p): ' + str(rmsp_avg_5(y_tests, y_preds)))
    print('\tcount(r): ' + str(len(y_tests)))
    return True

def plt_draw(store_id, goodsn, df_draw, res_list):
    y_preds = []
    dts = []
    for res in res_list:
        if not res:
            continue
        y_preds.append(res['y_pred'])
        dts.append(res['rundate'])
    if len(y_preds) == 0:
        return False
    # draw sales chart
    plt.figure(1, figsize=(20, 7))
    plt.plot(df_draw['rundate'], df_draw['result'], color='#6aa84f', marker='o')
    # plt.plot(df_draw['rundate'], df_draw['stockqty'], color='black', marker='o')
    plt.plot([datetime.strptime(d, '%Y-%m-%d').date() for d in dts], y_preds, color='red', marker='o')
    plt.savefig('%s/%s' % (ROOT_DIR, 'sources/imgs/' + str(store_id) + '_' + str(goodsn) + '.png'))
    plt.close('all')
    return True

def gen_predicts(store_id, goodsn, res_sale_list, res_stock_list):
    y_tests_sale = []
    y_preds_sale = []
    y_tests_stock = []
    y_preds_stock = []
    dts = []
    for res in res_sale_list:
        if not res:
            continue
        y_tests_sale.append(res['y_test'])
        y_preds_sale.append(res['y_pred'])
        dts.append(res['rundate'])
    for res in res_stock_list:
        if not res:
            continue
        y_tests_stock.append(res['y_test'])
        y_preds_stock.append(res['y_pred'])
    if len(y_preds_sale) == 0 or len(y_preds_stock) == 0:
        return False, None
    df_results = pd.DataFrame({'rundate':dts, 'storeid':store_id, 'goodsn':goodsn, 'sales':y_tests_sale, 'pred_sale':y_preds_sale, 'pred_stock':y_preds_stock})
    return True, df_results

def corr_evaluation(df_result, store_id, goodsn, df_goods_full):
    df_y = df_goods_full.drop(['result','rundate'],1)
    df_y.index = range(0,len(df_y))
    df_x = df_goods_full['result']
    df_1 = pd.DataFrame({'store_id':[store_id],'goodsn':[goodsn]})
    for y in df_y.columns:
        cor = corr(list(df_x),list(df_y[y]))
        df_y[y] = cor
    df_2 = df_y.drop(range(1,len(df_y)),0)
    # df_goods_full.to_csv('../test/output/abc.csv', index=False)
    df_result = pd.concat([df_result, pd.concat([df_1,df_2], axis=1)], axis=0)
    return df_result

def write_corr(df_corr):
    df_corr.to_csv('%s/%s' % (ROOT_DIR, 'sources/output/corr_evaluation.csv'), index=False)