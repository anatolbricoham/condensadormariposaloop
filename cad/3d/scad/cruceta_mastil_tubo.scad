// CRUCETA: sujeta el tubo de cobre del loop (Ø22) al mástil (Ø40). Imprimir 2.
// El plano del loop queda desplazado 'separacion_loop' mm del eje del mástil.
include <parametros.scad>
include <comun.scad>
h = 40;
difference() {
  union() {
    collar(d_mastil + 0.5, h);
    translate([-h/2, 0, 0]) cube([h, separacion_loop, h]);                         // puente
    translate([0, separacion_loop, h/2]) rotate([0, 90, 0]) cylinder(d = d_tubo + 10, h = h, center = true);
    translate([-10, separacion_loop, h/2]) cube([20, d_tubo/2 + 16, h/2]);          // oreja tubo
  }
  translate([0, 0, -1]) cylinder(d = d_mastil + 0.5, h = h + 2);
  translate([0, separacion_loop, h/2]) rotate([0, 90, 0]) cylinder(d = d_tubo + 0.3, h = h + 2, center = true);
  translate([-h, separacion_loop - 1, h/2]) cube([2*h, 2, h]);                     // ranura del tubo
  translate([0, separacion_loop + d_tubo/2 + 9, h/2 + 10]) rotate([0, 90, 0]) cylinder(d = 4.5, h = 30, center = true);
}
