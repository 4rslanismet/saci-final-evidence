param([string]$Name,[string]$AssetId,[string]$Role,[string]$Profile)
New-Item -ItemType Directory -Path C:\SACI -Force | Out-Null
@"
name=$Name
asset_id=$AssetId
role=$Role
profile=$Profile
"@ | Set-Content -Path C:\SACI\node.conf -Encoding UTF8
Write-Host "[SACI] Windows scaffold completed for $Name ($AssetId)."
