param([ValidateSet("evidence","portable","native")][string]$Profile="evidence")
$ErrorActionPreference="Stop"
$repo=(Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Push-Location $repo
try {
    $python=Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) { throw "Python 3 bulunamadı." }
    & $python.Source "lab/verify.py"
    if ($LASTEXITCODE -ne 0) { throw "SACI baseline doğrulaması başarısız." }
    $vagrant=Get-Command vagrant -ErrorAction SilentlyContinue
    if (-not $vagrant) { Write-Warning "Vagrant bulunamadı; yalnız baseline doğrulandı."; exit 0 }
    $env:SACI_LAB_PROFILE=$Profile
    & $vagrant.Source validate
    if ($LASTEXITCODE -ne 0) { throw "Vagrantfile doğrulaması başarısız." }
    & $vagrant.Source plugin list
} finally { Pop-Location }
