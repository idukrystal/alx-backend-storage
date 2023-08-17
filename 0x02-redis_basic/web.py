#!/usr/bin/env python3
''' A mkdule '''

import requests
import redis
from functools import wraps


def cache_and_track(func):
    ''' track hiw manyvtimes a url is accesed withen a function '''
    redis_instance = redis.Redis()

    @wraps(func)
    def wrapper(url):
        if url is None:
            return "Invalid URL"

        count_key = f"count:{url}"
        cache_key = f"cache:{url}"

        redis_instance.incr(count_key)
        redis_instance.expire(count_key, 10)

        cached_content = redis_instance.get(cache_key)
        if cached_content:
            return cached_content.decode('utf-8')

        content = func(url)
        redis_instance.setex(cache_key, 10, content)
        return content
    return wrapper


@cache_and_track
def get_page(url: str) -> str:
    ''' Returns the contents of a u.r.l '''
    response = requests.get(url)
    return response.text
