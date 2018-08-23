//sAngle1 = 30;
//eAngle1 = 60;
//sAngle2 = 120;
//eAngle2 = 150;
sAngle1 = 22.5;
eAngle1 = 67.5;
sAngle2 = 112.5;
eAngle2 = 157.5;
stA1 = eAngle1-sAngle1;
stA2 = eAngle2-sAngle2;
steps = stA1;

supp = false;
suppExact = false;
LEDDir = 14.5;
OuterDir = 16.5;
InnerDir = 10;
height=3.4;
// Helper
hSp = 0.5;
//inner Helper
//outer helpers
th=0.15;
translate([0,0,10+th])
      difference () {
        cylinder(d1=5.8,d2=5.8,h=height-0.75-th,$fn=360);
        translate([0,0,0]) cylinder(d1=4.75,d2=4.75,h=height-0.75,$fn=360);
};
// Base
difference() {
    cylinder(10, 6, 3, $fn=360);
translate([-0.05,0,1.95]) cube([4.2,24,4.1],center=true);
}
translate([0,0,4])
difference() {
linear_extrude(6) polygon([for ( i = [-1:steps]) (i==-1) ? [0,0] : 
         [OuterDir/2*sin(sAngle1 + i/steps*stA1),OuterDir/2*cos(sAngle1 + i/steps*stA1)]]);
translate([5,5]) 
    rotate(v=[0,0,1], a=45) rotate(v=[1,0,0],a=90) linear_extrude(7,center=true)
        scale([.9,1.666]) circle(3,$fn=360);
}
translate([0,0,4])
difference() {
linear_extrude(6) polygon(
     [for ( i = [-1:steps]) (i==-1) ? [0,0] : 
         [OuterDir/2*sin(sAngle2 + i/steps*stA2),OuterDir/2*cos(sAngle2 + i/steps*stA2)]]);
translate([5,-5]) 
    rotate(v=[0,0,1], a=-45) rotate(v=[1,0,0],a=90) linear_extrude(7,center=true)
        scale([.9,1.666]) circle(3,$fn=360);
}
translate([0,0,4]) rotate(v=[0,0,1],a=180)
difference() {
linear_extrude(6) polygon([for ( i = [-1:steps]) (i==-1) ? [0,0] : 
         [OuterDir/3*sin(sAngle1 + i/steps*stA1),OuterDir/3*cos(sAngle1 + i/steps*stA1)]]);
translate([5,5]) 
    rotate(v=[0,0,1], a=45) rotate(v=[1,0,0],a=90) linear_extrude(7,center=true)
        scale([.9,1.666]) circle(3,$fn=360);
}
translate([0,0,4]) rotate(v=[0,0,1],a=-180)
difference() {
linear_extrude(6) polygon([for ( i = [-1:steps]) (i==-1) ? [0,0] : 
         [OuterDir/3*sin(sAngle2 + i/steps*stA2),OuterDir/3*cos(sAngle2 + i/steps*stA2)]]);
translate([5,-5]) 
    rotate(v=[0,0,1], a=-45) rotate(v=[1,0,0],a=90) linear_extrude(7,center=true)
        scale([.9,1.666]) circle(3,$fn=360);
}

//Side Ring
translate([0,0,9]) linear_extrude(height)
difference() {
    difference() {circle(d=OuterDir,$fn=360); circle(d=LEDDir,$fn=360);};
    translate([-7,0]) square(13,center=true);
    polygon([ [0,0], [(OuterDir+6)/2*sin(eAngle1),(OuterDir+6)/2*cos(eAngle1)], [(OuterDir+6)/2*sin(sAngle2),(OuterDir+6)/2*cos(sAngle2)]]);
}
// Top Ring
translate([0,0,10-1.5+height]) linear_extrude(.75)
difference() {
    difference() {circle(d=OuterDir,$fn=360); circle(d=InnerDir,$fn=360);};
    polygon([ [0,0], [(OuterDir+6)/2*sin(eAngle1),(OuterDir+6)/2*cos(eAngle1)], [(OuterDir+6)/2*sin(sAngle2),(OuterDir+6)/2*cos(sAngle2)]]);
    translate([0,InnerDir/2-0.5]) scale([1,1]) circle(2.5,$fn=90);
    translate([0,-InnerDir/2+0.5]) scale([1,1]) circle(2.5,$fn=90);
    translate([-InnerDir/2+0.5,0]) scale([1,1]) circle(2.5,$fn=90);
    translate([InnerDir/2+0.5,0]) scale([1,1]) circle(2.5,$fn=90);
}
// bottom extension
difference() {
    rotate(v=[0,1,0], a=180) linear_extrude(3,scale=0.8) circle(d=9,$fn=360);
    rotate(v=[0,1,0], a=180) translate([0,0,-2]) linear_extrude(5.01,scale=1) square([3.75,10],center=true);
}