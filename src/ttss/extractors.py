import re
from datetime import timedelta, datetime
from html import unescape
from typing import List, Dict, Tuple, Optional, Any, Union

from ttss.Passage import Passage
from ttss.Path import Path
from ttss.Route import Route
from ttss.Status import Status
from ttss.Stop import Stop
from ttss.StopPoint import StopPoint
from ttss.Trip import Trip
from ttss.Vehicle import Vehicle
from ttss.utils import parse_time, round_seconds


def extract_autocomplete_stops(html_text: str, /) -> List[Stop]:
    pattern = re.compile(r'<li stop="(\d+)">(.*)</li>')
    matches = re.finditer(pattern, html_text)
    return [
        Stop(number=match.group(1), name=unescape(match.group(2)))
        for match in matches
    ]


def extract_autocomplete_stops_json(data: dict, /) -> List[Stop]:
    return [
        Stop(number=stop['id'], name=unescape(stop['name']))
        for stop in data[1:]
    ]


def extract_lookup_fulltext(data: dict, /) -> List[Union[Stop, StopPoint]]:
    return [
        (
            Stop(number=result['stop'], name=result['stopPassengerName'])
            if 'stop' in result
            else StopPoint(code=result['stopPoint'], name=result['stopPointPassengerName'])
        )
        for result in data['results']
    ]


def extract_stops_by_character(data: dict, /) -> List[Stop]:
    return [
        Stop(id=stop['id'], name=stop['name'], number=stop['number'])
        for stop in data['stops']
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
                  label=stop_point['label'],
                  latitude=stop_point['latitude'] / 3_600_000,
                  longitude=stop_point['longitude'] / 3_600_000)
        for stop_point in data['stopPoints']
    ]


def extract_stop(data: dict, /) -> Stop:
    return Stop(id=data['id'], name=data['passengerName'])


def extract_stop_point(data: dict, /) -> StopPoint:
    return StopPoint(id=data['id'], name=data['passengerName'], code=data['stopPointCode'])


def extract_stop_passages(data: dict, /, *, now: datetime) -> Tuple[Stop, List[Route], List[Passage]]:
    stop = Stop(name=data['stopName'])

    routes = [extract_route(route) for route in data['routes']]

    passages = extract_stop_passages_list(data['old'], stop=stop, now=now, old=True) + \
               extract_stop_passages_list(data['actual'], stop=stop, now=now, old=False)  # noqa

    return stop, routes, passages


def extract_stop_passages_list(passages: List[Dict[str, Any]], /, *,
                               stop: Stop, now: datetime, old: bool) -> List[Passage]:
    return [extract_stop_passage(passage, stop=stop, now=now, old=old) for passage in passages]


def extract_stop_passage(passage: Dict[str, Any], /, *, stop: Stop, now: datetime, old: bool) -> Passage:
    route = Route(id=passage['routeId'], name=passage['patternText'])

    trip = Trip(id=passage['tripId'],
                route=route,
                direction=passage['direction'])

    vehicle = Vehicle(id=passage['vehicleId'], trip=trip) if 'vehicleId' in passage else None

    return Passage(id=passage['passageid'],
                   stop=stop,
                   trip=trip,
                   route=route,
                   vehicle=vehicle,
                   planned_time=parse_time(passage['plannedTime']),
                   actual_time=parse_time(passage['actualTime']) if 'actualTime' in passage else None,
                   dt=round_seconds(now + timedelta(seconds=passage['actualRelativeTime'])),
                   status=Status(passage['status']),
                   old=old)


def extract_stop_point_passages(data: dict, /, *, now: datetime) -> Tuple[Stop, List[Route], List[Passage]]:
    return extract_stop_passages(data, now=now)


def extract_trip_passages_list(passages: List[Dict[str, Any]], /, *, trip: Trip, old: bool) -> List[Passage]:
    return [extract_trip_passage(passage, trip=trip, old=old) for passage in passages]


def extract_trip_passage(data: dict, /, *, trip: Trip, old: bool) -> Passage:
    stop = Stop(id=data['stop']['id'],
                name=data['stop']['name'],
                number=data['stop']['shortName'])

    return Passage(stop=stop,
                   seq_num=int(data['stop_seq_num']),
                   planned_time=parse_time(data['plannedTime']) if 'plannedTime' in data else None,
                   actual_time=parse_time(data['actualTime']) if 'actualTime' in data else None,
                   status=Status(data['status']),
                   trip=trip,
                   route=trip.route,
                   old=old)


def extract_trip_passages(data: dict, /) -> Tuple[Optional[Trip], List[Passage]]:
    route = Route(name=data.get('routeName', None))
    trip = Trip(route=route, direction=data.get('directionText', None))
    passages = extract_trip_passages_list(data['old'], trip=trip, old=True) + \
               extract_trip_passages_list(data['actual'], trip=trip, old=False)  # noqa
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
                 type=data.get('routeType', None),
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
    active = 'isDeleted' not in data

    latitude = data['latitude'] / 3_600_000 if 'latitude' in data else None
    longitude = data['longitude'] / 3_600_000 if 'longitude' in data else None

    if 'name' in data:
        name = data['name']
        if ' ' in name:
            route_number, direction = name.split(' ', 1)
        else:
            route_number, direction = name, None
    else:
        route_number = direction = None

    if 'tripId' in data:
        route = Route(name=route_number)
        trip = Trip(id=data.get('tripId', None),
                    route=route,
                    direction=direction)
    else:
        trip = None

    return Vehicle(id=data['id'],
                   active=active,
                   category=data.get('category', None),
                   latitude=latitude,
                   longitude=longitude,
                   heading=data.get('heading', None),
                   color=data.get('color', None),
                   trip=trip)
