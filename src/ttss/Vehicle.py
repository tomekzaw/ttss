from dataclasses import dataclass
from typing import Optional

from ttss.Trip import Trip


@dataclass
class Vehicle:
    id: Optional[str] = None
    active: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    heading: Optional[int] = None
    category: Optional[str] = None
    color: Optional[str] = None
    trip: Optional[Trip] = None
