"""
Genera los planos de corte (DXF para corte láser + SVG + PNG de vista previa)
del condensador mariposa diseñado en calc/modelo.py.

  python cad/generar_planos.py            -> escribe en cad/salida/

Piezas:
  rotor.dxf    placa de rotor (mariposa, 2 lóbulos de 90°)  -> aluminio 1 mm
  estator.dxf  placa de estátor (1 lóbulo; se usa girada 180° en el otro lado)
  tapa.dxf     placa final/soporte (policarbonato, metacrilato o PETG impreso) 10 mm
Cotas en milímetros. Origen = eje del condensador.
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "calc"))
import ezdxf
from shapely.geometry import Point, Polygon
from shapely.ops import unary_union
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from modelo import GeometriaPlacas

G = GeometriaPlacas()
OUT = os.path.join(os.path.dirname(__file__), "salida")
os.makedirs(OUT, exist_ok=True)
AGUJERO_M5 = 5.3          # taladro de paso M5
RADIO_REDONDEO = 2.0      # redondeo de esquinas (importante en alta tensión)
ANG_VARILLAS = 30.0       # varillas del estátor a ±30° del centro del lóbulo


def sector(r_in, r_out, ang_centro, ang_ancho, n=180):
    a0 = math.radians(ang_centro - ang_ancho / 2)
    a1 = math.radians(ang_centro + ang_ancho / 2)
    ext = [(r_out * math.cos(a0 + (a1 - a0) * i / n), r_out * math.sin(a0 + (a1 - a0) * i / n)) for i in range(n + 1)]
    inn = [(r_in * math.cos(a1 - (a1 - a0) * i / n), r_in * math.sin(a1 - (a1 - a0) * i / n)) for i in range(n + 1)]
    return Polygon(ext + inn)


def redondear(poly, r=RADIO_REDONDEO):
    return poly.buffer(-r, quad_segs=16).buffer(2 * r, quad_segs=16).buffer(-r, quad_segs=16)


def agujero(x, y, d=AGUJERO_M5):
    return Point(x, y).buffer(d / 2, quad_segs=32)


def rotor():
    lob1 = sector(0, G.r_rotor, 0, G.angulo_lobulo)
    lob2 = sector(0, G.r_rotor, 180, G.angulo_lobulo)
    hub = Point(0, 0).buffer(G.r_hub, quad_segs=32)
    forma = redondear(unary_union([lob1, lob2, hub]))
    return forma.difference(agujero(0, 0)), [(0, 0)]


def varillas_estator(ang_centro):
    return [(G.r_varillas * math.cos(math.radians(ang_centro + s * ANG_VARILLAS)),
             G.r_varillas * math.sin(math.radians(ang_centro + s * ANG_VARILLAS))) for s in (-1, 1)]


def estator(ang_centro=0.0):
    # mismo ángulo que el lóbulo del rotor: a 90° de giro no hay solape (Cmin real)
    forma = redondear(sector(G.r_stator_int, G.r_stator_ext, ang_centro, G.angulo_lobulo))
    hs = varillas_estator(ang_centro)
    for x, y in hs:
        forma = forma.difference(agujero(x, y))
    return forma, hs


def tapa(lado=240.0, esquina=10.0):
    h = lado / 2
    forma = redondear(Polygon([(-h, -h), (h, -h), (h, h), (-h, h)]), 8)
    pts = [(0, 0, 8.2)]                                   # eje (casquillo/rodamiento 8 mm o M5+casquillo)
    pts += [(x, y, AGUJERO_M5) for x, y in varillas_estator(0) + varillas_estator(180)]
    c = h - esquina
    pts += [(sx * c, sy * c, 6.5) for sx in (-1, 1) for sy in (-1, 1)]   # 4 tirantes M6 de nylon/fibra
    for x, y, d in pts:
        forma = forma.difference(agujero(x, y, d))
    return forma, pts


def a_dxf(poly, nombre, notas):
    doc = ezdxf.new("R2010", setup=True)
    doc.units = ezdxf.units.MM
    msp = doc.modelspace()
    doc.layers.add("CORTE", color=1)
    doc.layers.add("NOTAS", color=3)
    for ring in [poly.exterior, *poly.interiors]:
        msp.add_lwpolyline(list(ring.coords), close=True, dxfattribs={"layer": "CORTE"})
    minx, miny, maxx, maxy = poly.bounds
    for i, t in enumerate(notas):
        msp.add_text(t, height=3.5, dxfattribs={"layer": "NOTAS"}).set_placement((minx, miny - 10 - 6 * i))
    ruta = os.path.join(OUT, nombre + ".dxf")
    doc.saveas(ruta)
    return ruta


def a_svg(poly, nombre):
    minx, miny, maxx, maxy = poly.bounds
    w, h = maxx - minx, maxy - miny
    def path(ring):
        return "M " + " L ".join(f"{x - minx:.3f},{maxy - y:.3f}" for x, y in ring.coords) + " Z"
    d = " ".join(path(r) for r in [poly.exterior, *poly.interiors])
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.2f}mm" height="{h:.2f}mm" '
           f'viewBox="0 0 {w:.3f} {h:.3f}"><path d="{d}" fill="none" stroke="#ff0000" '
           f'stroke-width="0.1" fill-rule="evenodd"/></svg>')
    with open(os.path.join(OUT, nombre + ".svg"), "w") as f:
        f.write(svg)


def dibujar(ax, poly, **kw):
    x, y = poly.exterior.xy
    ax.fill(x, y, **kw)
    for r in poly.interiors:
        x, y = r.xy
        ax.fill(x, y, color="white")


def main():
    rot, _ = rotor()
    est, hs = estator(0)
    est_b, _ = estator(180)
    tap, _ = tapa()
    a_dxf(rot, "rotor", ["ROTOR mariposa - aluminio 1 mm - desbarbar y redondear cantos",
                         f"R lobulo {G.r_rotor} mm, cubo R{G.r_hub}, taladro {AGUJERO_M5} (M5)"])
    a_dxf(est, "estator", ["ESTATOR - aluminio 1 mm - cortar 2x(juegos) unidades",
                           f"R int {G.r_stator_int} / R ext {G.r_stator_ext}; varillas M5 a R{G.r_varillas} +-{ANG_VARILLAS} grados"])
    a_dxf(tap, "tapa", ["TAPA / PLACA FINAL - policarbonato o metacrilato 8-10 mm (2 uds)",
                        "Centro 8,2 mm (casquillo o rodamiento 608 con eje 8 mm) / varillas 5,3 / tirantes 6,5"])
    for p, n in ((rot, "rotor"), (est, "estator"), (tap, "tapa")):
        a_svg(p, n)

    # vista previa: máxima y mínima capacidad
    fig, axs = plt.subplots(1, 3, figsize=(15, 5.2))
    for ax, ang, tit in ((axs[0], 0, "Rotor a Cmax (0°)"), (axs[1], 90, "Rotor a Cmin (90°)")):
        dibujar(ax, tap, color="#dde7f0")
        dibujar(ax, est, color="#8a9bb0")
        dibujar(ax, est_b, color="#8a9bb0")
        from shapely import affinity
        dibujar(ax, affinity.rotate(rot, ang, origin=(0, 0)), color="#e39a3b", alpha=0.85)
        ax.set_title(tit); ax.set_aspect("equal"); ax.axis("off")
    dibujar(axs[2], rot, color="#e39a3b")
    dibujar(axs[2], affinity.translate(est, 0, 0), color="#8a9bb0", alpha=0.6)
    axs[2].set_title("Rotor (naranja) y estátor (gris)\ncotas en mm"); axs[2].set_aspect("equal")
    axs[2].grid(alpha=0.3)
    fig.suptitle("Condensador mariposa – vista frontal (estátor A derecha, estátor B izquierda)")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "vista_previa.png"), dpi=130)
    print("Planos generados en", OUT)


if __name__ == "__main__":
    main()
