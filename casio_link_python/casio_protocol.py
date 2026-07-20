from dataclasses import dataclass
from casio_transport import HEADER_SIZE
from casio_checksum import *

@dataclass
class Header:
    raw:bytes
    object_type:str
    category:str
    header_field:int
    payload_length:int
    identifier:str
    checksum:int
    terminates_transfer:bool

def payload_length(obj,f):
    if obj in ('TXT','FNC','MEM'):
        return f
    if obj=='VAL':
        if f==0:return 0
        if f==1:return 16
        raise RuntimeError(f'Unsupported VAL field {f}')
    raise RuntimeError(f'Unsupported object {obj}')

def parse(raw):
    t=raw[1:4].decode('ascii','replace')
    c=raw[5:7].decode('ascii','replace')
    f=int.from_bytes(raw[9:11],'big')
    ident=raw[11:35].split(b'\xff')[0].decode('ascii','replace')
    return Header(raw, t, c, f, payload_length(t,f), ident,raw[-1], t=='MEM' and c=='BU')

def is_end(raw):
    return raw[:4]==b':END'

def header_end():
    raw = bytearray([0xFF]*HEADER_SIZE)
    prefix = b":END"
    raw[:len(prefix)] = prefix
    raw[-1] = calculate_casio_checksum(raw)
    t=raw[1:4].decode('ascii','replace')
    return Header(raw, t, "", 0, 0, "", raw[-1], True)
