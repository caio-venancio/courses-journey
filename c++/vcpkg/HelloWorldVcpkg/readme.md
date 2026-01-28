vcpkg new --application
vcpkg add port fmt

.\mingw-msys2.bat
$env:VCPKG_DEFAULT_TRIPLET="x64-mingw-dynamic"
$env:VCPKG_DEFAULT_HOST_TRIPLET="x64-mingw-dynamic"

cmake --preset default
cmake --build build
.\build\HelloWorld.exe