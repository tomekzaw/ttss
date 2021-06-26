import re
from datetime import timedelta, datetime
from html import unescape
from typing import List, Dict, Tuple, Optional, Any

from ttss.Passage import Passage
from ttss.Path import Path
from ttss.Route import Route
from ttss.Status import Status
from ttss.Stop import Stop
from ttss.StopPoint import StopPoint
from ttss.Trip import Trip
from ttss.Vehicle import Vehicle
from ttss.utils import parse_time


def extract_autocomplete_stops(html_text: str, /) -> List[Stop]:
    pattern = re.compile(r'<li stop="(\d+)">(.*)</li>')
    matches = re.finditer(pattern, html_text)
    return [
        Stop(number=match.group(1), name=unescape(match.group(2)))
        for match in matches
    ]


def extract_autocomplete_stops_json(data: dict, /) -> List[Stop]:
    return [
        Stop(number=stop['id'], name=stop['name'])
        for stop in data[1:]
    ]


def extract_stops(data: dict, /) -> List[Stop]:
    return [
        Stop(id=stop['id'],
             name=stop['name'],
             number=stop['shortName'],
             category=stop['category'],
             latitude=stop['latitude'] / 3_600_000,
             longitude=stop['longitude'] / 3_600_000)
        for stop in data['stops']
    ]


def extract_stop_points(data: dict, /) -> List[StopPoint]:
    return [
        StopPoint(id=stop_point['id'],
                  name=stop_point['name'],
                  code=stop_point['stopPoint'],
                  category=stop_point['category'],
                  latitude=stop_point['latitude'] / 3_600_000,
                  longitude=stop_point['longitude'] / 3_600_000)
        for stop_point in data['stopPoints']
    ]


def extract_stop(data: dict, /) -> Stop:
    return Stop(id=data['id'], name=data['passengerName'])


def extract_stop_point(data: dict, /) -> StopPoint:
    return StopPoint(id=data['id'], name=data['passengerName'], code=data['stopPointCode'])


def extract_stop_passages(data: dict, /, *, now: datetime) -> Tuple[Stop, List[Passage]]:
    stop = Stop(name=data['stopName'])
    passages = extract_stop_passages_list(data['old'], old=True, now=now) + \
               extract_stop_passages_list(data['actual'], old=False, now=now)  # noqa
    return stop, passages


def extract_stop_passages_list(passages: List[Dict[str, Any]], /, *, old: bool, now: datetime) -> List[Passage]:
    return [extract_stop_passage(passage, old=old, now=now) for passage in passages]


def extract_stop_passage(passage: Dict[str, Any], /, *, old: bool, now: datetime) -> Passage:
    trip = Trip(id=passage['tripId'],
                route_number=passage['patternText'],
                direction=passage['direction'])

    route = Route(id=passage['routeId'], name=passage['patternText'])

    vehicle = Vehicle(id=passage['vehicleId'], trip=trip) if 'vehicleId' in passage else None

    return Passage(id=passage['passageid'],
                   trip=trip,
                   route=route,
                   vehicle=vehicle,
                   planned_time=parse_time(passage['plannedTime']),
                   actual_time=parse_time(passage['actualTime']) if 'actualTime' in passage else None,
                   dt=now + timedelta(seconds=passage['actualRelativeTime']),
                   status=Status(passage['status']),
                   old=old)


def extract_stop_point_passages(data: dict, /, *, now: datetime) -> Tuple[Stop, List[Passage]]:
    return extract_stop_passages(data, now=now)


def extract_trip_passages_list(passages: List[Dict[str, Any]], /, *, old: bool) -> List[Passage]:
    return [extract_trip_passage(passage, old=old) for passage in passages]


def extract_trip_passage(data: dict, /, *, old: bool) -> Passage:
    trip = Trip(route_number=data.get('patternText', None),
                direction=data.get('direction', None))

    stop = Stop(id=data['stop']['id'],
                name=data['stop']['name'],
                number=data['stop']['shortName'])

    return Passage(trip=trip,
                   stop=stop,
                   seq_num=int(data['stop_seq_num']),
                   actual_time=parse_time(data['actualTime']),
                   status=Status(data['status']),
                   old=old)


def extract_trip_passages(data: dict, /) -> Tuple[Optional[Trip], List[Passage]]:
    trip = Trip(route_number=data.get('routeName', None),
                direction=data.get('directionText', None))
    passages = extract_trip_passages_list(data['old'], old=True) + \
               extract_trip_passages_list(data['actual'], old=False)  # noqa
    return trip, passages


def extract_routes(data: dict, /) -> List[Route]:
    return [extract_route(route) for route in data['routes']]


def extract_route_stops(data: dict, /) -> Tuple[Route, List[Stop]]:
    route = extract_route(data['route'])
    stops = [
        Stop(id=stop['id'], name=stop['name'], number=stop['number'])
        for stop in data['stops']
    ]
    return route, stops


def extract_route(data: dict, /) -> Route:
    return Route(id=data['id'],
                 name=data['name'],
                 authority=data['authority'],
                 directions=data.get('directions', []),
                 alerts=data['alerts'])


def extract_route_paths(data: dict, /) -> List[Path]:
    return extract_paths(data)


def extract_vehicle_paths(data: dict, /) -> List[Path]:
    return extract_paths(data)


def extract_paths(data: dict, /) -> List[Path]:
    return [extract_path(path) for path in data['paths']]


def extract_path(data: dict, /) -> Path:
    waypoints = [
        (point['lat'] / 3_600_000, point['lon'] / 3_600_000)
        for point in data['wayPoints']
    ]
    return Path(color=data['color'], waypoints=waypoints)


def extract_vehicles(data: dict, /) -> List[Vehicle]:
    return [extract_vehicle(vehicle) for vehicle in data['vehicles']]


def extract_vehicle(data: dict, /) -> Vehicle:
    latitude = data['latitude'] / 3_600_000 if 'latitude' in data else None
    longitude = data['longitude'] / 3_600_000 if 'longitude' in data else None

    if 'name' in data:
        route_number, direction = data['name'].split(' ', 1)
    else:
        route_number = direction = None

    trip = Trip(id=data.get('tripId', None),
                route_number=route_number,
                direction=direction)

    return Vehicle(id=data['id'],
                   active='isDeleted' not in data,
                   category=data.get('category', None),
                   latitude=latitude,
                   longitude=longitude,
                   heading=data.get('heading', None),
                   color=data.get('color', None),
                   trip=trip)
