import os
import pefile

for f in os.listdir("."):
    try:
        pe = pefile.PE(f)
        print(f"\n==== {f} ====")
        print("Subsystem:", pe.OPTIONAL_HEADER.Subsystem)
        print("EntryPoint:", hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint))

        if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                dll = entry.dll.decode(errors="ignore")
                print(" ", dll)
    except Exception:
        pass
