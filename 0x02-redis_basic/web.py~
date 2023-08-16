#!/usr/bin/env python3
''' A module thst does stuff '''

import requests
import redis


def get_page(url: str) -> str:
    ''' return a urls content and tracks how many times it has been called'''
    r  = redis.Redis()

    count_key = f"count:{url}"
    cache_key = f"cache:{url}"

    r.incr(count_key)
    r.expire(count_key, 10)

    cached = r.get(cache_key)
    if cached:
        return cached.decode('utf-8')

    response = requests.get(url)
    content = response.text
    r.setex(cache_key, 10, content)
    
    return content
