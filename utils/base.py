# -*- coding: UTF-8 -*-

import pickle
import functools

from app import redis_cache

cache = redis_cache["DEFAULT"]


def get_func_cache_key(func, args, kw):
    # print("get_func_cache_key", args, kw)
    args_str = ",".join([str(arg) for arg in sorted(args)])
    kw_str = "&".join(["%s=%s" % (key, kw[key]) for key in sorted(kw)])
    func_pos = "%s.%s" % (func.__module__, func.__name__)

    cache_key = "%s:(%s):{%s}" % (func_pos, args_str, kw_str)
    # print("func_cache_key", args, kw, cache_key)
    return cache_key


def cached(cache_time):
    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kw):
            add_cache = False
            cache_key = get_func_cache_key(func, args, kw)

            if not cache.exists(cache_key):
                result = func(*args, **kw)
                add_cache = True
                # print("get from func...")

            else:
                cache_dat = cache.get(cache_key)
                result = pickle.loads(cache_dat)
                # print("get from cache...")

            if add_cache:
                dumped_str = pickle.dumps(result)
                cache.set(cache_key, dumped_str)
                cache.expire(cache_key, cache_time)

            return result
        return inner
    return decorator
