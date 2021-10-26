import itertools
import logging
from datetime import datetime
from typing import List, AnyStr, Optional, Union, Any

from django.core.cache import cache as default_cache


logger = logging.getLogger('visit.clients')


# Typings
# --------------------------------------------------------------------------------------------------
LINKS = List[AnyStr]


class Visit:

    cache = default_cache
    timeout = None

    cache_key_prefix = 'timestamp'
    cache_key_delimeter = '_'

    def __init__(self, key: Optional[Union[str, None]] = None):
        self.key = key or None

    def __flush(self):
        """
        Function that flushes visits in Redis
        """

        self.cache.delete_pattern(self._construct_cache_key('*'))

    def _load(self):
        """
        Function that set `key` attribute to instance
        """
        self.key = self.key or self._construct_cache_key()

    def _construct_cache_key(self, key: Union[str, None] = None) -> str:
        """
        Function that constructs cache key value.
        Algorithm:
        (1)     'timestamp'  +
        (2)     '_'          +
        (3)     '1234567890'
        ---------------------
        'timestamp_123456789'

        Where:
            1 - prefix ({self.cache_key_prefix})
            2 - delimeter ({self.cache_key_delimeter})
            3 - POSIX datetime ({datetime.now().timestamp()})

        :return: <str>
        """

        key = key or int(datetime.now().timestamp())
        return f'{self.cache_key_prefix}{self.cache_key_delimeter}{key or "*"}'

    @staticmethod
    def _parse_input_value(value: Any) -> Union[int, None]:
        """
        Function that parses input value and returns <int>.

        :param value: (<Any>) - input value

        :return: <int>|None
        """

        value = str(value)
        try:
            if '.' in value:
                value = float(value)
            else:
                assert value.isdigit()
        except (ValueError, AssertionError):
            return None
        else:
            return int(value)

    def _get_cache_key_wo_prefix(self, cache_key: str) -> str:
        """
        Function that returns cache key without prefix.

        :param cache_key: (<str>) - cache key, that has prefix

        I.e.:
            Input -> `timestamp_1234567890` -> `1234567890`

        :return: <str>
        """

        return next(iter(cache_key.split(self.cache_key_delimeter)[1:]))

    def _get_visit_cache_keys(self, start: int, end: int) -> Union[List[None], List[str]]:
        """
        Function that returns list of cache keys without {self.cache_key_prefix} and
        {self.cache_key_delimeter} by condition:
        - start <= timestamp <= end

        :param start: (<int>) - start date in POSIX format
        :param end: (<int>) - end date in POSIX format

        :return: <List[str, str, ...]>|<List[None]>
        """

        return [
            self._get_cache_key_wo_prefix(cache_key)
            for cache_key in self.cache.iter_keys(self._construct_cache_key('*'))
            if start <= int(self._get_cache_key_wo_prefix(cache_key)) <= end
        ]

    def register(self, links: LINKS):
        """
        Function that register visited resourse.
        For each visited resourse is assigned a date in format POSIX.

        :param links: (<List[AnyStr]>) - List that contains resources

        :return: <List[AnyStr]>
        """

        self._load()
        logger.info(f'VISIT. METHOD: "register')
        logger.info(f'VISIT. PARAMS: "key={self.key}')

        if cache := self.cache.get(self.key): links += cache  # NOQA
        self.cache.set(self.key, list(set(links)), self.timeout)

    def find(self, start: Union[int, float], end: Union[int, float]
             ) -> Union[List[str], List[None]]:
        """
        Function that returns list of visited resources.

        :param start: (<int>) - start date in POSIX format
        :param end: (<int>) - end date in POSIX format

        :return: <List[str, str, ...]>|<List[None]>
        """

        start, end = self._parse_input_value(start), self._parse_input_value(end)
        if not start or not end:
            logger.info(f'VISIT. METHOD: "find')
            logger.info(f'VISIT. INFO: "Parising `start`|`end` error"')
            logger.info(f'VISIT. PARAMS: start={start}')
            logger.info(f'VISIT. PARAMS: end={end}')
            return list()

        visit_cache_keys = self._get_visit_cache_keys(*sorted([start, end]))
        return list(
            itertools.chain.from_iterable(
                [self.cache.get(self._construct_cache_key(visit_cache_key))
                 for visit_cache_key in visit_cache_keys])
        )
