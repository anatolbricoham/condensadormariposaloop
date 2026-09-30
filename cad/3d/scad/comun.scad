// Utilidades comunes
$fn = 72;
module rrect(w, h, r, t) { linear_extrude(t) offset(r) square([w - 2*r, h - 2*r], center = true); }
// Collar partido con oreja y tornillo de apriete (eje Z). d = diámetro interior
module collar(d, h, pared = 5, oreja = 12, tornillo = 4.5) {
  difference() {
    union() {
      cylinder(d = d + 2*pared, h = h);
      translate([-oreja/2, -(d/2 + pared + oreja - 2), 0]) cube([oreja, oreja + 2, h]);
    }
    translate([0, 0, -1]) cylinder(d = d, h = h + 2);
    translate([-1, -(d/2 + pared + oreja + 1), -1]) cube([2, pared + oreja + 2, h + 2]);   // ranura
    translate([-oreja, -(d/2 + pared + oreja/2 - 1), h/2]) rotate([0, 90, 0]) cylinder(d = tornillo, h = 2*oreja); // tornillo
  }
}
module collar_hueco(d, h, pared = 5) { translate([0, 0, -1]) cylinder(d = d, h = h + 2); }
