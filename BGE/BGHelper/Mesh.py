"""
Copyright (c) 2014 SolarLune

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

from bge import logic, constraints

import math, mathutils, time


def make_unique_mesh(mesh):

    if not hasattr(logic, 'lib_new_counter'):

        logic.lib_new_counter = 0

    newmesh = logic.LibNew(mesh + str(logic.lib_new_counter), 'Mesh', [mesh])[0]

    logic.lib_new_counter += 1

    return newmesh


def get_all_vertices(o):

    verts = []

    for mesh in o.meshes:

        for mat in range(mesh.numMaterials):

            for v in range(mesh.getVertexArrayLength(mat)):

                verts.append(mesh.getVertex(mat, v))

    return verts


def get_shared_vertices(mesh, vert, max_diff = 0, mat = 0):

    """Returns the vertices sharing the position occupied by the vertex 'vert'.
    'mesh' = which object's vertices to check;
    'vert' = which vertex to find the duplicates of
    'mat' = which vertices of 'mesh' to check, according to material index, I believe.
    note that this goes through all vertices, so this should only be used with lower-poly objects
    and	should only be done rarely to keep up efficiency."""

    list = []

    for a in range(mesh.getVertexArrayLength(mat)):

        v = mesh.getVertex(mat, a)

        if max_diff != 0:
            if abs(v.x - vert.x) < max_diff and abs(v.y - vert.y) < max_diff and abs(v.z - vert.z) < max_diff:
                list.append(v)
        else:
            if v.x == vert.x and v.y == vert.y and v.z == vert.z:
                list.append(v)

    return list


def soft_body_pin(softbodyobj, controls):

    """
    Pins the soft body object to an object using its vertices (a control object). It will pin the soft-body
    object to all of the vertices of all of the objects in the controls list. So, for controls pass a list like:

    [ControlObject, ControlObject2, etc.]

    where ControlObject are Game Objects fetched through the scene list, for example.
    """

    softid = softbodyobj.getPhysicsId()
    ctype = 2 # Constraint type, 1 = edge; 0 = point, 2 = angular?

    for c in controls:

        cid = c.getPhysicsId()

        for vert in range(c.meshes[0].getVertexArrayLength(0)):

            vpos = c.meshes[0].getVertex(0, vert).getXYZ()

            constraints.createConstraint(softid, cid, ctype, vpos[0], vpos[1], vpos[2], 8, -1, 0.5)


def get_dimensions(object = None, roundit = 3, offset = 1, meshnum = 0, factor_in_scale = 1):

    """
    Gets the dimensions of the object (what you see under dimensions in the properties window in the 3D menu).
    mesh = which mesh to use to get the object's dimensions.
    roundit = how far down to round the returned dimension values; set it to a negative number to not round the numbers off at all.
    offset = Whether or not to return the offset point of the dimensions (the center point);
    This negated (-offset, literally) is the origin point, generally.
    meshnum = The index of the mesh to use. Usually 0 is okay.
    factor_in_scale = If it should multiply the dimensions by the object's world scale.
    """

    if object == None:
        object = logic.getCurrentController().owner

    s = object.worldScale

    mesh = object.meshes[meshnum]

    #print (dir(mesh))

    verts = [[], [], []]

    originpos = [0, 0, 0]

    for mat in range(len(mesh.materials)):

        for v in range(mesh.getVertexArrayLength(mat)):

            vert = mesh.getVertex(mat, v)

            pos = vert.getXYZ()

            verts[0].append(pos[0])
            verts[1].append(pos[1])
            verts[2].append(pos[2])

    verts[0].sort()
    verts[1].sort()
    verts[2].sort()

    if offset != 0:

        offsetpos = [
            (verts[0][len(verts[0])-1] + verts[0][0]) / 2,
            (verts[1][len(verts[1])-1] + verts[1][0]) / 2,
            (verts[2][len(verts[2])-1] + verts[2][0]) / 2,
            ]

    size = [(verts[0][len(verts[0]) - 1] - verts[0][0]),
            (verts[1][len(verts[0]) - 1] - verts[1][0]),
            (verts[2][len(verts[0]) - 1] - verts[2][0])]

    if factor_in_scale:

        size = [size[0] * s[0],
        size[1] * s[1],
        size[2] * s[2]]

    if roundit >= 0:

        size = [
        round(size[0], roundit),
        round(size[1], roundit),
        round(size[2], roundit),
        ]

    if offset:
        return (mathutils.Vector(size), mathutils.Vector(offsetpos))

    else:
        return (mathutils.Vector(size), None)


def uv_scroll(uspd = 0.0025, vspd = 0.0, layer = 0, mesh = None, mat = 0, freqstretch = 1):
    """
    Scrolls the UV Coordinate of each vertex in the specified mesh by
    uspd and vspd.
    uspd = how fast to scroll on the X-axis (X)
    vspd = how fast to scroll on the V-axis (Y)
    layer = which UV-layer to scroll; 0 = first layer, 1 = second, 2 = both
    mesh = which mesh to use for UV-animation
    mat = which material to look for (I think it's organized by material)
    freqstretch = frequency-stretching enabled - if set to 1, then you can run this script with an Always sensor set to a
    limited frequency rate and still scroll the UV-map by the same speed, so you should only connect this script's controller to a single Always sensor
    """

    from bge import logic

    cont = logic.getCurrentController()
    obj = cont.owner

    if mesh == None:
        mesh = obj.meshes[mat]

    if freqstretch:
        f = cont.sensors[0].frequency + 1
    else:
        f = 1

    for v in range(mesh.getVertexArrayLength(mat)):

        vert = mesh.getVertex(0, v)

        if layer == 0 or layer == 2:
            vert.u += uspd * f
            vert.v += vspd * f
        if layer == 1 or layer == 2:
            vert.u2 += uspd * f
            vert.v2 += vspd * f

# Flattening meshes together


def flatten(destination, sources):

    """
    Author: SolarLune
    Date Updated: 3/11/13

    Sets all vertices of the destination object to match each vertex of each of the sourceobjects' meshes. Useful for
    voxel-ish games.

    destination = object that you want to alter
    sources = list of objects that you want to flatten into the local mesh

    Returns a list of the vertices that have been flattened into the destination mesh

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

                vert.XYZ = tv.XYZ
                vert.x *= targetobj.worldScale.x
                vert.y *= targetobj.worldScale.y
                vert.z *= targetobj.worldScale.z

                vert.XYZ += (op - lp)		# Set each vertex of the source mesh to match one of the target objects'
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


def unflatten(destination, verts):

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


def unflatten_all(destination):

    """
    Unflattens all vertices from the destination object.
    """

    mesh = destination.meshes[0]

    for m in range(mesh.numMaterials):

        for v in range(mesh.getVertexArrayLength(m)):

            vert = destination.meshes[0].getVertex(m, v)

            vert.setXYZ([0, 0, 0])

            destination['vertsavailable'][m][v] = 1

# Waves


def wave_planar(wave_num = 1, wave_rate_x = 1, wave_rate_y = 1, wave_height = 1.0, scale_color = 0, only_color = 1, obj = None):

    """

    Moves the vertices of the mesh around to give a waving effect.

    wave_num = how many waves to display on the mesh. Use a whole number >= 1 to increase the number of waves
    the mesh attempts to display. Note that you need enough detail on the mesh to accurately display the waves.
    Also note that numbers below 1 will display a part of a wave, and so will not loop correctly (when placed
    next to other instances of the same waving mesh).

    wave_rate = how many oscillations to make per second.

    wave_height = how high the waves should reach from the base Z value that the mesh starts with.

    scale_color = 0 means it will ignore the wave's vertex color channel.
    scale_color = 1 means it will scale the wave effect by the brightness of the wave's red vertex color.
    scale_color = 2 means it will scale the wave effect by the brightness of the wave's red vertex color
    binarily (on or off, if the channel's value is greater than 0.5).

    only_color = Only registers vertices to update if their red vertex color channel is greater than 0.5

    obj = Object to influence. If None, then the object running this Python controller will be used.

    """

    if obj == None:

        o = logic.getCurrentController().owner

    else:

        o = obj

    if not 'wave_planar_info' in o:

        o['wave_planar_info'] = {}

        o['wave_planar_info']['verts'] = {}

        o['wave_planar_info']['dimensions'] = GetDimensions(o, factor_in_scale = 0)[0]

        for vert in GetAllVertices(o):

            if only_color:

                if vert.r > 0.5:

                    o['wave_planar_info']['verts'][vert] = vert.getXYZ() # Only add the vertex to the list if it's red (cuts down processing)

            else:

                o['wave_planar_info']['verts'][vert] = vert.getXYZ()

    t = time.clock()

    d = o['wave_planar_info']['dimensions'].copy()

    d.magnitude /= 2

    twrx = t * wave_rate_x
    twry = t * wave_rate_y

    if not scale_color: # Moving these if blocks outside of the vertex changes

        for vert in o['wave_planar_info']['verts']:

            osc_time_x = (twrx + ((vert.x / d.x) * wave_num)) * math.pi
            osc_time_y = (twry + ((vert.y / d.y) * wave_num)) * math.pi

            wave = ((math.sin(osc_time_x) + math.cos(osc_time_y) / 2) + 0.5) * wave_height

            vert.z = o['wave_planar_info']['verts'][vert].z + wave

    elif scale_color == 1: # Scale wave by vertex color

        for vert in o['wave_planar_info']['verts']:

            osc_time_x = (twrx + ((vert.x / d.x) * wave_num)) * math.pi
            osc_time_y = (twry + ((vert.y / d.y) * wave_num)) * math.pi

            wave = ((math.sin(osc_time_x) + math.cos(osc_time_y) / 2) + 0.5) * wave_height

            wave *= vert.r

            vert.z = o['wave_planar_info']['verts'][vert].z + wave

    else: # Scale wave by vertex color (binarily)

        for vert in o['wave_planar_info']['verts']:

            osc_time_x = (twrx + ((vert.x / d.x) * wave_num)) * math.pi
            osc_time_y = (twry + ((vert.y / d.y) * wave_num)) * math.pi

            wave = ((math.sin(osc_time_x) + math.cos(osc_time_y) / 2) + 0.5) * wave_height

            if vert.r < 0.5:
                wave = 0.0

            vert.z = o['wave_planar_info']['verts'][vert].z + wave

