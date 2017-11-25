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
rH = 4; //depth of the fix hole
dH = 10; //width and height
plotTh=0.2; //Thickness of plate in front of magnet - one filamentline?
mFn = 90; //Resolution of the spheres
// don't change these values
nC = 2*fC+2; //number of Divisions, due to 2fC+1 segments anC one segment that split in the corners
nD = 2*fD;
shortenSide = wW/tan(60)+wW;
sH = 2*(wW/tan(60)+wW/sin(60)); //shorten inner
Expl=0; //-1: closed, the larger the further apart
// concat with shfted rotated versions... bottom left right


SLside();
translate([sL/2-8,10,0])
cube([16,bD-10,wW/2]);
translate([sL,0,0]) SLside();

translate([1.5*sL-8,10,0])
cube([16,bD-10,wW/2]);
translate([2*sL,0,0]) SLside();

translate([-sL/2-8,10,0])
cube([16,bD-10,wW/2]);
translate([-sL,0,0]) SLside();

translate([-1.5*sL-8,10,0])
cube([16,bD-10,wW/2]);
translate([-2*sL,0,0]) SLside();

translate([sL/2-7,-3,0])
cube([14,13,wW/2]);
translate([-sL/2-7,-3,0])
cube([14,13,wW/2]);
translate([1.5*sL-7,-3,0])
cube([14,13,wW/2]);
translate([-1.5*sL-7,-3,0])
cube([14,13,wW/2]);

    translate([0,-2,-19.5])
    rotate(v=[0,0,1], a=180)
    rotate(v=[1,0,0], a=270)
    linear_extrude(height=1)
    text("Stackenlichten", font="Paddington", valign="center", halign="center",size=45,spacing=1.05);
//    text("Stackenlichten", font="Pump Triline", valign="center", halign="center",size=45,spacing=1.05);
translate([0,-2.5,1])
cube([5*sL,1,2],center=true);

//translate([0,-2.5,-20])
//cube([5*sL,1,40],center=true);

module SLside() {
    PointLine = concat(genSide(),genSide(-120,[sL/4,sL*sqrt(3)/4]),genSide(120,[-sL/4,sL*sqrt(3)/4]));
    difference() {
    union() {
        linear_extrude(height=wW/2, twist=0)
        difference() {
            midFC = (fC + 1)/2;
            SidePointLine = concat(genSide(0,[0,0], shortenSide,shortenSide+wW,fW),
                genDepth(0,[sL/2-shortenSide/2-wW,0],[0,0],0),
                [[sL/2-shortenSide/2,-bD],[-sL/2+shortenSide/2+wW,-bD]],
                -genDepth(0,[sL/2-shortenSide/2-wW,bD],[0,0],0)   );
            rotate(a=180,v=[1,0,0])
            polygon(points=SidePointLine);
        };
    };
    // emphasize bottom plate holders 
    //Friction holes
      translate([sL/8,dH,0]) rotate(v=[1,0,0],a=90)
      linear_extrude(dH+0.4)
            circle(d=rH+.2,$fn=6);
      translate([-3*sL/8,dH,0]) rotate(v=[1,0,0],a=90)
      linear_extrude(dH+0.4)
            circle(d=rH+.2,$fn=6);
      translate([-sL/8,bD,0]) rotate(v=[1,0,0],a=90)
      linear_extrude(dH+0.4)
            circle(d=rH+.2,$fn=6);
      translate([3*sL/8,bD,0]) rotate(v=[1,0,0],a=90)
      linear_extrude(dH+0.4)
            circle(d=rH+.2,$fn=6);
    }
    //Friction bumps
    translate([-sL/8,dH,0]) rotate(v=[1,0,0],a=90)
      linear_extrude(dH)
            circle(d=rH,$fn=6);
      translate([3*sL/8,dH,0]) rotate(v=[1,0,0],a=90)
      linear_extrude(dH)
            circle(d=rH,$fn=6);
      translate([sL/8,bD,0]) rotate(v=[1,0,0],a=90)
      linear_extrude(dH)
            circle(d=rH,$fn=6);
      translate([-3*sL/8,bD,0]) rotate(v=[1,0,0],a=90)
      linear_extrude(dH)
            circle(d=rH,$fn=6);
}

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