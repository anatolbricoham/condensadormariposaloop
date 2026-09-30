// GENERADO por cad/generar_3d.py – posiciones iniciales calculadas.
#pragma once
struct Banda { const char* nombre; uint32_t khz; int32_t preset; int32_t paso_fino; };
const int32_t PASOS_MAX = 22800;   // 95° de recorrido
const float PASOS_GRADO = 240.00;
const Banda BANDAS[] = {
  {"40m", 7100, 19554, 8},
  {"30m", 10120, 9064, 4},
  {"20m", 14200, 4061, 3},
  {"17m", 18120, 2068, 3},
  {"15m", 21200, 1214, 3},
};
const int N_BANDAS = sizeof(BANDAS) / sizeof(BANDAS[0]);
