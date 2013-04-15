
""""
Module that stores profile input setups for the different joysticks. I only have a couple, but I'll add them.

You don't have to make a CJoyProfile object to use it - it's just a container. Use it as you would use a static class in C++ -
refer to the class's attributes, rather than making an object to do so.

For example:

ps2prof = BGHelper.CJoyProfile.PS2USB

test = obj['joystate'].ButtonDown(2) 				# Just a number
test = obj['joystate'].ButtonDown(ps2prof['Cross']) # The X button for a PS2 controller

It might seem a little messy to have all values next to each other, but it's generally
easier than having an extra dictionary to separate them.

"""
		
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

	'Up':1,						# Hat values
	'Up-Right':3,
	'Right':2,
	'Right-Down':6,
	'Down':4,
	'Left-Down':12,
	'Left':8,
	'Left-Up':9,
	'None':0,

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
	
	'Up':1,						# Hat values
	'Up-Right':3,
	'Right':2,
	'Right-Down':6,
	'Down':4,
	'Left-Down':12,
	'Left':8,
	'Left-Up':9,
	'None':0,
	
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
LT = axis 2 < 0, RT = axis 2 > 0; added together, they approach 0...). There's no alternative way to tell
which axis is being pressed, either. :1

Note that this should be the profile used for X-Input controllers, even if they aren't XBOX 360 controllers,
like the Logitech F310.		
"""
	
XBOX360 = {
	
	"A":0,					# Buttons and aliases
	"Cross":0,
	
	"B":1,
	"Circle":1,
	
	"X":2,
	"Square":2,
	
	"Y":3,
	"Triangle":3,
	
	"LB":4,
	"L1":4,
	
	"RB":5,
	"R1":5,
	
	"Back":6,
	"Select":6,
	
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