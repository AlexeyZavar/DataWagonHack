'''
PEREGON_HACKATON.xlsx

Example:
START_CODE	END_CODE	LEN
2	        805	        32
6	        2	        27
8	        6	        27
12	        8	        29
15	        12	        19

- START_CODE – станция начала ребра графа
- END_CODE – станция окончания ребра графа
- LEN – длительность ребра в км.

'''

import faker
import pandas as pd

from controller import Session, engine
from models import StationConnection, Base

Base.metadata.create_all(engine)

# df2 = pd.read_excel('./data/STATION_COORDS_HACKATON.xlsx')
# df2 = df2.interpolate()

df = pd.read_excel('./data/PEREGON_HACKATON.xlsx')
df = df.interpolate()

sosi = faker.Faker()

for i in range(len(df)):
    start_station_id = int(df['START_CODE'][i])
    end_station_id = int(df['END_CODE'][i])
    length = int(df['LEN'][i])

    if start_station_id == end_station_id:
        print(f'{start_station_id}')
        continue

    # if start_station_id not in df2['ST_ID'].values:
    #     print(f'{start_station_id}')
    #     continue
    #
    # if end_station_id not in df2['ST_ID'].values:
    #     print(f'{end_station_id}')
    #     continue

    station_connection1 = StationConnection(
        from_station=start_station_id,
        to_station=end_station_id,
        length=length
    )
    station_connection2 = StationConnection(
        from_station=end_station_id,
        to_station=start_station_id,
        length=length
    )
    try:
        Session.add(station_connection1)
        Session.add(station_connection2)
        Session.commit()
    except:
        print(f': {start_station_id} -> {end_station_id}')

    if i % 1000 == 0:
        print(f'added station connection {start_station_id} -> {end_station_id}: {length} km')
