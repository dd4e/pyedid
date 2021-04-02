'''Registry test module'''

import os
import csv
import contextlib
import pytest
from unittest.mock import patch

from requests.exceptions import HTTPError, ConnectionError

from pyedid import Registry, DEFAULT_REGISTRY
from pyedid.types.registry import _WebPnpIdParser

from .data import PNP_DATA, HTML_TABLE, HTML_RESULT


def test_html_parser():
    parser = _WebPnpIdParser()
    parser.feed(HTML_TABLE)

    assert parser.result == HTML_RESULT

def test_from_web():
    # only if internet is available
    with contextlib.suppress(RuntimeError):
        r = Registry.from_web()

        assert isinstance(r, Registry)
        assert len(r) > 2000

def test_from_web_with_filter():
    _, pnp_id, name = PNP_DATA[0]

    # only if internet is available
    with contextlib.suppress(RuntimeError):
        r = Registry.from_web(filter_by_id=pnp_id)

        assert isinstance(r, Registry)
        assert len(r) == 1
        assert r.get_company_by_pnp(pnp_id) == name

def test_from_web_bad_args():
    with pytest.raises(TypeError):
        Registry.from_web(filter_by_id=123)

def test_from_web_bad_response():
    with patch('requests.get', side_effect=HTTPError()):
        r = Registry.from_web()

        assert isinstance(r, Registry)
        assert len(r) == 0

def test_from_web_connection_error():
    with patch('requests.get', side_effect=ConnectionError()):
        with pytest.raises(RuntimeError):
            Registry.from_web()

def test_to_csv(tmpdir):
    tmp_csv_path = os.path.join(tmpdir.dirname, 'test_export.csv')
    DEFAULT_REGISTRY.to_csv(tmp_csv_path)

    with open(tmp_csv_path, 'r') as f:
        dialect = csv.Sniffer().sniff(f.read(1024))
        f.seek(0)
        lines = f.readlines()

    assert dialect.delimiter == ','
    assert len(lines) == len(DEFAULT_REGISTRY)

def test_to_csv_bad_args():
    with pytest.raises(TypeError):
        DEFAULT_REGISTRY.to_csv(12345)

def test_from_csv(tmpdir):
    tmp_csv_path = os.path.join(tmpdir.dirname, 'test_import.csv')
    DEFAULT_REGISTRY.to_csv(tmp_csv_path)

    r = Registry.from_csv(tmp_csv_path)

    assert isinstance(r, Registry)
    assert r == DEFAULT_REGISTRY

def test_from_csv_with_filter(tmpdir):
    _, pnp_id, name = PNP_DATA[1]
    tmp_csv_path = os.path.join(tmpdir.dirname, 'test_import_with_f.csv')
    DEFAULT_REGISTRY.to_csv(tmp_csv_path)

    r = Registry.from_csv(tmp_csv_path, filter_by_id=pnp_id)

    assert isinstance(r, Registry)
    assert len(r) == 1
    assert r[pnp_id] == name

def test_from_csv_bad_args():
    with pytest.raises(TypeError):
        Registry.from_csv(12345)

    with pytest.raises(TypeError):
        Registry.from_csv('/foo/bar', filter_by_id=12345)

def test_get_company_by_pnp():
    for item in PNP_DATA:
        _, pnp_id, name = item
        assert DEFAULT_REGISTRY.get_company_by_pnp(pnp_id) == name

def test_get_comany_by_pnp_nf():
    # empty registry
    r = Registry()
    assert r.get_company_by_pnp('foo') == 'Unknown'

def test_get_company_by_raw():
    for item in PNP_DATA:
        raw_id, _, name = item
        assert DEFAULT_REGISTRY.get_company_by_raw(raw_id) == name

def test_get_company_by_raw_nf():
    assert DEFAULT_REGISTRY.get_company_by_raw(1134) == 'Unknown'

def test_get_company_by_raw_bad():
    assert DEFAULT_REGISTRY.get_company_by_raw(99999) == 'Unknown'

def test_repr():
    assert repr(DEFAULT_REGISTRY) == f'Registry({len(DEFAULT_REGISTRY)} items)'
