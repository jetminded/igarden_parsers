import pandas as pd
from sqlalchemy import text

from src.database_filling import connect_sqlalc


def find_cities(source_db: str, column_name, conn) -> pd.DataFrame:
    query = text(f'''SELECT DISTINCT {column_name} FROM {source_db};''')
    return pd.read_sql_query(query, con=conn)


if __name__ == '__main__':
    engine = connect_sqlalc()
    frame = find_cities('weather', 'City', engine.connect())
