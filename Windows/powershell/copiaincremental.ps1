$hashesDestino = Get-ChildItem "Destino" -Recurse -File |
  Get-FileHash -Algorithm SHA256 |
  Select-Object -ExpandProperty Hash

Get-ChildItem "Origem" -Recurse -File | ForEach-Object {
  $h = (Get-FileHash $_.FullName -Algorithm SHA256).Hash
  if ($hashesDestino -notcontains $h) {
    Copy-Item $_.FullName -Destination "Destino"
  }
}

# ✔ copia somente arquivos cujo conteúdo não existe
# ✔ ignora arquivos duplicados em pastas diferentes
# ✔ funciona mesmo com estruturas completamente distintas