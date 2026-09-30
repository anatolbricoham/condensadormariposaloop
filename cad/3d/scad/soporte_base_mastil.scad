// UNIÓN BASE DEL CONDENSADOR <-> MÁSTIL (tubo PVC Ø40). Imprimir 1.
// La placa se atornilla bajo el tablero base; el collar abraza el mástil.
include <parametros.scad>
include <comun.scad>
difference() {
  union() {
    rrect(120, 120, 10, 6);
    collar(d_mastil + 0.5, 55);
  }
  translate([0, 0, -1]) cylinder(d = d_mastil + 0.5, h = 60);
  for (x = [-48, 48]) for (y = [-48, 48]) translate([x, y, -1]) cylinder(d = 5, h = 8);
}
