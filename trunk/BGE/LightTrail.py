"""

Copyright (c) 2013 SolarLune

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

It would be greatly appreciated if you could attribute me, the creator of
this script, SolarLune, should you use this script.

"""


from bge import logic

def Init(cont):
	
	obj = cont.owner
	
	sce = obj.scene
	
	mesh = obj.meshes[0]
	
	if not 'init' in obj:
		
		if not 'trail_axis' in obj:
			obj['trail_axis'] = 'y'
		
		obj['init'] = 1
		
		obj['verts'] = []
		
		for mat in range(mesh.numMaterials):
			
			for v in range(mesh.getVertexArrayLength(mat)):

				vert = mesh.getVertex(mat, v)

				obj['verts'].append(vert)						# Get all verts
				
		obj['vert_offsets'] = {}
		
		for vert in obj['verts']:
			
			obj['vert_offsets'][vert] = vert.XYZ
				
		vert_pairs = {}
	
		for vert in obj['verts']:
			
			if obj['trail_axis'].lower() == 'x':
				vert_y = round(vert.x, 2)			# Round it off to ensure that verts that have very close X positions (i.e. 0 and 0.01) get grouped togethe
			elif obj['trail_axis'].lower() == 'y':
				vert_y = round(vert.y, 2)			
			else:
				vert_y = round(vert.z, 2)
				
			if not vert_y in vert_pairs:
				
				vert_pairs[vert_y] = []
				
			vert_pairs[vert_y].append(vert)		# Get the verts paired with their positions
										
		obj['vert_pairs']= []
						
		for vp in vert_pairs:
			
			obj['vert_pairs'].append([vp, vert_pairs[vp]])
			
		obj['vert_pairs'] = sorted(obj['vert_pairs'], key = lambda x: x[0], reverse = True)
		
		obj['target_positions'] = []
				
		#if not 'trail_length' in obj:
		#	obj['trail_length'] = 1.0	# Trail length in seconds
		
		
		
		if not 'trail_stretch' in obj:
			obj['trail_stretch'] = 1			# Stretch the trail to 'fit' the movements
		
		if not 'trail_spacing' in obj:
			obj['trail_spacing'] = 3		# Number of frames between each edge in the trail
				
		if not 'trail_reverse' in obj:
			obj['trail_reverse'] = 0
			
		if not 'trail_onmoving' in obj:
			obj['trail_onmoving'] = 0	# Update the trail only when moving
				
		obj['trail_counter'] = obj['trail_spacing']			# Number of frames between each 'keyframe'
				
		if not 'target' in obj:			# Target of the trail
			
			obj['target'] = obj.parent
		
		else:
			
			if isinstance(obj['target'], str):
				
				obj['target'] = sce.objects[obj['target']]
				
		obj['target_past_pos'] = obj['target'].worldPosition.copy()
		obj['target_past_ori'] = obj['target'].worldOrientation.copy()
		
		target_info = [obj['target'].worldPosition.copy(), obj['target'].worldOrientation.copy()]
		
		for x in range(len(obj['vert_pairs']) * obj['trail_spacing']):
			
			obj['target_positions'].insert(0, target_info)
					
	else:
		
		return 1
	
def Main(cont):
	
	obj = cont.owner
	
	if Init(cont):
		
		if not obj.parent == obj['target']:
			obj.worldPosition = obj['target'].worldPosition
			obj.worldOrientation = obj['target'].worldOrientation
		
		target_info = [obj['target'].worldPosition.copy(), obj['target'].worldOrientation.copy()]
		
		
		insert = 0
		
		if not obj['trail_onmoving']:
			insert = 1
		else:
			
			pos_diff = (obj['target'].worldPosition - obj['target_past_pos']).magnitude
			ori_diff = (obj['target'].worldOrientation - obj['target_past_ori']).median_scale
			threshold = 0.0001
			
			if pos_diff > threshold or ori_diff > threshold:
				
				insert = 1
				
		if insert:
			obj['target_positions'].insert(0, target_info)
	
		if len(obj['target_positions']) > len(obj['vert_pairs']) * obj['trail_spacing']:
			
			obj['target_positions'].pop()		# Remove oldest position value

		for vp in range(0, len(obj['vert_pairs'])):

			verts = obj['vert_pairs'][vp][1]
			
			if len(obj['target_positions']) > vp * obj['trail_spacing']:
			
				pos = obj['target_positions'][vp * obj['trail_spacing']][0]
				ori = obj['target_positions'][vp * obj['trail_spacing']][1]
			
				for vert in verts:
					
					if obj['trail_reverse']:
						if obj['trail_stretch']:		# Factor in position of the target to 'stretch' (useful for trails, where the end point stays still, hopefully, until the rest 'catches up'')
							diff = (pos - obj['target'].worldPosition) * ori#.inverted()
							vert.XYZ = (obj['vert_offsets'][vert] + diff) * obj['target'].worldOrientation.inverted()
						else:								# Don't factor in movement of the trail (useful for things that wouldn't stretch, like scarves)
							vert.XYZ = obj['vert_offsets'][vert] * obj['target'].worldOrientation.inverted()
						vert.XYZ = vert.XYZ * ori
					else:
						
						if obj['trail_stretch']:		# Factor in position of the target to 'stretch' (useful for trails, where the end point stays still, hopefully, until the rest 'catches up'')
							diff = (pos - obj['target'].worldPosition) * ori
							vert.XYZ = (obj['vert_offsets'][vert] + diff) * obj['target'].worldOrientation
						else:								# Don't factor in movement of the trail (useful for things that wouldn't stretch, like scarves)
							vert.XYZ = obj['vert_offsets'][vert] * obj['target'].worldOrientation
						vert.XYZ = vert.XYZ * ori.inverted()

		obj['target_past_pos'] = obj['target'].worldPosition.copy()
		obj['target_past_ori'] = obj['target'].worldOrientation.copy()
