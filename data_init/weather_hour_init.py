import pandas as pd

from definitions import ROOT_DIR


def gen_weather_hour(df_weather_hour):
    df_weather_hour_morning = df_weather_hour[(df_weather_hour['hour'] >= 6) & (df_weather_hour['hour'] <= 9)]
    df_weather_hour_noon = df_weather_hour[(df_weather_hour['hour'] >= 10) & (df_weather_hour['hour'] <= 13)]
    df_weather_hour_evening = df_weather_hour[(df_weather_hour['hour'] >= 17) & (df_weather_hour['hour'] <= 20)]

    df_weather_hour_morning = df_weather_hour_morning.groupby(['dt'], as_index=False).mean()
    df_weather_hour_noon = df_weather_hour_noon.groupby(['dt'], as_index=False).mean()
    df_weather_hour_evening = df_weather_hour_evening.groupby(['dt'], as_index=False).mean()

    df_weather_hour_morning = df_weather_hour_morning[['dt', 'temp', 'windspeed', 'preci', 'humi']]
    df_weather_hour_noon = df_weather_hour_noon[['dt', 'temp', 'windspeed', 'preci', 'humi']]
    df_weather_hour_evening = df_weather_hour_evening[['dt', 'temp', 'windspeed', 'preci', 'humi']]
    df_weather_hour_morning.columns = ['dt', 'morn_temp', 'morn_windspeed', 'morn_preci', 'morn_humi']
    df_weather_hour_noon.columns = ['dt', 'noon_temp', 'noon_windspeed', 'noon_preci', 'noon_humi']
    df_weather_hour_evening.columns = ['dt', 'even_temp', 'even_windspeed', 'even_preci', 'even_humi']

    df_result = pd.merge(df_weather_hour_morning, df_weather_hour_noon, how='left', on=['dt'])
    df_result = pd.merge(df_result, df_weather_hour_evening, how='left', on=['dt'])
    return df_result


def weather_init(weather_hour_path):
    df_weather_hourly = pd.read_csv(weather_hour_path, parse_dates=['dt'])
    df_weather_hourly = gen_weather_hour(df_weather_hourly)
    return df_weather_hourly


if __name__ == '__main__':
    df_weather = weather_init('%s/%s' % (ROOT_DIR, 'sources/input/weather_hour.csv'))
    df_weather.to_csv('%s/%s' % (ROOT_DIR, 'sources/output/weather_hour_feature.csv'), index=False)
