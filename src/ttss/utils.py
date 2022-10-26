from datetime import datetime, time, timedelta
from time import time_ns


def parse_time(string: str) -> time:
    return datetime.strptime(string, '%H:%M').time()


def timestamp_ms() -> str:
    return str(time_ns() // 1_000_000)


def round_seconds(dt: datetime) -> datetime:
    return dt + timedelta(seconds=60 - dt.second) if dt.second > 30 else dt.replace(second=0)
