from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Route:
    id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[str] = None
    authority: Optional[str] = None
    directions: Optional[List[str]] = None
    alerts: Optional[List[str]] = None
