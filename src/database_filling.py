import json
import os

import pandas as pd
from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder

creds = json.load(open('creds.json', 'r'))


def connect_sqlalc():
    try:
        print('Connecting to the PostgreSQL Database...')

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
        ))
    except Exception as e:
        print(e)
        print('Connection Has Failed...')
    return engine


def run():
    engine = connect_sqlalc()
    tomatoes = pd.read_csv('../aelita/ready/parsed_tomato_aelita.csv')
    features = pd.read_csv('../technical_data/features_technical.csv')
    culture_temp = pd.read_csv('../technical_data/culture_x_temp.csv')
    with engine.connect() as conn:
        tomatoes.to_sql('temp_tomato_table', con=conn, if_exists='replace', index=False)
        features.to_sql('features_technical', con=conn, if_exists='replace', index=True)
        culture_temp.to_sql('culture_x_temperature', con=conn, if_exists='replace', index=True)
        conn.commit()
        conn.close()

    path_to_weather = '../weather'
    with engine.connect() as conn:
        for filename in os.listdir(path_to_weather):
            df = pd.read_csv(os.path.join(path_to_weather, filename))
            df.to_sql('weather', con=conn, if_exists='append', index=True)
            conn.commit()
            print(filename)


if __name__ == '__main__':
    run()