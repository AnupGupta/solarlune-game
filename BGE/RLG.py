###########################
# Random Level Generation #
# V1.1					  #
###########################

# Author : SolarLune
# Date Updated: 9/27/11

# This resource and the functions below are released under something similar to Creative Commons licensing;
# You may use it for any work, commercial or otherwise, as long as you credit the original author (SolarLune).
# 
# By using this script or any part thereof, you agree to this license agreement.
#
# You may NOT edit this license agreement.
#

from bge import logic

import random, math, mathutils

GN_CONNECTION_STYLE_ONE = 0 # Connection styles for the GenNodes function; ONE = all nodes connect to another one (other than themselves) randomly
GN_CONNECTION_STYLE_ALL = 1 # ALL = Each node makes a connect to every other node
GN_CONNECTION_STYLE_HUB = 2 # HUB = Each node connects to a pre-determined node (like a spiderweb)

#### Helper Functions ####

def GetDimensions(object, roundit = 3, mesh = None):

	"""
	Gets the dimensions of the object (what you see under dimensions in the properties window in the 3D menu).
	object = which object to use; note that it will by default use the first mesh; you can specify which mesh by providing the mesh
	via the mesh property.
	roundit = how far down to round the returned dimension values; set it to a negative number to not round the numbers off at all.
	"""

	s = object.worldScale
	
	if mesh == None:	
		mesh = object.meshes[0]

	#print (dir(mesh))
	
	verts = [[], [], []]
	
	for v in range(mesh.getVertexArrayLength(0)):
	
		vert = mesh.getVertex(0, v)
		
		pos = vert.getXYZ()
		
		verts[0].append(pos[0])
		verts[1].append(pos[1])
		verts[2].append(pos[2])
	
	verts[0].sort()
	verts[1].sort()
	verts[2].sort()

	if roundit >= 0:
		size = [
		round( (verts[0][len(verts[0]) - 1] - verts[0][0]) * s[0] , roundit), 
		round( (verts[1][len(verts[0]) - 1] - verts[1][0]) * s[1] , roundit), 
		round( (verts[2][len(verts[0]) - 1] - verts[2][0]) * s[2] , roundit) ]
	else:
		size = [(verts[0][len(verts[0]) - 1] - verts[0][0]) * s[0], 
		(verts[1][len(verts[0]) - 1] - verts[1][0]) * s[1], 
		(verts[2][len(verts[0]) - 1] - verts[2][0]) * s[2]]
		
	#print (size)
	
	return (size)

def GetSurroundingCells(room, celly, cellx):

	"""
	
	Author : SolarLune
	Date Updated : 6/24/11
	
	Gets the surrounding cells from the room array supplied.
	
	room = Room array
	celly, cellx = cell co-ordinates to check around

	Y'know, wrapping around the map would be possible, too - you'd just have
	to check for that case.
	"""
	
	if cellx > 0:
		left = room[celly][cellx - 1]
	else:
		left = 0
		
	if cellx < len(room[celly]) - 1:
		right = room[celly][cellx + 1]
	else:
		right = 0
		
	if celly > 0:
		up = room[celly - 1][cellx]
	else:
		up = 0
		
	if celly < len(room) - 1:
		down = room[celly + 1][cellx]
	else:
		down = 0
	
	#print (down)
		
	cells = [left, right, up, down]
	
	num = len(cells) - cells.count(0)

	return [[left, right, up, down], num]

def Clamp(value, minimum, maximum):
	"""
	Clamp: Clamps the specified 'value' between the maximum and minimum values.
	Returns 'max' when 'value' is greater than 'max', 'min' when 'value' is less than 'min',
	and 'value' itself when neither is true.	
	"""
	return (min(max(value, minimum), maximum))

# ~~~~ Generation Functions ~~~~~
	
