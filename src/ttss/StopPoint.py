from dataclasses import dataclass
from typing import Optional


@dataclass
class StopPoint:
    id: Optional[str] = None
    name: Optional[str] = None
    code: Optional[str] = None
    category: Optional[str] = None
    label: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
