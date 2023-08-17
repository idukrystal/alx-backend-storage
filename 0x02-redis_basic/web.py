#!/usr/bin/env python3
''' A module thst does stuff '''

import requests
import redis
from functools import wraps
from typing import Callable


def track(fn: Callable) -> Callable:
    ''' tracks no of timesa function is called with a particular url '''
    r = redis.Redis()

    @wraps(fn)
    def wrapper(url: str) -> str:
        count_key = f"count:{url}"
        cache_key = f"cache:{url}"

        r.incr(count_key)

        cache = redis_instance.get(cache_key)
        if cache:
            return cache.decode('utf-8')

        r.set(count_key, 0)
        return fn(url)
    return wrapper


@track
def get_page(url: str) -> str:
    ''' return a urls content '''
    response = requests.get(url)

    return response.text
