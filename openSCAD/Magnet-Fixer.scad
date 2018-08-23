wW = 4;    // Thickness/Width of wood
mW = 4;    //                 of a Magnet-Cube
fW = 2;    // Thickness of the front plastic plate
sL = 80;   // sidelength of a triangle
bD = 80;   // Depth of a box (depth w.r.t. frontview)
fC = 3;    // number of fingers in the triangle
fD = 4;    // number on fingers downwards
pW = 12; //width of plug inlet
pD = 8; //depth of plug inlet
pS = 40; //shift from baseline of plug inlet
eW = 15; //larger ellipse width
hR=3; //Rounded con
// don't change these values
nC = 2*fC+2; //number of Divisions, due to 2fC+1 segments anC one segment that split in the corners
nD = 2*fD;
shortenSide = wW/tan(60)+wW;
sH = 2*(wW/tan(60)+wW/sin(60)); //shorten inner
Expl=0; //-1: closed, the larger the further apart
fnN = 270;
// concat with shfted rotated versions... bottom left right
/* // Bottom magnets from 
            translate([2*sL/nC,0,0.5])
            cube(size = [mW,mW,1], center = true);
            translate([-2*sL/nC,0,0.5])
            cube(size = [mW,mW,1], center = true);
*/
/* hull() {
   translate([-sL/4-wW/2,-wW/2,0]) circle(wW,$fn=360);
   translate([-sL/4-wW/2,wW/2,0]) circle(wW,$fn=360);
   translate([sL/4+wW/2,-wW/2,0]) circle(wW,$fn=360);
   translate([sL/4+wW/2,wW/2,0]) circle(wW,$fn=360);
};*/
rotate(v=[1,0,0],a=180) union() {

difference() {
translate([0,0,3/4*wW])
    linear_extrude(3*wW/4)
    hull() {
    translate([-sL/4-wW/2,0,0])
    circle(wW,$fn=fnN);
    translate([+sL/4+wW/2,0,0])
    circle(wW,$fn=fnN);
    };
// Magnets
   translate([2*sL/nC,0,wW/2+1])
       cube(size = [1.1*mW,1.1*mW,wW], center = true);
   translate([-2*sL/nC,0,wW/2+1])
       cube(size = [1.1*mW,1.1*mW,wW], center = true);
   translate([0,-7.5])
    scale([2.5,.85,1])
    linear_extrude(2*wW)
    circle(8,$fn=fnN);
}

   # translate([0,0,wW-1.5])
        cube([sL/2-2*wW,.9,1],center=true);
}