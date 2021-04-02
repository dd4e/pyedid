# pyEDID

[![Build Status](https://travis-ci.com/dd4e/pyedid.svg?branch=master)](https://travis-ci.com/dd4e/pyedid)
[![codecov](https://codecov.io/gh/dd4e/pyedid/branch/master/graph/badge.svg?token=pM61OV0pzx)](https://codecov.io/gh/dd4e/pyedid)
![PyPI](https://img.shields.io/pypi/v/pyedid)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyedid)
![PyPI - Status](https://img.shields.io/pypi/status/pyedid)
![PyPI - Downloads](https://img.shields.io/pypi/dm/pyedid)
![PyPI - License](https://img.shields.io/pypi/l/pyedid)

## Getting started

This is a python library to parse extended display identification data (EDID).

This project based on [pyedid](https://github.com/jojonas/pyedid)

## EDID data format

The EDID data frame format is described in detail on the [Wikipedia](https://en.wikipedia.org/wiki/Extended_Display_Identification_Data) page.

## Requirements

- Python 3.6+
- requests

## Setup

```bash
pip3 install pyedid
```

## Features

- Parsing EDID data from hex or bytes
- Embedded PNP ID registry with dump/restore to CSV file
- Updatable PNP ID registry from www.uefi.org

## Docs

> ToDO

## Quickstart

### Parsing some hex EDID data with the default registry

```python
import pyedid

edid_hex = (
    '00ffffffffffff000469982401010101'
    '1e1b01031e351e78ea9265a655559f28'
    '0d5054bfef00714f818081409500a940'
    'b300d1c00101023a801871382d40582c'
    '4500132b2100001e000000fd00324c1e'
    '5311000a202020202020000000fc0056'
    '533234380a20202020202020000000ff'
    '0048374c4d51533132323136310a0000'
)

# returned Edid object, used the Default embedded registry
edid = pyedid.parse_edid(edid_hex)

edid.name # 'VS248'
edid.manufacturer # 'Ancor Communications Inc'
edid.serial # 'H7LMQS122161'
edid.year # 2017
edid.width # 53.0
edid.height # 30.0
edid.resolutions # list with resulutions (x, y, rate), ex (720, 400, 70.0)
edid. # some other EDID data

json_str = str(edid) # making JSON string object
```

### Getting EDID from `xrandr --verbose`

```python
from pyedid import get_edid_from_xrandr_verbose
from subprocess import check_output

# getting `xrandr --verbose` output
randr = check_output(['xrandr', '--verbose'])

# parsing xrandr outputs to a bytes edid's list
edids = get_edid_from_xrandr_verbose(randr)

# parsing edid
edid = pyedid.parse_edid(edids[0])
```

### Working with registry

```python
from pyedid import Registry, DEFAULT_REGISTRY

# making a registry object from www.uefi.org
r_web = Registry.from_web()

# dumping the default registry to csv file
DEFAULT_REGISTRY.to_csv('/path/to/csv.file')

# restoring registry from csv file
r_csv = Registry.from_csv('/path/to/csv.file')
```

## Licensing

See LICENSE
