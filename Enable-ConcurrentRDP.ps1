$ErrorActionPreference     = "SilentlyContinue"
$RDP_WRAPPER               = "C:\Windows\Temp\RDPWrapper.zip"
$EXTRACT_DEST              = "C:\Windows\Temp\RDPWrapper\"
$PROGRAM_FOLDER            = "C:\Program Files\RDP Wrapper"
$DOWNLOAD_URL              = "https://github.com/stascorp/rdpwrap/releases/download/v1.6.2/RDPWrap-v1.6.2.zip"
$REPLACEMENT_CONFIG        = "https://raw.githubusercontent.com/sebaxakerhtc/rdpwrap.ini/master/rdpwrap.ini"
$SELF                      = $MyInvocation.MyCommand.Path

# Delete this script
function Invoke-SelfDestruct {
    Start-Sleep -Seconds 5
    Remove-Item -Path $SELF -Force
    exit
}

# Clean up temporary files
function Invoke-CleanUp {
    Write-Host "[*] Cleaning up file artifacts."
    Remove-Item $RDP_WRAPPER -Force 
    Remove-Item $EXTRACT_DEST -Force -Recurse
    Invoke-SelfDestruct
}

# Check if RDP is enabled. Attempt to enable RDP if it's not.
Write-Host "[*] Checking if RDP is enabled."
if ((Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections").fDenyTSConnections -eq 1) {
    Write-Host "[*] RDP is disabled. Attempting to enable RDP."
    Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections" -Value 0
    if ((Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server" -Name "fDenyTSConnections").fDenyTSConnections -eq 1) {
        Write-Host "[-] Failed to enable RDP."
        Invoke-SelfDestruct
    }
    else {
        Write-Host "[+] Successfully enabled RDP."
    }
}
else {
    Write-Host "[*] RDP is enabled."
}

# Download the RDP Wrapper program
Invoke-Webrequest -Uri $DOWNLOAD_URL -OutFile $RDP_WRAPPER
if (!(Test-Path -Path $RDP_WRAPPER)) {
    Write-Error "Failed to download RDP Wrapper."
    Invoke-SelfDestruct
}

# Extract archive and execute installer. Set file attributes to hidden.
Write-Host ("[+] Downloaded RDPWrapper to path: {0}. Starting installation." -f $RDP_WRAPPER)
Expand-Archive -Path $RDP_WRAPPER -Destination $EXTRACT_DEST -Force
Start-Process ("{0}\RDPWInst.exe" -f $EXTRACT_DEST) -ArgumentList "-i", "-o" -WindowStyle Hidden -Wait
if (!(Test-Path -Path $PROGRAM_FOLDER)) {
    Write-Host "[-] Installation failed."
    Invoke-CleanUp
}
Write-Host ("[*] Installation Succeeded. Setting attribute {0} to hidden." -f $PROGRAM_FOLDER)
(Get-Item $PROGRAM_FOLDER).Attributes = "Hidden"

# Download configuration file
Write-Host "[*] Fetching new configuration content."
$Request = Invoke-WebRequest -Uri $REPLACEMENT_CONFIG
if ($Request.StatusCode -ne 200) {
    Write-Host "[-] Failed to retrieve configuration, attempting retrieval with UseBasicParsing specification."
    $Request = Invoke-WebRequest -Uri $REPLACEMENT_CONFIG -UseBasicParsing
    if ($Request.StatusCode -ne 200) {
        Write-Host "[-] Failed to retrieve config with basic parsing enabled. Quitting."
        Invoke-CleanUp
    }
}

# Write new configuration file
Write-Host "[*] Got new configuration. Stopping TermService and replacing configuration."
Stop-Service TermService -Force
Set-Content -Path ("{0}\rdpwrap.ini" -f $PROGRAM_FOLDER) -Value $Request.Content -Force
Start-Service TermService
if ((Get-Service -Name TermService).Status -eq "Running") {
    Write-Host "[+] Started TermService. Multi session RDP should now be available."
}
else {
    Write-Host "[-] TermService is not running. An issue has occurred."
}

# Cleanup artifacts
Invoke-CleanUp