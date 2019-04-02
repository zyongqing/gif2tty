import functools


def cache(key):
    def decorator(func):
        _dict = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = key(args)

            if cache_key in _dict:
                return _dict[cache_key]

            result = func(*args, **kwargs)
            _dict[cache_key] = result
            return result

        return wrapper

    return decorator
