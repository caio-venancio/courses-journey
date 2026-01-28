https://learn.microsoft.com/pt-br/vcpkg/get_started/get-started?pivots=shell-powershell

## Instalação
git clone https://github.com/microsoft/vcpkg.git
cd vcpkg; .\bootstrap-vcpkg.bat
$env:VCPKG_ROOT = "C:\path\to\vcpkg"
$env:PATH = "$env:VCPKG_ROOT;$env:PATH"

## Uso
mkdir helloworld && cd helloworld
vcpkg new --application
vcpkg add port fmt
...fazer alguns arquivos cmake e cpp...
cmake --preset=default
cmake --build build