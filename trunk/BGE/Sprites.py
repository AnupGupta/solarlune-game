##
##~~~~~~~~SPRITES.PY~~~~~~~~
##
## Author: SolarLune
##
## Date Updated: 7/30/12
##
##
##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##
## License Agreement: This script may be used in any project for
## commercial, educational, personal, or any purpose
## as long as you attribute the author with the creation of the script.
##
## You may NOT sell the script.
##
## This license may not be rewritten, altered, or deleted under any circumstance.
## You may otherwise alter or distribute the script, as long as the deritive work
## has the same license agreement.
##
## This license agreement is known as the Creative Commons CC BY-SA 3.0 license.
##
## For more information, check it out here:
##
## http://creativecommons.org/licenses/by-sa/3.0/
##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##
##
##
## 		This script is written for use in the Blender
## Game Engine. All you have to do to install it into
## an object is create an Always sensor with 0 pulse
## setting (necessary for correct time calculation)
## and set the always sensor to a controller set to a simple script
## that sets the animation. That is all that is necessary to run it;
## To see the benefit, though, you must also UV-map said object
## object to a sprite image on a sprite sheet.
##
## To define an animation for use in the Sprite() function, use the following format:
##
## anim = [0, 0, 1, 2, 3, 2]
##
## In the format above, the animation is defined as a list, and the
## numbers indicate how the animation plays. The first number is the
## sprite cell column to be drawn using the UV-map you set for the
## sprite object earlier. The remaining numbers are used to define
## which frame to play, and when. In the above example, first, frame 0
## would display, then 1, then 2, then 3, and finally, 2 again. After this,
## the animation repeats. 

## To define an animation for use in the SpriteMesh() function, use the following format:

## anim = ['MarkWalk', 0, 1, 2, 3, 4, 5]

## In the format above, the animation is again defined as a list. However, in this
## animation format, the first value is the base name of the mesh to swap out to achieve
## animation - the first mesh used would be 'MarkWalk0', and then 'MarkWalk1', and so on.
## Name meshes in a hidden layer after these frames, and the animation will play through.
## There's an example present in the blend files that come with this script.

## To set the object's animation to an animation, use
## the obj['currentanim'] variable to set the object's currently displayed
## animation to another defined animation. For example:
##
## obj['spranim'] = anim
##
## Would set the object's currently displayed animation to the anim variable,
## which has already been defined above. That is it; Note that the object
## for the sprite will only display the sprite on the FIRST face.

## After defining and setting an animation, run the matching sprite function, and that's it:

## Sprite(obj) # Note that obj can be omitted, as it will
## assume that you mean the object if you don't define which one in particular.

## NOTE that you don't have to call SpriteInit(), as the animation functions will call it when necessary.

## Here are the variables to manipulate the sprite with

## (note that they are accessed using obj['variablename']:
##
## sprsubimage
##
## Indicates which frame of the animation the sprite is showing - note that in
## the example animation [0, 1, 5, 9], if subimage = 2, then the current frame
## drawing is 5. To set the subimage of a animation directly, simply set the variable.
##
## sprpastsubimage
##
## Indicates which frame of the animation was last drawn (one script-run ago).
## This would be the past game frame if the frequency of the script was 0 (every
## game frame).
## 
## sprfps
##
## Indicates how quickly the animation should advance (how many
## frames per second for the animation).
##
## sprflipx / sprflipy
##
## Indicates whether the sprite should be flipped on the
## X-axis (left-to-right), or the Y-axis (top-to-bottom). Note that when
## SpriteMesh is used, this physically flips the sprite around on the Z-axis,
## while if the Sprite function is used, then the UV-maps are flipped.
##
## sprrotate
##
## Rotates the sprite around on the local Y-axis 
##
## spractiveface and spractivemesh
##
## activeface tells which face to animate for the active mesh indicated
## by none other than activemesh
##
## ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##
## This script can be used by anyone for any purpose,
## including commercial use (selling a product with this script in use
## or distributed within), educational use (teaching others
## using this script), and individual use (using it for one's own,
## non-commercial projects).
##

## CHANGE-LOG

## 10/15/11 - Fixed some incorrect width-setting code in the SpriteInit() function. :P

