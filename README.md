xrandr-keystone-helper

This programm helps finding the parameters for xrandr --transform.
Helpfull for e.g. keystone-correction for projektors.

Transformed pictures with "xrandr --tranform" may (very likely) still have some issues espacially around the cursor.
The result could sufficide for viewing movies or presenting slides.

Dependencies:
python 3
numpy
matplotlib

execute:
$python xrandr-keystone-helper.py

adjust the red tetragon/quadrilateral and test the result until you find the right parameters. The string to use with xrandr --transform gets printed to the terminal.
