/* 
 * Stackenlichten-Files I: The top plate
 *
 * kellertuer, 2017-02-19
 */

/*
 * Variables, all Data in mm
 */
wW      = 4;  // Thickness/Width of wood
mW    = 4;   //                 of a Magnet-Cube
fW     = 3; // Thickness of the front plastic plate
sL = 80;    // sidelength of a triangle
bD = 80;   // Depth of a box (depth w.r.t. frontview)
fC = 3; // number of fingers
// don't change these values
nD = 2*fC+2; //number of Divisions, due to 2fC+1 segments and one segment that split in the corners

// concat with shfted rotated versions... bottom left right

// Generate triangle
PointLine = concat(genSide(),genSide(-120,[sL/4,sL*sqrt(3)/4]),genSide(120,[-sL/4,sL*sqrt(3)/4]));

linear_extrude(height=fW, twist=0)
difference() {
    polygon(points=PointLine);
    translate([0,1.5*wW,0])
        text("k",font="Pump Triline",size=30,halign="center");
};
/* translate([0,sL*sqrt(3)/8,.5])
    #cube([sL/2,1,1],center=true);
/*
 * Helping Functions - Generate one side of the triangle recursion olé olé
 */
function genSide(a=0,v=[0,0]) = generateSide([rotM(a)*[-sL/2,0]+v],0,a,v);   
//Recursively generate fC toothes
function generateSide(pL,i,a,v) = (i==fC) ? concat(pL,[rotM(a)*[sL/2,0]+v])
    : generateSide(concat(pL,[
        rotM(a)*[-sL/2+(2*i+1.5)*sL/nD,0]+v, rotM(a)*[-sL/2+(2*i+1.5)*sL/nD,wW]+v,
        rotM(a)*[-sL/2+(2*i+2.5)*sL/nD,wW]+v, rotM(a)*[-sL/2+(2*i+2.5)*sL/nD,0]+v]),i+1,a,v);
function rotM(a) = [[cos(a),sin(a)],[-sin(a),cos(a)]];