def GenGrowth(xsize = 9, ysize = 9, maxnum = 0, randseed = None, mustconnect = 1, maxcon = 0, roomtypes = [1], roomlist = None):

	"""
	
		2D RANDOM ROOM GENERATOR
		
		Author: SolarLune
		Date Updated: 6/24/11
		
		xsize = X-size of the randomly generated room
		
		ysize = Y-size of the randomly generated room
		
		Note that if you use an even number, then there's no middle cell, so you can't be exactly sure which cell WILL be filled.
		
		maxnum = Maximum number of rooms; by default will make half of the total rooms populated (i.e. 5x5 = 25 / 2 = ~13)
		
		randseed = Random seed value; this will (hopefully) make it so that each randomly generated map can be the same with a specific seed
		
		maxcon = Maximum connections each room can have. Hallways can only have one other connection, 
		for example, and the default is 0, which is as many as possible (yes, hallways actually have two, 
		but each hallway thinks it's the last one, basically)
			
		roomtypes = Room types (for example, you might want some rooms to be sand, others rock, etc.); basically, the
		generation will contain random selections of these numbers. So, if you wanted a map of sand, grass, and concrete,
		you could make a list of three numbers, and replace those numbers with the correct values later on
		
		roomlist = A previous room list (maybe you have a list that you got and want to add on values, or change the theme by using the same seed
		as before and using different 'roomtypes'. Beware - ensuring that the roomlist is the correct size is up to you.
	"""

	currentnum = 0

	if roomlist == None:
	
		room = []
		
		for y in range(ysize):					# Create empty rooms
			room.append([])
			for x in range(xsize):
				room[y].append(0)
	else:
		
		room = roomlist[:]
		
		roomnumbers = 0
		
		for x in room:							# Add number of occupied rooms (not 0)
			
			currentnum += x.count(not 0)
			
		#print ([x.count(0) for x in room[:]]) 
		#print ('----')
	
	#### CELL GENERATION ####
	
	randomstate = random.getstate() 					# Used to preserve random settings before using the function
	
	random.seed(randseed)								# Set the seed, if there is one

	if mustconnect:
	
		middley = math.floor(ysize / 2.0)			# Set the middle cell to be filled
		middlex = math.floor(xsize / 2.0)
		room[middley][middlex] = random.choice(roomtypes)
		
		currentnum += 1
	
	if maxnum > 0:
		maxsize = maxnum
	else:
		maxsize = (xsize * ysize) / 2
	
	rlgpass = 0										# Failsafe

	while (currentnum < maxsize):
	
		rlgpass += 1
		if rlgpass > 100000:						# If the number of passes exceeds a certain amount, it breaks out; unnecessary now
			currentnum = maxsize
			break
	
		randomy = math.floor(random.random() * ysize)			# Choose a random cell
		randomx = math.floor(random.random() * xsize)
		
		if room[randomy][randomx] == 0:				# Don't set a cell more than once
		
			if mustconnect:
			
				sur = GetSurroundingCells(room, randomy, randomx)
				
				cellaround = 0						# If there's a connection around the current cell
				
				#print (sur)
				
				for cell in sur[0]:
					if cell != 0 and cell != None:
						cellaround = 1				# If there's another cell surrounding this one that isn't 0 or None
				
				if sur[1] > maxcon and maxcon > 0:
					pass
			
				elif cellaround:
					room[randomy][randomx] = random.choice(roomtypes)
					currentnum += 1
				
			else:
				room[randomy][randomx] = random.choice(roomtypes)
				currentnum += 1
				
	random.setstate(randomstate)	# Reset random settings

	#print ('Room:')
	
	#for y in room:		# Quickie room debug
	#	print (y)
		
	return room

