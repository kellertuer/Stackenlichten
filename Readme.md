# Stackenlichten
<div align="right">by [@kellertuer](https://twitter.com/kellertuer), [@k4sp4r](https://twitter.com/k4sp4r)</div>
<div align="center"><img src="png/logo_light.png" width="300"></div>

## Motivation
The idea of this project is to provide a blueprint for single pixels, that
can be connected via magnets. The data and power supply works via connectors.
The pixels themselves are equilateral triangles, that can easire be used to
stack different forms of Lichten.

## Material
For bulding one of the pixels the following is required
* 6 [Neodyn magnets](http://www.magnetportal.de/wuerfel/neodym-magnet-wuerfel-n45-4mm-1-3kg/a-64/) of size `4x4x4 mm` (0,10 € ab 200 Stk.)
* 1 [connector](https://www.reichelt.de/Molex-Vielfachsteckverbinder/MOLEX-22035035/3/index.html?ACTION=3&LA=446&ARTICLE=185732) (0,14 €)
* 1 [jack](https://www.reichelt.de/Molex-Vielfachsteckverbinder/MOLEX-50375033/3/index.html?ACTION=3&LA=446&ARTICLE=186239) (0,10 €)
* 1 [NeoPixel](https://www.adafruit.com/products/1559) (1,75 €) or any other WS2812 LED having the classical 4 ports +,-,in,out
* 4mm thick wood
* a laser cutter

## Sketches
<div align="center"><img src="png/top.png" width="50%"></div>
Seen from the top, the pixel consists of 3 equal sides. with finger joints of
1cm indicated in cyan (the fingers). The three sides are shortened, such that
the edges don't overlap the triangular shape.
<div align="center"><img src="png/top-plexi.png" width="50%"></div>
The top plate made of plexi glas obtains a shape, that looks quite fance but is
basically just the triangular shape with the fingers of `0.4x1 cm` cut out.
<div align="center"><img src="png/side.png" width="50%"></div>
Each side plate is made with equal fingers for the sides, but for each pixel
two sides sould consists of the same pole pointing outward ([S]outh in the sketch)
and one having the other. This yields South dominated or North dominated pixels,
which should be produced in equal amounts.
<div align="center"><img src="png/bottom.png" width="50%"></div>
The bottom plate is placed 1cm inwards of the sides with 2 bolts for each side.
The magnets should join into the sides by 3/4th (`3 mm`) the top one should be
glued, the bottom one should be held by the bottom plate.

## Wires
Using a 3-pole connectos, the fadecandy board can directly be provided with ground by using the ground of the LEDs. On the other hand at the end of each data line the power supply can be directly connected. If there is a need to
power supply in between, two connectors can be used between two pixels, where
the data line is just passed through and hence both pixels are provided with power.

## KuDos
* [Blinkenlichten](http://blinkenlights.net)
* [Stackenblochen](https://www.youtube.com/watch?v=QEN5-_93gQg)

## TODO
The sketches have to be transformed into laser cutting plans and a layout of
the jacks has to be made for a usual bottom plate (placement of the connector,
  length of the cable to the jack (10cm?).
