'''
DISL_HACKATON

Название колонок в файле:
- WAGNUM – номер вагона
- OPERDATE – дата отправки
- ST_ID_DISL – станция отправки
- ST_ID_DEST – станция назначения вагона
- TRAIN_INDEX - номер поезда движения вагона

TRAIN_INDEX:

Пример:
WAGNUM	OPERDATE	            ST_ID_DISL	ST_ID_DEST	TRAIN_INDEX
5,266	30/Aug/2023 01:02:00	7,475	    61	         7475-335-62
5,266	30/Aug/2023 05:26:00	63	        61	         7475-335-62
5,266	30/Aug/2023 05:05:00	7,475	    61	         7475-335-62
5,266	28/Aug/2023 23:45:00	7,475	    61	         6999-471-7475
5,266	28/Aug/2023 22:29:00	7,469	    61	         6999-471-7475


'''
from pprint import pprint

import pandas as pd

from controller import engine
from models import Base

Base.metadata.create_all(engine)

df2 = pd.read_excel('./data/STATION_COORDS_HACKATON.xlsx')
df2 = df2.interpolate()

df = pd.read_excel('./data/DISL_HACKATON.xlsx')

# sort by WAGNUM and OPERDATE
df = df.sort_values(by=['WAGNUM', 'OPERDATE'])

wagons = {}
trains = {}

# for i in range(len(df)):
for i in range(30):
    wagon_id = int(df['WAGNUM'][i])
    start_station_id = int(df['ST_ID_DISL'][i])
    end_station_id = int(df['ST_ID_DEST'][i])
    train_idx = df['TRAIN_INDEX'][i]

    train_start_station_id = int(train_idx.split('-')[0])
    train_id = int(train_idx.split('-')[1])
    train_end_station_id = int(train_idx.split('-')[2])

    ts = df['OPERDATE'][i]

    # check if station exists from pd2
    if start_station_id not in df2['ST_ID'].values:
        print(f'{start_station_id}')
        continue

    if end_station_id not in df2['ST_ID'].values:
        print(f'{end_station_id}')
        continue

    if wagon_id not in wagons:
        wagons[wagon_id] = {
            'train_id': train_id,
            'current_station_id': start_station_id,
            'target_station_id': end_station_id,
            'ts': ts
        }
    else:
        if wagons[wagon_id]['current_station_id'] != start_station_id:
            wagons[wagon_id]['ts'] = ts

        wagons[wagon_id]['current_station_id'] = start_station_id
        wagons[wagon_id]['target_station_id'] = end_station_id

    if train_id not in trains:
        trains[train_id] = {
            'start_station_id': train_start_station_id,
            'current_station_id': start_station_id,
            'end_station_id': train_end_station_id
        }
    else:
        trains[train_id]['start_station_id'] = train_start_station_id
        trains[train_id]['current_station_id'] = start_station_id
        trains[train_id]['end_station_id'] = train_end_station_id

    if i % 1000 == 0:
        print(f'added wagon {wagon_id}: {start_station_id} -> {end_station_id} ({ts})')

pprint(wagons)
pprint(trains)
