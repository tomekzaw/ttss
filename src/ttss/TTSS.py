from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, List, Optional

import requests

from ttss.ColorType import ColorType
from ttss.Mode import Mode
from ttss.Passage import Passage
from ttss.Path import Path
from ttss.PositionType import PositionType
from ttss.Route import Route
from ttss.Stop import Stop
from ttss.StopPoint import StopPoint
from ttss.Trip import Trip
from ttss.Vehicle import Vehicle
from ttss.extractors import extract_autocomplete_stops, extract_autocomplete_stops_json, extract_stops, \
    extract_stop_points, extract_stop, extract_stop_point, extract_stop_passages, extract_stop_point_passages, \
    extract_trip_passages, extract_routes, extract_route_stops, extract_route_paths, extract_vehicle_paths, \
    extract_vehicles
from ttss.utils import timestamp_ms


@dataclass
class TTSS:
    base_url: str

    def autocomplete_stops(self, query: str) -> List[Stop]:
        url = f'{self.base_url}/internetservice/services/lookup/autocomplete'
        params = {
            'query': query,
            'language': 'pl',
        }
        response = requests.post(url, params)
        response.raise_for_status()
        return extract_autocomplete_stops(response.text)

    def autocomplete_stops_json(self, query: str) -> List[Stop]:
        url = f'{self.base_url}/internetservice/services/lookup/autocomplete/json'
        params = {
            'query': query,
            'language': 'pl',
        }
        response = requests.post(url, params)
        response.raise_for_status()
        return extract_autocomplete_stops_json(response.json())

    def get_stops(self, *,
                  min_latitude: float = -90.0, max_latitude: float = 90.0,
                  min_longitude: float = -180.0, max_longitude: float = 180.0) -> List[Stop]:
        url = f'{self.base_url}/internetservice/geoserviceDispatcher/services/stopinfo/stops'
        params = {
            'left': int(min_longitude * 3_600_000),
            'bottom': int(min_latitude * 3_600_000),
            'right': int(max_longitude * 3_600_000),
            'top': int(max_latitude * 3_600_000),
        }
        response = requests.post(url, params)
        response.raise_for_status()
        return extract_stops(response.json())

    def get_stop_points(self, *,
                        min_latitude: float = -90.0, max_latitude: float = 90.0,
                        min_longitude: float = -180.0, max_longitude: float = 180.0) -> List[StopPoint]:
        url = f'{self.base_url}/internetservice/geoserviceDispatcher/services/stopinfo/stopPoints'
        params = {
            'left': int(min_longitude * 3_600_000),
            'bottom': int(min_latitude * 3_600_000),
            'right': int(max_longitude * 3_600_000),
            'top': int(max_latitude * 3_600_000),
        }
        response = requests.post(url, params)
        response.raise_for_status()
        return extract_stop_points(response.json())

    def get_stop(self, stop_number: str) -> Optional[Stop]:
        url = f'{self.base_url}/internetservice/services/stopInfo/stop'
        params = {
            'stop': stop_number,
            'language': 'pl',
        }
        response = requests.post(url, params)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return extract_stop(response.json())

    def get_stop_point(self, stop_point_code: str) -> Optional[StopPoint]:
        url = f'{self.base_url}/internetservice/services/stopInfo/stopPoint'
        params = {
            'stopPoint': stop_point_code,
            'language': 'pl',
        }
        response = requests.post(url, params)
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return extract_stop_point(response.json())

    def get_stop_passages(self, stop_number: str, *,
                          mode: Mode = Mode.DEPARTURES, timeframe: int = 120) -> Tuple[Stop, List[Passage]]:
        now = datetime.now().replace(microsecond=0)
        url = f'{self.base_url}/internetservice/services/passageInfo/stopPassages/stop'
        params = {
            'language': 'pl',
            'stop': stop_number,
            'mode': mode.value,
            'timeFrame': timeframe,
            'cacheBuster': timestamp_ms(),
        }
        response = requests.post(url, params)
        response.raise_for_status()
        return extract_stop_passages(response.json(), now=now)

    def get_stop_point_passages(self, stop_point_id: str, *,
                                mode: Mode = Mode.DEPARTURES, timeframe: int = 120) -> Tuple[Stop, List[Passage]]:
        now = datetime.now().replace(microsecond=0)
        url = f'{self.base_url}/internetservice/services/passageInfo/stopPassages/stopPoint'
        params = {
            'language': 'pl',
            'stopPoint': stop_point_id,
            'mode': mode.value,
            'timeFrame': timeframe,
            'cacheBuster': timestamp_ms(),
        }
        response = requests.post(url, params)
        response.raise_for_status()
        return extract_stop_point_passages(response.json(), now=now)

    def get_trip_passages(self, trip_id: str, *, vehicle_id: Optional[str] = None,
                          mode: Mode = Mode.DEPARTURES) -> Tuple[Optional[Trip], List[Passage]]:
        url = f'{self.base_url}/internetservice/services/tripInfo/tripPassages'
        params = {
            'language': 'pl',
            'tripId': trip_id,
            'mode': mode.value,
            'vehicleId': vehicle_id,
            'cacheBuster': timestamp_ms(),
        }
        response = requests.post(url, params)
        response.raise_for_status()
        return extract_trip_passages(response.json())

    def get_routes(self) -> List[Route]:
        url = f'{self.base_url}/internetservice/services/routeInfo/route'
        params = {'language': 'pl'}
        response = requests.post(url, params)
        response.raise_for_status()
        return extract_routes(response.json())

    def get_route_stops(self, route_id: str) -> Tuple[Route, List[Stop]]:
        url = f'{self.base_url}/internetservice/services/routeInfo/routeStops'
        params = {
            'routeId': route_id,
            'language': 'pl',
            'cacheBuster': timestamp_ms(),
        }
        response = requests.post(url, params)
        response.raise_for_status()
        return extract_route_stops(response.json())

    def get_route_paths(self, route_id: str, *, direction: Optional[str] = None) -> List[Path]:
        url = f'{self.base_url}/internetservice/geoserviceDispatcher/services/pathinfo/route'
        params = {
            'id': route_id,
            'direction': direction,
        }
        response = requests.post(url, params)
        if response.status_code == 404:
            return []
        response.raise_for_status()
        return extract_route_paths(response.json())

    def get_vehicle_paths(self, vehicle_id: str) -> List[Path]:
        url = f'{self.base_url}/internetservice/geoserviceDispatcher/services/pathinfo/vehicle'
        params = {'id': vehicle_id}
        response = requests.post(url, params)
        response.raise_for_status()
        return extract_vehicle_paths(response.json())

    def get_vehicles(self, *,
                     last_update: Optional[int] = None,
                     position_type: PositionType = PositionType.CORRECTED,
                     color_type: ColorType = ColorType.ROUTE_BASED) -> List[Vehicle]:
        url = f'{self.base_url}/internetservice/geoserviceDispatcher/services/vehicleinfo/vehicles'
        params = {
            'lastUpdate': last_update,
            'positionType': position_type,
            'colorType': color_type,
        }
        response = requests.post(url, params)
        response.raise_for_status()
        return extract_vehicles(response.json())

    def get_language(self) -> None:
        # url = f'{self.base_url}/internetservice/messages/language'
        raise NotImplementedError()
