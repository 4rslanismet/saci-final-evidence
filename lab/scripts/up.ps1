param(
 [ValidateSet("virtualbox","hyperv","vmware_desktop","libvirt","parallels","qemu")][string]$Provider="virtualbox",
 [ValidateSet("evidence","portable","native")][string]$Profile="evidence",
 [ValidateSet("dhcp","static")][string]$Network="dhcp",
 [switch]$DeployServices
)
$ErrorActionPreference="Stop"
$repo=(Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$env:SACI_LAB_PROFILE=$Profile
$env:SACI_NETWORK_MODE=$Network
$env:VAGRANT_DEFAULT_PROVIDER=$Provider
$env:SACI_DEPLOY_SERVICES=if($DeployServices){"1"}else{"0"}
Push-Location $repo
try {
    & (Join-Path $PSScriptRoot "check.ps1") -Profile $Profile
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    vagrant up --provider=$Provider
} finally { Pop-Location }
