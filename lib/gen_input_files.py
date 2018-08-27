import os
from definitions import ROOT_DIR
from datetime import datetime, timedelta, date

from global_sources.file_operation import union_file

INPUT_PATH = '%s/%s' % (ROOT_DIR, 'sources/input')
ORIGIN_PATH = '%s/%s' % (ROOT_DIR, 'sources/origin')

def day_shift(dt, gap):
    tmp = datetime.strptime(dt, "%Y-%m-%d")
    n_time = tmp + timedelta(days=gap)
    n_nyr = n_time.strftime('%Y-%m-%d')
    return n_nyr


def run(dt):
    test_date = dt
    test_date_past = day_shift(test_date, -1)
    test_date_weather_day = day_shift(test_date, 7)
    dirs = [
        {'dir_name': 'weather_day', 'dt_name': 'dt', 'last_date': test_date_weather_day},
        {'dir_name': 'weather_hour', 'dt_name': 'dt', 'last_date': test_date},
        {'dir_name': 'stock', 'dt_name': 'rundate', 'last_date': test_date_past},
        {'dir_name': 'saledata', 'dt_name': 'buydate', 'last_date': test_date_past},
    ]
    for item in dirs:
        dir_name = item['dir_name']
        dt_name = item['dt_name']
        last_date = item['last_date']
        input_path = '%s/%s/' % (INPUT_PATH, dir_name)
        origin_path = '%s/%s' % (ORIGIN_PATH, dir_name)
        # file_check(INTERNAL_PATH, dir_name, dt)
        os.system('cp -r %s %s' % (origin_path, INPUT_PATH))

        all_data_frames = union_file(input_path, dir_name)
        all_data_frames = all_data_frames[all_data_frames[dt_name] <= last_date]
        all_data_frames.to_csv('%s/%s.csv' % (INPUT_PATH, dir_name), index=False)


if __name__ == '__main__':
    dt = str(date.today())
    run('2018-06-24')
