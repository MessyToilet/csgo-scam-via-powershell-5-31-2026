# extract_cert.py
import sys
import pefile

path = sys.argv[1]
pe = pefile.PE(path)

sec = pe.OPTIONAL_HEADER.DATA_DIRECTORY[
    pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_SECURITY"]
]

if sec.Size == 0:
    print("No certificate table")
    sys.exit(1)

with open(path, "rb") as f:
    f.seek(sec.VirtualAddress)
    data = f.read(sec.Size)

# WIN_CERTIFICATE header is 8 bytes
cert = data[8:]

out = path + ".p7b"
with open(out, "wb") as f:
    f.write(cert)

print(out)
