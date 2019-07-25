"""
Test registry module
"""

import tempfile

from pyedid.helpers.registry import Registry
from . import data


class TestRegistry:

    def setup(self):
        self.registry = Registry.from_web()

    def test_load_from_web(self):
        """Test loading registry from web"""
        assert len(self.registry) > 2000

    def test_dump_to_csv(self):
        """Test dump/load registry to csv"""
        with tempfile.NamedTemporaryFile() as temp_csv:
            self.registry.to_csv(temp_csv.name)
            assert self.registry == Registry.from_csv(temp_csv.name)

    def test_get_company(self):
        """Test converting pnp id to company"""
        assert self.registry.get_company_from_id(data.PNP_ID) == data.COMPANY_NAME
        assert self.registry.get_company_from_raw(data.COMPANY_RAW) == data.COMPANY_NAME
