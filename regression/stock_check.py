from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib

from lib.evaluation import mape

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from definitions import ROOT_DIR
from global_sources.file_operation import read_feature_full, union_file
from lib.interval_group import interval_group_from_future



df_stock = pd.read_csv('../sources/input/stock/stock.csv', parse_dates=['rundate'])
df_goods_list = pd.read_csv('../sources/goods_list/561.csv')

df_result = union_file('../sources/output/result/')
df_result['rundate'] = df_result['rundate'].astype('datetime64[ns]')
df_result.columns = ['rundate', 'storeid', 'goodscode', 'sales', 'pred_sale', 'pred_stock']
df_result = df_result[['goodscode', 'storeid', 'rundate', 'pred_stock']]
df_stock = pd.merge(df_stock, df_goods_list, how='left', on=['goodscode', 'storeid'])
df_stock = df_stock[['goodscode','storeid','rundate','saleqty','beginqty','interval']]
df_stock = interval_group_from_future(df_stock)
df_result = pd.merge(df_result, df_stock, how='left', on=['goodscode', 'rundate', 'storeid'])
df_result = df_result[['goodscode','rundate','pred_stock','beginqty','saleqty']]

outfile = open('../sources/imgs/stock_report.csv', 'w')
goodsns = df_result['goodscode'].unique()
for goodsn in goodsns:
     df_good = df_result[df_result['goodscode'] == goodsn]
     pred_stock_boom = 0
     real_stock_boom = 0
     for i in df_good.index:
          if (df_good['beginqty'][i] <= df_good['saleqty'][i]):
               real_stock_boom += 1
          if(df_good['pred_stock'][i] <= df_good['saleqty'][i]):
               pred_stock_boom += 1
     ps_mean = df_good['pred_stock'].mean()
     rs_mean = df_good['beginqty'].mean()
     stock_save = (rs_mean - ps_mean)/ rs_mean
     title = '%s,%s,%.2f' % (goodsn, pred_stock_boom,stock_save)
     outfile.write('%s,%s,%s,%s,%s\n' % (goodsn, pred_stock_boom, stock_save, ps_mean, rs_mean))
     #print (title)

     # draw sales chart
     df_draw = df_result[df_result['goodscode']==goodsn]
     df_draw = df_draw.sort_values(['rundate'])
     fig = plt.figure(1, figsize=(20, 7))
     ax = fig.add_subplot(1,1,1)
     ax.set_title('%s' % (title))
     # print(goodsn)
     # print(mape(df_draw['result'].tolist(), df_draw['pred'].tolist()))

     plt.plot(df_draw['rundate'], df_draw['pred_stock'], color='#6aa84f', marker='o')
     plt.plot(df_draw['rundate'], df_draw['beginqty'], color='black', marker='o')
     plt.plot(df_draw['rundate'], df_draw['saleqty'], color='red', marker='o')
     plt.ylim(ymin=0)
     plt.savefig('%s/%s' % (ROOT_DIR, 'sources/imgs/' + str(goodsn) + '.png'))
     plt.close('all')