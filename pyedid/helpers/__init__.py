'''Edid helpers'''

from typing import List, Union


def get_edid_from_xrandr_verbose(verbose_output: Union[bytes, str]) -> List[bytes]:
    '''Parse raw Edid value from `xrandr --verbose` command output

    :param verbose_output: `xrandr --verbose` command output
    '''
    if isinstance(verbose_output, bytes):
        verbose_output = verbose_output.decode()

    edid = []
    lines = verbose_output.splitlines()
    for i, line in enumerate(lines):
        if line.strip().startswith('EDID:'):
            selection = [s.strip() for s in lines[i+1:i+9]]
            bytes_section = bytes.fromhex(''.join(selection))
            edid.append(bytes_section)
    return edid
