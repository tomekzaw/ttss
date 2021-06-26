from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional

from ttss.Route import Route
from ttss.Status import Status
from ttss.Stop import Stop
from ttss.Trip import Trip
from ttss.Vehicle import Vehicle


@dataclass
class Passage:
    id: Optional[str] = None
    old: Optional[bool] = None
    status: Optional[Status] = None
    planned_time: Optional[time] = None
    actual_time: Optional[time] = None
    dt: Optional[datetime] = None
    seq_num: Optional[int] = None
    stop: Optional[Stop] = None
    trip: Optional[Trip] = None
    route: Optional[Route] = None
    vehicle: Optional[Vehicle] = None
