"""
Modelo de cálculo: condensador de aire tipo mariposa (butterfly) + antena loop magnética.

Unidades SI salvo que se indique. Todas las funciones son puras para poder
reutilizarlas desde otros scripts o desde un notebook.
"""
from __future__ import annotations
import math
from dataclasses import dataclass, asdict

EPS0 = 8.8541878128e-12      # F/m
MU0 = 4e-7 * math.pi         # H/m
RHO_CU = 1.72e-8             # ohm·m (cobre)
C0 = 299_792_458.0           # m/s

# -------------------------------------------------------------------------
# 1. CONDENSADOR MARIPOSA
# -------------------------------------------------------------------------
@dataclass
class GeometriaPlacas:
    """Geometría de las placas (mm). Valores por defecto = diseño de este repo."""
    r_rotor: float = 82.0        # radio exterior de los lóbulos del rotor
    r_hub: float = 12.0          # radio del cubo central del rotor
    r_stator_int: float = 16.0   # radio interior (hueco) del estator
    r_stator_ext: float = 102.0  # radio exterior del estator (aloja las varillas)
    r_varillas: float = 92.0     # radio donde van las varillas M5 del estator
    angulo_lobulo: float = 85.0  # grados de cada lóbulo y de cada estátor (<90° => hueco angular a Cmin)
    espesor: float = 1.0         # espesor de chapa (mm)

    def area_solape_mm2(self) -> float:
        """Área de solape rotor-estator de UN lóbulo con el rotor totalmente dentro."""
        th = math.radians(self.angulo_lobulo)
        return 0.5 * th * (self.r_rotor**2 - self.r_stator_int**2)


@dataclass
class ResultadoCondensador:
    juegos: int              # nº de placas de estátor por lado (como en el artículo TA2WK)
    placas_rotor: int        # = juegos - 1
    gap_mm: float            # separación de aire rotor-estátor
    separador_mm: float      # longitud de separador entre dos placas de estátor = 2·gap + t
    c_por_hueco_pF: float
    c_max_ideal_pF: float    # sin efectos de borde (mismo criterio que la tabla TA2WK)
    c_max_pF: float          # con corrección de borde estimada
    c_min_pF: float          # estimación (rotor girado 90°)
    v_rms_practico: float    # tensión RMS recomendada total (criterio conservador)
    v_pico_teorico: float    # ruptura teórica aire seco (3 kV/mm por hueco, 2 huecos en serie)
    longitud_pack_mm: float  # longitud del paquete de placas (sin placas finales)


def factor_borde(gap_mm: float, ancho_mm: float) -> float:
    """Corrección de borde tipo Palmer para placas paralelas (estimación)."""
    x = gap_mm / (math.pi * ancho_mm)
    return 1.0 + x * (1.0 + math.log(2 * math.pi * ancho_mm / gap_mm))


# criterio práctico derivado de la tabla del artículo TA2WK (≈1,0–1,25 kV/mm)
V_PRACTICO_TA2WK = {3: 3000, 4: 4300, 5: 5900, 6: 7400}


def v_practico(gap_mm: float) -> float:
    if gap_mm in V_PRACTICO_TA2WK:
        return float(V_PRACTICO_TA2WK[gap_mm])
    # interpolación lineal / extrapolación ≈ 1,45 kV/mm - 1,4 kV
    return 1450.0 * gap_mm - 1400.0


