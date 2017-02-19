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

// don't change these values
nC = 2*fC+2; //number of Divisions, due to 2fC+1 segments anC one segment that split in the corners
nD = 2*fD;
shortenSide = wW/tan(60);
// concat with shfted rotated versions... bottom left right

// Generate Top Part
TopPointLine = concat(genSide(),genSide(-120,[sL/4,sL*sqrt(3)/4],0),genSide(120,[-sL/4,sL*sqrt(3)/4],0));
color([.1,.5,.7,.25]) linear_extrude(height=fW, twist=0) polygon(points=TopPointLine);

//Generate one side
SidePointLine = concat(genSide(0,[0,0], shortenSide,shortenSide+wW,fW),
    genDepth(0,[sL/2-shortenSide/2-wW,0],[0,0],wW),
    [[sL/2-shortenSide/2,-bD],[-sL/2+shortenSide/2+wW,-bD]],
    -genDepth(0,[sL/2-shortenSide/2-wW,bD],[0,0],wW)   );

color([0,.7,.7]) translate([0,wW,0]) rotate(a=90,v=[1,0,0]) linear_extrude(height=wW, twist=0) polygon(points=SidePointLine);
color([.7,0,.7]) translate([-sL/4,sL*sqrt(3)/4,0]) rotate(a=-120,v=[0,0,1]) translate([0,wW,0]) rotate(a=90,v=[1,0,0]) linear_extrude(height=wW, twist=0) polygon(points=SidePointLine);
color([.7,.7,0]) translate([sL/4,sL*sqrt(3)/4,0]) rotate(a=120,v=[0,0,1]) translate([0,wW,0]) rotate(a=90,v=[1,0,0]) linear_extrude(height=wW, twist=0) polygon(points=SidePointLine);

/*
 * Helping Functions - Generate one side of the triangle recursion olé olé
 */
function genSide(a=0,v=[0,0],sLe=0,sRi=0,h=wW) = generateSide([rotM(a)*[-(sL-sLe)/2,0]+v],0,a,v,sLe,sRi,h);   
//Recursively generate fC toothes
function generateSide(pL,i,a,v,sLe,sRi,h) = (i==fC) ? concat(pL,[rotM(a)*[(sL-sRi)/2,0]+v])
    : generateSide(concat(pL,[
        rotM(a)*[-sL/2+(2*i+1.5)*sL/nC,0]+v, rotM(a)*[-sL/2+(2*i+1.5)*sL/nC,h]+v,
        rotM(a)*[-sL/2+(2*i+2.5)*sL/nC,h]+v, rotM(a)*[-sL/2+(2*i+2.5)*sL/nC,0]+v]),i+1,a,v,sLe,sRi,h);
function genDepth(a=0,v=[0,0],start=[0,0],h=wW) = generateDepth([start+v],0,a,v,h,start);
function generateDepth(pL,i,a,v,h,start) = (i==fD) ? pL
    : generateDepth(concat(pL,[
        rotM(a)*(start+[0,-(2*i+1)*bD/nD])+v, rotM(a)*(start+[h,-(2*i+1)*bD/nD])+v,
        rotM(a)*(start+[h,-(2*i+2)*bD/nD])+v, rotM(a)*(start+[0,-(2*i+2)*bD/nD])+v
        ]),i+1,a,v,h,start);
/*
 * Small Helpers
 */
function rotM(a) = [[cos(a),sin(a)],[-sin(a),cos(a)]];