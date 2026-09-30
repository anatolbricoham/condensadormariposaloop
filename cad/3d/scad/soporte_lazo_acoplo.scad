// SOPORTE DEL LAZO DE ACOPLO + CONECTOR SO-239 (o N con brida cuadrada 25,4). Imprimir 1.
include <parametros.scad>
include <comun.scad>
h = 30;
difference() {
  union() {
    collar(d_mastil + 0.5, h);
    translate([-10, 0, 0]) cube([20, separacion_loop, h]);
    translate([-30, separacion_loop, 0]) cube([60, 5, 60]);                       // placa del conector
  }
  translate([0, 0, -1]) cylinder(d = d_mastil + 0.5, h = h + 2);
  translate([0, separacion_loop - 1, 38]) rotate([-90, 0, 0]) {
    cylinder(d = 16.2, h = 8);                                                  // cuerpo SO-239
    for (x = [-9.15, 9.15]) for (z = [-9.15, 9.15]) translate([x, z, 0]) cylinder(d = 3.3, h = 8);
  }
  for (x = [-22, 22]) translate([x, separacion_loop - 1, 12]) rotate([-90, 0, 0]) cylinder(d = 7, h = 8); // bridas
}
