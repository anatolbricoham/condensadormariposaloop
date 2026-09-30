// SOPORTE DEL SENSOR HALL A3144 (home = posición de Cmin). Imprimir 1.
include <parametros.scad>
include <comun.scad>
h = altura_eje - 25/2 - 1.5;       // cara del sensor 1,5 mm por debajo del acoplamiento
difference() {
  union() {
    translate([-15, -10, 0]) cube([30, 20, 4]);
    translate([-6, -4, 0]) cube([12, 8, h]);
  }
  translate([-2.3, -1, h - 1.6]) cube([4.6, 10, 1.7]);     // cuerpo TO-92 plano (4,1 x 1,5)
  translate([0, 0, 2]) cylinder(d = 3.5, h = h);          // paso de patillas
  translate([-7, -1.75, 4]) cube([14, 3.5, 8]);           // salida de cables
  for (x = [-10, 10]) translate([x, 0, -1]) cylinder(d = 4.5, h = 6);
}
