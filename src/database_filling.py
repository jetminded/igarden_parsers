import json
import os

import pandas as pd
from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder

creds = json.load(open('creds.json', 'r'))


def connect_sqlalc():
    try:
        # print('Connecting to the PostgreSQL Database...')

        ssh_tunnel = SSHTunnelForwarder(
            creds["SSH_HOST"],
            ssh_username=creds["PG_UN"],
            ssh_password=creds["SSH_KEY"],
            remote_bind_address=(creds["DB_HOST"], 5432),
            allow_agent=False
        )

        ssh_tunnel.start()

        engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{db}'.format(
            host=creds["LOCALHOST"],
            port=ssh_tunnel.local_bind_port,
            user=creds["PG_UN"],
            password=creds["PG_DB_PW"],
            db=creds["PG_DB_NAME"]
        ), future=True)
    except Exception as e:
        print(e)
        print('Connection Has Failed...')
    return engine


def create_temp_tables_for_vegetables(engine):
    for file in os.listdir('../aelita/tech'):
        if file.split('_')[0] == 'parsed':
            culture = file.split('_')[1]
            data = pd.read_csv(os.path.join('../aelita/tech', file))


            features = pd.read_csv('../technical_data/features_technical.csv')
            culture_temp = pd.read_csv('../technical_data/culture_x_temp.csv')
            with engine.connect() as conn:
                data.to_sql(f'temp_{culture}_table', con=conn, if_exists='replace', index=False)
                features.to_sql('features_technical', con=conn, if_exists='replace', index=True)
                culture_temp.to_sql('culture_x_temperature', con=conn, if_exists='replace', index=True)
                conn.commit()
                # conn.close()


def create_tables_for_weather(engine):
    path_to_weather = '../weather'
    for filename in os.listdir(path_to_weather):
        with engine.connect() as conn:
            df = pd.read_csv(os.path.join(path_to_weather, filename))
            df = df.drop(df[df['Avg temp'].str.len() > 5].index)
            # df = pd.read_csv(path_to_weather, names=['index', 'city', 'weather']) .drop(columns=['index'])
            city = filename[:-4]
            df.to_sql(f'{city.replace(" ", "_")}', con=conn, if_exists='replace', index=True)
            conn.commit()
            print(filename)
            # conn.close()

def run():
    engine = connect_sqlalc()
    create_temp_tables_for_vegetables(engine)
    create_tables_for_weather(engine)


if __name__ == '__main__':
    run()
