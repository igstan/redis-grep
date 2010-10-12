"""Perform regex searches through Redis values"""
import sys
import re

from optparse import OptionParser
from redis import Redis

__version__ = "0.1.0"
__author__ = "Ionut G. Stan"


class RedisString(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return '<RedisString: %s=%s>' % (self.name, self.value)

    def grep(self, pattern):
        match = pattern.search(self.value)
        if match is not None:
            return [(self.name, self.value)]
        return []


class RedisList(object):
    def __init__(self, redis, key_name, range_size=100):
        self.name = key_name
        self._redis = redis
        self._range_size = range_size

    def __repr__(self):
        return '<RedisList: %s>' % (self.name)

    def grep(self, pattern):
        list_length = self._redis.llen(self.name)
        chunck = self._range_size

        while chunck <= list_length:
            list = self._redis.lrange(self.name, chunck - self._range_size, chunck)

            for (i, item) in enumerate(list):
                if pattern.search(item) is not None:
                    yield (self.name, chunck - self._range_size + i, item)

            chunck += self._range_size


class RedisGrepper(object):
    def __init__(self, redis, key_pattern='*'):
        self._redis = redis
        self._pattern = key_pattern

    def __iter__(self):
        for key in self._redis.keys(self._pattern):
            type = self._redis.type(key)

            if type == "string":
                yield RedisString(key, self._redis.get(key))
            elif type == "list":
                yield RedisList(self._redis, key)
            else:
                raise Exception('Unsupported key type "%s"' % type)


def search(pattern, key_pattern='*', host=None, port=None, db=None):
    redis = Redis(host=host, port=port, db=db)
    pattern = re.compile(pattern)

    for key in RedisGrepper(redis, key_pattern=key_pattern):
        for match in key.grep(pattern):
            yield match
