# Versiones propuestas del condensador (para loop Ø 1.0 m, tubo 22 mm)

## Versión A · QRP / portable

- Separación rotor-estátor: **3 mm** → separador entre placas de estátor **7 mm** (1 tuerca + 3 arandelas)
- Juegos: **16** → 32 placas de estátor (16 por lado) + 15 placas de rotor
- Cmax ≈ **212 pF** (ideal) / 231 pF con bordes · Cmin estimada ≈ **19 pF**
- Tensión práctica admisible ≈ **3000 V rms** (ruptura teórica aire seco ≈ 18 kV pico)
- Longitud del paquete de placas: **106 mm**

| Banda | C necesaria (pF) | ¿Sintoniza? | V a potencia nominal (V rms) | Potencia máx. segura (W) |
|---|---|---|---|---|
| 80 m | 774 | ❌ poca C | 1499 | — |
| 60 m | 358 | ❌ poca C | 1988 | — |
| 40 m | 203 | ✅ | 2366 | 32 |
| 30 m | 98 | ✅ | 2676 | 25 |
| 20 m | 49 | ✅ | 2553 | 28 |
| 17 m | 29 | ✅ | 2231 | 36 |
| 15 m | 20 | ✅ | 1984 | 46 |
| 12 m | 14 | ❌ Cmin alta | 1728 | — |
| 10 m | 10 | ❌ Cmin alta | 1531 | — |

## Versión B · 50 W

- Separación rotor-estátor: **4 mm** → separador entre placas de estátor **9 mm** (2 tuercas + 1 arandela)
- Juegos: **22** → 44 placas de estátor (22 por lado) + 21 placas de rotor
- Cmax ≈ **223 pF** (ideal) / 247 pF con bordes · Cmin estimada ≈ **20 pF**
- Tensión práctica admisible ≈ **4300 V rms** (ruptura teórica aire seco ≈ 24 kV pico)
- Longitud del paquete de placas: **190 mm**

| Banda | C necesaria (pF) | ¿Sintoniza? | V a potencia nominal (V rms) | Potencia máx. segura (W) |
|---|---|---|---|---|
| 80 m | 774 | ❌ poca C | 2370 | — |
| 60 m | 358 | ❌ poca C | 3144 | — |
| 40 m | 203 | ✅ | 3741 | 66 |
| 30 m | 98 | ✅ | 4232 | 52 |
| 20 m | 49 | ✅ | 4036 | 57 |
| 17 m | 29 | ✅ | 3528 | 74 |
| 15 m | 20 | ✅ | 3137 | 94 |
| 12 m | 14 | ❌ Cmin alta | 2733 | — |
| 10 m | 10 | ❌ Cmin alta | 2421 | — |

## Versión C · 100 W

- Separación rotor-estátor: **5 mm** → separador entre placas de estátor **11 mm** (2 tuercas + 3 arandelas)
- Juegos: **27** → 54 placas de estátor (27 por lado) + 26 placas de rotor
- Cmax ≈ **221 pF** (ideal) / 250 pF con bordes · Cmin estimada ≈ **20 pF**
- Tensión práctica admisible ≈ **5900 V rms** (ruptura teórica aire seco ≈ 30 kV pico)
- Longitud del paquete de placas: **287 mm**

| Banda | C necesaria (pF) | ¿Sintoniza? | V a potencia nominal (V rms) | Potencia máx. segura (W) |
|---|---|---|---|---|
| 80 m | 774 | ❌ poca C | 3352 | — |
| 60 m | 358 | ❌ poca C | 4446 | — |
| 40 m | 203 | ✅ | 5291 | 124 |
| 30 m | 98 | ✅ | 5985 | 97 |
| 20 m | 49 | ✅ | 5708 | 107 |
| 17 m | 29 | ✅ | 4989 | 140 |
| 15 m | 20 | ❌ Cmin alta | 4436 | — |
| 12 m | 14 | ❌ Cmin alta | 3865 | — |
| 10 m | 10 | ❌ Cmin alta | 3424 | — |

**Notas**

- *Potencia máx. segura* = potencia a la que la tensión del loop iguala la tensión práctica del condensador (criterio TA2WK ≈ 1–1,2 kV/mm). En SSB/CW puedes estirar algo; en FT8/RTTY (100 % ciclo) respeta el valor.
- Si Cmin impide llegar a 12/10 m, quita placas (el diseño es modular) o usa un loop más pequeño para esas bandas.
