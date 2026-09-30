"""
Genera las piezas imprimibles en 3D y los datos del autoajuste.

  python cad/generar_3d.py [--version B]

1. Escribe cad/3d/scad/parametros.scad a partir de calc/modelo.py (para que todo cuadre).
2. Renderiza cada .scad a STL (cad/3d/stl) y PNG (cad/3d/png) con OpenSCAD.
3. Calcula la tabla de posiciones del motor por banda (resultados/posiciones_motor.md)
   y escribe firmware/autotune_loop/bandas.h.
Requiere OpenSCAD en el PATH (https://openscad.org).
"""
import argparse, math, os, shutil, subprocess, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.join(AQUI, "..")
sys.path.insert(0, os.path.join(RAIZ, "calc"))
from modelo import GeometriaPlacas, condensador, loop

SCAD = os.path.join(AQUI, "3d", "scad")
STL = os.path.join(AQUI, "3d", "stl")
PNG = os.path.join(AQUI, "3d", "png")

VERSIONES = {"A": (3, 16), "B": (4, 22), "C": (5, 27)}

# ---- mecánica del accionamiento ----
PASOS_VUELTA = 200          # motor NEMA17 1,8°
MICROPASOS = 16             # TMC2209 con MS1=MS2=1
REDUCTORA = 27              # reductora planetaria 27:1 (real 26,85:1)
HUECO_ANGULAR = (90.0 - GeometriaPlacas().angulo_lobulo)   # grados sin solape desde Cmin

# ---- mecánica general (mm) ----
PARAM = dict(d_eje=5, d_eje_motor=8, rodamiento_d=16.2, rodamiento_h=5.2,
             altura_eje=75, d_mastil=40, d_tubo=22, separacion_loop=40)

BANDAS = [("80m", 3.65), ("60m", 5.36), ("40m", 7.10), ("30m", 10.12), ("20m", 14.20),
          ("17m", 18.12), ("15m", 21.20), ("12m", 24.94), ("10m", 28.50)]

PIEZAS = [  # fichero, parámetros extra, nombre de salida, cantidad, notas
    ("tapa_condensador.scad", {}, "tapa_condensador", 2, "PETG/ASA · 5 perímetros · 40 % gyroid · cara interior en la cama"),
    ("acoplamiento_aislante.scad", {}, "acoplamiento_aislante", 1, "PETG · 100 % relleno · de pie"),
    ("soporte_motor.scad", {"parte": '"cuna"'}, "soporte_motor_cuna", 1, "PETG · 30 % · sobre el pie"),
    ("soporte_motor.scad", {"parte": '"brida"'}, "soporte_motor_brida", 1, "PETG · 40 %"),
    ("soporte_hall.scad", {}, "soporte_hall", 1, "PETG · 40 %"),
    ("soporte_base_mastil.scad", {}, "soporte_base_mastil", 1, "ASA/PETG · 50 % · placa en la cama"),
    ("cruceta_mastil_tubo.scad", {}, "cruceta_mastil_tubo", 1, "ASA/PETG · 50 % · soportes en el agujero del tubo"),
    ("soporte_lazo_acoplo.scad", {}, "soporte_lazo_acoplo", 1, "ASA/PETG · 50 %"),
    ("clip_lazo_acoplo.scad", {}, "clip_lazo_acoplo", 1, "ASA/PETG · 40 % (ajusta d_cable)"),
    ("cajas.scad", {"pieza": '"controlador"'}, "caja_controlador", 1, "PLA/PETG · 20 %"),
    ("cajas.scad", {"pieza": '"controlador_tapa"'}, "caja_controlador_tapa", 1, "PLA/PETG · 20 %"),
    ("cajas.scad", {"pieza": '"puente"'}, "caja_puente_roe", 1, "PLA/PETG · 20 %"),
    ("cajas.scad", {"pieza": '"puente_tapa"'}, "caja_puente_roe_tapa", 1, "PLA/PETG · 20 %"),
]


