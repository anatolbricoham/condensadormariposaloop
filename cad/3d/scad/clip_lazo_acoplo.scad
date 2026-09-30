// CLIP superior del lazo de acoplo al mástil. Imprimir 1 (o 2).
include <parametros.scad>
include <comun.scad>
d_cable = 10.5;   // RG-213 = 10,3 mm ; RG-58 = 5 mm ; tubo cobre 8 mm
h = 15;
difference() {
  union() {
    collar(d_mastil + 0.5, h);
    translate([-6, 0, 0]) cube([12, separacion_loop, h]);
    translate([0, separacion_loop, 0]) cylinder(d = d_cable + 6, h = h);
  }
  translate([0, 0, -1]) cylinder(d = d_mastil + 0.5, h = h + 2);
  translate([0, separacion_loop, -1]) cylinder(d = d_cable, h = h + 2);
  translate([-d_cable * 0.35, separacion_loop, -1]) cube([d_cable * 0.7, 20, h + 2]);   // entrada a presión
}
