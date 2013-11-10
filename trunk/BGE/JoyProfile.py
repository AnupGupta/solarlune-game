
""""
Module that stores profile input setups for the different joysticks. I only have a couple, but I'll add them.

11/9/13 UPDATE: I've refactored how joystick profiles work. Now, they are objects of classes, rather than
dictionaries. This was done so that it would be easier to work with when you're dealing with IDEs that can
do code intelligence. Now, you can just do:

inp = BGInput.CInputDevice()

jp = JoyProfile.Xbox360

inp.Add('jump', BGInput.JOYBUTTON, jp.A)

"""

class _JP_GameCubeUSB():
	
	"""
	Joystick profile for a GameCube controller connected via a USB adapter.
	Interestingly, the D-Pad can be detected as either buttons (the "Pad" ones below), or a standard Hat hat
	like most other joysticks (the Hat variables).
	
	The triggers are individual axes, unlike the 360's (which show up as a single axis).
	"""
	
	A = 1
	B = 2
	X = 0
	Y = 3
	
	L = 4
	R = 5
	Z = 7
	
	Start = 9
	
	Pad_Up = 12		# D-pad registers as buttons and a hat, for some reason
	Pad_Right = 13
	Pad_Down = 14
	Pad_Left = 15
	
	Hat_Up = 1
	Hat_Right = 2
	Hat_Down = 4
	Hat_Left = 8
	Hat_None = 0
	
	Stick_LeftHori = 0
	Stick_LeftVert = 1
	Stick_RightHori = 2
	Stick_RightVert = 3
	Trigger_Right = 4
	Trigger_Left = 5
	
GamecubeUSB = _JP_GameCubeUSB()

class _JP_PS2USB():
	
	"""
	Joystick profile for a PS2 controller connected via a USB adapter.
	"""
	
	Triangle = 0
	Circle = 1
	Cross = 2
	Square = 3
	
	L2 = 4
	R2 = 5
	L1 = 6
	R1 = 7
	Select = 8
	Start = 9
	L3 = 10
	R3 = 11
	
	Hat_Up = 1
	Hat_Right = 2
	Hat_Down = 4
	Hat_Left = 8
	Hat_None = 0
	
	Stick_LeftHori = 0
	Stick_LeftVert = 1
	Stick_RightHori = 3
	Stick_RightVert = 2
	
PS2USB = _JP_PS2USB

class _JP_Chillstream():
	
	"""
	Joystick profile for a Logitech Chillstream controller.
	"""
	
	Triangle = 3
	Circle = 2
	Cross = 1
	Square = 0
	
	L2 = 6
	R2 = 7
	L1 = 4
	R1 = 5
	Select = 8
	Start = 9
	L3 = 10
	R3 = 11
	
	Hat_Up = 1
	Hat_Right = 2
	Hat_Down = 4
	Hat_Left = 8
	Hat_None = 0
	
	Stick_LeftHori = 0
	Stick_LeftVert = 1
	Stick_RightHori = 2
	Stick_RightVert = 3
	
Chillstream = _JP_Chillstream
	
class _JP_Xbox360():
	
	"""
	Joystick profile for an XBOX 360 or otherwise X-Input controller.
	
	Note that the triggers are implemented as a single axis; the controls don't seem to add up correctly (i.e.
	LT = axis 5 < 0, RT = axis 5 > 0; added together, they approach 0...). There's no alternative way to tell
	which axis is being pressed, either. :1
	
	Note that this should be the profile used for X-Input controllers, even if they aren't XBOX 360 controllers,
	like the Logitech F310.	
	"""
	
	A = 0
	B = 1
	X = 2
	Y = 3
	LB = 4
	RB = 5
	Back = 6
	Start = 7
	LS = 8
	RS = 9
	
	Hat_Up = 1
	Hat_Right = 2
	Hat_Down = 4
	Hat_Left = 8
	Hat_None = 0
	
	Stick_LeftHori = 0
	Stick_LeftVert = 1
	Stick_RightHori = 4
	Stick_RightVert = 3
	
	Triggers = 2

Xbox360 = _JP_Xbox360()
