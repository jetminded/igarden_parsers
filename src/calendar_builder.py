import json
import os

from datetime import datetime, timedelta
from time import time_ns
from typing import Dict, List, Tuple

import pandas as pd
import numpy as np
import sqlalchemy.engine
from numpy import NaN
from sqlalchemy import text

from definitions import ROOT_DIR, CALENDAR_DIR
from src.database_filling import connect_sqlalc


def find_best_date(weather: pd.DataFrame, good_temp: Dict[str, Dict[str, float]], culture: str) -> datetime:
    weather['Date'] = pd.to_datetime(weather['Date'])
    weather['Day'] = weather['Date'].dt.day
    weather['Month'] = weather['Date'].dt.month
    weather['Max temp'] = pd.to_numeric(weather['Max temp'])
    weather['Min temp'] = pd.to_numeric(weather['Min temp'])
    weather['Avg temp'] = pd.to_numeric(weather['Avg temp'])
    weather_stats = weather.drop(columns='Date').groupby(['Month', 'Day'], as_index=False).mean()
    good_weather = weather_stats[
        (weather_stats['Min temp'] >= good_temp['min_temp'][culture]) &
        (weather_stats['Max temp'] <= good_temp['max_temp'][culture]) &
        (weather_stats['Avg temp'] >= good_temp['avg_temp'][culture])
        ]
    return datetime(datetime.now().year, *(good_weather[['Month', 'Day']].iloc[0].to_list()))


def get_instant_name(culture: str, city: str) -> str:
    return os.path.join(CALENDAR_DIR, f'{culture}_{city}_{time_ns()}.json'.replace(" ", "_"))


def select_query(x: str, condition: str = None):
    if condition is None:
        return text(f'SELECT * FROM {x};')
    else:
        return text(f'SELECT * FROM {x} WHERE {condition};')


class CalendarBuilder:
    """
    Составляет календарь по заданной культуре (пока что без сложных параметров).
    """

    def __init__(self,
                 temperature_db: str,
                 cultures_db: str,
                 weather_db: str,
                 features_db: str,
                 conn: sqlalchemy.engine.Connection):
        """
        :param temperature_db: Имя БД с температурой высадки культур в открытый грунт.
        :param cultures_db: Имя БД с местоположением данных о культурах.
        :param weather_db: Имя БД, где лежат файлы с погодой в регионах.
        :param features_db: Имя БД с параметрами, влияющими на даты высадки.
        """
        # как записывать в датафреймы запросы
        # df = pd.read_sql_query('select * from "Stat_Table"',con=engine)
        self.temp_df = pd.read_sql_query(select_query(temperature_db), con=conn, index_col='culture')
        self.cultures_location = pd.read_sql_query(select_query(cultures_db), con=conn, index_col='culture_id')
        self.weather_db_name = weather_db
        self.features_df = pd.read_sql_query(select_query(features_db), con=conn, index_col='index')
        self.conn = conn

    def create_calendar(self, culture: str, sort: str, city: str) -> str:
        """
        Составляет календарь для заданной культуры в заданном городе.
        :param culture: Название культуры.
        :param sort: Сорт культуры.
        :param city: Город, для которого генерируется календарь.
        :return: Путь до файла, где лежит календарь в формате json
        """
        condition = f'weather.\"City\" = \'{city}\''
        weather = pd.read_sql_query(select_query(self.weather_db_name, condition), con=self.conn, index_col='index')
        culture_name = self.cultures_location[self.cultures_location.culture_name == culture].culture_table_name.item()
        culture_df = pd.read_sql_query(select_query(culture_name), con=self.conn)

        sort_info = culture_df[culture_df['Название'] == sort].to_dict(orient='list')

        chores = self.create_chores(culture, sort_info, weather)

        file_name = get_instant_name(culture, city)
        with open(file_name, 'w') as f:
            json.dump(chores, f, default=str)
        return file_name

    def create_chores(self, culture: str, sort_info: Dict, weather: pd.DataFrame) -> List[Dict[str, Tuple[datetime]]]:
        """
        Создаёт список задач с привязкой к температуре;
        :param culture: Культура, по которой производится запрос;
        :param sort_info: Информация о конкретном сорте;
        :param weather: Погода в указанном городе;
        :return: Список задач.
        """
        usual_temp = self.temp_df.loc[[culture]][['min_temp', 'max_temp', 'avg_temp']].to_dict()
        features = self.features_df[self.features_df.culture == culture][['feature', 'min', 'max', 'chores']]
        params = np.array(list(sort_info.values()), dtype=str).flatten().tolist()

        chores = []
        for row in features.iterrows():
            feature, min_time, max_time, chore = row[1].tolist()
            if feature in params or feature is None or feature is NaN:
                chores.append({chore: (int(min_time), int(max_time))})

        best_date = find_best_date(weather, usual_temp, culture)

        for chore in chores:
            chore_name = list(chore.keys())[0]
            min_date, max_date = chore[chore_name]
            chore[chore_name] = (best_date + timedelta(min_date), best_date + timedelta(max_date))

        return chores


if __name__ == '__main__':
    engine = connect_sqlalc()
    builder = CalendarBuilder(
        'culture_x_temperature',
        'cultures',
        'weather',
        'features_technical',
        engine.connect()
    )
    print(builder.create_calendar('Томат', 'Томат Ранний красный', 'Брест'))
    print(builder.create_calendar('Томат', 'Томат Брутус', 'Москва'))
