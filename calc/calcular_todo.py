"""
Ejecuta todos los cálculos y escribe los resultados en /resultados.

    python calc/calcular_todo.py [--diametro 1.0] [--tubo 22] [--potencia 100]

Genera:
  resultados/tabla_condensador.csv|md     C vs nº de juegos y separación (comparada con TA2WK)
  resultados/loop_<D>m.csv|md             parámetros del loop banda por banda
  resultados/variantes.md                 3 versiones propuestas + cobertura y potencia máx.
  resultados/lista_materiales.csv|md      despiece y cantidades por versión
  resultados/*.png                        gráficas
"""
import argparse, csv, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "cad"))
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from modelo import condensador, loop, GeometriaPlacas, lazo_acoplo_diametro_m, capacidad_parasita_loop_pF

RAIZ = os.path.join(os.path.dirname(__file__), "..")
RES = os.path.join(RAIZ, "resultados")
os.makedirs(RES, exist_ok=True)

BANDAS = [("80 m", 3.65), ("60 m", 5.36), ("40 m", 7.10), ("30 m", 10.12), ("20 m", 14.20),
          ("17 m", 18.12), ("15 m", 21.20), ("12 m", 24.94), ("10 m", 28.50)]
TA2WK = {5: (58, 39, 29, 23), 10: (131, 87, 66, 53), 15: (204, 136, 102, 79),
         20: (277, 185, 139, 110), 30: (423, 282, 212, 163)}
GAPS = (3, 4, 5, 6)

# nombre, separación (mm), juegos, potencia nominal pensada (W)
VARIANTES = [("A · QRP / portable", 3, 16, 20),
             ("B · 50 W", 4, 22, 50),
             ("C · 100 W", 5, 27, 100)]

# receta de separadores con tuercas DIN 934 M5 (4,0 mm) y arandelas DIN 125 M5 (1,0 mm)
RECETA = {7: "1 tuerca + 3 arandelas", 9: "2 tuercas + 1 arandela", 11: "2 tuercas + 3 arandelas",
          13: "3 tuercas + 1 arandela"}


def md_tabla(cab, filas):
    s = "| " + " | ".join(cab) + " |\n|" + "---|" * len(cab) + "\n"
    for f in filas:
        s += "| " + " | ".join(str(x) for x in f) + " |\n"
    return s


