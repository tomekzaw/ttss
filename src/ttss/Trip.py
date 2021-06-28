from dataclasses import dataclass
from typing import Optional

from ttss.Route import Route


@dataclass
class Trip:
    id: Optional[str] = None
    route: Optional[Route] = None
    direction: Optional[str] = None
