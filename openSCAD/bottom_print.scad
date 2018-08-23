/* 
 * Stackenlichten-Files I: The top plate
 *
 * kellertuer, 2017-02-19
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

number="9";
useFix=false;
numberHundreds="";
useHFix=false;
//fix global rotation for export
rotate(v=[0,1,0],a=180)
union(){
bottomPlate();
tN= 4;
dist = 3.75;
translate([-1*dist,44.625,-3*wW/4])
    linear_extrude(3*wW/4,scale=[2/tN,1])
    square([tN,10],center=true);
translate([dist,44.625,-3*wW/4])
    linear_extrude(3*wW/4,scale=[2/tN,1])
    square([tN,10],center=true);

translate([16,15-dist,-3/4*wW])
rotate(v=[0,0,1],a=90)
    linear_extrude(3*wW/4,scale=[2/tN,1])
    square([tN,10],center=true);
translate([16,15+dist,-3/4*wW])
rotate(v=[0,0,1],a=90)
    linear_extrude(3*wW/4,scale=[2/tN,1])
    square([tN,10],center=true);

translate([-16,15-dist,-3/4*wW])
rotate(v=[0,0,1],a=90)
    linear_extrude(3*wW/4,scale=[2/tN,1])
    square([tN,10],center=true);
translate([-16,15+dist,-3/4*wW])
rotate(v=[0,0,1],a=90)
    linear_extrude(3*wW/4,scale=[2/tN,1])
    square([tN,10],center=true);
}
module bottomPlate() {
    difference() {
    linear_extrude(height=wW, twist=0)
    difference() {
    polygon(points=concat(
            genInnerSide(0,[0,0],sH,sH),
            genInnerSide(-120,[sL/4,sL*sqrt(3)/4],sH,sH),
            genInnerSide(120,[-sL/4,sL*sqrt(3)/4],sH,sH)
        ));
     translate([0,sL*sqrt(3)/6+7.5]) hull() {
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
    translate([1,4.2,-0*wW/4])
    linear_extrude(1.1*wW)
    rotate(v=[0,1,0],a=180)
    text("@kellertuer",font="Vollkorn",size=8.5,halign="center");
    translate([-13.5,27,-0*wW/4])
    linear_extrude(1.2*wW)
    rotate(v=[0,1,0],a=180)
    text(str(number), font="Pump Triline", valign="center", halign="center",size=14);
    translate([13.5,27,-0*wW/4])
    linear_extrude(1.2*wW)
    rotate(v=[0,1,0],a=180)
    text(str(numberHundreds), font="Pump Triline", valign="center", halign="center",size=14);
    };
    // Fix numbers
    translate([-8,38,wW-wW/16])
    rotate(v=[0,0,1],a=60)
    if (useFix)
        difference() {
            cube([40,3.9,wW/8],center=true);
            cube([40,1.5,wW/4],center=true);
        }
    if (useHFix)
        translate([8,38,wW-wW/16])
        rotate(v=[0,0,1],a=-60)
        difference() {
            cube([40,3.9,wW/8],center=true);
            cube([40,1.5,wW/4],center=true);
        }
    translate([0,8,wW-wW/16])
        cube([60,1,wW/8],center=true);
};

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
 * Small Helpers
 */
function rotM(a) = [[cos(a),sin(a)],[-sin(a),cos(a)]];