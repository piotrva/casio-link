from casio_checksum import verify
from casio_dump import *
def report(h):
 s,c,ok=verify(h.raw)
 print('='*60)
 print(f'{h.object_type}/{h.category} {h.identifier}')
 print('Header field :',h.header_field)
 print('Payload      :',h.payload_length)
 print(f'Checksum     : {s:02X} '+('OK' if ok else f'FAIL (calc {c:02X})'))
 print('Raw')
 print(hex_dump(h.raw))
 print(ascii_dump(h.raw))
