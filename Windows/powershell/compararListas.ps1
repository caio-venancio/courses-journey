# Não foi testado
$lista1 = Get-Content "C:\Users\caiov\Documents\Backups diversos\Comparacao\lista_final_G.txt"
$lista2 = Get-Content "C:\Users\caiov\Documents\Backups diversos\Comparacao\lista_final_H.txt"

$iguais = Compare-Object $lista1 $lista2 -IncludeEqual -ExcludeDifferent | Measure-Object

Write-Host "Iguais:" $iguais.Count