import csv
import os, os.path
import string

DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILENAME = os.path.join(DIR, 'pnp_ids.csv')

PNP_IDS = {}
with open('pnp_ids.csv', 'r') as file:
    reader = csv.reader(file)
    for line in reader:
        PNP_IDS[ line[0] ] = line[1]

def manufacturer_from_raw(raw):
    id = id_from_raw(raw)
    return manufacturer_from_id(id)

def manufacturer_from_id(id):
    return PNP_IDS.get(id, "Unknown")

def id_from_raw(raw):
    tmp = [ (raw >> 10) & 31, (raw >> 5) & 31, raw & 31 ]
    return "".join( string.ascii_uppercase[n-1] for n in tmp )

