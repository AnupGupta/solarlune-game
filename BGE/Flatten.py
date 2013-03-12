"""
Copyright (c) 2013 SolarLune

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

P.S. It would be nice if you could attribute me for the creation of this and my other scripts. Thanks!
"""

def Flatten(destination, sources):
	
	"""
	Author: SolarLune
	Date Updated: 3/11/13
	
	Sets all vertices of the destination object to match each vertex of each of the sourceobjects' meshes. Useful for
	voxel-ish games.
	
	destination = object that you want to alter
	sources = list of objects that you want to flatten into the local mesh
	
	- Notes -
	
	The Blender Game Engine can handle a lot of polygons drawing at once, but it tends to chug
	on drawing many objects, even if they are low-poly. A way to get around this is to make a
	'static mesh', which is a basic mesh that has a high number of faces, and then move the
	faces in that mesh to match many objects. The Blender Game Engine draws all of this in a
	single batch, much more quickly than the objects individually. The objects can be invisible,
	or even removed after the static mesh takes on their appearance. Obviously, this mesh
	can't move the individual appearance of the objects, but it's useful for having a complex
	world that doesn't need to be fully dynamic.
	
	
	- Advantages -
	
	
	. Allows the developer to draw a large number of objects much faster than usual.
	
	
	- Disadvantages -
	
	
	.  The flattened mesh is a single object, so you can't really do any dynamics (moving individual objects
	on part of a flattened mesh) without actually moving the vertices / faces for the mesh.
	
	. Forces you to create a mesh that has a high number of faces, thereby raising load times considerably.
	
	. The Flatten function moves the source object's vertices to match the objects in the objects list,
	so this method only works correctly when the both the source and destination objects share materials (since
	the BGE can't re-assign materials to the vertices).
	
	. For speed, there's no check to ensure that you have enough faces in your destination mesh to 'cover' all of the
	faces in the source meshes. Be aware of this if you find your destination mesh seems 'incomplete'.
	
	"""	

	objindex = 0
	vertindex = 0
	objverts = {}
	
	nomore = 0	# All through with objects?
	
	mesh = destination.meshes[0]
	lp = destination.worldPosition.copy()
	
	targetobj = sources[objindex]
	targetmesh = targetobj.meshes[0]

	allobjverts = []

	if not 'vertsavailable' in destination:

		destination['vertsavailable'] = {}
		
		for m in range(mesh.numMaterials):
			
			destination['vertsavailable'][m] = [1 for x in range(mesh.getVertexArrayLength(m))]
		
		UnflattenAll(destination)

	for m in range(mesh.numMaterials):
	
		# Actually loop through the vertices
			
		for v in range(mesh.getVertexArrayLength(m)):
			
			if destination['vertsavailable'][m][v] == 0:
				continue
			
			vert = mesh.getVertex(m, v)
				
			if nomore == 0:
				
				destination['vertsavailable'][m][v] = 0
				
				tv = targetmesh.getVertex(0, vertindex)
				vl = targetmesh.getVertexArrayLength(0)
				
				op = sources[objindex].worldPosition
					
				vert.XYZ = tv.XYZ + (op - lp)		# Set each vertex of the source mesh to match one of the target objects'
				vert.UV = tv.UV						# Mesh vertex position, UV, and normal properties, offset by the target
				vert.normal = tv.normal				# objects' world positions and the local mesh's world position (because all
				vert.color = tv.color					# of the vertices belong to the local mesh
				
				vertindex += 1						
				
				try:
					objverts[m].append(v)		# Append the vertex for the material index to the dictionary of verts used for the object
				except KeyError:
					objverts[m] = []
					objverts[m].append(v)
				
				if vertindex >= vl:	# If there's no more vertices for the current object, move to the next one
					vertindex = 0
					objindex += 1
					allobjverts.append(objverts)
					if objindex < len(sources):
						targetobj = sources[objindex]
						targetmesh = targetobj.meshes[0]
						objverts = {}
					else:
						nomore = 1
		
			else:
				
				break
		
	return allobjverts

def Unflatten(destination, verts):
	
	"""
	"Removes" the vertices from the flattened mesh.
	
	destination = destination object to use.
	verts = vertex index array indicating which vertices to unflatten.
	"""
	
	for m in verts:
		
		for v in verts[m]:
			
			vert = destination.meshes[0].getVertex(m, v)
			
			vert.setXYZ([0, 0, 0])
			
			destination['vertsavailable'][m][v] = 1
			
def UnflattenAll(destination):
	
	"""
	Unflattens all vertices from the destination object.
	"""
	
	mesh = destination.meshes[0]
	
	for m in range(mesh.numMaterials):
		
		for v in range(mesh.getVertexArrayLength(m)):
			
			vert = destination.meshes[0].getVertex(m, v)
			
			vert.setXYZ([0, 0, 0])
			
			destination['vertsavailable'][m][v] = 1
