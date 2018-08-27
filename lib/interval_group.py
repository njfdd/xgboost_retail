import pandas as pd
from datetime import datetime, timedelta

MAX_PREDICT_INTERVAL = 20

def interval_group_from_past(df_feature):
    result = df_feature.copy(deep=True)
    for i in range(1, MAX_PREDICT_INTERVAL):
        df_temp = df_feature.copy(deep=True)
        df_temp = df_temp[df_temp['interval']>=i]
        df_temp['rundate'] = df_temp['rundate'] + timedelta(days=i)
        result = pd.concat([result, df_temp], ignore_index=True)
    result = result.groupby(['rundate', 'storeid', 'goodscode'], as_index=False).mean()
    return result

def interval_group_from_future(df_feature):
    result = df_feature.copy(deep=True)
    for i in range(1, MAX_PREDICT_INTERVAL):
        df_temp = df_feature.copy(deep=True)
        df_temp = df_temp[df_temp['interval'] >= i]
        df_temp['rundate'] = df_temp['rundate'] + timedelta(days=-i)
        result = pd.concat([result, df_temp], ignore_index=True)
    result = result.groupby(['rundate', 'storeid', 'goodscode'], as_index=False).mean()
    return result