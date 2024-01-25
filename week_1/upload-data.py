import pandas as pd
import psycopg

#data loading
df = pd.read_csv("yellow_tripdata_2021-01.csv.gz", nrows=5)
print(pd.io.sql.get_schema(df, 'yellow_taxi_data'))

#casting dataype from text to timestamp
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()

#check the change
print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))
df_iter = pd.read_csv("yellow_tripdata_2021-01.csv.gz", iterator=True, chunksize=1_00_000)

df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')

from time import time
while True:
    time_start = time()
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
    time_end = time()
    print(f'inserting another chunk {time_end-time_start}')