def escribir(nombre, cab, filas, titulo, extra=""):
    with open(os.path.join(RES, nombre + ".csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(cab); w.writerows(filas)
    with open(os.path.join(RES, nombre + ".md"), "w") as f:
        f.write(f"# {titulo}\n\n{extra}\n\n" + md_tabla(cab, filas))


def tabla_condensador():
    cab = ["Juegos", "Placas rotor", "Placas estátor"] + [f"{g} mm: calc / TA2WK (pF)" for g in GAPS]
    filas = []
    for n in (5, 10, 15, 16, 20, 22, 25, 27, 30):
        fila = [n, n - 1, 2 * n]
        for i, g in enumerate(GAPS):
            c = condensador(n, g)
            ref = TA2WK.get(n)
            fila.append(f"{c.c_max_ideal_pF:.0f} / {ref[i]}" if ref else f"{c.c_max_ideal_pF:.0f}")
        filas.append(fila)
    g = GeometriaPlacas()
    extra = (f"Geometría: lóbulo {g.angulo_lobulo:.0f}°, R rotor {g.r_rotor} mm, R interior estátor "
             f"{g.r_stator_int} mm → área de solape por lóbulo = {g.area_solape_mm2():.0f} mm².\n\n"
             "`calc` = capacidad ideal (placas paralelas, sin bordes), mismo criterio que la tabla "
             "de TA2WK. Con 3 mm el modelo coincide con TA2WK dentro de ±3 %. Para 4–6 mm TA2WK da "
             "valores algo menores (calculadora KI6GD con otra definición de hueco): usa el menor de "
             "los dos como valor seguro y **mide siempre con un medidor LCR** al terminar.")
    escribir("tabla_condensador", cab, filas, "Capacidad máxima del condensador mariposa", extra)


def tabla_loop(D, tubo_mm, P):
    cab = ["Banda", "f (MHz)", "L (µH)", "C necesaria (pF)", "R rad (mΩ)", "R pérd (mΩ)",
           "Eficiencia", "Q cargado", "Ancho banda (kHz)", "I loop (A)", f"V cond @{P} W (V rms)", "V pico"]
    filas = []
    for b, f in BANDAS:
        r = loop(f, D, tubo_mm / 1000, P)
        filas.append([b, f, f"{r.L_uH:.2f}", f"{r.C_necesaria_pF:.0f}", f"{r.R_rad_mohm:.2f}",
                      f"{r.R_perd_mohm:.1f}", f"{r.eficiencia_pct:.1f} % ({r.eficiencia_dB:.1f} dB)",
                      f"{r.Q_cargado:.0f}", f"{r.BW_kHz:.1f}", f"{r.I_rms_A:.1f}",
                      f"{r.V_cap_rms:.0f}", f"{r.V_cap_pico:.0f}"])
    extra = (f"Loop circular (u octogonal equivalente) de **{D} m de diámetro** (perímetro "
             f"{math.pi*D:.2f} m) en tubo de cobre de **{tubo_mm} mm**. Capacidad parásita estimada "
             f"{capacidad_parasita_loop_pF(D, tubo_mm/1000):.1f} pF (ya restada). Resistencia extra de "
             f"uniones/soldaduras 5 mΩ. Lazo de acoplo recomendado: Ø {lazo_acoplo_diametro_m(D)*100:.0f} cm.\n\n"
             "⚠️ La tensión en el condensador es la de un loop perfectamente adaptado: con "
             f"{P} W aparecen varios kV. No toques el loop transmitiendo.")
    nombre = f"loop_{D:g}m".replace(".", "_")
    escribir(nombre, cab, filas, f"Loop magnético Ø {D} m – {tubo_mm} mm – {P} W", extra)


def variantes(D, tubo_mm):
    txt = f"# Versiones propuestas del condensador (para loop Ø {D} m, tubo {tubo_mm} mm)\n\n"
    resumen = []
    for nombre, gap, n, pnom in VARIANTES:
        c = condensador(n, gap)
        cab = ["Banda", "C necesaria (pF)", "¿Sintoniza?", "V a potencia nominal (V rms)",
               "Potencia máx. segura (W)"]
        filas = []
        for b, f in BANDAS:
            r = loop(f, D, tubo_mm / 1000, pnom)
            ok = c.c_min_pF <= r.C_necesaria_pF <= c.c_max_ideal_pF
            pmax = pnom * (c.v_rms_practico / r.V_cap_rms) ** 2
            filas.append([b, f"{r.C_necesaria_pF:.0f}", "✅" if ok else ("❌ poca C" if r.C_necesaria_pF > c.c_max_ideal_pF else "❌ Cmin alta"),
                          f"{r.V_cap_rms:.0f}", f"{pmax:.0f}" if ok else "—"])
        txt += (f"## Versión {nombre}\n\n"
                f"- Separación rotor-estátor: **{gap} mm** → separador entre placas de estátor **{c.separador_mm:.0f} mm** "
                f"({RECETA.get(round(c.separador_mm), 'tubo de aluminio cortado a medida')})\n"
                f"- Juegos: **{n}** → {2*n} placas de estátor ({n} por lado) + {n-1} placas de rotor\n"
                f"- Cmax ≈ **{c.c_max_ideal_pF:.0f} pF** (ideal) / {c.c_max_pF:.0f} pF con bordes · Cmin estimada ≈ **{c.c_min_pF:.0f} pF**\n"
                f"- Tensión práctica admisible ≈ **{c.v_rms_practico:.0f} V rms** (ruptura teórica aire seco ≈ {c.v_pico_teorico/1000:.0f} kV pico)\n"
                f"- Longitud del paquete de placas: **{c.longitud_pack_mm:.0f} mm**\n\n")
        txt += md_tabla(cab, filas) + "\n"
        resumen.append((nombre, gap, n, c))
    txt += ("**Notas**\n\n- *Potencia máx. segura* = potencia a la que la tensión del loop iguala la tensión "
            "práctica del condensador (criterio TA2WK ≈ 1–1,2 kV/mm). En SSB/CW puedes estirar algo; en FT8/RTTY "
            "(100 % ciclo) respeta el valor.\n- Si Cmin impide llegar a 12/10 m, quita placas (el diseño es modular) "
            "o usa un loop más pequeño para esas bandas.\n")
    with open(os.path.join(RES, "variantes.md"), "w") as f:
        f.write(txt)
    return resumen


def materiales(resumen):
    from generar_planos import rotor, estator
    a_rot = rotor()[0].area / 100      # cm²
    a_est = estator()[0].area / 100
    cab = ["Pieza", "Especificación"] + [v[0] for v in resumen]
    filas = []
    def fila(pieza, spec, fn):
        filas.append([pieza, spec] + [fn(g, n, c) for _, g, n, c in resumen])
    fila("Placa rotor (corte láser)", "Aluminio 1 mm (EN AW-1050/5754), rotor.dxf", lambda g, n, c: n - 1)
    fila("Placa estátor (corte láser)", "Aluminio 1 mm, estator.dxf", lambda g, n, c: 2 * n)
    fila("Placas de repuesto (+10 %)", "", lambda g, n, c: math.ceil(0.1 * (3 * n - 1)))
    fila("Superficie de aluminio neta", "cm² (pide chapa 1000×500 mm o que el taller ponga el material)",
         lambda g, n, c: f"{(n-1)*a_rot + 2*n*a_est:.0f}")
    fila("Tapas / placas finales", "Policarbonato o metacrilato 8–10 mm, 240×240, tapa.dxf", lambda g, n, c: 2)
    fila("Varilla roscada M5 estátor", "Inox A2 DIN 975, 4 tramos de (mm)", lambda g, n, c: f"4 × {c.longitud_pack_mm + 90:.0f}")
    fila("Eje del rotor", "Varilla M5 inox (o eje 8 mm + casquillo), mm", lambda g, n, c: f"1 × {c.longitud_pack_mm + 160:.0f}")
    fila("Separadores estátor", f"de {'/'.join(str(v) for v in RECETA)} mm según versión (ver receta)", lambda g, n, c: 4 * (n - 1))
    fila("Separadores rotor", "misma longitud, en el eje central", lambda g, n, c: n - 2)
    fila("Tuercas M5 DIN 934 inox", "incluye las de los separadores + 20 de fijación",
         lambda g, n, c: _tuercas(c, n) + 20)
    fila("Arandelas M5 DIN 125 inox", "incluye separadores + 20", lambda g, n, c: _arandelas(c, n) + 20)
    fila("Collarines / anillos de bloqueo 5 mm", "para fijar el rotor en el eje", lambda g, n, c: 2)
    fila("Tirantes entre tapas", "Varilla M6 nylon o fibra de vidrio + tuercas nylon", lambda g, n, c: 4)
    fila("Rodamiento 608ZZ o casquillo de bronce/teflón", "para el eje en las tapas", lambda g, n, c: 2)
    fila("Acoplamiento aislante", "manguito de nylon/PVC o acoplador flexible + tramo de varilla de fibra", lambda g, n, c: 1)
    fila("Reductora", "planetaria 6:1 (manual) o motorreductor 12 V 1–5 rpm", lambda g, n, c: 1)
    fila("Pletina/malla de cobre", "cinta 20–25 mm o malla de coaxial para unir estátores al loop", lambda g, n, c: "2 × 20 cm")
    fila("Terminales de cobre", "para crimpar 10–16 mm², ojal M5", lambda g, n, c: 4)
    escribir("lista_materiales", cab, filas, "Lista de materiales del condensador",
             "Cantidades por versión. Los separadores de tuerca+arandela son la opción más fácil de comprar en Murcia; "
             "el tubo de aluminio (Ø 8×1 mm) cortado a medida queda más limpio.")


def _tuercas(c, n):
    s = round(c.separador_mm)
    por_sep = {7: 1, 9: 2, 11: 2, 13: 3}.get(s, 0)
    return (4 * (n - 1) + (n - 2)) * por_sep


def _arandelas(c, n):
    s = round(c.separador_mm)
    por_sep = {7: 3, 9: 1, 11: 3, 13: 1}.get(s, 0)
    return (4 * (n - 1) + (n - 2)) * por_sep


def graficas(D, tubo_mm, resumen):
    fs = [f for _, f in BANDAS]
    fig, ax = plt.subplots(figsize=(9, 5.5))
    for Dx in (0.8, 1.0, 1.2, 1.6):
        ax.plot(fs, [max(loop(f, Dx, tubo_mm / 1000, 100).C_necesaria_pF, 1) for f in fs], "o-", label=f"Loop Ø {Dx} m")
    colores = ["#2a9d8f", "#e9c46a", "#e76f51"]
    cmin = min(c.c_min_pF for *_, c in resumen); cmax = max(c.c_max_ideal_pF for *_, c in resumen)
    ax.axhspan(cmin, cmax, color="#e9c46a", alpha=0.18)
    ax.text(fs[len(fs)//2], cmax * 1.05, f"Rango de sintonía versiones A/B/C ≈ {cmin:.0f}–{cmax:.0f} pF",
            ha="center", fontsize=9, color="#8a6d00")
    ax.set_yscale("log"); ax.set_xlabel("Frecuencia (MHz)"); ax.set_ylabel("Capacidad necesaria (pF)")
    ax.set_xticks(fs); ax.set_xticklabels([b for b, _ in BANDAS], rotation=45)
    ax.set_title(f"Capacidad necesaria por banda – tubo {tubo_mm} mm ")
    ax.grid(alpha=0.3, which="both"); ax.legend(); fig.tight_layout()
    fig.savefig(os.path.join(RES, "capacidad_por_banda.png"), dpi=130)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for P in (10, 50, 100):
        ax.plot(fs, [loop(f, D, tubo_mm / 1000, P).V_cap_rms / 1000 for f in fs], "o-", label=f"{P} W")
    for (nombre, g, n, c), col in zip(resumen, colores):
        ax.axhline(c.v_rms_practico / 1000, color=col, ls="--", label=f"Límite {g} mm ({nombre.split('·')[0].strip()})")
    ax.set_xticks(fs); ax.set_xticklabels([b for b, _ in BANDAS], rotation=45)
    ax.set_ylabel("Tensión en el condensador (kV rms)")
    ax.set_title(f"Tensión en el condensador – loop Ø {D} m, tubo {tubo_mm} mm")
    ax.grid(alpha=0.3); ax.legend(fontsize=8); fig.tight_layout()
    fig.savefig(os.path.join(RES, "tension_condensador.png"), dpi=130)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    for Dx in (0.8, 1.0, 1.2, 1.6):
        ax.plot(fs, [loop(f, Dx, tubo_mm / 1000, 100).eficiencia_pct for f in fs], "o-", label=f"Ø {Dx} m")
    ax.set_xticks(fs); ax.set_xticklabels([b for b, _ in BANDAS], rotation=45)
    ax.set_ylabel("Eficiencia (%)"); ax.set_title(f"Eficiencia del loop – tubo {tubo_mm} mm")
    ax.grid(alpha=0.3); ax.legend(); fig.tight_layout()
    fig.savefig(os.path.join(RES, "eficiencia_loop.png"), dpi=130)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--diametro", type=float, default=1.0, help="diámetro del loop en m")
    ap.add_argument("--tubo", type=float, default=22, help="diámetro exterior del tubo de cobre en mm")
    ap.add_argument("--potencia", type=float, default=100, help="potencia de transmisión en W")
    a = ap.parse_args()
    tabla_condensador()
    for Dx in sorted({0.8, 1.0, 1.2, 1.6, a.diametro}):
        tabla_loop(Dx, a.tubo, int(a.potencia))
    resumen = variantes(a.diametro, a.tubo)
    materiales(resumen)
    graficas(a.diametro, a.tubo, resumen)
    print("Resultados escritos en", os.path.abspath(RES))


if __name__ == "__main__":
    main()
