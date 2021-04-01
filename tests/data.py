'''Test data'''

HTML_TABLE = '''
<tbody>
    <tr  class="odd views-row-first">
        <td  class="views-field views-field-title active">
            2-Tel B.V          </td>
        <td  class="views-field views-field-field-pnp-id">
            TTL          </td>
        <td  class="views-field views-field-field-pnp-approved-on-date views-align-right">
            <span class="date-display-single">03/20/1999</span>          </td>
    </tr>
    <tr  class="even">
        <td  class="views-field views-field-title active">
            21ST CENTURY ENTERTAINMENT          </td>
        <td  class="views-field views-field-field-pnp-id">
            BUT          </td>
        <td  class="views-field views-field-field-pnp-approved-on-date views-align-right">
            <span class="date-display-single">04/25/2002</span>          </td>
    </tr>
    <tr  class="odd">
        <td  class="views-field views-field-title active">
            3Com Corporation          </td>
        <td  class="views-field views-field-field-pnp-id">
            TCM          </td>
        <td  class="views-field views-field-field-pnp-approved-on-date views-align-right">
            <span class="date-display-single">11/29/1996</span>          </td>
    </tr>
    <tr  class="even">
        <td  class="views-field views-field-title active">
            3D Perception          </td>
        <td  class="views-field views-field-field-pnp-id">
            TDP          </td>
        <td  class="views-field views-field-field-pnp-approved-on-date views-align-right">
            <span class="date-display-single">05/16/2002</span>          </td>
    </tr>
    <tr  class="odd">
        <td  class="views-field views-field-title active">
            3M          </td>
        <td  class="views-field views-field-field-pnp-id">
            VSD          </td>
        <td  class="views-field views-field-field-pnp-approved-on-date views-align-right">
            <span class="date-display-single">10/16/1998</span>          </td>
    </tr>
    <tr  class="even">
        <td  class="views-field views-field-title active">
            3NOD Digital Technology Co. Ltd.          </td>
        <td  class="views-field views-field-field-pnp-id">
            NOD          </td>
        <td  class="views-field views-field-field-pnp-approved-on-date views-align-right">
            <span class="date-display-single">12/11/2014</span>          </td>
    </tr>
    <tr  class="odd">
        <td  class="views-field views-field-title active">
            A D S Exports          </td>
        <td  class="views-field views-field-field-pnp-id">
            NGS          </td>
        <td  class="views-field views-field-field-pnp-approved-on-date views-align-right">
            <span class="date-display-single">07/16/1998</span>          </td>
    </tr>
</tbody>
'''

HTML_RESULT = {
    'TTL': ('2-Tel B.V', '03/20/1999'),
    'BUT': ('21ST CENTURY ENTERTAINMENT', '04/25/2002'),
    'TCM': ('3Com Corporation', '11/29/1996'),
    'TDP': ('3D Perception', '05/16/2002'),
    'VSD': ('3M', '10/16/1998'),
    'NOD': ('3NOD Digital Technology Co. Ltd.', '12/11/2014'),
    'NGS': ('A D S Exports', '07/16/1998')
}

PART_OF_XRANDR_VERBOSE_OUTPUT = (
    b'Screen 0: minimum 8 x 8, current 1920 x 1080, maximum 32767 x 32767\n'
    b'\n\n\n' # some skipped data
    b'\n\tEDID: \n\t\t00ffffffffffff00410cb1c068800000\n'
    b'\t\t0f1b010380301b782a92c5a259559e27\n'
    b'\t\t0e5054bd4b00d1c08180950f9500b300\n'
    b'\t\t81c001010101023a801871382d40582c\n'
    b'\t\t4500dd0c1100001e000000ff00554b30\n'
    b'\t\t31373135303332383732000000fc0050\n'
    b'\t\t68696c697073203232365634000000fd\n'
    b'\t\t00384c1e5311000a2020202020200058\n'
    b'\n\n\n' # some skipped data
    b'\tEDID: \n\t\t00ffffffffffff005a632c0501010101\n'
    b'\t\t171b010380301b782e84d5a25a52a226\n'
    b'\t\t0d5054bfef80b300a940950090408180\n'
    b'\t\t8140714f0101023a801871382d40582c\n'
    b'\t\t4500e00e1100001e000000ff00545835\n'
    b'\t\t3137323334303639310a000000fd0032\n'
    b'\t\t4c185313000a202020202020000000fc\n'
    b'\t\t005444323232302d320a202020200009\n'
    b'\n\n\n' # some skipped data
)

# from xrandr --verbose
BASE_HEX_EDID = (
    '00ffffffffffff000469982401010101'
    '1e1b01031e351e78ea9265a655559f28'
    '0d5054bfef00714f818081409500a940'
    'b300d1c00101023a801871382d40582c'
    '4500132b2100001e000000fd00324c1e'
    '5311000a202020202020000000fc0056'
    '533234380a20202020202020000000ff'
    '0048374c4d51533132323136310a0000'
)

EXTENTED_HEX_EDID = (
    '00ffffffffffff000469982401010101'
    '1e1b010380351e78ea9265a655559f28'
    '0d5054bfef00714f818081409500a940'
    'b300d1c00101023a801871382d40582c'
    '4500132b2100001e000000fd00324c1e'
    '5311000a202020202020000000fc0056'
    '533234380a20202020202020000000ff'
    '0048374c4d51533134373438350a018d'
    '02031ef14b900504030201111213141f'
    '230907078301000065030c0010001a36'
    '80a070381e4030203500132b2100001a'
    '662156aa51001e30468f3300132b2100'
    '001e011d007251d01e206e285500132b'
    '2100001e8c0ad08a20e02d10103e9600'
    '132b21000018011d8018711c1620582c'
    '2500132b2100009f0000000000000039'
)

PNP_DATA = (
    # raw_id, pnp_id, name
    (1129, 'ACI', 'Ancor Communications Inc'),
    (1138, 'ACR', 'Acer Technologies'),
    (1135, 'ACO', 'Allion Computer Inc.'),
    (1142, 'ACV', 'ActivCard S.A'),
    (1540, 'APD', 'AppliAdata')
)
