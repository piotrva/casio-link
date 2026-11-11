import serial
import time
from pathlib import Path
from casio_transport import *
from casio_protocol import *
from casio_report import report


PORT = 'COM5'
BAUD = 9600
FILE = "data_000_X"

out=Path('capture')
out.mkdir(exist_ok=True)

ser = serial.Serial(PORT, BAUD, timeout=5, stopbits=2)

wait_verify_response(ser, 0x15)
ser.write(bytes([DC3]))

hdr = read_exact(ser,HEADER_SIZE)
h = parse(hdr)
report(h)
(out/f'data_req_header.bin').write_bytes(hdr)
ack(ser)

payload = (out/f'{FILE}_payload.bin').read_bytes()
ser.write(payload)
print("waiting for ACK...")
wait_verify_response(ser, ACK)

print("got ACK, sending END...")

h = header_end()
report(h)
send_header(ser, h)

exit(666)

header = (out/f'{FILE}_header.bin').read_bytes()
report(parse(header))
ser.write(header)
print("waiting for ACK...")
resp = wait_for_response(ser)
if resp == ACK:
    print("got ACK, sending payload...")
    time.sleep(0.5)
    payload = (out/f'{FILE}_payload.bin').read_bytes()
    ser.write(payload)
    print("waiting for ACK...")
    wait_verify_response(ser, ACK)
    print("got ACK, sending END...")
elif resp == EXISTS:
    print("file already exists, sending END...")
    time.sleep(0.5)
    ser.write(bytes([ACK]))
    wait_verify_response(ser, ACK)

time.sleep(0.5)

h = header_end()
report(h)
send_header(ser, h)

print("DONE!!!")
