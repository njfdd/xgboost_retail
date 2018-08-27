import pandas as pd
from definitions import ROOT_DIR

def purchase_init(purchase_path):
    df_purchase_full = pd.read_csv(purchase_path, parse_dates=['buytime'])
    df_purchase_full['buytime'] = pd.to_datetime(df_purchase_full['buytime'].dt.strftime("%Y-%m-%d"))

    # get purchase feature
    df_purchase_full = df_purchase_full[['storeid', 'buytime', 'goodscode', 'price', 'totalamount', 'totaldiscount']]
    df_purchase_full = df_purchase_full.groupby(['storeid', 'buytime', 'goodscode'], as_index=False).mean()
    df_purchase_full.columns = ['storeid', 'rundate', 'goodscode', 'price', 'total_amount', 'total_discount']
    df_purchase_full.fillna(0)

    return df_purchase_full

if __name__ == '__main__':
    df_purchase_full = purchase_init('%s/%s' % (ROOT_DIR, 'sources/input/saledata.csv'))
    df_purchase_full.to_csv('%s/%s' % (ROOT_DIR, 'sources/output/purchase_feature.csv'), index=False)