#!/usr/bin/env python3
"""
Fetches the content of a webpage and
stores it in a cache for 10 seconds
"""
import requests
import redis
from functools import wraps
from typing import Callable


client = redis.Redis()


def cache(method: Callable) -> Callable:
    """
    Decorator that caches the response of a function
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function that checks if the url is in the cache
        """
        key = f"cache:{url}"
        result = client.get(key)
        if result is None:
            response = method(url)
            client.setex(key, 10, response)
            return response
        return result
    return wrapper


def count(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a url is called
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper function that counts the number of times a url is called
        """
        key = f"count:{url}"
        client.incr(key)
        return method(url)
    return wrapper


def get_page(url: str) -> str:
    """
    Fetches the content of a webpage and
    stores it in a cache for 10 seconds
    """
    response = requests.get(url)
    return response.text
