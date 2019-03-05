$url = "$env:SYSTEM_TEAMFOUNDATIONCOLLECTIONURI/$env:SYSTEM_COLLECTIONID/$env:SYSTEM_TEAMPROJECTID/_apis/build/latest/$env:SYSTEM_DEFINITIONID"
Write-Host "URL: $url"
$response = Invoke-RestMethod -Uri $url -Method Get -ContentType "application/json"
$lastBuild = $result.id
Write-Host "LastBuild = $lastBuild"
Write-Host "##vso[task.setvariable variable=lastBuild]$lastBuild"
