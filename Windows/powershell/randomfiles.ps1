# Define a pasta de destino
$folder = ".\TestFiles"
New-Item -ItemType Directory -Path $folder -Force

# Cria 100 arquivos com conteúdo "Teste"
1..100 | ForEach-Object {
    Set-Content -Path "$folder\Arquivo_$_.txt" -Value "Conteudo de teste aleatorio $_"
}
Write-Host "100 arquivos criados com sucesso em $folder" -ForegroundColor Green