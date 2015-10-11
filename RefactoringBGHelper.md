# Introduction #

I was going to implement something in one of my game projects when I saw that I needed to get the dimensions of an object. I have a function for that in BGHelper, but I found that I didn't want to import it on top of several of my custom modules that I had already imported. The BGHelper module is quite messy and in need of some assistance, and that goes for several more of my modules, as well. So, that made me decide to do something about it.

I've decided to refactor the BGHelper module and also get rid of all of my previous modules and compile them into one single, (at least somewhat) organized collection.


# Details #

It doesn't make sense from a logical point of view to have disparate related elements spread among multiple modules. For example, joystick profiles are available in the JoyProfile module, there's joystick checking code in BGHelper, and completely separate joystick-checking and binding code in BGInput (which is pretty much the preferred way to handle input over checking manually in BGHelper).

This new rearrangement of BGHelper should hopefully be far superior. I'll incrementally add to the "pack" using pre-existing modules or even full re-writes as necessary. I'm thinking about the following changes:

  * BGHelper.Filters < SFL (Screen Filter Library) module

  * BGHelper.Input < Input binding (BGInput, JoyProfile) module

  * BGHelper.Path < Node paths (from BGHelper); if I make a Math module, it would go into there.

  * BGHelper.RLG < RLG (Random Level Generation) module

  * BGHelper.Mesh < General Mesh-related code altering module (i.e. BGHelper.Mesh.GetDimensions)

  * BGHelper.Trail < LightTrail (waving scarves, trails behind moving objects, etc)

  * BGHelper.Wave < Waves (maybe)

  * BGHelper.Sprite < Sprites (2D sprite animations)

  * BGHelper.Flatten < Flatten (Flattening two meshes together)

  * BGHelper.Light < Light handling (LightHelper) module

  * BGHelper.API < BGE API improvement (BGEAPIPlus) module (works through modification of the built-in bge Python module simply on import)

And so on with different features.