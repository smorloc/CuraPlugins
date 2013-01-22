#Name: Change Filament At Z
#Info: Pause the print at a certain height, move to a specified parking location, disable extruder stepper
#Help: ChangeFilamentAtZ
#Depend: GCode
#Type: postprocess
#Param: targetZ(float:5.0) Z height to pause at (mm)
#Param: parkX(float:190) Head park X (mm)
#Param: parkY(float:190) Head park Y (mm)
#Param: parkZ(float:190) Head park Z (mm)
#Param: retractAmount(float:5) Retraction amount (mm)

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
pauseState = 0
with open(filename, "w") as f:
	for line in lines:
		if getValue(line, 'G', None) == 1:
			newZ = getValue(line, 'Z', z)
			x = getValue(line, 'X', x)
			y = getValue(line, 'Y', y)
			if newZ != z:
				z = newZ
				if z < targetZ and pauseState == 0:
					pauseState = 1
				if z >= targetZ and pauseState == 1:
					pauseState = 2
					# Retract
					f.write("M83\n")		# Set E codes relative while in Absolute Coordinates (G90) 
					f.write("G1 E-%f F6000\n" % (retractAmount))
					# Move the head to specified location
					f.write("G1 X%f Y%f Z%f F9000\n" % (parkX, parkY, parkZ))
					# Disable extruder stepper
					f.write("M84 E\n")					
					# Wait until the user continues printing
					f.write("M0\n")
					# Move the head back to printing location
					f.write("G1 X%f Y%f F9000\n" % (x, y))
					f.write("G1 E0 F6000\n")
					f.write("G1 F9000\n")
					f.write("M82\n")		# Set E codes absolute (default) 
		f.write(line)
