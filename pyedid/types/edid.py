'''Edid data types'''

import json

from collections import namedtuple
from typing import List, NamedTuple, Optional, Tuple, Union


class Edid(NamedTuple):
    '''Parsed EDID object'''
    manufacturer_id: int
    manufacturer: str
    product_id: int
    year: int
    edid_version: str
    type: str
    width: float
    height: float
    gamma: float
    dpms_standby: bool
    dpms_suspend: bool
    dpms_activeoff: bool
    resolutions: List[Tuple[int, int, float]]
    name: Optional[str]
    serial: Union[str, int]

    def __repr__(self) -> str:
        return f"Edid({self.manufacturer} {self.name}, s/n {self.serial})"

    def __str__(self) -> str:
        return json.dumps(self._asdict())

_RAW_EDID = namedtuple(
    '_RAW_EDID',
    (
        'header',
        'manu_id',
        'prod_id',
        'serial_no',
        'manu_week',
        'manu_year',
        'edid_version',
        'edid_revision',
        'input_type',
        'width',
        'height',
        'gamma',
        'features',
        'color',
        'timings_supported',
        'timings_reserved',
        'timings_edid',
        'timing_1',
        'timing_2',
        'timing_3',
        'timing_4',
        'extension',
        'checksum'
    )
)


_EDID_STRUCT_FORMAT = (
    '>'     # big-endian
    '8s'    # constant header (8 bytes)
    'H'     # manufacturer id (2 bytes)
    'H'     # product id (2 bytes)
    'I'     # serial number (4 bytes)
    'B'     # manufactoring week (1 byte)
    'B'     # manufactoring year (1 byte)
    'B'     # edid version (1 byte)
    'B'     # edid revision (1 byte)
    'B'     # video input type (1 byte)
    'B'     # horizontal size in cm (1 byte)
    'B'     # vertical size in cm (1 byte)
    'B'     # display gamma (1 byte)
    'B'     # supported features (1 byte)
    '10s'   # color characteristics (10 bytes)
    'H'     # supported timings (2 bytes)
    'B'     # reserved timing (1 byte)
    '16s'   # EDID supported timings (16 bytes)
    '18s'   # detailed timing block 1 (18 bytes)
    '18s'   # detailed timing block 2 (18 bytes)
    '18s'   # detailed timing block 3 (18 bytes)
    '18s'   # detailed timing block 4 (18 bytes)
    'B'     # extension flag (1 byte)
    'B'     # checksum (1 byte)
)

_TIMINGS = {
    0: (1280, 1024, 75.),
    1: (1024,  768, 75.),
    2: (1024,  768, 72.),
    3: (1024,  768, 60.),
    4: (1024,  768, 87.),
    5: ( 832,  624, 75.),
    6: ( 800,  600, 75.),
    7: ( 800,  600, 70.),
    8: ( 800,  600, 60.),
    9: ( 800,  600, 56.),
    10:( 640,  480, 75.),
    11:( 640,  480, 72.),
    12:( 640,  480, 67.),
    13:( 640,  480, 60.),
    14:( 720,  400, 88.),
    15:( 720,  400, 70.),
}

_ASPECT_RATIOS = {
    0b00: (16, 10),
    0b01: ( 4,  3),
    0b10: ( 5,  4),
    0b11: (16,  9),
}
