#!/usr/bin/env python3
''' A module to experiment with py-redis '''

import uuid
import redis
from functools import wraps
from typing import Callable, Union


def count_calls(method: Callable) -> Callable:
    ''' A decorator that keep track of fuction csll times  '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    '''
    Represents a cahe object implemented as a
    redis database
    '''
    def __init__(self):
        ''' initializes a new cache object '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data:  Union[str, bytes, int, float]) -> str:
        ''' Store new data in cache object '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str, bytes, int, float, None]:
        ''' Retrive stored data from cache object '''
        data = self._redis.get(key)
        if not data or not fn:
            return data
        else:
            return fn(data)

    def get_str(self, key: str) -> Union[str, None]:
        ''' Retrives a string from the cache object '''
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        ''' Retrives an int from the cache object '''
        return self.get(key, fn=int)