## 11/13/11 - Deleted the 'sprwait' variable; now only the sprsubimage variable is used, and it's expressed in fractions... Marvelous.
## However, this makes changing subimages as easy as pie! Just use the sprsubimage variable.

## 1/10/12 - Documentation and stuff.

import mathutils
from bge import logic
import math

def SpriteInit(spriteobj = None, override = 0):

	"""
	Initializes the values for sprite animation; you can alter these values as you wish, though
	it would be best not to alter certain values (sprvert, sprw or sprh (they get their values from the UV-map info), or sprfreqorig).
	
	You can override the initialization process to ensure that it is initialized on a given frame, regardless of whether it has been
	initialized or not, as well, by setting override to 1.
	
	
	
	*NOTE*: It's not necessary to call this function yourself, as the sprite animation functions below (Sprite and SpriteMesh) already
	call them as necessary (once when the sprite needs to be animated).	
	
	
	
	Object variables created are:
	
	spranim = Animation array
	sprfps = How many frames to display a second
	sprflipx, sprflipy = Flipping the sprite on the respective axes using the object's orientation matrix.
	
	sprrotate = Rotation of the sprite in radians (around, on the local Y-axis). Doesn't get added to the sprite's original rotation.
	Also, note that this doesn't work with Halo-enabled faces; they always face 'downwards'. To fix this, rotate the frame in 
	Blender before game play. 
	For example, if rotate = math.pi, then the sprite should rotate 180 degrees around, so that it's upside down and facing left.
	
	sprcamoptimize = Whether to slow down the connected sensor's frequency if the sprite goes out of frame
	sprfpslock = Whether to lock the sprite's animation speed to the logic tic rate (the target FPS) or rather 
	synchronize to the game's actual FPS rate; defaults to locking the animation rate to the actual game FPS
	
	sprsubimage = Which frame of the sprite to display. Initialized to 1.
	sprpastsubimage = The last frame of the sprite that was displayed the last time this function was run.
	
	This function's arguments:
	
	spriteobj = Which object to initialize sprite variables on
	override = Defaults to 0; if set to 1, then the sprite values will be created or set, regardless of whether it happened already or not.
	
	"""

	cont = logic.getCurrentController()
	
	if spriteobj == None:
		obj = cont.owner
	else:
		obj = spriteobj

	if not 'sprinit' in obj or override > 0:
	
		obj['sprinit'] = 1
		
		if not 'sprmat' in obj:
			obj['sprmat'] = 0	# Active material for the sprite; 0 = first material
		if not 'sprmesh' in obj:
			obj['sprmesh'] = 0	# Active mesh of the active material for the sprite; 0 = first mesh of 'sprmat' material
				
		obj['sprvert'] = [None, None, None, None]

		for a in range(4):
			obj['sprvert'][a] = obj.meshes[obj['sprmat']].getVertex(obj['sprmesh'],a)	# The sprite object's vertices; was used only by the Sprite() function, but it was
			# unreliable to change the UV values every frame (for some reason, the BGE would disconnect the reference; I think it has something to do with
			# the image assigned to the mesh). So, the Sprite function just gets the first four vertices of the mesh - note that if you want more faces, you shuold use the
			# SpriteMesh function.

		vertex = obj['sprvert']	
			
		if not 'sprw' in obj:
			obj['sprw'] = abs(vertex[0].getUV()[0] - vertex[2].getUV()[0])
			obj['sprh'] = abs(vertex[0].getUV()[1] - vertex[2].getUV()[1])
			obj['sprori'] = obj.orientation.to_euler()	# Original orientation of the sprite object; used in case of rotation
		
		if not 'sprsubimage' in obj:
			obj['sprsubimage'] = 1.000	# The subimage of the sprite; fractioned because you're setting the individual frames, but only whole changes actually matterchanging this changes 
			
		if not 'sprpastsubimage' in obj:
			obj['sprpastsubimage'] = 1.000
		
		if not 'sprflipx' in obj:
			obj['sprflipx'] = 0
		if not 'sprflipy' in obj:
			obj['sprflipy'] = 0
		if not 'sprrotate' in obj:
			obj['sprrotate'] = None
		
		if not 'spranim' in obj:
			obj['spranim'] = None
		if not 'sprfps' in obj:
			obj['sprfps'] = 10.0
			
		if not 'sprfreqorig' in obj:
			obj['sprfreqorig'] = cont.sensors[0].frequency
		
		if not 'sprcamoptimize' in obj:
			obj['sprcamoptimize'] = 0
			
		if not 'sprfpslock' in obj:
			obj['sprfpslock'] = 1		# Default to polling the game's FPS, rather than going by the logic tic rate

