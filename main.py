from src.calendar_builder import CalendarBuilder
from src.database_filling import connect_sqlalc

if __name__ == '__main__':
    engine = connect_sqlalc()
    builder = CalendarBuilder(
        'culture_x_temperature',
        'cultures',
        'weather',
        'features_technical',
        engine.connect()
    )
    while True:
        culture = input('Культура: ')
        sort = input('Сорт: ')
        city = input('Город: ')
        # culture, sort, city = input().split()
        print(builder.create_calendar(culture, sort, city))
