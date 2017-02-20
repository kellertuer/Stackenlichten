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
eW = 15; //larger ellipse width
// don't change these values
nC = 2*fC+2; //number of Divisions, due to 2fC+1 segments anC one segment that split in the corners
nD = 2*fD;
echo(sin(90));
shortenSide = wW/tan(60)+wW;
sH = 2*(wW/tan(60)+wW/sin(60)); //shorten inner
Expl=-1; //-1: closed, the larger the further apart
// concat with shfted rotated versions... bottom left right

// Generate Top Part
TopPointLine = concat(genSide(),genSide(-120,[sL/4,sL*sqrt(3)/4],0),genSide(120,[-sL/4,sL*sqrt(3)/4],0));
color([.1,.5,.7,.25]) translate([0,0,(Expl+1)/2*wW]) linear_extrude(height=fW, twist=0) polygon(points=TopPointLine);

//Generate one side

color([0,.7,.7]) translate([0,-Expl*wW,0]) rotate(a=-90,v=[1,0,0])
    SLside();

color([.7,0,.7]) translate([-sL/4,sL*sqrt(3)/4,0]) rotate(a=-120,v=[0,0,1])
    translate([0,-Expl*wW,0]) rotate(a=-90,v=[1,0,0])
        SLside();

color([.7,.7,0]) translate([sL/4,sL*sqrt(3)/4,0]) rotate(a=120,v=[0,0,1])
    translate([0,-Expl*wW,0]) rotate(a=-90,v=[1,0,0])
        SLside();

color([0,0,1]) translate([0,0,-3*bD/4-wW/2]) bottomPlate();
color([.3,.3,.3]) translate([0,sL*sqrt(3)/6,-3*bD/4]) cylinder(h=1.001*wW,r=5,$fn=360,center=true);


/* 
 * generate one side
 */
module SLside() { difference() {
    midFC = (fC + 1)/2;
    SidePointLine = concat(genSide(0,[0,0], shortenSide,shortenSide+wW,fW),
    genDepth(0,[sL/2-shortenSide/2-wW,0],[0,0],wW),
    [[sL/2-shortenSide/2,-bD],[-sL/2+shortenSide/2+wW,-bD]],
    -genDepth(0,[sL/2-shortenSide/2-wW,bD],[0,0],wW)   );
  rotate(a=180,v=[1,0,0])
    linear_extrude(height=wW, twist=0) polygon(points=SidePointLine);
  // minus...
  translate([2*sL/nC,bD/2,-wW/2])
    cube(size = [mW,mW,1.02*wW], center = true);
  translate([-2*sL/nC,bD/2,-wW/2])
    cube(size = [mW,mW,1.02*wW], center = true);
  for (i = [1:fC]) {
    translate([-sL/2+2*i*sL/nC,3*bD/4,-wW/2])
      cube(size = [sL/nC,wW,1.02*wW], center = true);
  };
    translate([0,bD,-wW/2]) scale([2,1,1]) cylinder(h=1.001*wW,d=eW/2,$fn=360,center=true);
    translate([0,bD-wW,-wW/2]) cube([wW,2*wW,wW],center=true);
}}
/*
 * Generate bottom plate
 */
module bottomPlate() { difference() {
    linear_extrude(height=wW, twist=0) polygon(points=concat(
            genInnerSide(0,[0,0],sH,sH),
            genInnerSide(-120,[sL/4,sL*sqrt(3)/4],sH,sH),
            genInnerSide(120,[-sL/4,sL*sqrt(3)/4],sH,sH) ));
    translate([0,40-wW/2,wW/2]) cube([pW,pD,1.02*wW], center=true);
    translate([-sL/4,sL*sqrt(3)/4,0]) rotate(a=-120,v=[0,0,1])
        translate([0,40-wW/2,wW/2]) cube([pW,pD,1.02*wW], center=true);
    translate([sL/4,sL*sqrt(3)/4,0]) rotate(a=120,v=[0,0,1])
        translate([0,40-wW/2,wW/2]) cube([pW,pD,1.02*wW], center=true);
}
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