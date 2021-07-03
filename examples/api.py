from pprint import pprint

from ttss.TTSS import TTSS

if __name__ == '__main__':
    # base_url = 'http://www.ttss.krakow.pl'
    base_url = 'http://ttss.mpk.krakow.pl'

    ttss = TTSS(base_url)

    stops = ttss.autocomplete_stops(query='Rondo')
    pprint(stops)

    stops = ttss.autocomplete_stops_json(query='Rondo')
    pprint(stops)

    results = ttss.lookup_fulltext(search='Rondo')
    pprint(results)

    results = ttss.lookup_fulltext(search='3041')
    pprint(results)

    stops = ttss.get_stops_by_character(character='A')
    pprint(stops)

    stops = ttss.get_stops()
    pprint(stops)

    stops = ttss.get_stops(min_latitude=50.06, min_longitude=19.94, max_latitude=50.07, max_longitude=19.95)
    pprint(stops)
    stop_number = stops[0].number

    stop_points = ttss.get_stop_points()
    pprint(stop_points)

    stop_points = ttss.get_stop_points(min_latitude=50.06, min_longitude=19.94, max_latitude=50.07, max_longitude=19.95)
    pprint(stop_points)
    stop_point_code = stop_points[0].code

    stop = ttss.get_stop(stop_number=stop_number)
    pprint(stop)

    assert ttss.get_stop(stop_number='9999') is None

    stop_point = ttss.get_stop_point(stop_point_code=stop_point_code)
    pprint(stop_point)

    assert ttss.get_stop_point(stop_point_code='999999') is None

    stop, routes, passages = ttss.get_stop_passages(stop_number=stop_number)
    pprint(stop)
    pprint(routes)
    pprint(passages)
    passage = next(passage for passage in passages if passage.vehicle is not None)
    vehicle_id = passage.vehicle.id
    trip_id = passage.trip.id
    route_id = passage.trip.route.id
    direction = passage.trip.direction

    stop, routes, passages = ttss.get_stop_passages(stop_number=stop_number, route_id=route_id)
    pprint(stop)
    pprint(routes)
    pprint(passages)

    stop, routes, passages = ttss.get_stop_passages(stop_number=stop_number, direction=direction)
    pprint(stop)
    pprint(routes)
    pprint(passages)

    stop, routes, passages = ttss.get_stop_passages(stop_number=stop_number, route_id=route_id, direction=direction)
    pprint(stop)
    pprint(routes)
    pprint(passages)

    stop, routes, passages = ttss.get_stop_point_passages(stop_point_code=stop_point_code)
    pprint(stop)
    pprint(routes)
    pprint(passages)

    stop, routes, passages = ttss.get_stop_point_passages(stop_point_code=stop_point_code, route_id=route_id)
    pprint(stop)
    pprint(routes)
    pprint(passages)

    stop, routes, passages = ttss.get_stop_point_passages(stop_point_code=stop_point_code, direction=direction)
    pprint(stop)
    pprint(routes)
    pprint(passages)

    stop, routes, passages = ttss.get_stop_point_passages(stop_point_code=stop_point_code, route_id=route_id, direction=direction)
    pprint(stop)
    pprint(routes)
    pprint(passages)

    trip, passages = ttss.get_trip_passages(trip_id=trip_id)
    pprint(trip)
    pprint(passages)

    trip, passages = ttss.get_trip_passages(trip_id=trip_id, vehicle_id=vehicle_id)
    pprint(trip)
    pprint(passages)

    routes = ttss.get_routes()
    pprint(routes)
    route = routes[0]
    route_id = route.id
    direction = route.directions[0]

    route, stops = ttss.get_route_stops(route_id=route_id)
    pprint(route)
    pprint(stops)

    paths = ttss.get_route_paths(route_id=route_id)
    pprint(paths)

    paths = ttss.get_route_paths(route_id=route_id, direction=direction)
    pprint(paths)

    vehicles = ttss.get_vehicles()
    pprint(vehicles)

    paths = ttss.get_vehicle_paths(vehicle_id=vehicle_id)
    pprint(paths)
