$origem        = "Windows\tests\real"
$backup        = "Windows\tests\vazio"
$novos         = "Windows/tests/resultado"

# Garantir que a pasta final exista
New-Item -ItemType Directory -Path $novos -Force | Out-Null

# Criar estrutura de hash rápida
$hashes = [System.Collections.Generic.HashSet[string]]::new()

Write-Host "Indexando arquivos já existentes no backup..."

# 1. Indexar TUDO que já existe no backup
Get-ChildItem $backup -Recurse -File |
Where-Object { $_.FullName -notlike "$novos*" } |
ForEach-Object {
    try {
        $null = $hashes.Add(
            (Get-FileHash $_.FullName -Algorithm SHA256).Hash
        )
    } catch {}
}

Write-Host "Processando arquivos novos..."

# 2. Processar arquivos da origem
Get-ChildItem $origem -Recurse -File | ForEach-Object {

    try {
        $hashOrigem = (Get-FileHash $_.FullName -Algorithm SHA256).Hash

        # 3. Só entra se o CONTEÚDO não existir ainda
        if ($hashes.Add($hashOrigem)) {

            # Evitar sobrescrita por nome
            $destinoArquivo = Join-Path $novos $_.Name

            if (Test-Path $destinoArquivo) {
                $destinoArquivo = Join-Path $novos (
                    "{0}_{1}{2}" -f
                    [IO.Path]::GetFileNameWithoutExtension($_.Name),
                    $hashOrigem.Substring(0,8),
                    $_.Extension
                )
            }

            Copy-Item $_.FullName -Destination $destinoArquivo
            Write-Host "COPIADO:" $_.FullName
        }
    } catch {
        Write-Warning "Erro ao processar: $($_.FullName)"
    }
}

Write-Host "Concluído."

# ✔ copia somente arquivos cujo conteúdo não existe
# ✔ ignora arquivos duplicados em pastas diferentes
# ✔ funciona mesmo com estruturas completamente distintas