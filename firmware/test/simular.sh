#!/bin/sh
# Compila el firmware en el PC con cabeceras simuladas y ejecuta una simulación del autoajuste
# (resonancia de 32 pasos de ancho + 300 pasos de holgura en la reductora). Requiere g++.
set -e
cd "$(dirname "$0")"
mkdir -p build
sed -e 's/#define USAR_OLED    1/#define USAR_OLED 0/' -e 's/#define USAR_WIFI    1/#define USAR_WIFI 0/' ../autotune_loop/config.h > build/config.h
cp ../autotune_loop/bandas.h build/
( echo '#include "Arduino.h"'; cat ../autotune_loop/autotune_loop.ino ) > build/main.cpp
g++ -std=c++17 -O2 -I build -I . build/main.cpp simulacion.cpp -o build/sim
./build/sim
