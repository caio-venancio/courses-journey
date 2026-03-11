Get-ChildItem "C:\Origem" -Recurse -File |
ForEach-Object {
    [PSCustomObject]@{
        Nome = $_.Name
        Caminho = $_.FullName
        Data = $_.LastWriteTime
        Tamanho = $_.Length
        Hash = (Get-FileHash $_.FullName -Algorithm SHA256).Hash
    }
} | Export-Csv origem.csv -NoTypeInformation