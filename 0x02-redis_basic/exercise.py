#!/usr/bin/env python3
"""
This script is used to generate a list
of all the files in a directory
"""
import redis
import uuid
from typing import Union


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
    
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        This method is used to store data in the cache
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
