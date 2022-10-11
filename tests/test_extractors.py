import pytest

from ttss.extractors import extract_vehicle


@pytest.mark.parametrize('name, expected_route_name, expected_trip_direction', [
    (None, None, None),
    ('123', '123', None),
    ('123 Mistrzejowice', '123', 'Mistrzejowice'),
    ('123 Mały Płaszów P+R', '123', 'Mały Płaszów P+R'),
])
def test_extract_vehicle(name: str, expected_route_name: str, expected_trip_direction: str) -> None:
    data = {'id': 'id', 'tripId': 'tripId'}
    if name is not None:
        data['name'] = name
    actual = extract_vehicle(data)
    assert actual.trip is not None
    assert actual.trip.route is not None
    assert actual.trip.route.name == expected_route_name
    assert actual.trip.direction == expected_trip_direction
