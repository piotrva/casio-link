import serial
import time
from pathlib import Path
from casio_transport import *
from casio_protocol import *
from casio_report import report


PORT = 'COM5'
BAUD = 9600
FILE = "obj_059"

out=Path('capture')
out.mkdir(exist_ok=True)

ser = serial.Serial(PORT, BAUD, timeout=5, stopbits=2)

enq(ser)
print("sent ENQ, waiting for DC3...")
wait_verify_response(ser, DC3)
print("got DC3, sending header...")
time.sleep(0.5)
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
