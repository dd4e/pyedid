import struct
import subprocess
from collections import namedtuple

import pnpid
import util

def get_edids():
    output = subprocess.check_output(["xrandr", "--verbose"])
    edids = []
    lines = output.splitlines()
    for i, line in enumerate(lines):
        line = line.decode().strip()
        if line.startswith("EDID:"):
            selection = lines[i+1:i+9]
            selection = list(s.decode().strip() for s in selection)
            selection = "".join(selection)
            bytes = util.hex2bytes(selection)
            edids.append(bytes)
    return edids

class Edid:
    _STRUCT_FORMAT = (  ">"     # big-endian
                        "8s"    # constant header (8 bytes)
                        "H"     # manufacturer id (2 bytes)
                        "H"     # product id (2 bytes)
                        "I"     # serial number (4 bytes)
                        "B"     # manufactoring week (1 byte)
                        "B"     # manufactoring year (1 byte)
                        "B"     # edid version (1 byte)
                        "B"     # edid revision (1 byte)
                        "B"     # video input type (1 byte)
                        "B"     # horizontal size in cm (1 byte)
                        "B"     # vertical size in cm (1 byte)
                        "B"     # display gamma (1 byte)
                        "B"     # supported features (1 byte)
                        "10s"   # color characteristics (10 bytes)
                        "H"     # supported timings (2 bytes)
                        "B"     # reserved timing (1 byte)
                        "16s"   # EDID supported timings (16 bytes)
                        "18s"   # detailed timing block 1 (18 bytes)
                        "18s"   # detailed timing block 2 (18 bytes)
                        "18s"   # detailed timing block 3 (18 bytes)
                        "18s"   # detailed timing block 4 (18 bytes)
                        "B"     # extension flag (1 byte)
                        "B" )   # checksum (1 byte)

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

    _RawEdid = namedtuple("RawEdid", ("header", "manu_id", "prod_id", "serial_no", "manu_week", "manu_year", "edid_version", "edid_revision", "input_type", "width", "height", "gamma", "features", "color", "timings_supported", "timings_reserved", "timings_edid", "timing_1", "timing_2", "timing_3", "timing_4", "extension", "checksum"))

    def __init__(self, bytes=None):
        if bytes is not None:
            self._parse_edid(bytes)

    def _parse_edid(self, bytes):
        if struct.calcsize(self._STRUCT_FORMAT) != 128:
            raise ValueError("Wrong edid size.")

        if sum(map(int, bytes)) % 256 != 0:
            raise ValueError("Checksum mismatch.")

        tuple = struct.unpack(self._STRUCT_FORMAT, bytes)
        raw_edid = self._RawEdid(*tuple)

        if raw_edid.header != b'\x00\xff\xff\xff\xff\xff\xff\x00':
            raise ValueError("Invalid header.")

        self.raw = bytes
        self.manufacturer = pnpid.manufacturer_from_raw(raw_edid.manu_id)
        self.product = raw_edid.prod_id
        self.year = raw_edid.manu_year + 1990
        self.edid_version = "%d.%d" % (raw_edid.edid_version, raw_edid.edid_revision)
        self.type = "digital" if (raw_edid.input_type & 0xFF) else "analog"
        self.width = float(raw_edid.width)
        self.height = float(raw_edid.height)
        self.gamma = (raw_edid.gamma+100)/100
        self.dpms_standby = bool( raw_edid.features & 0xFF )
        self.dpms_suspend = bool( raw_edid.features & 0x7F )
        self.dpms_activeoff = bool( raw_edid.features & 0x3F )

        self.resolutions = []
        for i in range(16):
            bit = raw_edid.timings_supported & i
            if bit:
                self.resolutions.append(self._TIMINGS[16-i])

        for i in range(8):
            bytes = raw_edid.timings_edid[2*i:2*i+2]
            if bytes == b'\x01\x01':
                continue
            byte1, byte2 = bytes
            x_res = 8*(int(byte1)+31)
            aspect_ratio = self._ASPECT_RATIOS[ (byte2>>6) & 0b11 ]
            y_res = int(x_res * aspect_ratio[1]/aspect_ratio[0])
            rate = (int(byte2) & 0b00111111) + 60.0
            self.resolutions.append((x_res, y_res, rate))

        self.name = None
        self.serial = None

        for bytes in (raw_edid.timing_1, raw_edid.timing_2, raw_edid.timing_3, raw_edid.timing_4):
            if bytes[0:2] == b'\x00\x00': # "other" descriptor
                type = bytes[3]
                if type in (0xFF, 0xFE, 0xFC):
                    buffer = bytes[5:]
                    buffer = buffer.partition(b"\x0a")[0]
                    text = buffer.decode("cp437")
                    if type == 0xFF:
                        self.serial = text
                    elif type == 0xFC:
                        self.name = text

        if not self.serial:
            self.serial = raw_edid.serial_no

    def __repr__(self):
        clsname = self.__class__.__name__
        attributes = []
        for name in dir(self):
            if not name.startswith("_"):
                value = getattr(self, name)
                attributes.append("\t%s=%r" % (name, value))
        return "%s(\n%s\n)" % (clsname, ", \n".join(attributes))

if __name__=="__main__":
    for raw in get_edids():
        edid = Edid(raw)
        print(edid)

