import re
import base64

with open("vars.txt", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Extract simple string assignments
vars_dict = {}

for name, value in re.findall(r"\$([A-Za-z0-9_]+)\s*=\s*'([^']*)'", text):
    vars_dict[name] = value

# Locate the large concatenation
m = re.search(r"\$PzgEetbY\s*=\s*(.+?)\n\$oGCpCSpU", text, re.S)

if not m:
    raise SystemExit("Couldn't find PzgEetbY assignment")

expr = m.group(1)

parts = re.findall(r"\$([A-Za-z0-9_]+)", expr)

blob = "".join(vars_dict.get(v, "") for v in parts)

print(f"Length: {len(blob)}")

# Try UTF-16LE Base64 decode
try:
    decoded = base64.b64decode(blob)
    decoded = decoded.decode("utf-16le", errors="replace")

    print("\n==== DECODED ====\n")
    print(decoded)

    with open("decoded.ps1", "w", encoding="utf-8") as f:
        f.write(decoded)

except Exception as e:
    print("Decode failed:", e)
