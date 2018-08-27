import os
import pandas as pd

def file_check(path):
    error_message = []
    # file exists
    if not os.path.exists(path):
        str = path + ' not exists' + '\n'
        error_message.append(str)
        return error_message
    # file null value
    df = pd.read_csv(path, header=None)
    row_num = df.shape[0]
    for col in df.columns:
        if df[col].count() / row_num < 0.7:
            str = path + ' col num:' + col + ' null value > 30%'
            error_message.append(str)
    return error_message