import numpy as np
from PIL import Image
from pathlib import Path

out = Path('capture')
raw_bytes = (out/f'obj_graph_payload.bin').read_bytes()
payload_bytes = raw_bytes[1:-1]  # Exclude frame start 0x3A and checksum 0x66

# 1. Reconstruct the 80x48 pixel grid
# Initialize 48 rows x 80 columns canvas with zeros
canvas = np.zeros((48, 80), dtype=np.uint8)

# 480 bytes total
byte_idx = 0
for row in range(48):
    for col in range(80):
        byte = payload_bytes[row + int(col/8)*48]
        bit = col%8
        pixel = (byte >> bit) & 1
        canvas[47-row, col] = pixel

# 2. Color Inversion: Active bit (1) = Black (0), Inactive bit (0) = White (255)
image_matrix = (1 - canvas) * 255

# 3. Render and scale up 8x
img = Image.fromarray(image_matrix, mode="L")
img_scaled = img.resize((80 * 8, 48 * 8), resample=Image.NEAREST)

img_scaled.save(out/"casio_fixed_screen.png")
img_scaled.show()
