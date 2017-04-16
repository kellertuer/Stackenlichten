//sAngle1 = 30;
//eAngle1 = 60;
//sAngle2 = 120;
//eAngle2 = 150;
sAngle1 = 22.5;
eAngle1 = 67.5;
sAngle2 = 112.5;
eAngle2 = 157.5;

LEDDir = 12.5;
OuterDir = 13.5;
InnerDir = 9.5;
height=3;
difference() {
    cylinder(10, 6, 3, $fn=360);
translate([-0.05,0,1.95]) cube([4.2,24,4.1],center=true);
}
translate([0,0,9]) linear_extrude(1) polygon(
    [ [0,0], [OuterDir/2*sin(sAngle1),OuterDir/2*cos(sAngle1)], [OuterDir/2*sin(eAngle1),OuterDir/2*cos(eAngle1)]]);
translate([0,0,9]) linear_extrude(1) polygon(
    [ [0,0], [OuterDir/2*sin(sAngle2),OuterDir/2*cos(sAngle2)], [OuterDir/2*sin(eAngle2),OuterDir/2*cos(eAngle2)]]);
translate([0,0,9]) linear_extrude(height)
difference() {
    difference() {circle(d=OuterDir,$fn=360); circle(d=LEDDir,$fn=360);};
    translate([-7,0]) square(14,center=true);
    polygon([ [0,0], [(OuterDir+6)/2*sin(eAngle1),(OuterDir+6)/2*cos(eAngle1)], [(OuterDir+6)/2*sin(sAngle2),(OuterDir+6)/2*cos(sAngle2)]]);
}
translate([0,0,10-2+height]) linear_extrude(1)
difference() {
    difference() {circle(d=OuterDir,$fn=360); circle(d=InnerDir,$fn=360);};
    polygon([ [0,0], [(OuterDir+6)/2*sin(eAngle1),(OuterDir+6)/2*cos(eAngle1)], [(OuterDir+6)/2*sin(sAngle2),(OuterDir+6)/2*cos(sAngle2)]]);
}
difference() {
    rotate(v=[0,1,0], a=180) linear_extrude(3,scale=0.9) circle(d=8,$fn=360);
    rotate(v=[0,1,0], a=180) translate([0,0,-2]) linear_extrude(5.01,scale=0.85) square([4,9],center=true);
}