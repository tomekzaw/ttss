import json
from datetime import datetime, time
from pathlib import Path

from ttss.Passage import Passage
from ttss.Route import Route
from ttss.Status import Status
from ttss.Stop import Stop
from ttss.StopPoint import StopPoint
from ttss.Trip import Trip
from ttss.Vehicle import Vehicle
from ttss.extractors import extract_autocomplete_stops, extract_autocomplete_stops_json, extract_stops, \
    extract_stop_points, extract_stop, extract_stop_point, extract_stop_passages, extract_trip_passages, \
    extract_routes, extract_route_stops, extract_route_paths, extract_vehicle_paths, extract_vehicles

resources_dir = Path(__file__).parent / 'resources'


def test_extract_autocomplete_stops() -> None:
    with open(resources_dir / 'lookup_autocomplete.html', 'r', encoding='utf-8') as f:
        data = f.read()

    assert extract_autocomplete_stops(data) == [
        Stop(name='Dworcowa', number='623'),
        Stop(name='Dworzec Główny', number='131'),
        Stop(name='Dworzec Główny Tunel', number='1173'),
        Stop(name='Dworzec Główny Zachód', number='2608'),
        Stop(name='Dworzec Płaszów Estakada', number='2870'),
        Stop(name='Dworzec Towarowy', number='70'),
    ]


def test_extract_autocomplete_stops_json() -> None:
    with open(resources_dir / 'lookup_autocomplete_json.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    assert extract_autocomplete_stops_json(data) == [
        Stop(name='Dworcowa', number='623'),
        Stop(name='Dworzec Główny', number='131'),
        Stop(name='Dworzec Główny Tunel', number='1173'),
        Stop(name='Dworzec Główny Zachód', number='2608'),
        Stop(name='Dworzec Płaszów Estakada', number='2870'),
        Stop(name='Dworzec Towarowy', number='70'),
    ]


