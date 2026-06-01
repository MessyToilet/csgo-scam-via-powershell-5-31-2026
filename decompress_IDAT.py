
from pathlib import Path
import struct, zlib, math

b = Path("msi_full/US8yBGmyj").read_bytes()
pos = b.find(b"IDAT") - 4

idat_parts = []
chunks = []

while pos + 8 <= len(b):
    length = struct.unpack(">I", b[pos:pos+4])[0]
    ctype = b[pos+4:pos+8]
    data = b[pos+8:pos+8+length]
    crc = b[pos+8+length:pos+8+length+4]

    chunks.append((pos, length, ctype, crc.hex()))

    if ctype == b"IDAT":
        idat_parts.append(data)
    elif ctype == b"IEND":
        break

    pos += 8 + length + 4

print("chunks:", len(chunks))
print("first chunk:", chunks[0])
print("last chunk:", chunks[-1])
print("total IDAT compressed bytes:", sum(len(x) for x in idat_parts))

compressed = b"".join(idat_parts)

for mode in ["normal", "raw-deflate"]:
    try:
        if mode == "normal":
            raw = zlib.decompress(compressed)
        else:
            raw = zlib.decompress(compressed, -15)

        print("\nDECOMPRESS OK:", mode)
        print("raw bytes:", len(raw))

        # Try common PNG pixel formats:
        # grayscale=1, RGB=3, RGBA=4 bytes/pixel
        for bpp, name in [(1, "gray8"), (3, "rgb8"), (4, "rgba8")]:
            print("\nFormat", name)
            hits = []
            for w in range(1, 5000):
                row = 1 + w * bpp  # PNG filter byte + pixels
                if len(raw) % row == 0:
                    h = len(raw) // row
                    if 1 <= h <= 5000:
                        hits.append((w, h))
            print("candidates:", hits[:50])
            print("count:", len(hits))

    except Exception as e:
        print("\nDECOMPRESS FAIL:", mode, e)

