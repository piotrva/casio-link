def hex_dump(d): return ' '.join(f'{b:02X}' for b in d)
def ascii_dump(d): return ''.join(chr(b) if 32<=b<127 else '.' for b in d)
