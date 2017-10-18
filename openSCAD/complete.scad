/* 
 * Stackenlichten-Files I: Collect all parts.
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
eW = 15; //larger ellipse width
hR=3; //Rounded con
// don't change these values
nC = 2*fC+2; //number of Divisions, due to 2fC+1 segments anC one segment that split in the corners
nD = 2*fD;
shortenSide = wW/tan(60)+wW;
sH = 2*(wW/tan(60)+wW/sin(60)); //shorten inner
Expl=0; //-1: closed, the larger the further apart
// concat with shfted rotated versions... bottom left right

color([.6,.6,1]) translate([0,0,-3*bD/4-wW/2]) bottomPlate();

/* A pointy hat */
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
color([.6,1,.6])
translate([0,sL*sqrt(3)/6,-3*bD/4-wW/2]) rotate(a=90,v=[0,0,1])
union() {
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
}
//Generate one side

color([0,.7,.7,0]) translate([0,-Expl*wW,0]) rotate(a=-90,v=[1,0,0])
    SLside();

color([.7,0,.7,0]) translate([-sL/4,sL*sqrt(3)/4,0]) rotate(a=-120,v=[0,0,1])
    translate([0,-Expl*wW,0]) rotate(a=-90,v=[1,0,0])
        SLside();

color([.7,.7,0,0]) translate([sL/4,sL*sqrt(3)/4,0]) rotate(a=120,v=[0,0,1])
    translate([0,-Expl*wW,0]) rotate(a=-90,v=[1,0,0])
        SLside();

// Generate Top Part
TopPointLine = concat(genSide(),genSide(-120,[sL/4,sL*sqrt(3)/4],0),genSide(120,[-sL/4,sL*sqrt(3)/4],0));
color([.9,.9,.9,.4]) translate([0,0,(Expl)/2*wW]) linear_extrude(height=fW, twist=0) polygon(points=TopPointLine);


/* 
 * generate one side
 */
module SLside() {
    linear_extrude(height=wW, twist=0)
    difference() {
    midFC = (fC + 1)/2;
    SidePointLine = concat(genSide(0,[0,0], shortenSide,shortenSide+wW,fW),
    genDepth(0,[sL/2-shortenSide/2-wW,0],[0,0],wW),
    [[sL/2-shortenSide/2,-bD],[-sL/2+shortenSide/2+wW,-bD]],
    -genDepth(0,[sL/2-shortenSide/2-wW,bD],[0,0],wW)   );
  rotate(a=180,v=[1,0,0])
  polygon(points=SidePointLine);
  // minus...
  translate([2*sL/nC,bD/2])
    square(size = [mW,mW], center = true);
  translate([-2*sL/nC,bD/2])
    square(size = [mW,mW], center = true);
  for (i = [1:fC]) {
    translate([-sL/2+2*i*sL/nC,3*bD/4])
      square([sL/nC,wW], center = true);
  };
    translate([0,bD,0]) scale([eW,2*wW])circle(d=1,$fn=360,center=true);
    translate([0,bD-wW]) square([wW,2*wW],center=true);
}}

/*
 * Generate bottom plate
 */
module bottomPlate() {
    linear_extrude(height=wW, twist=0)
    difference() {
    polygon(points=concat(
            genInnerSide(0,[0,0],sH,sH),
            genInnerSide(-120,[sL/4,sL*sqrt(3)/4],sH,sH),
            genInnerSide(120,[-sL/4,sL*sqrt(3)/4],sH,sH)
        ));
    translate([0,sL*sqrt(3)/6+8]) hull() {
        translate([-7.5+hR,-6+hR]) circle(r=hR,$fn=360);
        translate([-7.5+hR, 6-hR]) circle(r=hR,$fn=360);
        translate([ 7.5-hR,-6+hR]) circle(r=hR,$fn=360);
        translate([ 7.5-hR, 6-hR]) circle(r=hR,$fn=360);
       };
    translate([0,sL*sqrt(3)/6-7.5]) hull() {
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
function genSide(a=0,v=[0,0],sLe=0,sRi=0,h=wW) = generateSide([rotM(a)*[-(sL-sLe)/2,0]+v],0,a,v,sLe,sRi,h);   
//Recursively generate fC toothes
function generateSide(pL,i,a,v,sLe,sRi,h) = (i==fC) ? concat(pL,[rotM(a)*[(sL-sRi)/2,0]+v])
    : generateSide(concat(pL,[
        rotM(a)*[-sL/2+(2*i+1.5)*sL/nC,0]+v, rotM(a)*[-sL/2+(2*i+1.5)*sL/nC,h]+v,
        rotM(a)*[-sL/2+(2*i+2.5)*sL/nC,h]+v, rotM(a)*[-sL/2+(2*i+2.5)*sL/nC,0]+v]),i+1,a,v,sLe,sRi,h);
/* 
 * generate inner triangle side
 */
function genInnerSide(a=0,v=[0,0],sLe=0,sRi=0,h=wW) = generateInnerSide([rotM(a)*[-(sL-sLe)/2,h]+v],0,a,v,sLe,sRi,h);   
//Recursively generate fC toothes
function generateInnerSide(pL,i,a,v,sLe,sRi,h) = (i==fC) ? concat(pL,[rotM(a)*[(sL-sRi)/2,h]+v])
    : generateInnerSide(concat(pL,[
        rotM(a)*[-sL/2+(2*i+2.5)*sL/nC,h]+v, rotM(a)*[-sL/2+(2*i+2.5)*sL/nC,0]+v,
        rotM(a)*[-sL/2+(2*i+1.5)*sL/nC,0]+v, rotM(a)*[-sL/2+(2*i+1.5)*sL/nC,h]+v
        ]),i+1,a,v,sLe,sRi,h);
/*
 * generate side
 */
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