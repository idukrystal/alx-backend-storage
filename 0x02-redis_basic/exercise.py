#!/usr/bin/env python3
''' A module to experiment with py-redis '''

import uuid
import redis
from functools import wraps
from typing import Callable, Union


def replay(method: Callable):
    ''' relives method calls: prints imput/output vslues '''
    input_key = method.__qualname__ + ":inputs"
    output_key = method.__qualname__ + ":outputs"

    r = redis.Redis()
    input_history = r.lrange(input_key, 0, -1)
    output_history = r.lrange(output_key, 0, -1)

    print(f"{method.__qualname__} was called {len(input_history)} times:")

    for input_args_str, output_str in zip(input_history, output_history):
        output = output_str.decode("utf-8")
        print(
            f"{method.__qualname__}"
            + f"(*{input_args_str.decode('utf-8')}) -> {output}"
        )


def count_calls(method: Callable) -> Callable:
    ''' A decorator that keep track of fuction's call  '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    ''' A decorator that keeps track of functions input/outputs '''
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        input_args_str = str(args)
        self._redis.rpush(input_key, input_args_str)

        output = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(output))

        return output
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
    @call_history
    def store(self, data:  Union[str, bytes, int, float]) -> str:
        ''' Store new data in cache object '''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[
            str, bytes, int, float, None]:
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
