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

idx = 0
while True:
    hdr = read_exact(ser,HEADER_SIZE)
    if is_end(hdr):
        ack(ser)
        print('END')
        break
    h = parse(hdr)
    report(h)
    (out/f'obj_{idx:03d}_header.bin').write_bytes(hdr)
    ack(ser)
    if h.payload_length:
        p = read_exact(ser,h.payload_length)
        (out/f'obj_{idx:03d}_payload.bin').write_bytes(p)
        ack(ser)
    if h.terminates_transfer:
        print('MEM BU -> END')
        break
    idx+=1
