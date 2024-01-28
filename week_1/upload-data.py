import pandas as pd
from sqlalchemy import create_engine
from time import time
import psycopg2


df = pd.read_csv("raw_data/green_tripdata_2019-09.csv.gz", nrows=5)
print(pd.io.sql.get_schema(df, 'green_taxi_data'))

#casting dataype from text to timestamp
df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)



engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()

#check the change
print(pd.io.sql.get_schema(df, name='green_taxi_data', con=engine))
df_iter = pd.read_csv("raw_data/green_tripdata_2019-09.csv.gz", iterator=True, chunksize=1_00_000)

df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
df.head(n=0).to_sql(name='green_taxi_data', con=engine, if_exists='replace')

while True:
    time_start = time()
    df = next(df_iter)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    df.to_sql(name='green_taxi_data', con=engine, if_exists='append')
    time_end = time()
    print(f'inserting another chunk {time_end-time_start}')