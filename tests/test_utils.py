from datetime import datetime, time

import pytest
from freezegun import freeze_time

from ttss.utils import parse_time, round_seconds, timestamp_ms


def test_parse_time() -> None:
    assert parse_time('12:34') == time(12, 34)


@freeze_time('2021-06-28 21:33:19')
def test_timestamp_ms() -> None:
    assert timestamp_ms() == '1624915999000'


@pytest.mark.parametrize('dt, expected', [
    (datetime(2022, 10, 11, 11, 59, 30), datetime(2022, 10, 11, 11, 59, 0)),
    (datetime(2022, 10, 11, 11, 59, 31), datetime(2022, 10, 11, 12, 0, 0)),
    (datetime(2022, 10, 11, 11, 59, 59), datetime(2022, 10, 11, 12, 0, 0)),
    (datetime(2022, 10, 11, 12, 0, 0), datetime(2022, 10, 11, 12, 0, 0)),
    (datetime(2022, 10, 11, 12, 0, 1), datetime(2022, 10, 11, 12, 0, 0)),
    (datetime(2022, 10, 11, 12, 0, 30), datetime(2022, 10, 11, 12, 0, 0)),
    (datetime(2022, 10, 11, 12, 0, 31), datetime(2022, 10, 11, 12, 1, 0)),
])
def test_round_seconds(dt: datetime, expected: datetime) -> None:
    assert round_seconds(dt) == expected
