from pprint import pprint

from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from algorithmos import data_wagon_mega_search
from controller import Session, engine
from models import Station, Base, Train, Wagon
from utils import convert_to_dict, jsonify_trains, jsonify_wagons, jsonify_stations, group_stations, jsonify_station

Base.metadata.create_all(engine)

HOST = 'localhost'
PORT = 8000

app = Flask(__name__)
CORS(app)


@app.get('/stations')
def get_stations():
    session = Session()

    latitude1 = request.args.get('latitude1')
    longitude1 = request.args.get('longitude1')
    latitude2 = request.args.get('latitude2')
    longitude2 = request.args.get('longitude2')
    zoom = float(request.args.get('zoom'))

    latitude1 = float(latitude1)
    longitude1 = float(longitude1)
    latitude2 = float(latitude2)
    longitude2 = float(longitude2)

    # find where latitude and longitude are in range
    stations = session.query(Station).options(
        joinedload(Station.trains).joinedload(Train.start_station),
        joinedload(Station.trains).joinedload(Train.current_station),
        joinedload(Station.trains).joinedload(Train.end_station),
        joinedload(Station.trains).joinedload(Train.wagons),
        joinedload(Station.trains).joinedload(Train.wagons).joinedload(Wagon.current_station),
        joinedload(Station.trains).joinedload(Train.wagons).joinedload(Wagon.target_station),
        joinedload(Station.wagons).joinedload(Wagon.current_station),
        joinedload(Station.wagons).joinedload(Wagon.target_station),
    ).where(
        latitude1 <= Station.latitude,
        Station.latitude <= latitude2,
        longitude1 <= Station.longitude,
        Station.longitude <= longitude2
    ).all()

    # группировка рядом стоящих станций, чтобы карта не лагала
    grouped = False
    if (zoom < 10 or len(stations) > 350) and stations:
        stations = group_stations(stations)
        grouped = True

    res = [convert_to_dict(station) for station in stations]

    if not grouped:
        jsonify_stations(res)

    try:
        return jsonify(res)
    except:
        pprint(res)
        return jsonify([])


@app.get('/search')
def search_anything():
    query = request.args.get('q')

    query_int = -1
    try:
        query_int = int(query)
    except:
        pass

    session = Session()

    res = {
        'trains': [],
        'wagons': [],
        'stations': []
    }

    # find trains
    trains = session.query(Train).options(
        joinedload(Train.wagons).joinedload(Wagon.current_station),
        joinedload(Train.wagons).joinedload(Wagon.target_station),
        joinedload(Train.start_station),
        joinedload(Train.current_station),
        joinedload(Train.end_station)
    ).where(
        Train.id == query_int
    ).limit(20).all()
    res['trains'] = [convert_to_dict(train) for train in trains]
    jsonify_trains(res['trains'])

    # find wagons
    wagons = session.query(Wagon).options(
        joinedload(Wagon.current_station),
        joinedload(Wagon.target_station),
    ).where(
        Wagon.id == query_int
    ).limit(20).all()
    res['wagons'] = [convert_to_dict(wagon) for wagon in wagons]
    jsonify_wagons(res['wagons'])

    # find stations
    stations = session.query(Station).options(
        joinedload(Station.trains).joinedload(Train.start_station),
        joinedload(Station.trains).joinedload(Train.current_station),
        joinedload(Station.trains).joinedload(Train.end_station),
        joinedload(Station.trains).joinedload(Train.wagons),
        joinedload(Station.trains).joinedload(Train.wagons).joinedload(Wagon.current_station),
        joinedload(Station.trains).joinedload(Train.wagons).joinedload(Wagon.target_station),
        joinedload(Station.wagons).joinedload(Wagon.current_station),
        joinedload(Station.wagons).joinedload(Wagon.target_station),
    ).where(
        or_(Station.name.like(f'%{query}%'), Station.id == query_int)
    ).limit(20).all()
    res['stations'] = [convert_to_dict(station) for station in stations]
    jsonify_stations(res['stations'])

    try:
        return jsonify(res)
    except:
        pprint(res)
        return jsonify([])


@app.get('/build_route')
def buildos():
    from_station_id = request.args.get('from')
    to_station_id = request.args.get('to')

    from_station_id = int(from_station_id)
    to_station_id = int(to_station_id)

    session = Session()

    from_station = session.query(Station).where(Station.id == from_station_id).first()
    to_station = session.query(Station).where(Station.id == to_station_id).first()

    if from_station is None or to_station is None:
        return jsonify({'error': 'no such stations'})

    path_cost, path = data_wagon_mega_search(session, from_station_id, to_station_id)

    stations = session.query(Station).options(
        joinedload(Station.trains).joinedload(Train.start_station),
        joinedload(Station.trains).joinedload(Train.current_station),
        joinedload(Station.trains).joinedload(Train.end_station),
        joinedload(Station.trains).joinedload(Train.wagons),
        joinedload(Station.trains).joinedload(Train.wagons).joinedload(Wagon.current_station),
        joinedload(Station.trains).joinedload(Train.wagons).joinedload(Wagon.target_station),
        joinedload(Station.wagons).joinedload(Wagon.current_station),
        joinedload(Station.wagons).joinedload(Wagon.target_station),
    ).where(Station.id.in_(path)).all()
    stations_dict = {}
    for station in stations:
        stations_dict[station.id] = convert_to_dict(station)
        jsonify_station(stations_dict[station.id])

    return jsonify({
        'path_cost': path_cost,
        'path': path,
        'stations': stations_dict
    })


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
