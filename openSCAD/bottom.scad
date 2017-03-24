/* 
 * Stackenlichten-Files I: The top plate
 *
 * kellertuer, 2017-02-19
 */

/*
 * Variables, all Data in mm
 */
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
// don't change these values
nC = 2*fC+2; //number of Divisions, due to 2fC+1 segments and one segment that split in the corners
sH = 2*(wW/tan(60)+wW/sin(60)); //shorten inner

// concat with shfted rotated versions... bottom left right

bottomPlate();
//color([.3,.3,.3]) translate([0,sL*sqrt(3)/6,]) circle(r=5,$fn=360,center=true);
hR = 3;
module bottomPlate() {
    linear_extrude(height=wW, twist=0)
    difference() {
    polygon(points=concat(
            genInnerSide(0,[0,0],sH,sH),
            genInnerSide(-120,[sL/4,sL*sqrt(3)/4],sH,sH),
            genInnerSide(120,[-sL/4,sL*sqrt(3)/4],sH,sH)
        ));
    translate([0,sL*sqrt(3)/6+7]) hull() {
        translate([-7.5+hR,-5+hR]) circle(r=hR,$fn=360);
        translate([-7.5+hR, 5-hR]) circle(r=hR,$fn=360);
        translate([ 7.5-hR,-5+hR]) circle(r=hR,$fn=360);
        translate([ 7.5-hR, 5-hR]) circle(r=hR,$fn=360);
       };
    translate([0,sL*sqrt(3)/6-7]) hull() {
        translate([-7.5+hR,-5+hR]) circle(r=hR,$fn=360);
        translate([-7.5+hR, 5-hR]) circle(r=hR,$fn=360);
        translate([ 7.5-hR,-5+hR]) circle(r=hR,$fn=360);
        translate([ 7.5-hR, 5-hR]) circle(r=hR,$fn=360);
    };
};
};

/*
 * Helping Functions - Generate one side of the triangle recursion olé olé
 */
function genInnerSide(a=0,v=[0,0],sLe=0,sRi=0,h=wW) = generateInnerSide([rotM(a)*[-(sL-sLe)/2,h]+v],0,a,v,sLe,sRi,h);   
//Recursively generate fC toothes
function generateInnerSide(pL,i,a,v,sLe,sRi,h) = (i==fC) ? concat(pL,[rotM(a)*[(sL-sRi)/2,h]+v])
    : generateInnerSide(concat(pL,[
        rotM(a)*[-sL/2+(2*i+2.5)*sL/nC,h]+v, rotM(a)*[-sL/2+(2*i+2.5)*sL/nC,0]+v,
        rotM(a)*[-sL/2+(2*i+1.5)*sL/nC,0]+v, rotM(a)*[-sL/2+(2*i+1.5)*sL/nC,h]+v
        ]),i+1,a,v,sLe,sRi,h);
function rotM(a) = [[cos(a),sin(a)],[-sin(a),cos(a)]];