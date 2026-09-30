// CUNA DEL MOTOR NEMA17 (con o sin reductora planetaria). Imprimir 1 + 1 brida superior.
// El eje queda a la misma altura que el eje del condensador (altura_eje).
include <parametros.scad>
include <comun.scad>
m = 42.3 + 0.6;    // cuerpo NEMA17 + holgura
p = 4; L = 34;     // pared y longitud de agarre
suelo = altura_eje - m / 2;
parte = "cuna";    // "cuna" o "brida"
if (parte == "cuna") {
  difference() {
    union() {
      translate([-45, 0, 0]) cube([90, L, 5]);                                   // pie
      translate([-m/2 - p, 0, 0]) cube([m + 2*p, L, suelo + m]);
    }
    translate([-m/2, -1, suelo]) cube([m, L + 2, m + 1]);                         // hueco del motor
    translate([-12, -1, suelo - 6]) cube([24, L + 2, 7]);                          // paso de cables
    for (x = [-37, 37]) for (y = [8, L - 8]) translate([x, y, -1]) cylinder(d = 4.5, h = 7);
    for (x = [-(m/2 + p/2), m/2 + p/2]) for (y = [7, L - 7])
      translate([x, y, suelo + m - 12]) cylinder(d = 2.8, h = 13);                 // M3 rosca en plástico
  }
} else {
  difference() {
    translate([-m/2 - p, 0, 0]) cube([m + 2*p, L, 4]);
    for (x = [-(m/2 + p/2), m/2 + p/2]) for (y = [7, L - 7]) translate([x, y, -1]) cylinder(d = 3.4, h = 6);
  }
}