def escribir_parametros(version):
    g = GeometriaPlacas()
    gap, juegos = VERSIONES[version]
    c = condensador(juegos, gap)
    lineas = [f"// GENERADO por cad/generar_3d.py (versión {version}). No editar a mano.",
              f"r_varillas = {g.r_varillas};", "ang_varillas = 30;", f"r_rotor = {g.r_rotor};",
              f"r_stator_ext = {g.r_stator_ext};", f"gap = {gap};", f"separador = {c.separador_mm:g};",
              f"juegos = {juegos};", f"longitud_pack = {c.longitud_pack_mm:g};"]
    lineas += [f"{k} = {v};" for k, v in PARAM.items()]
    with open(os.path.join(SCAD, "parametros.scad"), "w") as f:
        f.write("\n".join(lineas) + "\n")
    return c


def vista_png(stl, png, titulo):
    """Vista isométrica sombreada del STL (sin depender de OpenGL)."""
    import numpy as np, trimesh, matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    m = trimesh.load(stl)
    tri = m.vertices[m.faces]
    luz = np.array([0.4, -0.6, 0.7]); luz /= np.linalg.norm(luz)
    k = np.clip(m.face_normals @ luz, 0, 1) * 0.65 + 0.3
    col = np.stack([0.95 * k, 0.55 * k, 0.2 * k, np.ones_like(k)], 1)
    fig = plt.figure(figsize=(6, 4.5)); ax = fig.add_subplot(projection="3d")
    ax.add_collection3d(Poly3DCollection(tri, facecolors=col, edgecolor="none"))
    lo, hi = m.bounds; c = (lo + hi) / 2; r = (hi - lo).max() / 2
    ax.set_xlim(c[0]-r, c[0]+r); ax.set_ylim(c[1]-r, c[1]+r); ax.set_zlim(c[2]-r, c[2]+r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(28, -55); ax.set_axis_off()
    e = hi - lo
    ax.set_title(f"{titulo}\n{e[0]:.0f} × {e[1]:.0f} × {e[2]:.0f} mm", fontsize=10)
    fig.tight_layout(); fig.savefig(png, dpi=110); plt.close(fig)


def render():
    exe = shutil.which("openscad")
    if not exe:
        print("OpenSCAD no encontrado: solo se escriben los .scad"); return []
    os.makedirs(STL, exist_ok=True); os.makedirs(PNG, exist_ok=True)
    hechas = []
    for fich, extra, nombre, n, notas in PIEZAS:
        defs = sum((["-D", f"{k}={v}"] for k, v in extra.items()), [])
        src = os.path.join(SCAD, fich)
        subprocess.run([exe, "-q", "-o", os.path.join(STL, nombre + ".stl"), *defs, src], check=True)
        vista_png(os.path.join(STL, nombre + ".stl"), os.path.join(PNG, nombre + ".png"), nombre)
        hechas.append((nombre, n, notas))
        print("  ✓", nombre)
    return hechas


def posiciones(c, diametro=1.0, tubo=22):
    pasos_grado = PASOS_VUELTA * MICROPASOS * REDUCTORA / 360.0
    filas, h = [], []
    for b, f in BANDAS:
        r = loop(f, diametro, tubo / 1000, 10)
        C = r.C_necesaria_pF
        if not (c.c_min_pF <= C <= c.c_max_ideal_pF):
            filas.append((b, f, C, None, None, None)); continue
        frac = (C - c.c_min_pF) / (c.c_max_ideal_pF - c.c_min_pF)
        ang = HUECO_ANGULAR + frac * (90 - HUECO_ANGULAR)
        pasos = round(ang * pasos_grado)
        dC_paso = (c.c_max_ideal_pF - c.c_min_pF) / ((90 - HUECO_ANGULAR) * pasos_grado)
        khz_paso = f * 1e3 * dC_paso / (2 * (C + 2.6))
        filas.append((b, f, C, ang, pasos, khz_paso, r.BW_kHz))
        h.append(f'  {{"{b}", {int(f*1000)}, {pasos}, {max(1, int(r.BW_kHz / khz_paso / 4))}}},')
    return filas, h, pasos_grado


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--version", default="B", choices=VERSIONES)
    ap.add_argument("--diametro", type=float, default=1.0); ap.add_argument("--tubo", type=float, default=22)
    a = ap.parse_args()
    c = escribir_parametros(a.version)
    print(f"Versión {a.version}: {c.juegos} juegos, hueco {c.gap_mm} mm, paquete {c.longitud_pack_mm:.0f} mm")
    hechas = render()
    filas, h, ppg = posiciones(c, a.diametro, a.tubo)
    pasos_max = round(90 * ppg)
    os.makedirs(os.path.join(RAIZ, "resultados"), exist_ok=True)
    with open(os.path.join(RAIZ, "resultados", "posiciones_motor.md"), "w") as f:
        f.write(f"# Posiciones del motor por banda (versión {a.version}, loop Ø {a.diametro} m, tubo {a.tubo:g} mm)\n\n"
                f"Motor {PASOS_VUELTA} pasos × {MICROPASOS} micropasos × reductora {REDUCTORA}:1 = "
                f"**{ppg:.0f} pasos/grado**. Home (sensor Hall) = Cmin. Recorrido útil 0–90° = 0–{pasos_max} pasos.\n"
                f"Modelo lineal C(θ): sin solape los primeros {HUECO_ANGULAR:.0f}°, después C crece linealmente hasta Cmax a 90°.\n\n"
                "| Banda | f (kHz) | C (pF) | Ángulo desde Cmin | Paso preset | kHz por paso | Ancho de banda (kHz) |\n|---|---|---|---|---|---|---|\n")
        for fila in filas:
            if fila[3] is None:
                f.write(f"| {fila[0]} | {fila[1]*1000:.0f} | {fila[2]:.0f} | fuera de rango | — | — | — |\n")
            else:
                b, fr, C, ang, p, k, bw = fila
                f.write(f"| {b} | {fr*1000:.0f} | {C:.0f} | {ang:.1f}° | {p} | {k:.3f} | {bw:.1f} |\n")
        f.write("\nLos presets son un **punto de partida**: el autoajuste busca el mínimo de ROE alrededor de ellos "
                "y guarda la posición real aprendida en la memoria del ESP32.\n")
    with open(os.path.join(RAIZ, "firmware", "autotune_loop", "bandas.h"), "w") as f:
        f.write("// GENERADO por cad/generar_3d.py – posiciones iniciales calculadas.\n#pragma once\n"
                "struct Banda { const char* nombre; uint32_t khz; int32_t preset; int32_t paso_fino; };\n"
                f"const int32_t PASOS_MAX = {pasos_max + round(5 * ppg)};   // 95° de recorrido\n"
                f"const float PASOS_GRADO = {ppg:.2f};\n"
                "const Banda BANDAS[] = {\n" + "\n".join(h) + "\n};\n"
                "const int N_BANDAS = sizeof(BANDAS) / sizeof(BANDAS[0]);\n")
    with open(os.path.join(AQUI, "3d", "PIEZAS.md"), "w") as f:
        f.write("# Piezas imprimibles\n\nParámetros comunes: capa 0,2 mm, boquilla 0,4, 4–5 perímetros. "
                "**Exterior: ASA o PETG** (el PLA se deforma al sol de Murcia).\n\n"
                "| Pieza | Cant. | Material / ajustes | Vista |\n|---|---|---|---|\n")
        for nombre, n, notas in hechas:
            f.write(f"| [`{nombre}.stl`](stl/{nombre}.stl) | {n} | {notas} | ![](png/{nombre}.png) |\n")
    print("Hecho.")


if __name__ == "__main__":
    main()
