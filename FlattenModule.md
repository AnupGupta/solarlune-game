> The Flatten Python module is used to copy the vertices of several meshes to a single mesh for the BGE to render quicker.

> The Blender Game Engine can handle a lot of polygons drawing at once, but it tends to chug on drawing >many objects< at once, even if they are very low-poly. A way to get around this is to run a function that I call Flatten. First, you make a 'static mesh', which is a basic mesh that has a high number of faces, and then use the Flatten function, which moves the faces in that mesh to match the various source objects that you designate. The Blender Game Engine will draw the static mesh in a single batch, much more quickly than drawing the objects individually. The source objects can be invisible, or even removed after the static mesh takes on their appearance. Obviously, the static mesh can't change the appearance of the individual objects after flattening, but it's useful for having a complex world that doesn't need to be fully dynamic.

> If you want to test the difference, open the example and delete the lines of the SpawnAndFlatten script from 'spheres.append(...)' down. That will spawn the individual objects, but won't flatten them. Compare your rasterizer percentage and frame-rate versus the original version.


> - Advantages -


  * Allows the developer to draw a large number of objects much faster than usual.


> - Disadvantages -


  * The flattened mesh is a single object, so you can't really do any dynamics (moving individual objects on part of a flattened mesh) without actually moving the vertices / faces for the mesh.

  * This process forces you to create a mesh that has a high number of faces, thereby raising load times considerably.

  * The Flatten function moves the source object's vertices to match the objects in the objects list, so this method only works correctly when the both the source and destination objects share materials (since the BGE can't re-assign materials to the vertices).

  * For speed, there's no check to ensure that you have enough faces in your destination mesh to 'cover' all of the faces in the source meshes. Be aware of this if you find your destination mesh seems 'incomplete'.

> To use the Flatten module with the example, just download both and place them next to each other. I didn't place the module in the same folder as the example to reduce redundancy.