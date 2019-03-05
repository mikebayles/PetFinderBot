$url = "$(System.TeamFoundationCollectionUri)/$(System.CollectionId)/$(System.TeamProjectId)/_apis/build/latest/$(System.DefinitionId)"
Write-Host "URL: $url"
$response = Invoke-RestMethod -Uri $url -Method Get -ContentType "application/json"
$lastBuild = $result.id
Write-Host "LastBuild = $lastBuild"
Write-Host "##vso[task.setvariable variable=lastBuild]$lastBuild"
