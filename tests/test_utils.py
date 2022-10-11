from datetime import time

import pytest

from ttss.utils import parse_time, timestamp_ms


def test_parse_time():
    assert parse_time('12:34') == time(12, 34)


@pytest.mark.freeze_time('2021-06-28 21:33:19')
def test_timestamp_ms():
    assert timestamp_ms() == 1624915999000
