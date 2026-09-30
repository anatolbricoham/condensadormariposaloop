"""Dibuja los esquemas de conjunto (antena, condensador motorizado y cableado) en docs/img/."""
import math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "img")
os.makedirs(OUT, exist_ok=True)
COBRE, PVC, PLAST, ALU = "#c8742c", "#9fb3c8", "#e39a3b", "#8a9bb0"


def antena(D=1.0):
    P = math.pi * D * 1000; lado = P / 8; R = lado / (2 * math.sin(math.pi / 8))
    ang = [math.radians(22.5 + 45 * i + 90) for i in range(8)]   # lado superior horizontal
    v = [(R * math.cos(a), R * math.sin(a)) for a in ang]
    apo = R * math.cos(math.pi / 8)
    fig, ax = plt.subplots(figsize=(8, 10))
    # mástil
    ax.add_patch(Rectangle((-20, -apo - 900), 40, 2 * apo + 900 + 30, color=PVC, zorder=1))
    # loop (sin el lado superior, donde va el condensador)
    for i in range(8):
        a, b = v[i], v[(i + 1) % 8]
        if abs(a[1] - apo) < 1 and abs(b[1] - apo) < 1:
            for s in (-1, 1):
                ax.plot([s * lado / 2, s * 100], [apo, apo], color=COBRE, lw=7, solid_capstyle="round", zorder=3)
            continue
        ax.plot([a[0], b[0]], [a[1], b[1]], color=COBRE, lw=7, solid_capstyle="round", zorder=3)
    ax.add_patch(FancyBboxPatch((-260, apo + 25), 520, 190, boxstyle="round,pad=4", fc="#f4f4f4", ec="k", zorder=4))
    ax.text(0, apo + 150, "Caja estanca\ncondensador mariposa + motor", ha="center", fontsize=9, zorder=5)
    ax.plot([-100, -80], [apo, apo + 60], color=COBRE, lw=3, zorder=5); ax.plot([100, 80], [apo, apo + 60], color=COBRE, lw=3, zorder=5)
    # lazo de acoplo
    rc = D * 1000 / 10
    ax.add_patch(Circle((0, -apo + rc + 12), rc, fill=False, ec="#2a6f97", lw=3, zorder=4))
    ax.text(rc + 25, -apo + rc, f"Lazo de acoplo\nØ {2*rc:.0f} mm (coaxial)", fontsize=9, color="#2a6f97")
    ax.add_patch(Rectangle((-30, -apo - 60), 60, 45, color=PLAST, zorder=5))
    ax.text(40, -apo - 50, "SO-239 (soporte_lazo_acoplo)", fontsize=8)
    for y, t in ((-apo, "cruceta_mastil_tubo"), (apo * 0.1, "")):
        if t:
            ax.add_patch(Rectangle((-35, y - 20), 70, 40, color=PLAST, zorder=6)); ax.text(-300, y - 70, t, fontsize=8)
    ax.add_patch(Rectangle((-35, -rc * 0.2 - apo + 2 * rc + 12), 70, 16, color=PLAST, zorder=6))
    ax.text(-360, -apo + 2 * rc + 30, "clip_lazo_acoplo", fontsize=8)
    # cotas
    ax.annotate("", (-R - 60, -apo), (-R - 60, apo), arrowprops=dict(arrowstyle="<->"))
    ax.text(-R - 80, 0, f"{2*apo:.0f} mm", rotation=90, va="center", ha="right")
    ax.annotate("", (-lado / 2, -apo - 120), (lado / 2, -apo - 120), arrowprops=dict(arrowstyle="<->"))
    ax.text(0, -apo - 185, f"lado = {lado:.0f} mm  (8 tramos, perímetro {P:.0f} mm)", ha="center")
    ax.text(40, -apo - 500, "Mástil PVC Ø40\n(no metálico dentro del loop)", fontsize=9)
    ax.text(0, apo + 280, f"Loop magnético octogonal Ø {D} m – tubo de cobre 22 mm", ha="center", fontsize=13, weight="bold")
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-R - 250, R + 350); ax.set_ylim(-apo - 950, apo + 330)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "antena_conjunto.png"), dpi=120); plt.close(fig)


