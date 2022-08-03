# Import csv to postgresql db

import psycopg2
import pandas as pd

# Update with your user name
conn = psycopg2.connect("host=localhost dbname=birds_heard_db user=postgres password=postgres")
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS birds_heard;')

cur.execute('''CREATE TABLE birds_heard (
    obs_id SERIAL PRIMARY KEY NOT NULL,
    ebird_code TEXT NOT NULL,
    confidence FLOAT NOT NULL,
    when_heard TIMESTAMP NOT NULL,
    device_id TEXT NOT NULL);''')

conn.commit()

df_birds = pd.read_csv('./data/predefined_birds.csv', index_col=0)
for idx, o in df_birds.iterrows():
    # Data cleaning

    q = cur.execute(
        '''INSERT INTO birds_heard (ebird_code, confidence, when_heard,device_id) VALUES (%s,%s,%s,%s)''',
        (o.ebird_code, o.confidence, o.when_heard, o.device_id)
    )
    print(f"INSERT INTO birds_heard (ebird_code, confidence, when_heard, device_id) VALUES ({o.ebird_code},{o.confidence},{o.when_heard},{o.device_id})")
    conn.commit()

cur.close()
conn.close()
