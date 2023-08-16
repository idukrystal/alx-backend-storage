#!/usr/bin/env python3
''' A module thst does stuff '''

import requests
import redis
from functools import wraps
from typing import Callable


def track(fn: Callable) -> Callable:
    r = redis.Redis()

    @wraps(fn)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"

        r.incr(count_key)
        r.expire(count_key, 10)
        return fn(url)
    return wrapper


@track
def get_page(url: str) -> str:
    ''' return a urls content '''
    response = requests.get(url)
    content = response.text

    return content
