from bge import logic

import math

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

"""
Change-log:

11/8/13: Slight code cleanup.

10/2/13: Updated input methods to drop the need to use states for each individual binding
(i.e. JumpPressed and JumpDown). Now you just specify the type of binding it is when you add it (KEY for keyboard,
JOYBUTTON for joystick button, etc.), and then use the input device itself to check the state. There are three
functions for this process now - BindDown, BindPressed, and BindReleased. Each function will return the state of the
binding should the state you specify be true (i.e. if the input is being held, then it will return the value of that
input. For a key or a button, it would be 1.0 or 0. For an axis, it would be a number indicating how far that axis
is being pressed).

Check the BGInput example to see how it works.
"""

KEY = 0
JOYBUTTON = 1
JOYHAT = 2
JOYAXIS = 3                # Return the percentage that the axis is being pressed (the axis values themselves)
MOUSEAXIS = 4

STATE_UP = 0
STATE_PRESSED = 1
STATE_DOWN = 2
STATE_RELEASED = 3

class CInputKey():
    
    """
    Tests for input from keyboard and joystick.
    """
    
    def __init__(self, inputtype, keycode, axisdirection = 1, deadzone = 0.1, joyindex = 0, scalar = 1.0):
        
        """
        A input handling object.
        
        inputtype = input type from CInputKey (CInputKey.KEYDOWN, for example)
        keycode = key, axis, hat, or button code for the input device (for example, events.XKEY, 5 for the fifth button on a joystick, etc.)
        axisdirection = direction to check for axis values for joystick and mouse axis checks.
        deadzone = percentage to disregard joystick movement.
        joyindex = joystick index to check.
        scalar = how large the end number is. Defaults to 1.0. This is useful to make corresponding inputs match up (i.e. make
        the mouse move at the same rate as the right analog stick).
        """
        
        self.inputtype = inputtype
        self.keycode = keycode
        
        self.prevstate = 0
        self.prevpos = [0.0, 0.0]                       # Previous position of the mouse
        self.active = 0.0
        self.state = STATE_UP                       # The state of the key input (just pressed, released, down, up, etc.)
        
        self.scalar = scalar
        self.axisdirection = axisdirection      # Default for axis checking
        self.deadzone = deadzone                # Deadzone amount for axis checking
        self.joyindex = joyindex                    # Defaults to the first one
        
    def Poll(self):
        
        """
        Polls the input to check whether it's active or not.
        """
        
        joy = logic.joysticks[self.joyindex]
    
        if self.inputtype == KEY:
            
            if logic.keyboard.events[self.keycode] == logic.KX_INPUT_ACTIVE:
                
                self.active = self.scalar
                                
            else:
                
                self.active = 0.0
        
        if self.inputtype == MOUSEAXIS:
            
            av = logic.mouse.position[self.keycode] - self.prevpos[self.keycode]
            
            self.state = STATE_DOWN
            
            if math.copysign(1, av) == self.axisdirection and abs(av) > self.deadzone:
            
                self.active = abs(av) * self.scalar
                
            else:
                
                self.active = 0.0
                
            self.prevpos = [0.5, 0.5]
             
        elif joy != None:
                        
            if self.inputtype == JOYBUTTON:
         
                if self.keycode in joy.activeButtons:
                
                    self.active = self.scalar
                                            
                else:
                    
                    self.active = 0.0
            
            elif self.inputtype == JOYHAT:
         
                if self.keycode in joy.hatValues:
                
                    self.active = self.scalar
                                                    
                else:
                    
                    self.active = 0.0
            
            elif self.inputtype == JOYAXIS:
                
                av = joy.axisValues[self.keycode]
                
                pressed = abs(av) > self.deadzone and math.copysign(1, av) == self.axisdirection
                
                if pressed:
                    
                    self.active = abs(av) * self.scalar
                            
                else:
                    
                    self.active = 0.0
        
        if self.active and not self.prevstate:
            
            self.state = STATE_PRESSED
        
        elif self.active and self.prevstate:
            
            self.state = STATE_DOWN
        
        elif not self.active and self.prevstate:
            
            self.state = STATE_RELEASED
        
        else:
            
            self.state = STATE_UP
        
        self.prevstate = self.active
    
