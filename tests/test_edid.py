"""
Test edid instance
"""
from pyedid.edid import Edid
from pyedid.helpers.registry import Registry
from . import data

class TestEdid:

    def setup(self):
        self.registry = Registry.from_web()

    def test_create_instance(self):
        """Test create Edid instance"""
        edid = Edid(edid=data.BASE_BYTE_EDID, registry=self.registry)
        assert edid.manufacturer == data.COMPANY_NAME
        assert edid.year == 2017
