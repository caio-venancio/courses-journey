$base = "F:\"
$out  = "F_hashes.csv"

Get-ChildItem $base -Recurse -File | ForEach-Object {
    try {
        [PSCustomObject]@{
            RelativePath = $_.FullName.Substring($base.Length)
            Size         = $_.Length
            LastWrite    = $_.LastWriteTimeUtc
            Hash         = (Get-FileHash $_.FullName -Algorithm SHA256).Hash
        }
    } catch {}
} | Export-Csv $out -NoTypeInformation