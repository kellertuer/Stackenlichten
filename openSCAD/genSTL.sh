#!/bin/bash
echo "--- Stackenlichten Parametric Generator ---"
for i in {1..256}
do
  h=$(( ($i - $i % 100)/100 ))
  t=$(( ($i - $h*100 - $i%10)/10 ))
  o=$(( $i - $h*100 - $t*10 ))
  ht=$(( $h*10+$t ))
  echo "Rendering $i ($h $t $o)"
  FixN="-DfixNumber=false "
  Fix=""
  FixH=""
  if [ $h -eq 8 ]; then
    FixN="-DfixNumber=true "
    FixH="-DuseHFix=true "
  fi
  if ( [ $t -eq 0 ] && [ $h -ne 0 ] ) || [ $t -eq 8 ]; then
    FixN="-DfixNumber=true "
    FixH="-DuseHFix=true "
  fi
  if [ $o -eq 0 ] || [ $o -eq 8 ]; then
    FixN="-DfixNumber=true "
    Fix="-DuseFix=true "
  fi
  #bottom
  if [ $ht -eq 0 ]; then
    /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD -D"number=\"$o\"" $Fix-o stl/bottom$h$t$o.stl bottom_print.scad
  else
    /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD -D"number=\"$o\"" -D"numberHundreds=\"$ht\"" $Fix$FixH-o stl/bottom$h$t$o.stl bottom_print.scad
  fi
  # side
  /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD -D"numberStr=\"$i\"" $FixN-D"type=\"Number\"" -o stl/side_num$h$t$o.stl side_print.scad
done
echo "---Finishing with Sides---"

/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD -D"type=\"Triangle\"" -o stl/side_triangle.stl side_print.scad
/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD -D"type=\"Stackenlichten\"" -o stl/side_stackenlichten.stl side_print.scad
