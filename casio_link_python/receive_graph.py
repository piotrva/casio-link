import serial
from pathlib import Path
from casio_transport import *
from casio_protocol import *
from casio_report import report


PORT = 'COM5'
BAUD = 9600

out = Path('capture')
out.mkdir(exist_ok=True)

ser = serial.Serial(PORT, BAUD, timeout=5, stopbits=2)

print('Waiting for ENQ...')
wait_verify_response(ser, ENQ)
ser.write(bytes([DC3]))



hdr = read_exact(ser,GRAPH_HEADER_SIZE)
ack(ser)
h = parse(hdr)
report(h)
(out/f'obj_graph_header.bin').write_bytes(hdr)
if h.payload_length:
    p = read_exact(ser,h.payload_length)
    print(hex_dump(p))
    (out/f'obj_graph_payload.bin').write_bytes(p)
    

print("DONE")

