# What is this "BDXHelper" business? #

This is the initial commit of my new BDXHelper package. BDXHelper is a helper module for making games with... BDX. Of course. You can find the BDX engine over at Goran's GitHub repo here:

https://github.com/GoranM/bdx

It's pretty early, and not nearly as "up to snuff" as BGHelper is. However, that should change over time (I think) - it already contains a variety of useful tools.

bdxhelper.input contains classes concerning checking for input from a variety of devices, and mapping them to easy to check names. It's fairly complete; just doesn't have mouse movement input checking at the moment.
bdxhelper.API will contain functions for general code usage. Currently it has a couple of functions to check if at least so many booleans out of a series of them are true or false.
bdxhelper.Math will handle mathematics (including vector math). Currently, the only function there is one that snaps a vector to a grid.
bdxhelper.navigation will contain classes for navigation between points. This currently doesn't work, as I'm in the process of transferring my Nodemap class from BGHelper over, and it's not without its difficulties, haha.

To actually use it, I think you need to place the jar in the /core/libs/ folder, and include it in your project if you're using an IDE (if you want it not to throw errors at you). From there, just referring to the package as com.solarlune.bdxhelper should get you going. To use it at all, I think you'll NEED gamepad support in your LibGDX project. To enable it, you'll need to edit your build.gradle file in your root project directory (not in any other folder underneath that one) to include it. See this page for more information: https://github.com/libgdx/libgdx/wiki/Dependency-management-with-Gradle

Using input maps boils down to referring to the InputMap's static "addBinding()" function and providing a new InputBase instance (which can be any of the derivative classes, like InputKey or InputGamepadAxis).Provide the arguments as you need (the hat directions should come from LibGDX, I think; numbers or values from gamepad profiles should work for other gamepad input classes, and key press names should just be the (non-capitalized) name of the key you need to check). Update the map by calling its poll() function, check for input changes with the bindDown / bindPressed / bindReleased functions, and you're good to go.

Included is a gamepad profile for XBOX 360 controllers (that may not be accurate across platforms, haha); just refer to the desired input by the class (it's static, too). Naturally, I've included the .jar file (the package) as well as the editable source code. Here's an example of how you'd use it:

```

package com.solarlune.kyro;

import com.nilunder.bdx.GameObject;
import com.solarlune.bdxhelper.input.InputGamepadButton;
import com.solarlune.bdxhelper.input.InputKey;
import com.solarlune.bdxhelper.input.InputMap;
import com.solarlune.bdxhelper.input.gamepadprofiles.Xbox360;


/**
 * Created by SolarLune on 1/16/2015.
 */
public class SysCon extends GameObject {


    @Override
    public void init() {


        InputMap.addBinding("attack", new InputGamepadButton(Xbox360.X));
        InputMap.addBinding("attack", new InputKey("x"));


    }


    @Override
    public void main() {
        InputMap.poll();


        if (InputMap.bp("attack"))
            System.out.println("Attacked.");
    }
}

```

Well, that's pretty much it!

The BDXHelper module is licensed under the "you can do whatever you want with it as long as you don't sell it" license.

Copyright SolarLune 2015.