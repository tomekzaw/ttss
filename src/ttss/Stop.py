from dataclasses import dataclass
from typing import Optional


@dataclass
class Stop:
    id: Optional[str] = None
    name: Optional[str] = None
    number: Optional[str] = None
    category: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
