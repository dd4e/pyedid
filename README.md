[![Build Status](https://travis-ci.com/dd4e/pyedid.svg?branch=master)](https://travis-ci.com/dd4e/pyedid)
[![codecov](https://codecov.io/gh/dd4e/pyedid/branch/master/graph/badge.svg?token=pM61OV0pzx)](https://codecov.io/gh/dd4e/pyedid)
[![PyPI version](https://badge.fury.io/py/pyedid.svg)](https://badge.fury.io/py/pyedid)

# pyEDID

This is a python library to parse extended display identification data (EDID)

## EDID data format

The EDID data frame format is described in detail on its [Wikipedia page](https://en.wikipedia.org/wiki/Extended_Display_Identification_Data).

# Getting started

## Requirements

* Python 3.6+

## Setup

From pypi

```bash
>>> pip install pyedid
```

or from github

```bash
>>> git clone https://github.com/dadmoscow/pyedid
>>> python pyedid/setup.py install
```

## Features

* Receive and decrypt EDID data
* Online converting manufacturer id, dumping registry to local csv
* Works as a shell utility
* Without third-party dependencies

## Usage

### As a library

```python
from pyedid.edid import Edid
from pyedid.helpers.edid_helper import EdidHelper
from pyedid.helpers.registry import Registry

#### Step 1: loading registry
# load pnp registry from http://www.uefi.org/pnp_id_list
registry = Registry.from_web()

# or loading from local csv file
registry = Registry.from_csv('/tmp/foo.csv')

# load from web and dump to csv
registry = Registry.from_web().to_csv('/tmp/bar.csv')

# only update
Registry.from_web().to_csv('/tmp/bar.csv')

#### Step 2: loading edid data

# loading list with edid data
edid_bs = EdidHelper.get_edids()[0]

# convert exist edid hex string from xrandr
edid_bs = EdidHelper.hex2bytes("hex string from xrandr...")

#### Step 3: create instance

# create Edid instance for fisrt edid data
edid = Edid(edid_bs, registry)
print(edid)

# Edid(
# 	dpms_activeoff=True,
# 	dpms_standby=True,
# 	dpms_suspend=True,
# 	edid_version=1.3,
# 	gamma=2.2,
# 	height=30.0,
# 	manufacturer=Ancor Communications Inc,
# 	manufacturer_id=1129,
# 	name=VS248,
# 	product=38948,
# 	raw=b'\x00\xff\xff\xff\xff\xff\xff\x00\x04i\x98$\x01\x01\x01\x01\x1e\x1b\x01\x03\x1e5\x1ex\xea\x92e\xa6UU\x9f(\rPT\xbf\xef\x00qO\x81\x80\x81@\x95\x00\xa9@\xb3\x00\xd1\xc0\x01\x01\x02:\x80\x18q8-@X,E\x00\x13+!\x00\x00\x1e\x00\x00\x00\xfd\x002L\x1eS\x11\x00\n      \x00\x00\x00\xfc\x00VS248\n       \x00\x00\x00\xff\x00H7LMQS122161\n\x00\x00',
# 	resolutions=[(720, 400, 70.0), (720, 400, 88.0), (640, 480, 60.0), (640, 480, 67.0), (640, 480, 72.0), (640, 480, 75.0), (800, 600, 56.0), (800, 600, 60.0), (800, 600, 70.0), (800, 600, 75.0), (832, 624, 75.0), (1024, 768, 87.0), (1024, 768, 60.0), (1024, 768, 72.0), (1024, 768, 75.0), (1152, 864, 75.0), (1280, 1024, 60.0), (1280, 960, 60.0), (1440, 900, 60.0), (1600, 1200, 60.0), (1680, 1050, 60.0), (1920, 1080, 60.0)],
# 	serial=H7LMQS123181,
# 	type=digital,
# 	width=53.0,
# 	year=2017
# )
```

### As a system utility

```bash
>>> pyedid

# Loading registry from web...
# Done!

# Edid(
# 	dpms_activeoff=True,
# 	dpms_standby=True,
# 	dpms_suspend=True,
# 	edid_version=1.3,
# 	gamma=2.2,
# 	height=30.0,
# 	manufacturer=Ancor Communications Inc,
# 	manufacturer_id=1129,
# 	name=VS248,
# 	product=38948,
# 	raw=b'\x00\xff\xff\xff\xff\xff\xff\x00\x04i\x98$\x01\x01\x01\x01\x1e\x1b\x01\x03\x1e5\x1ex\xea\x92e\xa6UU\x9f(\rPT\xbf\xef\x00qO\x81\x80\x81@\x95\x00\xa9@\xb3\x00\xd1\xc0\x01\x01\x02:\x80\x18q8-@X,E\x00\x13+!\x00\x00\x1e\x00\x00\x00\xfd\x002L\x1eS\x11\x00\n      \x00\x00\x00\xfc\x00VS248\n       \x00\x00\x00\xff\x00H7LMQS122161\n\x00\x00',
# 	resolutions=[(720, 400, 70.0), (720, 400, 88.0), (640, 480, 60.0), (640, 480, 67.0), (640, 480, 72.0), (640, 480, 75.0), (800, 600, 56.0), (800, 600, 60.0), (800, 600, 70.0), (800, 600, 75.0), (832, 624, 75.0), (1024, 768, 87.0), (1024, 768, 60.0), (1024, 768, 72.0), (1024, 768, 75.0), (1152, 864, 75.0), (1280, 1024, 60.0), (1280, 960, 60.0), (1440, 900, 60.0), (1600, 1200, 60.0), (1680, 1050, 60.0), (1920, 1080, 60.0)],
# 	serial=H7LMQS123181,
# 	type=digital,
# 	width=53.0,
# 	year=2017
# )
```

## Licensing

See LICENSE
