import pandas as pd
from definitions import ROOT_DIR

def user_count_init(purchase_path):
    df_purchase = pd.read_csv(purchase_path, parse_dates=['buytime'])
    df_purchase['buytime'] = pd.to_datetime(df_purchase['buytime'].dt.strftime("%Y-%m-%d"))

    # only after 2017
    df_purchase = df_purchase[df_purchase['buytime'] >= '2017-01-01']

    # get user_count
    df_user_count = df_purchase[['storeid', 'buytime', 'receiptid']].\
        groupby(['storeid', 'buytime'],as_index=False).agg({'receiptid': 'nunique'})
    df_user_count.columns = ['storeid', 'rundate', 'user_count']

    return df_user_count

if __name__ == '__main__':
    df_user_count = user_count_init('%s/%s' % (ROOT_DIR, 'sources/input/saledata.csv'))
    df_user_count.to_csv('%s/%s' % (ROOT_DIR, 'sources/output/user_count_feature.csv'), index=False)