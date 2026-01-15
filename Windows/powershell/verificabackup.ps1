# Verifica se todo arquivo na pasta A está na pasta B
# $pastaA = "Windows\tests\real"
$pastaA = "C:\Users\user\Documents\Backups diversos\audio note\audio"
# $pastaB = "Windows\tests\realestrutura"
$pastaB = "C:\Users\user\Music\Audio"

# Estrutura eficiente para comparação
$hashesB = [System.Collections.Generic.HashSet[string]]::new()

Write-Host "Indexando arquivos da pasta B..."

# 1. Indexar hashes da pasta B
Get-ChildItem $pastaB -Recurse -File | ForEach-Object {
    try {
        $null = $hashesB.Add(
            (Get-FileHash $_.FullName -Algorithm SHA256).Hash
        )
    } catch {}
}

Write-Host "Verificando arquivos da pasta A..."

# 2. Verificar arquivos da pasta A
$faltando = @()

Get-ChildItem $pastaA -Recurse -File | ForEach-Object {
    try {
        $hashA = (Get-FileHash $_.FullName -Algorithm SHA256).Hash
        if (-not $hashesB.Contains($hashA)) {
            $faltando += $_.FullName
        }
    } catch {
        $faltando += $_.FullName
    }
}

# 3. Resultado
if ($faltando.Count -eq 0) {
    Write-Host "Certo. Todos os arquivos da pasta A existem na pasta B."
} else {
    Write-Host "Errado. Arquivos da pasta A que NAO existem na pasta B."
    $faltando | ForEach-Object { Write-Host $_ }
}
