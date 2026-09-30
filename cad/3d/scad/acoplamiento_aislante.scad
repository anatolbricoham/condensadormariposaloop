// ACOPLAMIENTO AISLANTE motor -> eje del rotor (imprimir 1, PETG 100 % relleno)
// Lado A: eje de salida de la reductora (Ø8). Lado B: eje del rotor M5.
// 20 mm de plástico macizo en medio = aislamiento. Alojamiento radial para imán 6x3 mm (home).
include <parametros.scad>
include <comun.scad>
D = 25; L = 60; prof = 20;
module prisionero(z, rb) {   // tornillo M3 radial + hueco para tuerca
  translate([0, 0, z]) rotate([-90, 0, 0]) cylinder(d = 3.2, h = D);
  translate([-5.8/2, rb + 1.5, z - 3]) cube([5.8, 2.8, 30]);
}
difference() {
  cylinder(d = D, h = L);
  translate([0, 0, -1]) cylinder(d = d_eje_motor + 0.2, h = prof + 1);     // motor
  translate([0, 0, L - prof]) cylinder(d = d_eje + 0.2, h = prof + 1);     // rotor
  prisionero(prof / 2, d_eje_motor / 2);
  translate([0, 0, L]) mirror([0, 0, 1]) prisionero(prof / 2, d_eje / 2);
  translate([0, 0, L / 2]) rotate([90, 0, 0]) translate([0, 0, D/2 - 3.3]) cylinder(d = 6.3, h = 4); // imán
}
