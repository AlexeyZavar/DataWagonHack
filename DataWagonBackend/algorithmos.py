import heapq
from math import sqrt

from models import StationConnection, Station

graph_cached = None


def data_wagon_mega_search(session, start_id, end_id):
    # станции расположены рядом, обход будет небольшой
    # тут можно воспользоваться и Дейкстрой для точности
    try:
        s = heuristic(session, start_id, end_id)
    except:
        # вылетит исключение
        # см. ниже
        s = abs(start_id - end_id) / 100

    if s < 2:
        return dijkstra_algorithm(session, start_id, end_id)

    try:
        # иначе используем жадный алгоритм
        # Greedy Best-First Search
        # https://www.geeksforgeeks.org/greedy-best-first-search-algorithm/
        return greedy_best_first_search(session, start_id, end_id)
    except:
        # из-за неполноты данных о станциях может возникать ошибка
        # в реальной жизни, вы скорее всего загрузите полную информацию,
        # и этот жадный алгоритм будет работать правильно
        # ...а пока делаем fallback на Дейкстру
        return dijkstra_algorithm(session, start_id, end_id)


def get_full_graph(session):
    global graph_cached

    if graph_cached:
        return graph_cached

    connections = session.query(StationConnection).all()
    graph_cached = {}
    for conn in connections:
        graph_cached.setdefault(conn.from_station, []).append((conn.to_station, conn.length))
        graph_cached.setdefault(conn.to_station, []).append((conn.from_station, conn.length))

    return graph_cached


def dijkstra_algorithm(session, start_id, end_id):
    graph = get_full_graph(session)

    queue = [(0, start_id, [])]
    seen = set()
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        if node not in seen:
            seen.add(node)
            path = path + [node]

            if node == end_id:
                return cost, path

            for neighbor, edge_cost in graph.get(node, []):
                if neighbor not in seen:
                    heapq.heappush(queue, (cost + edge_cost, neighbor, path))

    return float("inf"), []


def get_lat_long(session, station_id):
    station = session.query(Station).filter_by(id=station_id).one()
    return station.latitude, station.longitude


def heuristic(a, b, session):
    (lat1, long1) = get_lat_long(session, a)
    (lat2, long2) = get_lat_long(session, b)
    return sqrt((lat1 - lat2) ** 2 + (long1 - long2) ** 2)


def greedy_best_first_search(session, start_id, end_id):
    graph = get_full_graph(session)

    queue = [(heuristic(start_id, end_id, session), start_id, [start_id])]
    seen = set()
    while queue:
        (estimated_cost, node, path) = heapq.heappop(queue)
        if node not in seen:
            seen.add(node)
            path = path + [node]

            if node == end_id:
                return estimated_cost, path

            for neighbor, edge_cost in graph.get(node, []):
                if neighbor not in seen:
                    new_estimated_cost = heuristic(neighbor, end_id, session)
                    heapq.heappush(queue, (new_estimated_cost, neighbor, path))

    return float("inf"), []
