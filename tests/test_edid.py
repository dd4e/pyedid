'''Parse Edid test module'''

import json
import pytest

from pyedid import parse_edid, Edid, Registry

from .data import BASE_HEX_EDID, EXTENTED_HEX_EDID


def test_parse_edid_base_hex():
    parsed = parse_edid(BASE_HEX_EDID)

    assert isinstance(parsed, Edid)
    assert parsed.name == 'VS248'
    assert parsed.serial == 'H7LMQS122161'
    assert parsed.manufacturer == 'Ancor Communications Inc'
    assert parsed.edid_version == '1.3'
    assert parsed.gamma == 2.2
    assert parsed.height == 30.0
    assert parsed.width == 53.0
    assert parsed.year == 2017
    assert parsed.week == 30
    assert len(parsed.resolutions) == 22
    assert parsed.dpms_activeoff
    assert parsed.dpms_standby
    assert parsed.dpms_suspend

def test_parse_edid_base_bytes():
    parsed = parse_edid(bytes.fromhex(BASE_HEX_EDID))

    assert isinstance(parsed, Edid)
    assert parsed.name == 'VS248'
    assert parsed.serial == 'H7LMQS122161'
    assert parsed.manufacturer == 'Ancor Communications Inc'
    assert parsed.edid_version == '1.3'
    assert parsed.gamma == 2.2
    assert parsed.height == 30.0
    assert parsed.width == 53.0
    assert parsed.year == 2017
    assert parsed.week == 30
    assert len(parsed.resolutions) == 22
    assert parsed.dpms_activeoff
    assert parsed.dpms_standby
    assert parsed.dpms_suspend

def test_parse_edid_extented_hex():
    parsed = parse_edid(EXTENTED_HEX_EDID)

    assert isinstance(parsed, Edid)
    assert parsed.name == 'VS248'
    assert parsed.serial == 'H7LMQS147485'
    assert parsed.manufacturer == 'Ancor Communications Inc'
    assert parsed.edid_version == '1.3'
    assert parsed.gamma == 2.2
    assert parsed.height == 30.0
    assert parsed.width == 53.0
    assert parsed.year == 2017
    assert parsed.week == 30
    assert len(parsed.resolutions) == 22
    assert parsed.dpms_activeoff
    assert parsed.dpms_standby
    assert parsed.dpms_suspend

def test_parse_edid_extented_bytes():
    parsed = parse_edid(bytes.fromhex(EXTENTED_HEX_EDID))

    assert isinstance(parsed, Edid)
    assert parsed.name == 'VS248'
    assert parsed.serial == 'H7LMQS147485'
    assert parsed.manufacturer == 'Ancor Communications Inc'
    assert parsed.edid_version == '1.3'
    assert parsed.gamma == 2.2
    assert parsed.height == 30.0
    assert parsed.width == 53.0
    assert parsed.year == 2017
    assert parsed.week == 30
    assert len(parsed.resolutions) == 22
    assert parsed.dpms_activeoff
    assert parsed.dpms_standby
    assert parsed.dpms_suspend

def test_parse_edid_custom_registry():
    parsed = parse_edid(BASE_HEX_EDID, registry=Registry())

    assert isinstance(parsed, Edid)
    assert parsed.manufacturer == 'Unknown'

def test_parse_edid_bad_types():
    with pytest.raises(TypeError) as err_edid_t:
        parse_edid(12345)

    with pytest.raises(TypeError) as err_registry_t:
        parse_edid(BASE_HEX_EDID, registry=123)

    assert str(err_edid_t.value) == 'Bad EDID type'
    assert str(err_registry_t.value) == 'Bad registry type'

def test_parse_edid_bad_values():
    with pytest.raises(ValueError) as err_checksum_t:
        parse_edid(b'\xff\xff\xff\xff\xff')

    with pytest.raises(ValueError) as err_header_t:
        # make incorrect edid
        bad_edid = list(bytes.fromhex(BASE_HEX_EDID))
        bad_edid[1] = 54
        bad_edid[2] = 200
        bad_edid = bytes(bad_edid)
        parse_edid(bad_edid)

    assert str(err_checksum_t.value) == 'Checksum mismatch'
    assert str(err_header_t.value) == 'Invalid EDID header'

def test_repr():
    parsed = parse_edid(BASE_HEX_EDID)
    assert repr(parsed) == f'Edid({parsed.manufacturer} {parsed.name}, s/n {parsed.serial})'

def test_str():
    parsed = parse_edid(BASE_HEX_EDID)
    json_obj = json.loads(str(parsed))

    for key, value in json_obj.items():
        if isinstance(value, list):
            value = [tuple(i) for i in value]
        assert getattr(parsed, key) == value
