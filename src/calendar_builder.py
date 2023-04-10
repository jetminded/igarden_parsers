import json
import os

from datetime import datetime, timedelta
from time import time_ns
from typing import List

import pandas as pd
import numpy as np
from numpy import NaN

from definitions import ROOT_DIR, CALENDAR_DIR


def find_best_date(weather: pd.DataFrame, good_temp: List[float]) -> datetime:
    weather['Date'] = pd.to_datetime(weather['Date'])
    weather['Day'] = weather['Date'].dt.day
    weather['Month'] = weather['Date'].dt.month
    weather_stats = weather.drop(columns='Date').groupby(['Month', 'Day'], as_index=False).mean()
    good_weather = weather_stats[
        (weather_stats['Min temp'] >= good_temp[0]) &
        (weather_stats['Max temp'] <= good_temp[1]) &
        (weather_stats['Avg temp'] >= good_temp[2])
        ]
    return datetime(datetime.now().year, *(good_weather[['Month', 'Day']].iloc[0].to_list()))


def get_instant_name(culture: str, city: str) -> str:
    return os.path.join(CALENDAR_DIR, f'{culture}_{city}_{time_ns()}.json'.replace(" ", "_"))


class CalendarBuilder:
    """
    Составляет календарь по заданной культуре (пока что без сложных параметров).
    """

    def __init__(self,
                 temperature_path: str,
                 cultures_path: str,
                 weather_path: str,
                 features_path: str):
        """
        :param temperature_path: Путь до файла с температурой высадки культур в открытый грунт в формате csv.
        :param cultures_path: Путь до файла с местоположением данных о культурах в формате csv.
        :param weather_path: Путь до папки, где лежат файлы с погодой в регионах в формате csv.
        :param features_path: Путь до файла с параметрами, влияющими на даты высадки, в формате csv.
        """
        self.temp_df = pd.read_csv(temperature_path, index_col='culture')
        self.cultures_location = pd.read_csv(cultures_path, index_col='culture')['data']
        self.weather_path = weather_path
        self.features_df = pd.read_csv(features_path)

    def create_calendar(self, culture: str, sort: str, city: str) -> str:
        """
        Составляет календарь для заданной культуры в заданном городе.
        :param culture: Название культуры.
        :param sort: Сорт культуры.
        :param city: Город, для которого генерируется календарь.
        :return: Путь до файла, где лежит календарь в формате json
        """
        weather = pd.read_csv(os.path.join(self.weather_path, f'{city}.csv'), index_col=[0]).drop(columns='City')
        culture_df = pd.read_csv(os.path.join(ROOT_DIR, self.cultures_location[culture]))
        sort_info = culture_df[culture_df['Название'] == sort].to_dict(orient='list')
        usual_temp = self.temp_df.loc[culture].tolist()
        features = self.features_df[self.features_df.culture == culture][['feature', 'min', 'max', 'chores']]
        params = np.array(list(sort_info.values())).flatten().tolist()

        chores = []
        for row in features.iterrows():
            feature, min_time, max_time, chore = row[1].tolist()
            if feature in params or feature is NaN:
                chores.append({chore: (int(min_time), int(max_time))})

        best_date = find_best_date(weather, usual_temp)

        for chore in chores:
            chore_name = list(chore.keys())[0]
            min_date, max_date = chore[chore_name]
            chore[chore_name] = (best_date + timedelta(min_date), best_date + timedelta(max_date))

        file_name = get_instant_name(culture, city)
        with open(file_name, 'w') as f:
            json.dump(chores, f, default=str)
        return file_name


if __name__ == '__main__':
    builder = CalendarBuilder(
        os.path.join(ROOT_DIR, 'technical_data', 'culture_x_temp.csv'),
        os.path.join(ROOT_DIR, 'technical_data', 'culture_x_data.csv'),
        os.path.join(ROOT_DIR, 'weather', ),
        os.path.join(ROOT_DIR, 'technical_data', 'features_technical.csv')
    )
    print(builder.create_calendar('Томат', 'Томат Ранний красный', 'Брест'))
