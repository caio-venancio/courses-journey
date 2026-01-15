# copiaincremental_estrutura.ps1

$origem        = "Windows\tests\real"
$backup        = "Windows\tests\vazio"
$novos         = "Windows/tests/resultado"

# Garantir que a pasta final exista
New-Item -ItemType Directory -Path $novos -Force | Out-Null

Write-Host "Indexando arquivos do backup..."

# 1. Criar índice de hashes do backup POR CAMINHO RELATIVO
$backupHashes = @{}

Get-ChildItem $backup -Recurse -File | ForEach-Object {
    try {
        $relativo = $_.FullName.Substring($backup.Length).TrimStart('\')
        $backupHashes[$relativo] = (Get-FileHash $_.FullName -Algorithm SHA256).Hash
    } catch {}
}

Write-Host "Processando arquivos da origem..."

# 2. Processar arquivos da origem
Get-ChildItem $origem -Recurse -File | ForEach-Object {

    try {
        # caminho relativo à origem
        $relativo = $_.FullName.Substring($origem.Length).TrimStart('\')

        # destino correspondente em $novos
        $destinoArquivo = Join-Path $novos $relativo
        $destinoPasta   = Split-Path $destinoArquivo -Parent

        # hash do arquivo da origem
        $hashOrigem = (Get-FileHash $_.FullName -Algorithm SHA256).Hash

        $copiar = $false

        if (-not $backupHashes.ContainsKey($relativo)) {
            # arquivo não existe no backup
            $copiar = $true
        }
        elseif ($backupHashes[$relativo] -ne $hashOrigem) {
            # arquivo existe mas conteúdo mudou
            $copiar = $true
        }

        if ($copiar) {
            # criar estrutura de diretórios
            New-Item -ItemType Directory -Path $destinoPasta -Force | Out-Null

            # copiar arquivo
            Copy-Item $_.FullName -Destination $destinoArquivo -Force

            Write-Host "COPIADO:" $relativo
        }

    } catch {
        Write-Warning "Erro ao processar: $($_.FullName)"
    }
}

Write-Host "Concluído."
