'''
STATION_COORDS_HACKATON.xlsx

Example:
ST_ID	LATITUDE	LONGITUDE
2	48	42
3	48	42

'''

import faker
import pandas as pd

from controller import Session, engine
from models import Station, Base

Base.metadata.create_all(engine)

df = pd.read_excel('./data/STATION_COORDS_HACKATON.xlsx')
df = df.interpolate()

sosi = faker.Faker('ru_RU')

for i in range(len(df)):
    station_id = int(df['ST_ID'][i])
    latitude = float(df['LATITUDE'][i])
    longitude = float(df['LONGITUDE'][i])

    station = Station(
        id=station_id,
        name=sosi.city() + ' ' + sosi.city_suffix() + ' ' + sosi.street_name() + ' ' + sosi.lexify(text='???????'),
        latitude=latitude,
        longitude=longitude
    )
    Session.add(station)

    if i % 1000 == 0:
        print(f'added station {station_id}: {station.name} ({latitude}, {longitude})')

Session.commit()
print('success')
