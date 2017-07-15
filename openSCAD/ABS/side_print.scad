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

number=1;

SLside();

module SLside() {
    PointLine = concat(genSide(),genSide(-120,[sL/4,sL*sqrt(3)/4]),genSide(120,[-sL/4,sL*sqrt(3)/4]));

    difference() {
    union() {
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
            // fist magnet
            translate([2*sL/nC,bD/2])
            square(size = [1.1*mW,1.1*mW], center = true);
            translate([-2*sL/nC,bD/2])
            square(size = [1.1*mW,1.1*mW], center = true);
            translate([0,bD,0]) scale([eW,2*wW])circle(d=1,$fn=360,center=true);
            translate([0,bD-wW]) square([wW,2*wW],center=true);
            for (i = [1:fC]) {
                translate([-sL/2+2*i*sL/nC,3*bD/4])
                square([sL/nC,wW], center = true);
            };
        };
    translate([2*sL/nC,bD/2,0.3])
        cube(size = [1.1*mW,1.1*mW,0.6], center = true);
    translate([-2*sL/nC,bD/2,0.3])
        cube(size = [1.1*mW,1.1*mW,0.6], center = true);
    translate([20,-fW]) linear_extrude(wW)
    polygon(points=[[-5.25,-1],[-5,0],[5,0],[5.25,-1]]);
    translate([0,-fW]) linear_extrude(wW)
    polygon(points=[[-5.25,-1],[-5,0],[5,0],[5.25,-1]]);
    translate([-20,-fW]) linear_extrude(wW)
    polygon(points=[[-5.25,-1],[-5,0],[5,0],[5.25,-1]]);
    };
    // emphasize bottom plate holders 
    for (i = [1:fC]) {
        translate([-sL/2+2*i*sL/nC,3*bD/4,0])
        difference () {
        cube([sL/nC+2.5,wW+2.5,2], center = true);
        }
    };
    // magnet fixer
    translate([0,2*bD/4,wW])
        cube([sL/2-2*wW,1.05,1],center=true);
    translate([0,0,-1*wW/4])
    linear_extrude(height=wW, twist=0)
    translate([0,sL/4])
    rotate(v=[0,1,0], a=180)
    rotate(v=[0,0,1], a=180)
//    text("Stackenlichten", font="Futura:style=Black", valign="center", halign="center",size=6);
    text("Stackenlichten", font="Pump Triline", valign="center", halign="center",size=7.5);
    //Triangle
    translate([0,0,-2*wW/4])
    linear_extrude(height=wW, twist=0)
    translate([0,sL/2+sL*sqrt(3)/16+6.5,0])
            rotate([0,0,1],a=180)
            scale(0.45)
            difference() {
                polygon(points=PointLine);
                offset(delta=-2.5) polygon(points=PointLine);
            }
    translate([0,0,-0*wW/4])
    linear_extrude(height=1.1*wW, twist=0)
    translate([0,sL/2+sL*sqrt(3)/128+5.5])
    rotate(v=[0,1,0], a=180)
    rotate(v=[0,0,1], a=180)
    //text(str(number), font="Futura:style=Black", valign="center", halign="center",size=5);
    text(str(number), font="Pump Triline", valign="center", halign="center",size=6.5);
    }
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