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
SideTolerance=0.175; //Shorten fingers (side) to smaller – less than half print with (so for .4 nozzle: .15?)
BottomPlateHoleTolerance = 0.5; //extend holes for bottom plate by...

//lower cable channel:
eW = 8*wW; //larger ellipse width
eH = 4*wW; //ellipse heigt
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


numberStr="3";
fixNumber=false;
type="Number";
//type="Triangle";
//type="Stackenlichten";

//fix global rotation for export
rotate(v=[1,0,0],a=180)
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
            // Magnets
            translate([2*sL/nC,bD/2])
            square(size = [1.1*mW,1.1*mW], center = true);
            translate([-2*sL/nC,bD/2])
            square(size = [1.1*mW,1.1*mW], center = true);
            //Bottom plate holes
            for (i = [1:fC]) {
                translate([-sL/2+2*i*sL/nC,3*bD/4])
                square([sL/nC+BottomPlateHoleTolerance,wW+BottomPlateHoleTolerance], center = true);
            };
        };
    //magnet holes front plates
    translate([2*sL/nC,bD/2,plotTh/2])
        cube(size = [1.1*mW,1.1*mW,plotTh], center = true);
    translate([-2*sL/nC,bD/2,plotTh/2])
        cube(size = [1.1*mW,1.1*mW,plotTh], center = true);
    translate([20,-fW]) linear_extrude(wW)
    polygon(points=[[-5.25,-1],[-5,0],[5,0],[5.25,-1]]);
    translate([0,-fW]) linear_extrude(wW)
    polygon(points=[[-5.25,-1],[-5,0],[5,0],[5.25,-1]]);
    translate([-20,-fW]) linear_extrude(wW)
    polygon(points=[[-5.25,-1],[-5,0],[5,0],[5.25,-1]]);
                //Friction bumps - front deactivated, back
    /* translate([-sL/8,dH,0]) rotate(v=[1,0,0],a=90)
      linear_extrude(dH)
            circle(d=rH,$fn=6);
      translate([3*sL/8,dH,0]) rotate(v=[1,0,0],a=90)
      linear_extrude(dH)
            circle(d=rH,$fn=6);*/
    //Inner bottom - deactivated for ellipse
      translate([sL/8,bD,0]) rotate(v=[1,0,0],a=90)
      linear_extrude(dH)
            circle(d=rH,$fn=6);
      translate([-3*sL/8,bD,0]) rotate(v=[1,0,0],a=90)
      linear_extrude(dH)
            circle(d=rH,$fn=6);
        };
    // emphasize bottom plate holders 
    for (i = [1:fC]) {
        translate([-sL/2+2*i*sL/nC,3*bD/4,0])
        cube([sL/nC+3+BottomPlateHoleTolerance,wW+3+BottomPlateHoleTolerance,4], center = true);
    };
    // cable channel at the bottom
    translate([0,bD,0])
        linear_extrude(3*wW,center=true)
            scale([eW,eH])
            circle(d=1,$fn=360,center=true);
        linear_extrude(3*wW,center=true)
            translate([0,bD-wW]) square([2*wW,4*wW],center=true);

    // magnet fixer
    translate([0,2*bD/4,wW-.4])
       cube([sL/2-2*wW+1.5,1.5,1.2],center=true);
    if (type=="Triangle") {
        translate([0,0,-2*wW/4])
        linear_extrude(height=wW, twist=0)
        translate([0,sL/2+sL*sqrt(3)/16+2,0])
            rotate([0,0,1],a=180)
            scale(0.75)
            difference() {
                polygon(points=PointLine);
                offset(delta=-2.5) polygon(points=PointLine);
            }
        translate([0,0,0*wW/4])
        linear_extrude(height=1.1*wW, twist=0)
        translate([0,sL/2+sL*sqrt(3)/16+2,0])
            rotate([0,0,1],a=180)
            scale(0.75)
            difference() {
                polygon(points=PointLine);
                offset(delta=-2.5) polygon(points=PointLine);
                translate([0,0]) rotate(-30) translate([-3*sL/8,0])
                square([sL/8,bD/2],center=true);
                translate([0,0]) rotate(30) translate([3*sL/8,0])
                square([sL/8,bD/2],center=true);
                translate([8*sL/16,sL/32])
                square([bD/2,sL/8],center=true);
                translate([-8*sL/16,sL/32])
                square([bD/2,sL/8],center=true);
            }
    }
    else
    if (type=="Stackenlichten") {
      lS=4;
      translate([0,0,-0*wW/4])
      linear_extrude(height=1.1*wW, twist=0)
      translate([0,2*sL/8-2-lS])
      rotate(v=[0,1,0], a=180)
      rotate(v=[0,0,1], a=180)
      text("Stacken", font="Pump Triline", valign="center", halign="center", size=15,spacing=1);
      translate([0,0,-0*wW/4])
      linear_extrude(height=1.1*wW, twist=0)
      translate([0,4*sL/8-6-lS])
      rotate(v=[0,1,0], a=180)
      rotate(v=[0,0,1], a=180)
      text("lichten", font="Pump Triline", valign="center", halign="center",size=15,spacing=1);
    }
    else
    if (type=="Number") {
        translate([0,0,-0*wW/4])
        linear_extrude(height=1.1*wW, twist=0)
        translate([0,2.5*sL/8-1])
        rotate(v=[0,1,0], a=180)
        rotate(v=[0,0,1], a=180)
        text(numberStr, font="Pump Triline", valign="center", halign="center",size=24,spacing=1.05);
    };
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
    //Fix numbers
    if (fixNumber)
    translate([0,5.5*sL/16,wW-1/2])
    #    cube([13*sL/16,1,1],center=true);
    if (fixNumber)
    translate([0,3.8*sL/16,wW-1/2])
    #    cube([13*sL/16,1,1],center=true);
    // Fix/Foots
    if (type=="Stackenlichten") {//fix e and i
           translate([16,3.1*sL/16,wW-1/2])
        cube([13*sL/128,1,1],center=true);
    translate([11.5,6.3*sL/16,wW-1/2])
        cube([13*sL/128,1,1],center=true);
    translate([-18,4.9*sL/16,wW-1/2])
        cube([13*sL/128,1,1],center=true);
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
        rotM(a)*(start+[0,-SideTolerance-(2*i+1)*bD/nD])+v, rotM(a)*(start+[h,-SideTolerance-(2*i+1)*bD/nD])+v,
        rotM(a)*(start+[h,SideTolerance-(2*i+2)*bD/nD])+v, rotM(a)*(start+[0,SideTolerance-(2*i+2)*bD/nD])+v
        ]),i+1,a,v,h,start);
/*
 * Small Helpers
 */
function rotM(a) = [[cos(a),sin(a)],[-sin(a),cos(a)]];