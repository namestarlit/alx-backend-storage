#!/usr/bin/env python3
"""
Task: Advance Task
"""
import redis
import requests
from functools import wraps
from typing import Callable


# Redis instance for storing data
redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """
    Decorator function that caches the result of a method
    with a given URL and tracks access count.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """

    @wraps(method)
    def invoker(url: str) -> str:
        """
        Invokes the given method, tracks access count
        and caches the result with expiration.

        Args:
            url (str): The URL for which data is accessed.

        Returns:
            str: The result obtained from the method.
        """
        # Reset access count to 0
        redis_store.set(f"count:{url}", 0)

        # Increment the access count for the URL
        redis_store.incr(f"count:{url}")

        # Check if result is already cached
        result = redis_store.get(f"result:{url}")
        if result:
            return result.decode("utf-8")

        # Fetch result from the method
        result = method(url)

        # Cache the result with expiration time
        redis_store.setex(f"result:{url}", 10, result)

        return result

    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    Retrieves the HTML content of a given URL using the requests module.

    Args:
        url (str): The URL to fetch the HTML content from.

    Returns:
        str: The HTML content of the specified URL.
    """
    return requests.get(url).text
