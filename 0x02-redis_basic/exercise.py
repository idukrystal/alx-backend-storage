#!/usr/bin/env python3
''' A module to experiment with py-redis '''

import uuid
import redis
from typing import Union


class Cache:
    '''
    Represents a cahe object implemented as a
    redis database
    '''
    def __init__(self):
        ''' initializes a new cache object '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data:  Union[str, bytes, int, float]) -> str:
        ''' Store new data in cache object '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
