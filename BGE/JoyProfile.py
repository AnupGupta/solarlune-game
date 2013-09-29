
""""
Module that stores profile input setups for the different joysticks. I only have a couple, but I'll add them.

You don't have to make a CJoyProfile object to use it - it's just a container. Use it as you would use a static class in C++ -
refer to the class's attributes, rather than making an object to do so.

For example:

ps2prof = JoyProfile.PS2USB

test = obj['joystate'].ButtonDown(2) 				# Just a number
test = obj['joystate'].ButtonDown(ps2prof['Cross']) # The X button for a PS2 controller

It might seem a little messy to have all values next to each other, but it's generally
easier than having an extra dictionary to separate them.

"""

GCUSB = {		

	'A':1,						# BUTTONS
	'B':2,
	'X':0,
	'Y':3,
	'L':4,
	'R':5,
	'Z':7,
	'Start':9,
	
	'D-Pad-Up':12,					# D-pad registers as button and a POV hat
	'D-Pad-Right':13,
	'D-Pad-Down':14,
	'D-Pad-Left':15,

	'Pov-Up':1,					# Hat values
	'Pov-Up-Right':3,
	'Pov-Right':2,
	'Pov-Right-Down':6,
	'Pov-Down':4,
	'Pov-Left-Down':12,
	'Pov-Left':8,
	'Pov-Left-Up':9,
	'Pov-None':0,

	'LHorizontal':0,			# Analog stick axes
	'LVertical':1,
	'RVertical':2,
	'RHorizontal':3,
	'RTrigger':4,
	'LTrigger':5,

	'AxisRight':1,				# Analog stick directions (for use with AxisDown and other Axis check functions)
	'AxisDown':1,				# Both sticks work the same way, so you can use any of these for either stick.
	}
PS2USB = {		

	'Triangle':0,				# BUTTONS
	'Circle':1,
	'Cross':2,
	'Square':3,
	'L2':4,
	'R2':5,
	'L1':6,
	'R1':7,
	'Select':8,
	'Start':9,
	'L3':10,
	'R3':11,

	'Pov-Up':1,						# Hat values
	'Pov-Up-Right':3,
	'Pov-Right':2,
	'Pov-Right-Down':6,
	'Pov-Down':4,
	'Pov-Left-Down':12,
	'Pov-Left':8,
	'Pov-Left-Up':9,
	'Pov-None':0,

	'LHorizontal':0,			# Analog stick axes
	'LVertical':1,
	'RVertical':2,
	'RHorizontal':3,

	'AxisRight':1,				# Analog stick directions (for use with AxisDown and other Axis check functions)
	'AxisDown':1,				# Both sticks work the same way, so you can use any of these for either stick.
	}
LOGITECHCHILLSTREAM = {
	
	'Triangle':3,				# BUTTONS
	'Circle':2,
	'Cross':1,									
	'Square':0,
	
	'L2':6,
	'R2':7,
	'L1':4,
	'R1':5,
	'Select':8,
	'Start':9,
	'L3':10,
	'R3':11,
	
	'Pov-Up':1,						# Hat values
	'Pov-Up-Right':3,
	'Pov-Right':2,
	'Pov-Right-Down':6,
	'Pov-Down':4,
	'Pov-Left-Down':12,
	'Pov-Left':8,
	'Pov-Left-Up':9,
	'Pov-None':0,
	
	'LHorizontal':0,			# Analog stick axes
	'LVertical':1,
	'RHorizontal':2,
	'RVertical':3,
			
	'AxisRight':1,				# Analog stick directions (for use with AxisDown and other Axis check functions)
	'AxisDown':1,				# Both sticks work the same way, so you can use any of these for either stick.
	
	}

"""
--------------
XBOX 360 NOTES
--------------

Note that the triggers are implemented as a single axis; the controls don't seem to add up correctly (i.e.
LT = axis 5 < 0, RT = axis 5 > 0; added together, they approach 0...). There's no alternative way to tell
which axis is being pressed, either. :1

Note that this should be the profile used for X-Input controllers, even if they aren't XBOX 360 controllers,
like the Logitech F310.		
"""
	
XBOX360 = {
	
	"A":0,					# Buttons and aliases
	"B":1,
	"X":2,
	"Y":3,
	
	"LB":4,
	"RB":5,
	
	"Back":6,
	"Start":7,
	
	"L3":8,
	"R3":9,
	
	"Up":1,					# Hat (D-Pad)
	"Up-Right":3,
	"Right":2,
	"Right-Down":6,
	"Down":4,
	"Down-Left":12,
	"Left":8,
	"Left-Up":9,
	
	"LHorizontal":0,		# Axes
	"LVertical":1,
	"RHorizontal":4,
	"RVertical":3,
	"Triggers":5,
	
	"AxisRight":1,			# Axis directions
	"AxisDown":1,
}