def Sprite(spriteobj = None):

	"""
	Animates the UV-coordinates of the object specified (or the object that the function is performed on) to draw a sprite.
	
	The average animation looks like:
	[0, 0, 1, 2, 3]
	Where the first value is the position of the animation's column, and the later ones are the frame numbers (going upwards)
	
	The only argument for this function is:
	
	spriteobj = Which sprite's UV-mesh to change; None or omitted = this object
	"""
	
	sce = logic.getCurrentScene()
	cam = sce.active_camera

	cont = logic.getCurrentController()
		
	if spriteobj == None:
		obj = cont.owner
	else:
		obj = spriteobj
	
	frequency = cont.sensors[0].frequency + 1

	try:
	
		#obj['anim'] = [0, 0, 1, 0, 3]		# A test animation using the first column of the spritesheet, with the first, second, and fourth sprite sheet cells being used

		if obj['sprcamoptimize']:					# Optimization where if the sprite isn't on screen, it won't update every frame
			if cam.pointInsideFrustum(obj.position):
				cont.sensors[0].frequency = obj['sprfreqorig']
			else:
				cont.sensors[0].frequency = obj['sprfreqorig'] + 5
		
		if obj['sprfpslock'] == 0:					# Without FPS Locking on, the sprite will attempt to speed up when the game slows down and vise versa.
			fps = logic.getAverageFrameRate()
			if fps == 0.0:						# At the game engine's initializing, getAverageFrameRate may return 0.0 because it samples the FPS over some time
				fps = logic.getLogicTicRate()

		else:									# With FPS Locking on, the sprite will animate regardless of FPS changes.
			fps = logic.getLogicTicRate()

		## I'll generally only use exact squares (e.g. 4 64x64 subimages on a 256x256 image),
		## but I've decided to go with both a width and height variable for uneven images.
		## The number for each is obtained by dividing one by the total number of sprite
		## frames available on the sprite sheet (the same either way to equal a square
		## sheet). For example, if you can fit 4 images on a 64x64 image, and each
		## sprite is equal-sized and takes up the most space, then you would end up with
		## even 32x32 images, or images whose sizes equal 0.5 each way.

		sprfps = obj['sprfps'] / fps

		anim = obj['spranim']
		
		if anim != None:
			
			obj['sprpastsubimage'] = obj['sprsubimage']
			
			if obj['sprfps'] != 0.0:	# If spritefps == 0, don't advance the subimage
				obj['sprsubimage'] += round(sprfps, 2) * frequency	# GameLogic's logic tic rate is constant, but if FPS drops below the tic rate, the animations won't adjust

			if math.floor(obj['sprsubimage']) > len(anim) - 1:
				if obj['sprfps'] > 0:
					while obj['sprsubimage'] > (len(anim) - 1):
						obj['sprsubimage'] -= (len(anim) - 1)
				else:
					obj['sprsubimage'] = 1.0	

			elif math.floor(obj['sprsubimage']) < 1.0:	# Hack that makes sure the subimage is never looking at the animation column for a frame
				if obj['sprfps'] > 0:
					obj['sprsubimage'] = 1.0		# Shouldn't really ever happen that the subimage is going up, but somehow goes below 0; if it does, just set it to a healthy 1.
				else:
					while obj['sprsubimage'] < (len(anim) - 1):
						obj['sprsubimage'] += (len(anim) - 1)	
						
			if obj['sprsubimage'] < 1.0:
				obj['sprsubimage'] = 1.0
			if obj['sprsubimage'] > len(anim):
				obj['sprsubimage'] = len(anim) - 1

			subi = math.floor(obj['sprsubimage'])
			
			## This below is pretty much the only way to get the info from the vertices
			## When viewing a plane so that the sprite appears straight on:
			## Vertex 0 = Top-Right
			## Vertex 1 = Top-Left
			## Vertex 2 = Bottom-Left
			## Vertex 3 = Bottom-Right
			## I believe this has to do with culling, which apparently takes place 
			## counter-clockwise here (?)

			vertex = [None, None, None, None]
			for a in range(4):
				vertex[a] = obj.meshes[obj['sprmat']].getVertex(obj['sprmesh'],a)	# The sprite object's vertices; used only by the Sprite() function
			
			if obj['sprflipx'] == 0 and obj['sprflipy'] == 0:
				vertex[0].setUV([obj['sprw'] + (obj['sprw'] * anim[0]),obj['sprh'] + (obj['sprh'] * anim[subi])])
				vertex[1].setUV([obj['sprw'] * anim[0],obj['sprh'] + (obj['sprh'] * anim[subi])])
				vertex[2].setUV([obj['sprw'] * anim[0],obj['sprh'] * anim[subi]])
				vertex[3].setUV([obj['sprw'] + (obj['sprw'] * anim[0]),obj['sprh'] * anim[subi]])
			elif obj['sprflipx'] == 0 and obj['sprflipy'] == 1:
				vertex[3].setUV([obj['sprw'] + (obj['sprw'] * anim[0]),obj['sprh'] + (obj['sprh'] * anim[subi])])
				vertex[2].setUV([obj['sprw'] * anim[0],obj['sprh'] + (obj['sprh'] * anim[subi])])
				vertex[1].setUV([obj['sprw'] * anim[0],obj['sprh'] * anim[subi]])
				vertex[0].setUV([obj['sprw'] + (obj['sprw'] * anim[0]),obj['sprh'] * anim[subi]])
			elif obj['sprflipx'] == 1 and obj['sprflipy'] == 0:
				vertex[1].setUV([obj['sprw'] + (obj['sprw'] * anim[0]),obj['sprh'] + (obj['sprh'] * anim[subi])])
				vertex[0].setUV([obj['sprw'] * anim[0],obj['sprh'] + (obj['sprh'] * anim[subi])])
				vertex[3].setUV([obj['sprw'] * anim[0],obj['sprh'] * anim[subi]])
				vertex[2].setUV([obj['sprw'] + (obj['sprw'] * anim[0]),obj['sprh'] * anim[subi]])
			else:
				vertex[2].setUV([obj['sprw'] + (obj['sprw'] * anim[0]),obj['sprh'] + (obj['sprh'] * anim[subi])])
				vertex[3].setUV([obj['sprw'] * anim[0],obj['sprh'] + (obj['sprh'] * anim[subi])])
				vertex[0].setUV([obj['sprw'] * anim[0],obj['sprh'] * anim[subi]])
				vertex[1].setUV([obj['sprw'] + (obj['sprw'] * anim[0]),obj['sprh'] * anim[subi]])
			
			if obj['sprrotate'] != None:					# If you don't set the rotate value, then you're saying that you'll handle it.
				ori = obj['sprori'].copy()
				ori.y += obj['sprrotate']
				obj.orientation = ori
	
	except KeyError:	# Initialize the sprite object if it hasn't been initialized
		SpriteInit(obj)
			
