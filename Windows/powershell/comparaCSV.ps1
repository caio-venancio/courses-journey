# Não foi testado
$origem  = Import-Csv "origem.csv"
$destino = Import-Csv "destino.csv"

$groupOrigem = $origem | Group-Object Hash, Data | Select-Object Name, Count
$groupDestino = $destino | Group-Object Hash, Data | Select-Object Name, Count

Compare-Object $groupOrigem $groupDestino -Property Name, Count