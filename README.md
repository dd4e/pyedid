# pyEDID
This is a python library to parse extended display identification data (EDID)!

## EDID data format
The EDID data frame format is described in detail on its [Wikipedia page](https://en.wikipedia.org/wiki/Extended_Display_Identification_Data).

## Library
The library is still work in progress, the main features are implemented in `edid.py`.
The CSV file `pnp_ids.csv` and the corresponding module `pnpid.py` contains a pythonic way to read the plug-and-play ids which are maintained by Microsoft and obtained from [this page](http://www.uefi.org/pnp_id_list).
