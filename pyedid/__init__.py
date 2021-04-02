'''PyEDID module'''

import struct
from typing import Optional, Union

from .types import Edid, Registry, DEFAULT_REGISTRY
from .types.edid import _RAW_EDID, _EDID_STRUCT_FORMAT, _ASPECT_RATIOS, _TIMINGS
from .helpers import get_edid_from_xrandr_verbose

__all__ = (
    'Edid',
    'Registry',
    'DEFAULT_REGISTRY',
    'get_edid_from_xrandr_verbose',
    'parse_edid'
)

__version__ = '1.0'


def parse_edid(raw: Union[bytes, str], registry: Registry = DEFAULT_REGISTRY) -> Edid:
    '''Parse raw EDID and return parsed object

    :param raw: Raw edid value
    :param registry: Edid registry, default uses the DEFAULT_REGISTRY

    :raises ValueError: bad Edid format
    :raises TypeError: bad inputs
    '''
    if not isinstance(raw, bytes):
        if isinstance(raw, str):
            raw = bytes.fromhex(raw)
        else:
            raise TypeError('Bad EDID type')

    if not isinstance(registry, Registry):
        raise TypeError('Bad registry type')

    # crop additional edid
    if len(raw) > 128:
        raw = raw[:128]

    if sum(raw) % 256 != 0:
        raise ValueError('Checksum mismatch')

    if raw[:8] != b'\x00\xff\xff\xff\xff\xff\xff\x00':
        raise ValueError('Invalid EDID header')

    unpacked = struct.unpack(_EDID_STRUCT_FORMAT, raw)
    raw_edid = _RAW_EDID(*unpacked)

    resolutions = []
    for i in range(16):
        bit = raw_edid.timings_supported & i
        if bit:
            resolutions.append(_TIMINGS[16-i])

    for i in range(8):
        bytes_data = raw_edid.timings_edid[2*i:2*i+2]
        if bytes_data == b'\x01\x01':
            continue
        byte1, byte2 = bytes_data
        x_res = 8*(int(byte1)+31)
        aspect_ratio = _ASPECT_RATIOS[(byte2>>6) & 0b11]
        y_res = int(x_res * aspect_ratio[1]/aspect_ratio[0])
        rate = (int(byte2) & 0b00111111) + 60.0
        resolutions.append((x_res, y_res, rate))

    name: Optional[str] = None
    serial: Optional[str] = None

    for timing_bytes in (raw_edid.timing_1, raw_edid.timing_2, raw_edid.timing_3, raw_edid.timing_4):
        # 'other' descriptor
        if timing_bytes[0:2] == b'\x00\x00':
            timing_type = timing_bytes[3]
            if timing_type in (0xFF, 0xFE, 0xFC):
                buffer = timing_bytes[5:]
                buffer = buffer.partition(b'\x0a')[0]
                text = buffer.decode('cp437')
                if timing_type == 0xFF:
                    serial = text
                elif timing_type == 0xFC:
                    name = text

    return Edid(
        manufacturer_id = raw_edid.manu_id,
        manufacturer = registry.get_company_by_raw(raw_edid.manu_id),
        product_id = raw_edid.prod_id,
        year = raw_edid.manu_year + 1990,
        edid_version = '{:d}.{:d}'.format(raw_edid.edid_version, raw_edid.edid_revision),
        type = 'digital' if (raw_edid.input_type & 0xFF) else 'analog',
        width = float(raw_edid.width),
        height = float(raw_edid.height),
        gamma = (raw_edid.gamma + 100) / 100,
        dpms_standby = bool(raw_edid.features & 0xFF),
        dpms_suspend = bool(raw_edid.features & 0x7F),
        dpms_activeoff = bool(raw_edid.features & 0x3F),
        resolutions = resolutions,
        name = name,
        serial = serial if serial else raw_edid.serial_no
    )
