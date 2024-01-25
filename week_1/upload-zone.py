import pandas as pd
import os

# url = 'https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv'

# os.system(f"wget {url}")

from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()

df_zones = pd.read_csv('taxi+_zone_lookup.csv')
df_zones.head()
df_zones.to_sql(name='zones', con=engine, if_exists='replace')

#data loading
# df = pd.read_csv("output.csv", nrows=5)
# print(pd.io.sql.get_schema(df, 'yellow_taxi_data'))

# #casting dataype from text to timestamp
# df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
# df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


# from sqlalchemy import create_engine
# engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
# engine.connect()

# #check the change
# print(pd.io.sql.get_schema(df, name='zones', con=engine))
# df_iter = pd.read_csv("output.csv", iterator=True, chunksize=1_00_000)

# df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
# df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
# df.head(n=0).to_sql(name='zones', con=engine, if_exists='replace')

# from time import time
# while True:
#     time_start = time()
#     df = next(df_iter)
#     df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
#     df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
#     df.to_sql(name='zones', con=engine, if_exists='append')
#     time_end = time()
#     print(f'inserting another chunk {time_end-time_start}')