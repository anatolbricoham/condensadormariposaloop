// TAPA DEL CONDENSADOR (imprimir 2). PETG/ASA, 5 perímetros, 40 % gyroid.
// Imprimir tumbada tal cual (cara interior sobre la cama). El pie sirve para atornillarla a la base.
include <parametros.scad>
include <comun.scad>
W = 210; H = 150; T = 10; R = 8;
pie_prof = 40; pie_t = 6;
difference() {
  union() {
    rrect(W, H, R, T);
    translate([-W/2 + R, -H/2, 0]) cube([W - 2*R, pie_t, T + pie_prof]);            // pie
    for (x = [-50, 0, 50]) translate([x - 2.5, -H/2 + pie_t, T])                       // cartelas
      rotate([90, 0, 90]) linear_extrude(5) polygon([[0,0],[30,0],[0,pie_prof - 4]]);
  }
  // eje: alojamiento de rodamiento 625ZZ (5x16x5) por la cara exterior + paso
  translate([0, 0, -1]) cylinder(d = 6.5, h = T + 2);
  translate([0, 0, T - rodamiento_h]) cylinder(d = rodamiento_d, h = rodamiento_h + 1);
  // varillas M5 de los estátores
  for (s = [-1, 1]) for (a = [-ang_varillas, ang_varillas])
    translate([s * r_varillas * cos(a), r_varillas * sin(a), -1]) cylinder(d = 5.4, h = T + 2);
  // tirantes M6 de nylon/fibra
  for (x = [-95, 95]) for (y = [-60, 60]) translate([x, y, -1]) cylinder(d = 6.5, h = T + 2);
  // taladros del pie para fijar a la base (tornillo M4 de nylon o inox lejos del rotor)
  for (x = [-85, -25, 25, 85]) translate([x, -H/2 - 1, T + pie_prof/2 + 3]) rotate([-90, 0, 0]) cylinder(d = 4.5, h = pie_t + 2);
  // rebaje para aligerar (fuera de las zonas de varillas)
  translate([0, 45, T - 3]) linear_extrude(4) offset(4) square([60, 20], center = true);
}
