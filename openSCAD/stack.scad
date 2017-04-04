wW = 4;
wL = 3;
linear_extrude(4)
polygon( [
    [-0.975*wW,wW],[-1.025*wW,wL*wW],
    [-2*wW,wL*wW],[-2*wW,0],[2*wW,0],
    [2*wW,wL*wW],[1.025*wW,wL*wW],
    [0.975*wW,wW]]);