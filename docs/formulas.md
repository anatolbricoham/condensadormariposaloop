# Fórmulas usadas

Todo está implementado en [`calc/modelo.py`](../calc/modelo.py). Unidades SI.

## 1. Condensador mariposa

Un condensador mariposa tiene **dos grupos de estátor (A y B)** y **un rotor común flotante**.
La RF entra por A, pasa al rotor a través del aire y sale por B, así que **no hay contacto
deslizante** (sin escobillas ⇒ sin pérdidas ni ruido) y los dos grupos quedan **en serie**.

Con `N` = nº de juegos (placas de estátor por lado, criterio del artículo TA2WK):

| Magnitud | Fórmula |
|---|---|
| Placas de rotor | `N − 1` |
| Huecos de aire por grupo | `2·(N − 1)` |
| Área de solape de un lóbulo | `A = ½·θ·(R_rotor² − r_int²)` (θ en rad) |
| Capacidad de un hueco | `C_h = ε₀·A / d` |
| Capacidad de un grupo | `C_g = 2·(N−1)·C_h` |
| **Capacidad total (A y B en serie)** | **`C_max = C_g / 2 = (N−1)·ε₀·A/d`** |
| Separador entre placas de estátor | `s = 2·d + t` (t = espesor de chapa) → TA2WK: `d = (s − t)/2` |
| Corrección de bordes (estimación) | `k = 1 + d/(π·w)·(1 + ln(2π·w/d))`, w = ancho radial del lóbulo |
| Capacidad mínima (estimación empírica) | `C_min ≈ 0,07·C_max + 3 pF` |

Con la geometría del repo (θ = 85°, R_rotor = 82 mm, r_int = 16 mm) → A = 4 798 mm² y
con d = 3 mm la tabla coincide con la de TA2WK dentro de ±3 %.

### Tensión

- Ruptura teórica del aire seco: ~3 kV/mm (campo uniforme, DC). En RF, con bordes, polvo
  y humedad (Murcia en verano ≈ 60–70 % HR en costa) hay que derratear mucho.
- Criterio práctico (tabla TA2WK): 3 mm → 3 000 V · 4 mm → 4 300 V · 5 mm → 5 900 V · 6 mm → 7 400 V.
- En la mariposa la tensión del loop se reparte entre los dos huecos en serie (A-rotor y
  rotor-B), lo que da margen extra frente a un condensador normal con el mismo hueco.

## 2. Loop magnético

| Magnitud | Fórmula |
|---|---|
| Inductancia (aro circular, radio R, conductor radio a) | `L = μ₀·R·(ln(8R/a) − 2)` |
| Reactancia | `X = 2π·f·L` |
| Capacidad de resonancia | `C = 1/(ω²·L) − C_parásita` |
| Resistencia de radiación | `R_rad = 320·π⁴·A²/λ⁴ ≈ 31 170·A²/λ⁴` |
| Resistencia superficial del cobre | `R_s = √(π·f·μ₀·ρ)` , ρ = 1,72·10⁻⁸ Ω·m |
| Resistencia de pérdidas | `R_p = R_s·P/(π·D_tubo) + R_uniones` |
| Eficiencia | `η = R_rad/(R_rad + R_p)` |
| Q cargado (adaptado) | `Q = X / (2·(R_rad+R_p))` |
| Ancho de banda (−3 dB) | `BW = f / Q` |
| Corriente en el loop | `I = √(P/(R_rad+R_p))` |
| **Tensión en el condensador** | **`V = I·X`** (rms), pico = V·√2 |
| Lazo de acoplo | `D_acoplo ≈ D_loop / 5` |

Un loop octogonal hecho con 8 tramos rectos y codos de 45° se comporta prácticamente
como un aro circular del mismo perímetro (error < 5 % en L).
