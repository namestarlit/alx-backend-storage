#!/usr/bin/env python3
"""A module that creates a Redis cache class"""
import sys
import redis
from uuid import uuid4
from functools import wraps
from typing import Union, Optional, Callable


def decode_utf8(b: bytes) -> str:
    """decodes binary data into string data"""
    return b.decode("utf-8") if type(b) == bytes else b


def replay(method: Callable):
    """displays the history of call of a particular function"""
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":ouputs"])

    count = method.__self__.get(key)
    i_list = method.__self__._redis.lrange(i, 0, -1)
    o_list = method.__self__._redis.lrange(o, 0, -1)

    queue = list(zip(i_list, o_list))
    print(f"{key} was called {decode_utf8(count)} times:")
    for k, v in queue:
        k = decode_utf8(k)
        v = decode_utf8(v)
        print(f"{key}(*{k}) -> {v}")


def call_history(method: Callable) -> Callable:
    """write a function call history"""
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":ouputs"])

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """A wrapper function"""
        self._redis.rpush(i, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(o, str(res))
        return res

    return wrapper


def count_calls(method: Callable) -> Callable:
    """keeps a count of call stats to the store function"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """function wrapper"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


class Cache:
    """implementantion of a Redis Cache class"""

    def __init__(self):
        """instantiates an instance of Cache class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(
        self, data: Union[str, bytes, int, float]
    ) -> Union[str, bytes, int, float]:
        """stores a random key-value pair into the redis db"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self, key: str, fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """retrives values from the redis db"""
        res = self._redis.get(key)
        return fn(res) if fn else res

    def get_str(self, data: bytes) -> str:
        """convert bytes data to string data"""
        return data.decode("utf-8")

    def get_int(self, data: bytes) -> int:
        """converts bytes data to integer data"""
        return int.from_bytes(data, sys.byteorder)
