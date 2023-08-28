from datetime import datetime, time
from pathlib import Path

import pytest
import pytz
from requests_mock.mocker import Mocker

from ttss import Passage, Route, Status, Stop, StopPoint, Trip, TTSS, Vehicle

base_url = 'http://www.ttss.krakow.pl'

tz = pytz.timezone('Europe/Warsaw')

resources_dir = Path(__file__).parent / 'resources'


@pytest.fixture
def ttss() -> TTSS:
    return TTSS(base_url=base_url)


def test_autocomplete_stops(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'lookup_autocomplete.html', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/services/lookup/autocomplete', text=data)

    assert ttss.autocomplete_stops(query='dwor') == [
        Stop(name='Dworcowa', number='623'),
        Stop(name='Dworzec Główny', number='131'),
        Stop(name='Dworzec Główny Tunel', number='1173'),
        Stop(name='Dworzec Główny Zachód', number='2608'),
        Stop(name='Dworzec Płaszów Estakada', number='2870'),
        Stop(name='Dworzec Towarowy', number='70'),
    ]


def test_autocomplete_stops_json(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'lookup_autocomplete_json.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/services/lookup/autocomplete/json', text=data)

    assert ttss.autocomplete_stops_json(query='dwor') == [
        Stop(name='Dworcowa', number='623'),
        Stop(name='Dworzec Główny', number='131'),
        Stop(name='Dworzec Główny Tunel', number='1173'),
        Stop(name='Dworzec Główny Zachód', number='2608'),
        Stop(name='Dworzec Płaszów Estakada', number='2870'),
        Stop(name='Dworzec Towarowy', number='70'),
    ]


def test_lookup_fulltext_stops(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'lookup_fulltext_stops.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/services/lookup/fulltext', text=data)

    assert ttss.lookup_fulltext(search='dwor') == [
        Stop(name='Dworcowa', number='623'),
        Stop(name='Dworzec Główny', number='131'),
        Stop(name='Dworzec Główny Tunel', number='1173'),
        Stop(name='Dworzec Główny Zachód', number='2608'),
        Stop(name='Dworzec Płaszów Estakada', number='2870'),
        Stop(name='Dworzec Towarowy', number='70'),
    ]


def test_lookup_fulltext_stop_points(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'lookup_fulltext_stopPoints.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/services/lookup/fulltext', text=data)

    assert ttss.lookup_fulltext(search='dwor') == [
        StopPoint(name='Dworcowa (62319)', code='62319'),
        StopPoint(name='Dworcowa (62329)', code='62329'),
        StopPoint(name='Dworcowa (62339)', code='62339'),
    ]


def test_get_stops_by_character(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'lookup_stopsByCharacter.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/services/lookup/stopsByCharacter', text=data)

    assert ttss.get_stops_by_character(character='D') == [
        Stop(id='8059230041856278824', name='Dworcowa', number='623'),
        Stop(id='8059230041856278737', name='Dworzec Główny', number='131'),
        Stop(id='8059230041856278850', name='Dworzec Główny Tunel', number='1173'),
        Stop(id='8059230041856278863', name='Dworzec Główny Zachód', number='2608'),
        Stop(id='8059230041856278952', name='Dworzec Płaszów Estakada', number='2870'),
        Stop(id='8059230041856278714', name='Dworzec Towarowy', number='70'),
    ]


def test_get_near_stops(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'lookup_autocomplete_nearStops_json.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/services/lookup/autocomplete/nearStops/json', text=data)

    near_stops = ttss.get_near_stops(latitude=50, longitude=20)

    assert len(near_stops) == 20

    assert near_stops[0] == Stop(name='Prokocim Szpital', number='682')
    assert near_stops[1] == Stop(name='Teligi', number='681')
    assert near_stops[7] == Stop(name='Nowy Bieżanów P+R', number='3175')


def test_get_stops(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'geoserviceDispatcher_stopinfo_stops.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/geoserviceDispatcher/services/stopinfo/stops', text=data)

    stops = ttss.get_stops()

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


def test_get_stop_points(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'geoserviceDispatcher_stopinfo_stopPoints.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/geoserviceDispatcher/services/stopinfo/stopPoints', text=data)

    stop_points = ttss.get_stop_points()

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


def test_get_stop(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'stopInfo_stop.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/services/stopInfo/stop', text=data)

    stop = ttss.get_stop(stop_number='3242')

    assert stop == Stop(id='8059230041856279380', name='Teatr Słowackiego')


def test_get_stop_point(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'stopInfo_stopPoint.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/services/stopInfo/stopPoint', text=data)

    stop_point = ttss.get_stop_point(stop_point_code='324239')

    assert stop_point == StopPoint(id='8059229492100788879', name='Teatr Słowackiego (324239)', code='324239')


@pytest.mark.freeze_time(datetime(2021, 6, 28, 21, 33, 19).replace(tzinfo=tz))
def test_get_stop_passages(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'passageInfo_stopPassages_stop.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/services/passageInfo/stopPassages/stop', text=data)

    stop, routes, passages = ttss.get_stop_passages(stop_number='3242')

    expected_stop = Stop(name='Teatr Słowackiego')
    assert stop == expected_stop

    assert len(routes) == 8

    assert routes[0] == Route(id='8059228650286875578',
                              name='2',
                              type='tram',
                              authority='MPK',
                              directions=['Cmentarz Rakowicki', 'Salwator'],
                              alerts=[])

    assert routes[1] == Route(id='8059228650286874679',
                              name='3',
                              type='tram',
                              authority='MPK',
                              directions=['Krowodrza Górka', 'Nowy Bieżanów P+R'],
                              alerts=[])

    assert len(passages) == 65

    expected_route = Route(id='8059228650286874686', name='24')
    expected_trip = Trip(id='8059232507168618514', route=expected_route, direction='Bronowice Małe')
    expected_vehicle = Vehicle(id='-1188950296502609670', trip=expected_trip)
    assert passages[0] == Passage(id='-1188950300820634092',
                                  old=True,
                                  status=Status.DEPARTED,
                                  planned_time=time(21, 30),
                                  actual_time=None,
                                  dt=datetime(2021, 6, 28, 21, 30).replace(tzinfo=tz),
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
                                  dt=datetime(2021, 6, 28, 21, 33).replace(tzinfo=tz),
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
                                  dt=datetime(2021, 6, 28, 21, 34).replace(tzinfo=tz),
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
                                  dt=datetime(2021, 6, 28, 21, 36).replace(tzinfo=tz),
                                  stop=expected_stop,
                                  trip=expected_trip,
                                  route=expected_route,
                                  vehicle=expected_vehicle)


@pytest.mark.freeze_time(datetime(2021, 6, 28, 21, 33, 19).replace(tzinfo=tz))
def test_get_stop_point_passages(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'passageInfo_stopPassages_stopPoint.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/services/passageInfo/stopPassages/stopPoint', text=data)

    stop, routes, passages = ttss.get_stop_point_passages(stop_point_code='324239')

    expected_stop = Stop(name='Teatr Słowackiego')
    assert stop == expected_stop

    assert len(routes) == 4

    assert routes[0] == Route(id='8059228650286874679',
                              name='3',
                              type='tram',
                              authority='MPK',
                              directions=['Krowodrza Górka', 'Nowy Bieżanów P+R'],
                              alerts=[])

    assert routes[1] == Route(id='8059228650286875580',
                              name='10',
                              type='tram',
                              authority='MPK',
                              directions=['Pleszów', 'Łagiewniki'],
                              alerts=[])

    assert len(passages) == 16

    expected_route = Route(id='8059228650286874686', name='24')
    expected_trip = Trip(id='8059232507168618514', route=expected_route, direction='Bronowice Małe')
    expected_vehicle = Vehicle(id='-1188950296502609670', trip=expected_trip)
    assert passages[0] == Passage(id='-1188950300820634092',
                                  old=True,
                                  status=Status.DEPARTED,
                                  planned_time=time(21, 30),
                                  actual_time=None,
                                  dt=datetime(2021, 6, 28, 21, 30).replace(tzinfo=tz),
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
                                  dt=datetime(2021, 6, 28, 21, 39).replace(tzinfo=tz),
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
                                  dt=datetime(2021, 6, 28, 21, 43).replace(tzinfo=tz),
                                  stop=expected_stop,
                                  trip=expected_trip,
                                  route=expected_route,
                                  vehicle=expected_vehicle)


def test_get_trip_passages_actual(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'tripInfo_tripPassages_actual.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/services/tripInfo/tripPassages', text=data)

    trip, passages = ttss.get_trip_passages(trip_id='trip_id')  # TODO: real id

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


def test_get_trip_passages_planned(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'tripInfo_tripPassages_planned.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/services/tripInfo/tripPassages', text=data)

    trip, passages = ttss.get_trip_passages(trip_id='trip_id')  # TODO: real id

    expected_route = Route(name='20')
    expected_trip = Trip(route=expected_route, direction='Mały Płaszów P+R')
    assert trip == expected_trip

    assert len(passages) == 13

    assert passages[0] == Passage(planned_time=time(13, 26),
                                  old=True,
                                  status=Status.PLANNED,
                                  stop=Stop(id='8059230041856278719', name='Teatr Bagatela', number='77'),
                                  seq_num=7,
                                  trip=expected_trip,
                                  route=expected_route)

    assert passages[2] == Passage(planned_time=time(13, 30),
                                  old=False,
                                  status=Status.PLANNED,
                                  stop=Stop(id='8059230041856279380', name='Teatr Słowackiego', number='3242'),
                                  seq_num=9,
                                  trip=expected_trip,
                                  route=expected_route)


def test_get_routes(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'routeInfo_route.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/services/routeInfo/route', text=data)

    routes = ttss.get_routes()

    assert len(routes) == 25

    assert routes[0] == Route(id='8059228650286874655',
                              name='1',
                              authority='MPK',
                              directions=['Salwator', 'Wzgórza Krzesławickie'],
                              alerts=[])


def test_get_route_stops(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'routeInfo_routeStops.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/services/routeInfo/routeStops', text=data)

    route, stops = ttss.get_route_stops(route_id='route_id')  # TODO: real id

    assert route == Route(id='8059228650286874655',
                          name='1',
                          authority='MPK',
                          directions=['Salwator', 'Wzgórza Krzesławickie'],
                          alerts=[])

    assert len(stops) == 49

    assert stops[0] == Stop(id='8059230041856278841',
                            name='Bieńczycka',
                            number='867')


def test_get_route_paths(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'geoserviceDispatcher_pathinfo_route.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/geoserviceDispatcher/services/pathinfo/route', text=data)

    paths = ttss.get_route_paths(route_id='route_id')  # TODO: real id

    assert len(paths) == 2

    assert paths[0].color == '#f89f05'
    assert len(paths[0].waypoints) == 507
    assert paths[0].waypoints[0] == (50.09481611111111, 20.065258888888888)
    assert paths[0].waypoints[506] == (50.05264, 19.913836944444444)

    assert paths[1].color == '#f89f05'
    assert len(paths[1].waypoints) == 561
    assert paths[1].waypoints[0] == (50.05264, 19.913836944444444)
    assert paths[1].waypoints[560] == (50.09481611111111, 20.065258888888888)


def test_get_vehicle_paths(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'geoserviceDispatcher_pathinfo_vehicle.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/geoserviceDispatcher/services/pathinfo/vehicle', text=data)

    paths = ttss.get_vehicle_paths(vehicle_id='vehicle_id')  # TODO: real id

    assert len(paths) == 1

    assert paths[0].color == '#f89f05'
    assert len(paths[0].waypoints) == 434

    assert paths[0].waypoints[0] == (50.01357194444444, 19.950415)
    assert paths[0].waypoints[433] == (50.08179694444444, 19.88190888888889)


def test_get_vehicles(ttss: TTSS, requests_mock: Mocker) -> None:
    with open(resources_dir / 'geoserviceDispatcher_vehicleinfo_vehicles.json', 'r', encoding='utf-8') as f:
        data = f.read()
    requests_mock.get(f'{base_url}/internetservice/geoserviceDispatcher/services/vehicleinfo/vehicles', text=data)

    vehicles = ttss.get_vehicles()

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
