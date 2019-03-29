import functools


def cache(key):
    def decorator(func):
        _cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = key(args)

            if cache_key in _cache:
                return _cache[cache_key]

            result = func(*args, **kwargs)
            _cache[cache_key] = result
            return result

        return wrapper

    return decorator


@cache(key=lambda args: args[0])
def fitting_pixel(pixel, weights):
    w = float(pixel) / 255
    wf = -1.0
    k = -1
    for i in range(len(weights)):
        if abs(weights[i] - w) <= abs(wf - w):
            wf = weights[i]
            k = i
    return chr(k + 32)
