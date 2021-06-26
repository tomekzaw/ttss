from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Path:
    color: str
    waypoints: List[Tuple[float, float]]