def condensador(juegos: int, gap_mm: float, g: GeometriaPlacas = GeometriaPlacas()) -> ResultadoCondensador:
    """
    Mariposa: dos grupos de estátor (A y B) y un rotor flotante común.
    Cada grupo tiene `juegos` placas de estátor y `juegos-1` placas de rotor intercaladas
    -> 2·(juegos-1) huecos de aire por grupo. Los dos grupos quedan EN SERIE
    (A -> rotor -> B), así que C_total = C_grupo / 2 = (juegos-1)·C_hueco.
    """
    area = g.area_solape_mm2() * 1e-6
    d = gap_mm * 1e-3
    c_hueco = EPS0 * area / d
    n_rot = juegos - 1
    c_ideal = n_rot * c_hueco
    ancho = g.r_rotor - g.r_stator_int
    c_max = c_ideal * factor_borde(gap_mm, ancho)
    # Cmin: capacidad residual (bordes, varillas, eje). Estimación empírica típica
    # de mariposas medidas: 6–10 % de Cmax + ~3 pF de conexiones.
    c_min = 0.07 * c_max + 3e-12
    sep = 2 * gap_mm + g.espesor
    long_pack = (juegos - 1) * sep + g.espesor
    return ResultadoCondensador(
        juegos=juegos, placas_rotor=n_rot, gap_mm=gap_mm, separador_mm=sep,
        c_por_hueco_pF=c_hueco * 1e12,
        c_max_ideal_pF=c_ideal * 1e12, c_max_pF=c_max * 1e12, c_min_pF=c_min * 1e12,
        v_rms_practico=v_practico(gap_mm),
        v_pico_teorico=2 * 3000.0 * gap_mm,
        longitud_pack_mm=long_pack,
    )


# -------------------------------------------------------------------------
# 2. ANTENA LOOP MAGNÉTICA (circular u octogonal ≈ circular del mismo perímetro)
# -------------------------------------------------------------------------
@dataclass
class ResultadoLoop:
    f_MHz: float
    L_uH: float
    X_ohm: float
    C_necesaria_pF: float
    R_rad_mohm: float
    R_perd_mohm: float
    eficiencia_pct: float
    eficiencia_dB: float
    Q_cargado: float
    BW_kHz: float
    I_rms_A: float
    V_cap_rms: float
    V_cap_pico: float


def inductancia_loop(diametro_m: float, d_conductor_m: float) -> float:
    R = diametro_m / 2
    a = d_conductor_m / 2
    return MU0 * R * (math.log(8 * R / a) - 2.0)


def capacidad_parasita_loop_pF(diametro_m: float, d_conductor_m: float) -> float:
    """Capacidad propia aproximada de un aro (fórmula de Medhurst-like simplificada)."""
    perimetro = math.pi * diametro_m
    # ~ 0.82 pF por metro de perímetro para conductores 15–25 mm (valor típico calculadoras)
    return 0.82 * perimetro * 1.0


def loop(f_MHz: float, diametro_m: float, d_conductor_m: float, potencia_W: float,
         r_extra_ohm: float = 0.005, c_parasita_pF: float | None = None) -> ResultadoLoop:
    f = f_MHz * 1e6
    w = 2 * math.pi * f
    lam = C0 / f
    L = inductancia_loop(diametro_m, d_conductor_m)
    X = w * L
    if c_parasita_pF is None:
        c_parasita_pF = capacidad_parasita_loop_pF(diametro_m, d_conductor_m)
    C_tot = 1 / (w * w * L)
    C_nec = C_tot * 1e12 - c_parasita_pF
    area = math.pi * (diametro_m / 2) ** 2
    r_rad = 320 * math.pi**4 * area**2 / lam**4
    rs = math.sqrt(math.pi * f * MU0 * RHO_CU)          # resistencia superficial
    perimetro = math.pi * diametro_m
    r_perd = rs * perimetro / (math.pi * d_conductor_m) + r_extra_ohm
    r_tot = r_rad + r_perd
    eff = r_rad / r_tot
    q_l = X / (2 * r_tot)
    bw = f / q_l
    i_rms = math.sqrt(potencia_W / r_tot)
    v = i_rms * X
    return ResultadoLoop(
        f_MHz=f_MHz, L_uH=L * 1e6, X_ohm=X, C_necesaria_pF=C_nec,
        R_rad_mohm=r_rad * 1e3, R_perd_mohm=r_perd * 1e3,
        eficiencia_pct=eff * 100, eficiencia_dB=10 * math.log10(eff),
        Q_cargado=q_l, BW_kHz=bw / 1e3, I_rms_A=i_rms, V_cap_rms=v, V_cap_pico=v * math.sqrt(2),
    )


def lazo_acoplo_diametro_m(diametro_loop_m: float) -> float:
    """Regla clásica: lazo de acoplo (Faraday) = 1/5 del diámetro del loop principal."""
    return diametro_loop_m / 5


as_dict = asdict
