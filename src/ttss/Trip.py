from dataclasses import dataclass
from typing import Optional


@dataclass
class Trip:
    id: Optional[str] = None
    route_number: Optional[str] = None
    direction: Optional[str] = None
