#!/usr/bin/env python3
"""
This script is used to generate a list
of all the files in a directory
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    """
    This class is used to manage the cache
    """
    def __init__(self):
        """
        This method is used to initialize the cache
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        This method is used to store data in the cache
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """
        This method is used to get data from the cache
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_int(self, key: str) -> int:
        """
        This method is used to get an integer from the cache
        """
        return self.get(key, int)

    def get_str(self, key: str) -> str:
        """
        This method is used to get a string from the cache
        """
        return self.get(key, lambda d: d.decode('utf-8'))