def SpriteMesh(spriteobj = None):

	"""
		Replaces the mesh of the object specified (or the object that the function is performed on) to draw a sprite.
		The average sprite replacement animation looks like:
		['Explosion', 0, 1, 2, 3]
		Where the first value is the name of the mesh to replace for the sprite, and the later values are the image numbers
		(going upwards), where each individual sprite mesh is named the first value, then a later one. An example would be that the
		first sprite of an explosion would be named 'Explosion0'.
	
		If the sprite seems to be animating slowly (not on time), it's probably because the Rasterizer is working extra hard to change the meshes.
		You can see this in the profiler.
		To fix this, ensure no modifiers are present on the mesh frames to replace.
		Also, if there's a slight lag between switching sprites, this is because the sprite frames have a lot of polygons, and so loading them into
		and out of memory is slowing the BGE down. To fix this, place the sprites somewhere in the game scene to keep them around in memory.
		
		See SpriteInit function for possible object variables to change.
		
		The only argument for this function is:
		
		spriteobj = Which sprite's UV-mesh to change; None or omitted = this object
	"""

	from bge import logic
	import math
	
	sce = logic.getCurrentScene()
	cam = sce.active_camera

	cont = logic.getCurrentController()
	
	if spriteobj == None:
		obj = cont.owner
	else:
		obj = spriteobj
	
	if spriteobj == None:
		obj = cont.owner
	else:
		obj = spriteobj
		
	frequency = cont.sensors[0].frequency + 1

	try:
		
		if obj['sprcamoptimize']:					# Optimization where if the sprite isn't on screen, it won't update every frame
			if cam.pointInsideFrustum(obj.position):
				cont.sensors[0].frequency = obj['sprfreqorig']
			else:
				cont.sensors[0].frequency = obj['sprfreqorig'] + 5
		
		if obj['sprfpslock'] == 0:					# Without FPS Locking on, the sprite will attempt to speed up when the game slows down and vise versa.
			fps = logic.getAverageFrameRate()
			if fps == 0.0:						# At the game engine's initializing, getAverageFrameRate may return 0.0 because it samples the FPS over some time
				fps = logic.getLogicTicRate()

		else:									# With FPS Locking on, the sprite will animate regardless of FPS changes.
			fps = logic.getLogicTicRate()

		## I'll generally only use exact squares (e.g. 4 64x64 subimages on a 256x256 image),
		## but I've decided to go with both a width and height variable for uneven images.
		## The number for each is obtained by dividing one by the total number of sprite
		## frames available on the sprite sheet (the same either way to equal a square
		## sheet). For example, if you can fit 4 images on a 64x64 image, and each
		## sprite is equal-sized and takes up the most space, then you would end up with
		## even 32x32 images, or images whose sizes equal 0.5 each way.

		sprfps = obj['sprfps'] / fps

		anim = obj['spranim']
		
		if anim != None and len(anim) > 1:
		
			obj['sprpastsubimage'] = obj['sprsubimage']
			
			if obj['sprfps'] != 0.0:	# If spritefps == 0, don't advance the subimage
				obj['sprsubimage'] += round(sprfps, 2) * frequency	# GameLogic's logic tic rate is constant, but if FPS drops below the tic rate, the animations will adjust

			if math.floor(obj['sprsubimage']) > len(anim) - 1:				
				if obj['sprfps'] > 0:
					while obj['sprsubimage'] > (len(anim) - 1):
						obj['sprsubimage'] -= (len(anim) - 1)
				else:
					obj['sprsubimage'] = 1.0	
			
			elif math.floor(obj['sprsubimage']) < 1.0:	# Hack that makes sure the subimage is never looking at the animation column for a frame
				if obj['sprfps'] > 0:
					obj['sprsubimage'] = 1.0		# Shouldn't really ever happen that the subimage is going up, but somehow goes below 0; if it does, just set it to a healthy 1.
				else:
					while obj['sprsubimage'] < (len(anim) - 1):
						obj['sprsubimage'] += (len(anim) - 1)	

			if obj['sprsubimage'] < 1.0:
				obj['sprsubimage'] = 1.0
			if obj['sprsubimage'] > len(anim):
				obj['sprsubimage'] = len(anim) - 1
				
			subi = math.floor(obj['sprsubimage'])
		
			frame = anim[0] + str( anim[subi] )
			
			if str(obj.meshes[0]) != frame:	# Only replace the mesh if the object's current mesh isn't equal to the one to use (if it's equal, then the mesh was replaced earlier)
			
				obj.replaceMesh(frame)

			ori = obj.worldOrientation.to_euler()
			
			if obj['sprflipx']:
				ori.z += math.pi
				
			if obj['sprflipy']:
				ori.x += math.pi
			
			if obj['sprrotate'] != None:					# If you set the rotate value, then you're saying that you'll handle it, so be aware of that
				ori.y += obj['sprrotate']

			obj.worldOrientation = ori
	
	except KeyError:	# Initialize the sprite object if it hasn't been initialized
	
		SpriteInit(obj)
