# Posiciones del motor por banda (versión B, loop Ø 1.0 m, tubo 22 mm)

Motor 200 pasos × 16 micropasos × reductora 27:1 = **240 pasos/grado**. Home (sensor Hall) = Cmin. Recorrido útil 0–90° = 0–21600 pasos.
Modelo lineal C(θ): sin solape los primeros 5°, después C crece linealmente hasta Cmax a 90°.

| Banda | f (kHz) | C (pF) | Ángulo desde Cmin | Paso preset | kHz por paso | Ancho de banda (kHz) |
|---|---|---|---|---|---|---|
| 80m | 3650 | 774 | fuera de rango | — | — | — |
| 60m | 5360 | 358 | fuera de rango | — | — | — |
| 40m | 7100 | 203 | 81.5° | 19554 | 0.172 | 5.5 |
| 30m | 10120 | 98 | 37.8° | 9064 | 0.498 | 8.8 |
| 20m | 14200 | 49 | 16.9° | 4061 | 1.374 | 19.0 |
| 17m | 18120 | 29 | 8.6° | 2068 | 2.855 | 40.6 |
| 15m | 21200 | 20 | 5.1° | 1214 | 4.570 | 70.3 |
| 12m | 24940 | 14 | fuera de rango | — | — | — |
| 10m | 28500 | 10 | fuera de rango | — | — | — |

Los presets son un **punto de partida**: el autoajuste busca el mínimo de ROE alrededor de ellos y guarda la posición real aprendida en la memoria del ESP32.
