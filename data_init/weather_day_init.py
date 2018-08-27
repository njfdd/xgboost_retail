import pandas as pd
from sklearn.preprocessing import LabelEncoder
from definitions import ROOT_DIR


def weather_engine(weathre_day_path):
    le = LabelEncoder()
    df_weather_day = pd.read_csv(weathre_day_path)
    df_weather_day['descrip'] = le.fit_transform(df_weather_day['descrip'].values)
    df_weather_day = df_weather_day.drop(['city_code', 'winddir'], axis=1)
    return df_weather_day


if __name__ == '__main__':
    df_weather = weather_engine('%s/%s' % (ROOT_DIR, 'sources/input/weather_day.csv'))
    df_weather.to_csv('%s/%s' % (ROOT_DIR, 'sources/output/weather_day_feature.csv'), index=False)
