<#
.SYNOPSIS
    Setup script for Image Compression Analyzer on Windows.
    Installs Python, ImageMagick, and LibWebP.

.DESCRIPTION
    1. Checks for Python and ImageMagick (installs via Winget if missing).
    2. Checks for cwebp. If missing, downloads local copy and adds to session PATH.
    3. Installs Python requirements (matplotlib).
#>

# ==========================================
# CONFIGURATION
# ==========================================
# Update this version number when a newer release becomes available.
# Check https://developers.google.com/speed/webp/download for latest versions.
$WebPVersion = "1.5.0" 
$WebPFileName = "libwebp-$WebPVersion-windows-x64"
$WebPZip = "$WebPFileName.zip"
$WebPUrl = "https://storage.googleapis.com/downloads.webmproject.org/releases/webp/$WebPZip"
# ==========================================

$ErrorActionPreference = "Stop"

function Test-CommandExists {
    param ($Command)
    $exists = Get-Command $Command -ErrorAction SilentlyContinue
    return $null -ne $exists
}

Write-Host "=== Image Compression Analyzer Setup ===" -ForegroundColor Cyan

# -----------------------------------------------------------------------------
# 1. Check/Install Python
# -----------------------------------------------------------------------------
Write-Host "`n[1/4] Checking Python..."
if (Test-CommandExists "python") {
    Write-Host "Python is installed." -ForegroundColor Green
} else {
    Write-Host "Python not found. Attempting install via Winget..." -ForegroundColor Yellow
    try {
        winget install -e --id Python.Python.3 --accept-source-agreements --accept-package-agreements
        Write-Host "Python installed. NOTE: You may need to restart your terminal after this script finishes." -ForegroundColor Yellow
        
        # Attempt to refresh env vars for this session so we can continue
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    } catch {
        Write-Error "Failed to install Python via Winget. Please install manually from python.org."
        exit 1
    }
}

# -----------------------------------------------------------------------------
# 2. Check/Install ImageMagick
# -----------------------------------------------------------------------------
Write-Host "`n[2/4] Checking ImageMagick..."
if (Test-CommandExists "magick") {
    Write-Host "ImageMagick is installed." -ForegroundColor Green
} else {
    Write-Host "ImageMagick not found. Attempting install via Winget..." -ForegroundColor Yellow
    try {
        winget install -e --id ImageMagick.ImageMagick --accept-source-agreements --accept-package-agreements
        Write-Host "ImageMagick installed." -ForegroundColor Green
        
        # Refresh path again
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    } catch {
        Write-Error "Failed to install ImageMagick via Winget. Please install manually."
        exit 1
    }
}

# -----------------------------------------------------------------------------
# 3. Check/Install WebP (cwebp)
# -----------------------------------------------------------------------------
Write-Host "`n[3/4] Checking cwebp (WebP Tools)..."

$LocalLibWebPPath = Join-Path $PSScriptRoot "libwebp"
$LocalBinPath = Join-Path $LocalLibWebPPath "bin"

# Check Global Path
if (Test-CommandExists "cwebp") {
    Write-Host "cwebp found in global PATH." -ForegroundColor Green
} 
# Check Local Path (already downloaded)
elseif (Test-Path "$LocalBinPath\cwebp.exe") {
    Write-Host "Found local libwebp. Adding to current session PATH..." -ForegroundColor Green
    $env:PATH = "$LocalBinPath;$env:PATH"
} 
# Download
else {
    Write-Host "cwebp not found. Downloading LibWebP v$WebPVersion..." -ForegroundColor Yellow
    
    try {
        # Download
        Write-Host "Downloading from: $WebPUrl"
        Invoke-WebRequest -Uri $WebPUrl -OutFile $WebPZip -UseBasicParsing
        
        # Extract
        Write-Host "Extracting..."
        Expand-Archive -Path $WebPZip -DestinationPath $PSScriptRoot -Force
        
        # Rename and Clean up
        if (Test-Path $LocalLibWebPPath) { Remove-Item $LocalLibWebPPath -Recurse -Force }
        Rename-Item (Join-Path $PSScriptRoot $WebPFileName) "libwebp"
        Remove-Item $WebPZip -Force
        
        # Add to Session Path
        Write-Host "Adding $LocalBinPath to current session PATH..." -ForegroundColor Green
        $env:PATH = "$LocalBinPath;$env:PATH"
        
    } catch {
        Write-Error "Failed to download or setup WebP. Error: $_"
        exit 1
    }
}

# -----------------------------------------------------------------------------
# 4. Install Python Dependencies
# -----------------------------------------------------------------------------
Write-Host "`n[4/4] Installing Python Dependencies..."
try {
    pip install matplotlib
    Write-Host "Dependencies installed." -ForegroundColor Green
} catch {
    Write-Error "Failed to install pip packages. Ensure Python is in your PATH."
}

Write-Host "`n=== Setup Complete! ===" -ForegroundColor Cyan
Write-Host "You can now run the analyzer using:"
Write-Host "python compression_analyzer.py <your_image>"
Write-Host "Note: If 'python' or 'magick' commands fail, please restart your terminal/PowerShell window." -ForegroundColor Gray