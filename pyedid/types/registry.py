'''PNP ID registry module'''

import csv
import string
from collections import UserDict
from html.parser import HTMLParser
from urllib.parse import urljoin
from typing import Optional

import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout


__all__ = ('Registry')


class _WebPnpIdParser(HTMLParser):
    '''Parser for HTML table with pnp id data'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._find_table = False
        self._find_row = False
        # first -- company name, second -- pnp id, third -- approved date
        self._last_field = []
        # key -- pnp id, value -- tuple (company_name, approved_date)
        self.result = {}

    def handle_starttag(self, tag, attrs):
        if tag == 'tbody':
            self._find_table = True
        elif self._find_table and tag == 'tr':
            self._find_row = True

    def handle_endtag(self, tag):
        if tag == 'tbody':
            self._find_table = False
        elif self._find_table and tag == 'tr':
            self._find_row = False
            # add table row to result
            self.result[self._last_field[1]] = (self._last_field[0], self._last_field[-1])
            self._last_field.clear()

    def handle_data(self, data):
        # skip processing until table was found
        if not self._find_table:
            return

        if self._find_row:
            data = data.strip()
            if data:
                self._last_field.append(data)

    def error(self, message):
        super().close()


class Registry(UserDict):
    '''Registry PNP ID data

    key is pnp_id
    value is company name
    '''
    __PNP_BASE_URL = 'https://uefi.org'
    __PNP_EXPORT = '/uefi-pnp-export'
    __PNP_FILTER = '/pnp_id_list?search='
    __DEFAULT_NAME = 'Unknown'

    def __repr__(self) -> str:
        return f'Registry({len(self)} items)'

    @classmethod
    def from_web(cls, filter_by_id: Optional[str] = None) -> 'Registry':
        '''Return the registry updated from uefi.org

        If uefi.org return not 200 code then will returned empty registry

        :param filter_by_id: filtering by ID, (optional)

        :raises TypeError: bad argument type
        :raises RuntimeError: internet connection troubles
        '''
        if filter_by_id:
            if not isinstance(filter_by_id, str):
                raise TypeError

            url = urljoin(cls.__PNP_BASE_URL, cls.__PNP_FILTER)
            url += filter_by_id
        else:
            url = urljoin(cls.__PNP_BASE_URL, cls.__PNP_EXPORT)

        registry = cls()
        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except HTTPError:
            return registry
        except (ConnectionError, Timeout) as err:
            raise RuntimeError from err

        parser = _WebPnpIdParser()
        parser.feed(resp.text)

        for key, value in parser.result.items():
            # skip invalid search value
            if filter_by_id and key != filter_by_id:
                continue
            registry[key] = value[0]
        return registry

    @classmethod
    def from_csv(cls, path: str, filter_by_id: str = None) -> 'Registry':
        '''Load the registry from a local file in CSV format

        :param path: path to file
        :param filter_by_id: filter registry by id (optional)

        :raises TypeError: bad argument type
        '''
        if not isinstance(path, str):
            raise TypeError
        if filter_by_id:
            if not isinstance(filter_by_id, str):
                raise TypeError

        registry = cls()
        with open(path, 'r') as f:
            reader = csv.reader(f)
            for line in reader:
                # filter
                if filter_by_id and filter_by_id != line[0]:
                    continue
                registry[line[0]] = line[1]
        return registry

    def to_csv(self, path: str) -> None:
        '''Dump the registry to CSV file

        :raises TypeError: bad argument type
        '''
        if not isinstance(path, str):
            raise TypeError

        with open(path, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(self.items())

    def get_company_by_pnp(self, pnp_id: str) -> str:
        '''Convert PNP id to company name or 'Unknown' if not found'''
        return self.get(pnp_id, self.__DEFAULT_NAME)

    def get_company_by_raw(self, raw_id: int) -> str:
        '''Convert raw edid value to company name or 'Unknown' if not found'''
        tmp = [(raw_id >> 10) & 31, (raw_id >> 5) & 31, raw_id & 31]
        try:
            pnp_id = ''.join(string.ascii_uppercase[n-1] for n in tmp)
            return self.get_company_by_pnp(pnp_id)
        except IndexError:
            return self.__DEFAULT_NAME
