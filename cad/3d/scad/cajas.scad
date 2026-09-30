// CAJAS de la electrónica: controlador y puente de ROE. Seleccionar con 'pieza'.
include <comun.scad>
pieza = "controlador";     // controlador | controlador_tapa | puente | puente_tapa
p = 2.5;
module caja(w, d, h) {
  difference() {
    translate([0, 0, 0]) linear_extrude(h) offset(3) square([w - 6, d - 6], center = true);
    translate([0, 0, p]) linear_extrude(h) offset(3 - p) square([w - 6, d - 6], center = true);
  }
  for (sx = [-1, 1]) for (sy = [-1, 1]) translate([sx * (w/2 - p - 3), sy * (d/2 - p - 3), 0])
    difference() { cylinder(d = 7, h = h); cylinder(d = 2.8, h = h + 1); }
}
module tapa(w, d) {
  difference() {
    linear_extrude(2.5) offset(3) square([w - 6, d - 6], center = true);
    for (sx = [-1, 1]) for (sy = [-1, 1]) translate([sx * (w/2 - p - 3), sy * (d/2 - p - 3), -1]) cylinder(d = 3.4, h = 5);
  }
}
cw = 130; cd = 90; ch = 45;
if (pieza == "controlador") difference() {
  caja(cw, cd, ch);
  // frontal (y = -cd/2): ventana OLED 0,96" + 4 pulsadores 7 mm
  translate([0, -cd/2 - 1, ch - 16]) cube([27, 6, 16], center = true);
  for (x = [-39, -13, 13, 39]) translate([x, -cd/2 - 1, 14]) rotate([-90, 0, 0]) cylinder(d = 7.2, h = 6);
  // trasera: jack DC Ø8, conector GX16 (antena), jack 3,5 mm (puente ROE), USB del ESP32
  translate([-40, cd/2 - 3, 22]) rotate([-90, 0, 0]) cylinder(d = 8.2, h = 6);
  translate([-10, cd/2 - 3, 22]) rotate([-90, 0, 0]) cylinder(d = 16.2, h = 6);
  translate([18, cd/2 - 3, 22]) rotate([-90, 0, 0]) cylinder(d = 6.2, h = 6);
  translate([42, cd/2, 12]) cube([12, 8, 7], center = true);
  // taladros de placa perforada 7x5 cm en el fondo
  for (x = [-33, 33]) for (y = [-23, 23]) translate([x, y, -1]) cylinder(d = 3.2, h = 4);
}
if (pieza == "controlador_tapa") tapa(cw, cd);
pw = 75; pd = 55; ph = 38;
if (pieza == "puente") difference() {
  caja(pw, pd, ph);
  for (s = [-1, 1]) translate([s * (pw/2 - 3), 0, ph/2]) rotate([0, s * 90, 0]) {
    translate([0, 0, -4]) cylinder(d = 16.2, h = 8);
    for (a = [-9.15, 9.15]) for (b = [-9.15, 9.15]) translate([a, b, -4]) cylinder(d = 3.3, h = 8);
  }
  translate([0, pd/2 - 3, ph/2]) rotate([-90, 0, 0]) cylinder(d = 6.2, h = 6);
}
if (pieza == "puente_tapa") tapa(pw, pd);
