# Wagon Hack

Наша реализация 3 кейса с хакатона Data Wagon 2023.

Заняли 5 место.

## Запуск проекта

Наша реализация обёрнута в Docker.

Запустить просто:

```bash
docker compose up
```

И открыть [localhost:6969](http://localhost:6969).

## Данные

Мы их конвертировали с помощью скриптов в `DataWagonBackend/data-scripts`, итог - SQLite БД, данные из которой можно
запросто перенести в PostgreSQL в докере. Достаточно будет поменять `CONNECTION_STRING` в `docker-compose.yaml`.

## Поиск маршрута

Алгоритм Дейкстры и жадный алгоритм с теоремой Пифагора. Они находятся в файле `DataWagonBackend/algorithmos.py`.

## На чём можно проверить

В БД есть **вагон** с ID `666666`, на котором можно посмотреть прокладку маршрута от начальной точки до конечной.

И ещё вагон с ID `1`.

Станции для проверки "занятости" - ID `716`, `748`, `8810`, `8811`.

## Команда

- [AlexeyZavar](https://github.com/AlexeyZavar)
- [SharapaGorg](https://github.com/SharapaGorg)
