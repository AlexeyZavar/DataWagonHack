import numpy as np
from sklearn.cluster import DBSCAN

'''
В этом файле по большей части находятся функции для правильной сериализации моделек в json
(н.п. убирание рекурсивных зависимостей)
'''


def convert_to_dict(elem):
    """
    elem - database model, i.e. Train, Car, Route, ...
    """
    result = dict()
    ignore_keys = ["_sa_instance_state"]
    if elem is None:
        return

    if isinstance(elem, dict):
        return elem

    for var in vars(elem):
        if var in ignore_keys:
            continue

        result[var] = getattr(elem, var)

    return result


def jsonify_trains(res):
    for train in res:
        train['wagons'] = list(train['wagons'])
        for i in range(len(train['wagons'])):
            elem = train['wagons'][i]
            converted = convert_to_dict(elem)

            train['wagons'][i] = converted

        jsonify_wagons(train['wagons'])

        train['start_station'] = convert_to_dict(train['start_station'])
        train['current_station'] = convert_to_dict(train['current_station'])
        train['end_station'] = convert_to_dict(train['end_station'])


def jsonify_wagons(res):
    for wagon in res:
        wagon['current_station'] = convert_to_dict(wagon['current_station'])
        wagon['target_station'] = convert_to_dict(wagon['target_station'])


def jsonify_stations(res):
    for station in res:
        jsonify_station(station)


def jsonify_station(station):
    station['wagons'] = [convert_to_dict(wagon) for wagon in station['wagons']]
    station['trains'] = [convert_to_dict(train) for train in station['trains']]

    jsonify_wagons(station['wagons'])
    jsonify_trains(station['trains'])

    remove_for_serialization(station['wagons'])

    for train in station['trains']:
        if not train:
            continue

        if 'trains' in train['start_station']:
            del train['start_station']['trains']
        if 'wagons' in train['start_station']:
            del train['start_station']['wagons']

        if 'trains' in train['current_station']:
            del train['current_station']['trains']
        if 'wagons' in train['current_station']:
            del train['current_station']['wagons']

        if 'trains' in train['end_station']:
            del train['end_station']['trains']
        if 'wagons' in train['end_station']:
            del train['end_station']['wagons']

        remove_for_serialization(train['wagons'])


def remove_for_serialization(train_wagons):
    for wagon in train_wagons:
        if 'trains' in wagon['current_station']:
            del wagon['current_station']['trains']
        if 'wagons' in wagon['current_station']:
            del wagon['current_station']['wagons']

        if 'trains' in wagon['target_station']:
            del wagon['target_station']['trains']
        if 'wagons' in wagon['target_station']:
            del wagon['target_station']['wagons']
        #
        # if 'train' in wagon:
        #     del wagon['train']


def group_stations(stations):
    coordinates = [(station.latitude, station.longitude) for station in stations]
    X = np.array(coordinates)
    dbscan = DBSCAN(eps=0.075, min_samples=5)
    dbscan.fit(X)
    cluster_labels = dbscan.labels_
    clustered_stations = {}
    for label in set(cluster_labels):
        clustered_stations[label] = [stations[i] for i in range(len(stations)) if cluster_labels[i] == label]

    res_stations = []
    for label in clustered_stations:
        stations = clustered_stations[label]
        res_stations.append({
            'id': ''.join([str(station.id) for station in stations]),
            'latitude': np.mean([station.latitude for station in stations]),
            'longitude': np.mean([station.longitude for station in stations]),
            'name': stations[0].name,
            'trains': [],  # it's grouped so ignore
            'wagons': []  # it's grouped so ignore
        })

    return res_stations