class CInputDevice():
    
    """
    A class for testing for input from different devices. Useful if you want to easily set up different bindings for your input.
    
    Basically, you add the inputs via their inputtype (retrieved from CInputKey's input type constant definitions) with the
    keycode that you need.
    
    You can also specify a group for each binding entry (i.e. you can add keyboard and joystick controls separately.)
    
    Then, you poll the device with the group that you specify (so you can easily switch between key setups, and so it
    won't matter which device you use).
    
    Finally, you can easily retrieve the key / button / axis being pressed by just checking the device's events dictionary:
    
    -------------
    
    device = CInputDevice()
    
    device.Add('jump', KEYPRESSED, events.ZKEY, 'keyboard')
    
    device.Poll('keyboard')
    
    print (device.bindings['jump'])
    
    -------------
    
    Note that you can also not specify a group if you want all input devices to work at the same time (i.e. use the joystick
    or the keyboard at the same time.)
    
    """
        
    def __init__(self):
        
        """
        Example code usage:
        
        device = CInputDevice()
        
        device.Add('jump', BGInput.KEYPRESSED, events.ZKEY, 'keyboard')
        
        device.Poll('keyboard')
        
        print (device.bindings['jump'])
        
        """
        
        self.events = {}
        self.bindings = {}
        self.states = {} # The states of individual bindings (seemed easier than having to use bindings['active'] and bindings['state'])
        
    def Add(self, bindingname, inputtype, keycode, group = "default", axisdir = 1, deadzone = 0.1, joyindex = 0, scalar = 1.0):
        
        """
        Add a key binding.
        
        bindingname = name of the binding to create (i.e. 'left', 'jump', 'run', 'interact'...)
        inputtype = input type from CInputKey (CInputKey.KEYDOWN, for example)
        keycode = key, axis, hat, or button code for the input device (for example, events.XKEY, 5 for the fifth button on a joystick, etc.)
        
        group = a string that designates what group to add this binding to. For example, you might add all of the joystick
        bindings to a 'joystick' group, and all of the keyboard bindings to a 'keyboard' group
        
        axisdir = direction to check for axis values for joystick and mouse axis checks.
        deadzone = Fraction to disregard joystick movement.
        joyindex = joystick index to check.
        scalar = how large the end number is. Defaults to 1.0. This is useful to make corresponding inputs match up (i.e. make
        the mouse move at the same rate as the right analog stick).
        
        """
        
        if not group in self.events:
                
            self.events[group] = {}
                
        if not bindingname in self.events[group]:
            
            #if not group in self.events:        # Set up the events dictionary
            
            #    self.events[group] = {}
                
            self.events[group][bindingname] = []
               
            self.bindings[bindingname] = 0
        
        self.events[group][bindingname].append(CInputKey(inputtype, keycode, axisdir, deadzone, joyindex, scalar))
        
    def Poll(self, group = None):
        
        """
        Poll the bindings for updates.
        
        group = which set of bindings to poll in particular. If left to None, then it will poll all groups specified.
        If you specify, then it will poll that one in particular. Useful for switching input schemes.
        """
        
        if group == None:
            
            poll_groups = [gr for gr in self.events]
            
        else:
            
            poll_groups = [group]
            
        for group in poll_groups:
    
            for binding in self.events[group]:
         
                self.bindings[binding] = {'active':0.0, 'state':0}
                
                for input in self.events[group][binding]:
                    
                    input.Poll()
                   
                    if input.active:
                  
                        self.bindings[binding] = {'active':input.active, 'state':input.state}
                    
                    else:
                        
                        if input.state == STATE_RELEASED:
                            
                            self.bindings[binding]['state'] = input.state
                    
                    #elif not self.bindings[binding]['active']:
                        
                    #    if input.state != STATE_UP and input.prevstate:
                        
                    #        self.bindings[binding]['state'] = input.state
    
    def BindDown(self, bind):
        """
        Checks to see if the binding you specify is activated currently (down).
        
        bind = binding name
        """
        return self.bindings[bind]['active'] if self.bindings[bind]['state'] == STATE_DOWN else 0.0
    def BindPressed(self, bind):
        """
        Checks to see if the binding you specify was just pressed this frame.
        
        bind = binding name
        """
        return self.bindings[bind]['active'] if self.bindings[bind]['state'] == STATE_PRESSED else 0.0
    def BindReleased(self, bind):
        """
        Checks to see if the binding you specify was just released this frame. If it was, 1 is returned.
        
        bind = binding name
        """
        return 1.0 if self.bindings[bind]['state'] == STATE_RELEASED else 0.0
