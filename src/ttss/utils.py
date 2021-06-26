from datetime import time, datetime
from time import time_ns


def parse_time(string: str) -> time:
    return datetime.strptime(string, '%H:%M').time()


def timestamp_ms() -> int:
    return time_ns() // 1_000_000
