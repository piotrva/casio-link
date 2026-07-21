import serial
from casio_dump import *
ENQ=0x16
DC3=0x13
ACK=0x06
ERR=0x22
EXISTS=0x21

HEADER_SIZE=50
GRAPH_HEADER_SIZE=40

def read_exact(ser,n):
    d=bytearray()
    while len(d)<n:
        b=ser.read(n-len(d))
        if not b: raise TimeoutError(f'Timeout: ({len(d)}/{n} bytes received)')
        d.extend(b)
    return bytes(d)

def wait_for_response(ser):
    for _ in range(4):
        b = ser.read(1)
        if b:
            return b[0]
    raise TimeoutError(f'Timeout: no response')

def wait_verify_response(ser, expected):
    resp = wait_for_response(ser)
    if resp != expected:
        raise ValueError(f"Unexpected response: {resp:02X} (expected: {expected:02X})")

def enq(ser):
    ser.write(bytes([ENQ]))

def ack(ser):
    ser.write(bytes([ACK]))

def send_header(ser, header):
    ser.write(header.raw)
