"""
Test get_edid helper
"""
from pyedid.helpers.edid_helper import EdidHelper
from . import data

class TestEdidHelper:
    """Test EdidHelper class"""

    def test_hex_to_bytes(self):
        """Test converting edid hex to byte string"""
        assert EdidHelper.hex2bytes(data.BASE_HEX_EDID) == data.BASE_BYTE_EDID
        assert EdidHelper.hex2bytes(data.EXTENTED_HEX_EDID) == data.EXTENTED_BYTE_EDID
