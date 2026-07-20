def calculate_casio_checksum(packet_bytes):
 total=sum(packet_bytes[:-1]); return (0x13A-total)&0xFF

def verify(packet_bytes):
 s=packet_bytes[-1]; c=calculate_casio_checksum(packet_bytes); return s,c,s==c
