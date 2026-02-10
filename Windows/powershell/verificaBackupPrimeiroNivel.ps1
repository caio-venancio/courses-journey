# Verifica se todo arquivo na pasta A está na pasta B
# Somente por nomes
$pastaA = "E:\"
$pastaB = "G:\Backup do Anisio 1"

Write-Host "Indexando backup (recursivo)..."

# Indexar todos os caminhos relativos do backup
$indexB = [System.Collections.Generic.HashSet[string]]::new()

Get-ChildItem $pastaB -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($pastaB.Length).TrimStart('\')
    $null = $indexB.Add($rel)
}

Write-Host "Verificando origem..."

$resultado = @()

# Para cada item da raiz da pasta A
Get-ChildItem $pastaA | ForEach-Object {

    if ($_.PSIsContainer) {
        # Pasta: se QUALQUER arquivo interno faltar → incompleta
        $incompleta = Get-ChildItem $_.FullName -Recurse -File -ErrorAction SilentlyContinue |
            Where-Object {
                $rel = $_.FullName.Substring($pastaA.Length).TrimStart('\')
                -not $indexB.Contains($rel)
            } |
            Select-Object -First 1

        if ($incompleta) {
            $resultado += [PSCustomObject]@{
                Nome   = $_.Name
                Tipo   = "Pasta"
                Status = "Conteufdo incompleto"
            }
        }

    } else {
        # Arquivo direto na raiz
        $rel = $_.FullName.Substring($pastaA.Length).TrimStart('\')
        if (-not $indexB.Contains($rel)) {
            $resultado += [PSCustomObject]@{
                Nome   = $_.Name
                Tipo   = "Arquivo"
                Status = "Ausente"
            }
        }
    }
}

# Mensagem final
if ($resultado.Count -eq 0) {
    Write-Host "Certo! Backup completo: todos os arquivos estao presentes." -ForegroundColor Green
} else {
    Write-Host "Nao... Backup incompleto: alguns itens estao ausentes." -ForegroundColor Yellow
    $resultado
}