def test_extract_stops() -> None:
    with open(resources_dir / 'geoserviceDispatcher_stopinfo_stops.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    stops = extract_stops(data)

    assert len(stops) == 4

    assert stops[0] == Stop(id='8059230041856278737',
                            name='Dworzec Główny',
                            number='131',
                            category='other',
                            latitude=50.064665,
                            longitude=19.945006111111113)

    assert stops[2] == Stop(id='8059230041856278863',
                            name='Dworzec Główny Zachód',
                            number='2608',
                            category='tram',
                            latitude=50.06803361111111,
                            longitude=19.945360833333332)


def test_extract_stop_points() -> None:
    with open(resources_dir / 'geoserviceDispatcher_stopinfo_stopPoints.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    stop_points = extract_stop_points(data)

    assert len(stop_points) == 12

    assert stop_points[1] == StopPoint(id='8059229492100477779',
                                       name='Dworzec Główny (13139)',
                                       code='13139',
                                       category='other',
                                       label='D',
                                       latitude=50.0642325,
                                       longitude=19.945034166666666)

    assert stop_points[9] == StopPoint(id='8059229492100725469',
                                       name='Dworzec Główny Zachód (260829)',
                                       code='260829',
                                       category='tram',
                                       label='B',
                                       latitude=50.06782694444444,
                                       longitude=19.945408055555557)


def test_extract_stop() -> None:
    with open(resources_dir / 'stopInfo_stop.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    stop = extract_stop(data)

    assert stop == Stop(id='8059230041856279380', name='Teatr Słowackiego')


def test_extract_stop_point() -> None:
    with open(resources_dir / 'stopInfo_stopPoint.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    stop_point = extract_stop_point(data)

    assert stop_point == StopPoint(id='8059229492100788879', name='Teatr Słowackiego (324239)', code='324239')


def test_extract_stop_passages() -> None:
    with open(resources_dir / 'passageInfo_stopPassages_stop.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    now = datetime(2021, 6, 28, 21, 33, 19)

    stop, passages = extract_stop_passages(data, now=now)

    expected_stop = Stop(name='Teatr Słowackiego')
    assert stop == expected_stop

    assert len(passages) == 65

    expected_route = Route(id='8059228650286874686', name='24')
    expected_trip = Trip(id='8059232507168618514', route=expected_route, direction='Bronowice Małe')
    expected_vehicle = Vehicle(id='-1188950296502609670', trip=expected_trip)
    assert passages[0] == Passage(id='-1188950300820634092',
                                  old=True,
                                  status=Status.DEPARTED,
                                  planned_time=time(21, 30),
                                  actual_time=None,
                                  dt=datetime(2021, 6, 28, 21, 29, 55),
                                  stop=expected_stop,
                                  trip=expected_trip,
                                  route=expected_route,
                                  vehicle=expected_vehicle)

    expected_route = Route(id='8059228650286874679', name='3')
    expected_trip = Trip(id='8059232507168765972', route=expected_route, direction='Nowy Bieżanów P+R')
    expected_vehicle = Vehicle(id='-1188950296502609298', trip=expected_trip)
    assert passages[2] == Passage(id='-1188950300820626854',
                                  old=False,
                                  status=Status.STOPPING,
                                  planned_time=time(21, 32),
                                  actual_time=time(21, 33),
                                  dt=datetime(2021, 6, 28, 21, 32, 55),
                                  stop=expected_stop,
                                  trip=expected_trip,
                                  route=expected_route,
                                  vehicle=expected_vehicle)

    expected_route = Route(id='8059228650286874686', name='24')
    expected_trip = Trip(id='8059232507168155665', route=expected_route, direction='Kurdwanów P+R')
    assert passages[3] == Passage(id='-1188950300820628464',
                                  old=False,
                                  status=Status.PLANNED,
                                  planned_time=time(21, 34),
                                  actual_time=None,
                                  dt=datetime(2021, 6, 28, 21, 33, 55),
                                  stop=expected_stop,
                                  trip=expected_trip,
                                  route=expected_route,
                                  vehicle=None)

    expected_route = Route(id='8059228650286875567', name='14')
    expected_trip = Trip(id='8059232507167852560', route=expected_route, direction='Bronowice')
    expected_vehicle = Vehicle(id='-1188950296502609338', trip=expected_trip)
    assert passages[4] == Passage(id='-1188950300820635578',
                                  old=False,
                                  status=Status.PREDICTED,
                                  planned_time=time(21, 36),
                                  actual_time=time(21, 36),
                                  dt=datetime(2021, 6, 28, 21, 35, 55),
                                  stop=expected_stop,
                                  trip=expected_trip,
                                  route=expected_route,
                                  vehicle=expected_vehicle)


def test_extract_stop_point_passages() -> None:
    with open(resources_dir / 'passageInfo_stopPassages_stopPoint.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    now = datetime(2021, 6, 28, 21, 33, 19)

    stop, passages = extract_stop_passages(data, now=now)

    expected_stop = Stop(name='Teatr Słowackiego')
    assert stop == expected_stop

    assert len(passages) == 16

    expected_route = Route(id='8059228650286874686', name='24')
    expected_trip = Trip(id='8059232507168618514', route=expected_route, direction='Bronowice Małe')
    expected_vehicle = Vehicle(id='-1188950296502609670', trip=expected_trip)
    assert passages[0] == Passage(id='-1188950300820634092',
                                  old=True,
                                  status=Status.DEPARTED,
                                  planned_time=time(21, 30),
                                  actual_time=None,
                                  dt=datetime(2021, 6, 28, 21, 29, 55),
                                  stop=expected_stop,
                                  trip=expected_trip,
                                  route=expected_route,
                                  vehicle=expected_vehicle)

    expected_route = Route(id='8059228650286874694', name='52')
    expected_trip = Trip(id='8059232507167926286', route=expected_route, direction='Os.Piastów')
    assert passages[1] == Passage(id='-1188950300820628463',
                                  old=False,
                                  status=Status.PLANNED,
                                  planned_time=time(21, 39),
                                  actual_time=None,
                                  dt=datetime(2021, 6, 28, 21, 38, 55),
                                  stop=expected_stop,
                                  trip=expected_trip,
                                  route=expected_route,
                                  vehicle=None)

    expected_route = Route(id='8059228650286874679', name='3')
    expected_trip = Trip(id='8059232507168970772', route=expected_route, direction='Krowodrza Górka')
    expected_vehicle = Vehicle(id='-1188950296502609386', trip=expected_trip)
    assert passages[2] == Passage(id='-1188950300820629382',
                                  old=False,
                                  status=Status.PREDICTED,
                                  planned_time=time(21, 43),
                                  actual_time=time(21, 43),
                                  dt=datetime(2021, 6, 28, 21, 42, 55),
                                  stop=expected_stop,
                                  trip=expected_trip,
                                  route=expected_route,
                                  vehicle=expected_vehicle)


def test_extract_trip_passages() -> None:
    with open(resources_dir / 'tripInfo_tripPassages.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    trip, passages = extract_trip_passages(data)

    expected_route = Route(name='24')
    expected_trip = Trip(route=expected_route, direction='Bronowice Małe')
    assert trip == expected_trip

    assert len(passages) == 13

    assert passages[0] == Passage(actual_time=time(21, 30),
                                  old=True,
                                  status=Status.DEPARTED,
                                  stop=Stop(id='8059230041856279380', name='Teatr Słowackiego', number='3242'),
                                  seq_num=16,
                                  trip=expected_trip,
                                  route=expected_route)

    assert passages[2] == Passage(actual_time=time(21, 34),
                                  old=False,
                                  status=Status.PREDICTED,
                                  stop=Stop(id='8059230041856278719', name='Teatr Bagatela', number='77'),
                                  seq_num=18,
                                  trip=expected_trip,
                                  route=expected_route)


def test_extract_routes() -> None:
    with open(resources_dir / 'routeInfo_route.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    routes = extract_routes(data)

    assert len(routes) == 25

    assert routes[0] == Route(id='8059228650286874655',
                              name='1',
                              authority='MPK',
                              directions=['Salwator', 'Wzgórza Krzesławickie'],
                              alerts=[])


def test_extract_route_stops() -> None:
    with open(resources_dir / 'routeInfo_routeStops.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    route, stops = extract_route_stops(data)

    assert route == Route(id='8059228650286874655',
                          name='1',
                          authority='MPK',
                          directions=['Salwator', 'Wzgórza Krzesławickie'],
                          alerts=[])

    assert len(stops) == 49

    assert stops[0] == Stop(id='8059230041856278841',
                            name='Bieńczycka',
                            number='867')


def test_extract_route_paths() -> None:
    with open(resources_dir / 'geoserviceDispatcher_pathinfo_route.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    paths = extract_route_paths(data)

    assert len(paths) == 2

    assert paths[0].color == '#f89f05'
    assert len(paths[0].waypoints) == 507
    assert paths[0].waypoints[0] == (50.09481611111111, 20.065258888888888)
    assert paths[0].waypoints[506] == (50.05264, 19.913836944444444)

    assert paths[1].color == '#f89f05'
    assert len(paths[1].waypoints) == 561
    assert paths[1].waypoints[0] == (50.05264, 19.913836944444444)
    assert paths[1].waypoints[560] == (50.09481611111111, 20.065258888888888)


def test_extract_vehicle_paths() -> None:
    with open(resources_dir / 'geoserviceDispatcher_pathinfo_vehicle.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    paths = extract_vehicle_paths(data)

    assert len(paths) == 1

    assert paths[0].color == '#f89f05'
    assert len(paths[0].waypoints) == 434

    assert paths[0].waypoints[0] == (50.01357194444444, 19.950415)
    assert paths[0].waypoints[433] == (50.08179694444444, 19.88190888888889)


def test_extract_vehicles() -> None:
    with open(resources_dir / 'geoserviceDispatcher_vehicleinfo_vehicles.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    vehicles = extract_vehicles(data)

    assert len(vehicles) == 754

    assert vehicles[0] == Vehicle(id='-1188950296508647671', active=False)

    assert vehicles[742] == Vehicle(id='-1188950296502609662',
                                    active=True,
                                    latitude=50.01460194444444,
                                    longitude=19.927843888888887,
                                    heading=None,
                                    category='tram',
                                    color='0x000000',
                                    trip=Trip(id='8059232507168356371',
                                              route=Route(name='19'),
                                              direction='Dworzec Towarowy'))

    assert vehicles[753] == Vehicle(id='-1188950296502609818',
                                    active=True,
                                    latitude=50.09469611111111,
                                    longitude=20.06513888888889,
                                    heading=180,
                                    category='tram',
                                    color='0x000000',
                                    trip=Trip(id='8059232507168536594',
                                              route=Route(name='1'),
                                              direction='Zajezdnia Nowa Huta'))
