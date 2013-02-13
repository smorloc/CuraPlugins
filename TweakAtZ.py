#Name: Tweak At Z
#Info: Change printing parameters at a given height
#Help: TweakAtZ
#Depend: GCode
#Type: postprocess
#Param: targetZ(float:5.0) Z height to tweak at (mm)
#Param: speed(int:) New Speed (%)
#Param: extruderOne(int:) New Extruder 1 Temp (deg C)
#Param: extruderTwo(int:) New Extruder 2 Temp (deg C)
#Param: extruderThree(int:) New Extruder 3 Temp (deg C)

## Written by Steven Morlock, smorloc@gmail.com
## This script is licensed under the Creative Commons - Attribution - Share Alike (CC BY-SA) terms

# Uses -
# M220 S<factor in percent> - set speed factor override percentage
# M104 S<temp> T<0-#toolheads> - set extruder <T> to target temperature <S>

# TODO:
# M140 S<temp> - set bed target temperature

import re

def getValue(line, key, default = None):
	if not key in line or (';' in line and line.find(key) > line.find(';')):
		return default
	subPart = line[line.find(key) + 1:]
	m = re.search('^[0-9]+\.?[0-9]*', subPart)
	if m == None:
		return default
	try:
		return float(m.group(0))
	except:
		return default

with open(filename, "r") as f:
	lines = f.readlines()

z = 0
x = 0
y = 0
state = 0
with open(filename, "w") as f:
	for line in lines:
		if getValue(line, 'G', None) == 1:
			newZ = getValue(line, 'Z', z)
			x = getValue(line, 'X', x)
			y = getValue(line, 'Y', y)
			if newZ != z:
				z = newZ
				if z < targetZ and state == 0:
					state = 1
				if z >= targetZ and state == 1:
					state = 2
					f.write("; Plugin: start TweakAtZ\n")
					if speed is not None and speed != '':
						f.write("M220 S%f\n" % float(speed))
					if extruderOne is not None and extruderOne != '':
						f.write("M104 S%f T0\n" % float(extruderOne))
					if extruderTwo is not None and extruderTwo != '':
						f.write("M104 S%f T1\n" % float(extruderTwo))
					if extruderThree is not None and extruderThree != '':
						f.write("M104 S%f T2\n" % float(extruderThree))					
					f.write("; Plugin: end TweakAtZ\n")
		f.write(line)
