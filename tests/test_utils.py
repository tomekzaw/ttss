from datetime import time

from ttss.utils import parse_time


def test_parse_time():
    assert parse_time('12:34') == time(12, 34)
