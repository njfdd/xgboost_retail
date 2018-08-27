from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib

from lib.evaluation import mape

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from definitions import ROOT_DIR
from global_sources.file_operation import read_feature_full, union_file

df_feature_full = read_feature_full()
df_predict = union_file('%s/%s' % (ROOT_DIR, 'sources/output/predict/'))
df_predict['rundate'] = df_predict['rundate'].astype('datetime64[ns]')
df_predict.columns = ['rundate', 'storeid', 'goodscode', 'sales', 'pred_sale', 'pred_stock']
df_predict = pd.merge(df_predict, df_feature_full, how='left', on=['goodscode', 'rundate'])
df_predict = df_predict[['goodscode', 'rundate', 'result', 'pred_sale', 'pred_stock']]
# print(len(df_result['rundate']))
# print(np.count_nonzero(df_result.isnull()))
# df_result['mape'] = (df_result['result'] - df_result['pred'])/df_result['result']
# df_result = df_result[['goodscode', 'mape']].abs()
# df_result = df_result.groupby(['goodscode'], as_index=False).mean()
# df_result.to_csv('../sources/output/mape.csv', index=False)

goodsns = df_predict['goodscode'].unique()
for goodsn in goodsns:
    # draw sales chart
    df_draw = df_predict[df_predict['goodscode'] == goodsn]
    df_draw = df_draw.sort_values(['rundate'])
    plt.figure(1, figsize=(20, 7))

    # print(goodsn)
    # print(mape(df_draw['result'].tolist(), df_draw['pred'].tolist()))

    plt.plot(df_draw['rundate'], df_draw['pred_stock'], color='blue', marker='o', label='pred_stock')
    plt.plot(df_draw['rundate'], df_draw['pred_sale'], color='red', marker='o', label='pred_sale')
    plt.plot(df_draw['rundate'], df_draw['result'], color='black', marker='o', label='real_sale')
    plt.ylim(ymin=0)
    plt.legend(loc='upper right')
    plt.savefig('%s/%s' % (ROOT_DIR, 'sources/imgs/' + str(goodsn) + '.png'))
    plt.close('all')