def GenNodes(xsize = 9, ysize = 9, nodecount = 0, spacing = 1,
			 randseed = None, nodetypes = [2], halltypes=[1], emptytypes = [0],
			 straight_halls = False,
			 connection_style = GN_CONNECTION_STYLE_ONE, roomlist = None):
	
	"""
	
	This method of random generation spawns several nodes, and then connects those nodes with halls.
	
	x, ysize = size of the generated list
	
	nodecount = number of nodes to spawn; defaults to 0, which is half of the width of the room.
	
	spacing = spawn nodes with a minimum number of >spacing< blank nodes between them (both x and y axes individually).
	An example would be a node at [4, 4] and another one at [18, 5]. If spacing == 1, then that won't work, since
	5 - 4 = 1 node difference.
	if spacing == 0 (default), distance has no bearing on where nodes are spawned
	
	Note! If spacing is too large and the room has too small a size, it will basically be tried for, but otherwise
	the room will generate however it can. Use small spacing amounts and large rooms.
	
	randseed = random seed for spawning the same list each time
	
	nodetypes = a list of different (randomly chosen) numbers that can spawn for the nodes separating halls
	
	halltypes = a list of different (randomly chosen) numbers that can spawn for the halls in-between nodes
	
	emptytypes = a list of different (randomly chosen) numbers that can spawn for the non-hall or node spots
	
	straight_halls = determines if the hallways basically only bend once max, or if they "stair-step" between nodes
	
	connection_style = determines how the nodes connect to each other.
	
	GN_CONNECTION_STYLE_ONE = All nodes each connect to one other randomly chosen node
	(this will result in the map being connected correctly, of course)
	
	GN_CONNECTION_STYLE_ALL = All nodes connect to each other. For an example, think of a square with four points -
	each point connects	to the three other points.
	
	GN_CONNECTION_STYLE_HUB = All nodes connect to one other node specifically; i.e., if you have 10 nodes, one
	node will connect to all other nodes, and every other node will only connect to the previous one
		
	roomlist = preexisting list to use
	"""
						
	if roomlist != None:
		
		maplist = roomlist
		middle = [xsize//2, ysize//2]
		
		ysize = len(maplist)
		xsize = len(maplist[0])
		
	else:
		
		maplist = []
		
		for j in range(ysize):
			
			maplist.append([])
			
			for i in range(xsize):
				
				maplist[j].append(random.choice(emptytypes))
		
		#maplist = [[random.choice(emptytypes) for j in range(xsize)] for i in range(ysize)]
	
		middle = [xsize//2, ysize//2]

	randomstate = random.getstate()
	
	random.seed(randseed)
		
	#maplist[middle[1]][middle[0]] = random.choice(
		
	nodelist = 	[]	# List of nodes
	toconnect = {}	# List of nodes that are still up for connections and their connection counts
		
	if nodecount == 0:
		ndc = int(xsize / 2)
	else:
		ndc = nodecount
	
	if roomlist:
		
		list_node_count = 0
		
		for c in range(len(roomlist)):
			for x in range(len(roomlist[c])):
				if roomlist[c][x] in nodetypes:
					
					node = (c,x)
					nodelist.append(node)
					toconnect[node] = []
					
					list_node_count += 1
		
		ndc -= list_node_count
				
	for n in range(ndc):	# Generate nodes
		
		node = None
		
		if spacing <= 0:
		
			while (node == None):
							
				cy = random.choice(range(len(maplist)))
				cx = random.choice(range(len(maplist[cy])))
							
				if maplist[cy][cx] == 0:
					node = (cy, cx)
				
					nodelist.append(node)
					toconnect[node] = [] # What nodes the node is connected to
				
		else:
			
			for dist in range(spacing+1, -1, -1):					# If you can't find a node at the specified minimum distance, then search at a closer distance

				for i in range(1000):							# Set a limit so that it doesn't hang the game :/
								
					cy = random.choice(range(len(maplist)))
					cx = random.choice(range(len(maplist[cy])))
							
					if maplist[cy][cx] in emptytypes:
						node = (cy, cx)

						for other in nodelist:
							if other != node:
								
								diffx = abs(node[1] - other[1])
								diffy = abs(node[0] - other[0])
																							
								if diffx < dist or diffy < dist:	# Discard the node placement if it's too close to another node
									node = None						# And find another node placement (in the same 100x for loop above)
									break		

					if node != None:
						nodelist.append(node)
						toconnect[node] = []
						break
				
				if node != None:
					break

		maplist[node[0]][node[1]] = random.choice(nodetypes)
	
	if nodecount == 1:
		print ("ERROR: nodecount needs to be larger than 1")
		return
			
	for node in list(toconnect.keys()):					# Connect nodes
		
		destnode = None
						
		while destnode == None:							# Find a destination node
			
			if len(toconnect[node]) >= len(toconnect.keys()) - 1: # Connected to all available nodes
				
				break
			
			else:
				
				if connection_style == GN_CONNECTION_STYLE_ONE:
					connection_list = [random.choice(list(toconnect.keys()))] # Changes with connection_style
				elif connection_style == GN_CONNECTION_STYLE_ALL:
					connection_list = [c for c in toconnect.keys()]#[random.choice(list(toconnect.keys()))] # Changes with connection_style
				elif connection_style == GN_CONNECTION_STYLE_HUB:
					connection_list = [list(toconnect.keys())[0]]
				
					if connection_list[0] == node:
						
						break	 # Break out of the while loop

				for dn in connection_list:
					
					if dn != node and not dn in toconnect[node]:
								
						destnode = dn
					
						diff = mathutils.Vector(dn) -  mathutils.Vector(node)
						
						if straight_halls:
							
							target = list(node)
						
						else:
							
							target = mathutils.Vector(node)
							axis_x = 1
						
						#for x in range(10000):				# Can make a 10000 unit path
						for x in range(50):				# Can make a 10000 unit path
								
							if straight_halls:
												
								if destnode[0] > target[0]:
									target[0] += 1
								elif destnode[0] < target[0]:
									target[0] -= 1
								elif destnode[1] > target[1]:
									target[1] += 1
								elif destnode[1] < target[1]:
									target[1] -= 1
								
							else:
								
								axis_x = not axis_x
								
								if axis_x:
									target.x += diff.normalized().x
								else:
									target.y += diff.normalized().y
								
							target_rnd = (int(Clamp(round(target[0]), 0, xsize - 1)),
										  int(Clamp(round(target[1]), 0, ysize - 1)))
						
							if target_rnd == destnode:#target_floor == destnode or target_ceil == destnode:									# Destination
								
								maplist[destnode[0]][destnode[1]] = random.choice(nodetypes) # Make sure we didn't overwrite it
								maplist[node[0]][node[1]] = random.choice(nodetypes)
								
								toconnect[tuple(node)].append(destnode)
								toconnect[tuple(destnode)].append(node)
								
								break
							
							else:
								
								if maplist[target_rnd[0]][target_rnd[1]] in emptytypes: # Not occupied
									maplist[target_rnd[0]][target_rnd[1]] = random.choice(halltypes)
								
	random.setstate(randomstate)
	
	return (maplist)

##### Map population functions #####

def Populate(roomlist, room4way, roomstraight, roomend, roomcorner, roommiddle, roomceiling = None, roomsize = [2.0, 2.0, 0.0], point = None):

	"""
	Populates the in-game world with floor pieces according to the room that you feed into the function.
	
	roomlist = a room list to check that's generated with a Gen...() function.
	
	room4way - roommiddle = dictionaries of room pieces to choose from; will be randomly chosen from to allow for some
	good-looking random level design. The dictionaries should look like:
	
	room4way > {1:['Room4WayRock', 'Room4WayStone', 'Room4WayStone2', etc], 2:[...]}
	
	The number represents the cell type (i.e. a 1 on the grid will spawn one of the rooms in the 1 list)
	
	roomceiling = a list of room objects that can be spawned in the 0 spaces of the room.
	
	roomsize = the size of the room objects to place down
	point = the starting world position of the random room (the center of the map, usually)
	
	point = center point
	
	Returns a list of the spawned rooms
	
	"""

	sce = logic.getCurrentScene()
	cont = logic.getCurrentController()
	obj = cont.owner
	
	spawned = []
	
	for ry in range(len(roomlist)):
	
		cy = abs(ry - (len(roomlist) - 1))	# We have to do this because otherwise, the check will go from bottom to top, incorrectly (the data will be turned around)

		for rx in range(len(roomlist[ry])):
			
			if roomlist[ry][rx] != 0:	# Not blank
			
				cell = roomlist[ry][rx]
				
				sur = GetSurroundingCells(roomlist, ry, rx)
				
				if sur[1] == 1:		# End
					
					roomchoice = random.choice(roomend[cell])
					
					r = sce.addObject(roomchoice, obj)
					ori = r.orientation.to_euler()
				
					dir = sur[0]
					
					if dir[1] == 1:
						ori.z = math.pi
					elif dir[0] == 1:
						ori.z = 0.0
					elif dir[2] == 1:
						ori.z = -math.pi / 2.0
					elif dir[3] == 1:
						ori.z = math.pi / 2.0
					
				elif sur[1] == 2:	# Corner or Straight-through
				
					dir = sur[0]
					
					if (dir[0] and dir[1]) or (dir[2] and dir[3]):
						straight = 1
					else:
						straight = 0
						
					if straight:
																
						roomchoice = random.choice(roomstraight[cell])
					
						r = sce.addObject(roomchoice, obj)
						ori = r.orientation.to_euler()
					
						if dir[0] and dir[1]:
							ori.z = 0.0
						elif dir[2] and dir[3]:
							ori.z = math.pi / 2.0
					else:
					
						roomchoice = random.choice(roomcorner[cell])
					
						r = sce.addObject(roomchoice, obj)
						ori = r.orientation.to_euler()
						
						if dir[0] and dir[2]:
							ori.z = 0.0
						elif dir[0] and dir[3]:
							ori.z = math.pi / 2.0
						elif dir[1] and dir[2]:
							ori.z = -math.pi / 2.0
						else:
							ori.z = math.pi
						
				elif sur[1] == 3:	# Middle
					
					roomchoice = random.choice(roommiddle[cell])
					r = sce.addObject(roomchoice, obj)
					ori = r.orientation.to_euler()
					
					dir = sur[0]
					
					if dir[0] and dir[1] and dir[2]:
						ori.z = 0.0
					elif dir[0] and dir[2] and dir[3]:
						ori.z = math.pi / 2.0
					elif dir[1] and dir[2] and dir[3]:
						ori.z = -math.pi / 2.0
					else:
						ori.z = math.pi
					
				else:				# 4-way
					roomchoice = random.choice(room4way[cell])
					r = sce.addObject(roomchoice, obj)
					ori = r.orientation.to_euler()
				
				spawned.append(r)
				
				r.orientation = ori
									
				halfmapw = math.floor(len(roomlist[0]) / 2.0) * roomsize[0]
				halfmaph = math.floor(len(roomlist) / 2.0) * roomsize[1]

				if point == None:
					point = list(obj.worldPosition)
				else:
					point = list(point)
				
				pos = [(rx * roomsize[0]) - (halfmapw) + point[0], (cy * roomsize[1]) - (halfmaph) + point[1], point[2]]
				
				r.worldPosition = pos
				
			else:						# Blank, so it's a ceiling piece.

				if not roomceiling == None:
					
					roomchoice = random.choice(roomceiling)
					r = sce.addObject(roomchoice, obj)
					spawned.append(r)
					
					halfmapw = math.floor(len(roomlist[0]) / 2.0) * roomsize[0]
					halfmaph = math.floor(len(roomlist) / 2.0) * roomsize[1]
					
					if point == None:
						point = list(obj.worldPosition)
					else:
						point = list(point)
						
					pos = [(rx * roomsize[0]) - (halfmapw) + point[0], (cy * roomsize[1]) - (halfmaph) + point[1], point[2]]
					r.worldPosition = pos

	return (spawned)

	#[print (x) for x in zpos]
	#print (zpos)