def condensador(pack=190):
    fig, ax = plt.subplots(figsize=(13, 4.6))
    x = 0
    ax.add_patch(Rectangle((-60, -12), pack + 2 * 22 + 2 * 10 + 60 + 300, 12, color="#b08b5b"))   # base
    ax.text(0, -30, "Tablero base (contrachapado marino / PVC espumado 10–12 mm) ≈ 500 × 180 mm", fontsize=9)
    # tapas
    for xt in (0, 10 + 12 + pack + 12):
        ax.add_patch(Rectangle((xt, 0), 10, 150, color=PLAST))
    ax.add_patch(Rectangle((-40, 0), 40, 6, color=PLAST)); ax.add_patch(Rectangle((10 + 24 + pack + 10, 0), 40, 6, color=PLAST))
    # placas
    n = 22; s = 9
    for i in range(n):
        xp = 10 + 12 + i * s
        ax.add_patch(Rectangle((xp, 75 + 16), 1.2, 60, color=ALU)); ax.add_patch(Rectangle((xp, 75 - 76), 1.2, 60, color=ALU))
    for i in range(n - 1):
        xp = 10 + 12 + i * s + 4.5
        ax.add_patch(Rectangle((xp, 75 - 70), 1.2, 140, color=COBRE, alpha=0.8))
    xe = 10 + 24 + pack + 10
    ax.plot([-15, xe + 5], [75, 75], color="k", lw=2)            # eje
    ax.plot([-15, xe + 5], [75 + 46, 75 + 46], color="#555", lw=1.5, ls="--"); ax.text(xe + 8, 75 + 46, "varillas M5 estátor", fontsize=7, va="center")
    ax.text(pack / 2 + 20, 175, f"Paquete {pack} mm – 22 juegos, separador 9 mm (hueco 4 mm)", ha="center")
    # acoplamiento + motor
    ax.add_patch(Rectangle((xe + 5, 62.5), 60, 25, color="#6aa84f")); ax.text(xe + 10, 95, "acoplamiento\naislante", fontsize=8)
    ax.add_patch(Circle((xe + 35, 62.5), 3, color="k"))
    ax.add_patch(Rectangle((xe + 25, 0), 20, 58, color=PLAST)); ax.text(xe + 27, 20, "Hall", fontsize=7, rotation=90)
    ax.add_patch(Rectangle((xe + 65, 55), 40, 40, color="#666")); ax.text(xe + 66, 100, "reductora\n27:1", fontsize=8)
    ax.add_patch(Rectangle((xe + 105, 54), 42, 42, color="#333"))
    ax.add_patch(Rectangle((xe + 100, 0), 55, 54, color=PLAST)); ax.text(xe + 110, 110, "NEMA17", fontsize=8)
    ax.text(-45, 158, "tapa ×2", fontsize=8)
    ax.text(-50, 75 + 52, "estátor A", fontsize=8, ha="right"); ax.text(-50, 75 - 52, "estátor B", fontsize=8, ha="right")
    ax.text(20, 75 + 3, "rotor (eje M5, 625ZZ)", fontsize=8)
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-160, xe + 200); ax.set_ylim(-45, 195)
    ax.set_title("Condensador mariposa motorizado – vista lateral (versión B)")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "condensador_motorizado.png"), dpi=120); plt.close(fig)


def cableado():
    fig, ax = plt.subplots(figsize=(13, 7))
    def caja(x, y, w, h, t, c="#eef3f8"):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02", fc=c, ec="k")); ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=9)
    caja(0, 4, 2.2, 1.2, "Transceptor HF")
    caja(3.2, 4, 2.2, 1.2, "Puente de ROE\n(tipo Bruene, FT50-43)")
    caja(3.2, 1.2, 2.6, 2.0, "ESP32 DevKit\n+ OLED 0,96\"\n+ 4 pulsadores", "#fde9cf")
    caja(6.6, 1.2, 1.8, 1.2, "TMC2209\n(1/16)", "#fde9cf")
    caja(0, 1.4, 2.2, 1.0, "Fuente 12 V 2 A\n+ LM2596 → 5 V", "#e6f2e6")
    caja(10, 4, 2.6, 1.2, "Lazo de acoplo\n(en la antena)", "#dfeaf5")
    caja(10, 1.2, 2.6, 1.6, "NEMA17 + reductora\n+ Hall A3144\n(en la antena)", "#dfeaf5")
    ax.add_patch(Rectangle((-0.2, 0.6), 9.8, 5.0, fill=False, ls="--", ec="#888")); ax.text(-0.1, 5.7, "Cuarto de radio", color="#888"); ax.text(10, 5.7, "Antena (exterior)", color="#888")
    def flecha(a, b, t="", c="k"):
        ax.annotate("", b, a, arrowprops=dict(arrowstyle="-", lw=2, color=c)); ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 0.12, t, ha="center", fontsize=8, color=c)
    flecha((2.2, 4.6), (3.2, 4.6), "coax", "#2a6f97")
    flecha((5.4, 4.6), (10, 4.6), "coax RG-213 + chokes de ferrita", "#2a6f97")
    flecha((4.3, 4.0), (4.3, 3.2)); ax.text(4.4, 3.55, "FWD / REF / GND (jack 3,5)", fontsize=8, color="#b3261e")
    flecha((5.8, 1.8), (6.6, 1.8)); ax.text(6.2, 0.95, "STEP 25 · DIR 26 · EN 27", fontsize=8, ha="center")
    flecha((8.4, 1.8), (10, 1.8), c="#6a3d9a"); ax.text(9.2, 2.05, "cable 8 hilos (GX16-8)\nA1 A2 B1 B2 · 5V · GND · HALL", fontsize=8, ha="center", color="#6a3d9a")
    flecha((2.2, 1.9), (3.2, 1.9), "12 V / 5 V", "#2e7d32")
    ax.set_xlim(-0.3, 13); ax.set_ylim(0.3, 6); ax.axis("off")
    ax.set_title("Diagrama de conexiones del autoajuste")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, "cableado.png"), dpi=120); plt.close(fig)


if __name__ == "__main__":
    antena(); condensador(); cableado(); print("Esquemas en", os.path.abspath(OUT))
