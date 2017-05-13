/* 
 * Stackenlichten-Files I: The top plate
 *
 * kellertuer, 2017-02-19
 */

/*
 * Variables, all Data in mm
 */
wW = 4;    // Thickness/Width of wood
sL = 80;   // sidelength of a triangle
// don't change these values
sH = 2*(wW/tan(60)+wW/sin(60)); //shorten inner
    linear_extrude(height=wW/2)
    difference() {
    polygon(points = [ [-sL/2+sH/2,wW],[sL/2-sH/2,wW],[0,(sL-sH+wW)*sqrt(3)/2]]);
    translate([0,sL*sqrt(3)/6]) circle(10,$fn=360);
    }