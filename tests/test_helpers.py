'''Edid helpers test module'''

from pyedid import get_edid_from_xrandr_verbose

from .data import PART_OF_XRANDR_VERBOSE_OUTPUT


def test_edid_from_xrandr_verbose_bytes():
    edids = get_edid_from_xrandr_verbose(PART_OF_XRANDR_VERBOSE_OUTPUT)

    assert isinstance(edids, list)
    assert len(edids) == 2
    for edid in edids:
        assert isinstance(edid, bytes)
        # edid header
        assert edid[:8] == b'\x00\xff\xff\xff\xff\xff\xff\x00'

def test_edid_from_xrandr_verbose_str():
    edids = get_edid_from_xrandr_verbose(PART_OF_XRANDR_VERBOSE_OUTPUT.decode())

    assert isinstance(edids, list)
    assert len(edids) == 2
    for edid in edids:
        assert isinstance(edid, bytes)
        # edid header
        assert edid[:8] == b'\x00\xff\xff\xff\xff\xff\xff\x00'

def test_edid_from_xrandr_verbose_bad_input():
    empty = get_edid_from_xrandr_verbose("foo\nbar\nsome not edid data")

    assert isinstance(empty, list)
    assert len(empty) == 0
