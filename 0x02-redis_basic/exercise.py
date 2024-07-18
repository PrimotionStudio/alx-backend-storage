#!/usr/bin/env python3
"""
This script is used to generate a list
of all the files in a directory
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def replay(method: Callable) -> None:
    """
    This function is used to replay the function
    """
    client = method.__self__._redis
    meth = method.__qualname__

    input_key = f"{meth}:inputs"
    output_key = f"{meth}:outputs"
    inputs = client.lrange(input_key, 0, -1)
    outputs = client.lrange(output_key, 0, -1)
    print(f"{meth} was called {len(inputs)} times:")
    for _in, _out in zip(inputs, outputs):
        print(f"{meth}(*{_in.decode("utf-8")}) -> {_out.decode("utf-8")}")

def call_history(method: Callable) -> Callable:
    """
    This function is used to log the history of the function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        This function is used to log the history of the function
        """
        result = method(self, *args, **kwargs)
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        self._redis.rpush(output_key, str(result))
        return result

    return wrapper

def count_calls(method: Callable) -> Callable:
    """
    This function is used to count the number of calls to a function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        This function is used to count the number of calls to a function
        """
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
    @call_history
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
