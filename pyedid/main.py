"""
Entrypoint
"""

from pyedid.edid import Edid
from pyedid.helpers.edid_helper import EdidHelper
from pyedid.helpers.registry import Registry


def main():
    """Main func"""
    print("Loading registry from web...")
    registry = Registry.from_web()
    print("Done!\n")

    for raw in  EdidHelper.get_edids():
        edid = Edid(raw, registry)
        print(edid)

if __name__ == "__main__":
    main()
