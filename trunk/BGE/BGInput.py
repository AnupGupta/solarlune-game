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

KEYDOWN = 0
KEYUP = 1
KEYPRESSED = 2
KEYRELEASED = 3

JOYBUTTONDOWN = 4
JOYBUTTONUP = 5
JOYBUTTONPRESSED = 6
JOYBUTTONRELEASED = 7

JOYHATDOWN = 8
JOYHATUP = 9
JOYHATPRESSED = 10
JOYHATRELEASED = 11

JOYAXIS = 12                # Return the percentage that the axis is being pressed (the axis values themselves)
JOYAXISDOWN = 13        # Otherwise, return 0 or 1 values
JOYAXISUP = 14
JOYAXISPRESSED = 15
JOYAXISRELEASED = 16

MOUSEAXIS = 17

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
        self.prevpos = [0, 0]                       # Previous position of the mouse
        self.active = 0.0
        
        self.scalar = scalar
        self.axisdirection = axisdirection      # Default for axis checking
        self.deadzone = deadzone                # Deadzone amount for axis checking
        self.joyindex = joyindex                    # Defaults to the first one
        
    def Poll(self):
        
        """
        Polls the input to check whether it's active or not.
        """
        
        joy = logic.joysticks[self.joyindex]
    
        if self.inputtype == self.KEYDOWN:
            
            if logic.keyboard.events[self.keycode] == logic.KX_INPUT_ACTIVE:    self.active = self.scalar
                
            else:   self.active = 0
            
        elif self.inputtype == self.KEYUP:
            
            if not logic.keyboard.events[self.keycode] == logic.KX_INPUT_ACTIVE: self.active = self.scalar
            
            else:   self.active = 0
            
        elif self.inputtype == self.KEYPRESSED:
            
            if logic.keyboard.events[self.keycode] == logic.KX_INPUT_JUST_ACTIVATED: self.active = self.scalar
            
            else:   self.active = 0
            
        elif self.inputtype == self.KEYRELEASED:
            
            if logic.keyboard.events[self.keycode] == logic.KX_INPUT_JUST_RELEASED: self.active = self.scalar
            
            else:   self.active = 0
          
        if joy != None:
                        
            if self.inputtype == self.JOYBUTTONDOWN:
         
                if self.keycode in joy.activeButtons:
                
                    self.active = self.scalar
                    
                else:
                    
                    self.active = 0

            elif self.inputtype == self.JOYBUTTONUP:
                
                if not self.keycode in joy.activeButtons:
                
                    self.active = self.scalar
                    
                else:
                    
                    self.active = 0
               
            elif self.inputtype == self.JOYBUTTONPRESSED:
                  
                if self.keycode in joy.activeButtons and self.prevstate == 0:
                   
                   self.active = self.scalar
                   
                else:
                    
                    self.active = 0
                    
                self.prevstate = self.keycode in joy.activeButtons
                    
            elif self.inputtype == self.JOYBUTTONRELEASED:

                if not self.keycode in joy.activeButtons and self.prevstate == 1:
                   
                   self.active = self.scalar
                   
                else:
                    
                    self.active = 0
                    
                self.prevstate = self.keycode in joy.activeButtons
                
            elif self.inputtype == self.JOYHATDOWN:
                
                if self.keycode in joy.hatValues:
                
                    self.active = self.scalar
                    
                else:
                    
                    self.active = 0
                    
            elif self.inputtype == self.JOYHATUP:
            
                if not self.keycode in joy.hatValues:
                
                    self.active = self.scalar
                    
                else:
                    
                    self.active = 0
                    
            elif self.inputtype == self.JOYHATPRESSED:
                
                if self.keycode in joy.hatValues and self.prevstate == 0:
                   
                   self.active = self.scalar
                   
                else:
                    
                    self.active = 0
                    
                self.prevstate = self.keycode in joy.hatValues

            elif self.inputtype == self.JOYHATRELEASED:
                
                if not self.keycode in joy.hatValues and self.prevstate == 1:
                   
                   self.active = self.scalar
                   
                else:
                    
                    self.active = 0
                    
                self.prevstate = self.keycode in joy.hatValues
            
            elif self.inputtype == self.JOYAXISDOWN:
                
                av = joy.axisValues[self.keycode]
                
                pressed = abs(av) > self.deadzone and math.copysign(1, av) == self.axisdirection
                
                if pressed:
                    
                    self.active = self.scalar
                    
                else:
                    
                    self.active = 0.0
            
            elif self.inputtype == self.JOYAXISUP:
                
                av = joy.axisValues[self.keycode]
                
                pressed = abs(av) > self.deadzone and math.copysign(1, av) == self.axisdirection
                
                if not pressed:
                    
                    self.active = self.scalar
                    
                else:
                    
                    self.active = 0.0
            
            elif self.inputtype == self.JOYAXISPRESSED:
                
                av = joy.axisValues[self.keycode]
                
                pressed = abs(av) >= self.deadzone and math.copysign(1, av) == self.axisdirection
                
                if pressed and self.prevstate == 0:
                    
                    self.active = self.scalar
                    
                else:
                    
                    self.active = 0.0
                    
                self.prevstate = pressed
            
            elif self.inputtype == self.JOYAXISRELEASED:
                
                av = joy.axisValues[self.keycode]
                
                pressed = abs(av) >= self.deadzone and math.copysign(1, av) == self.axisdirection
                
                if not pressed and self.prevstate == 1:
                    
                    self.active = self.scalar
                    
                else:
                    
                    self.active = 0.0
                    
                self.prevstate = pressed

            elif self.inputtype == self.JOYAXIS:
                
                av = joy.axisValues[self.keycode]

                if abs(av) > self.deadzone and math.copysign(1, av) == self.axisdirection:
                    
                    self.active = abs(av) * self.scalar
                    
                else:
                    
                    self.active = 0.0

        if self.inputtype == self.MOUSEAXIS:
            
            av = logic.mouse.position[self.keycode] - self.prevpos[self.keycode]
            
            if math.copysign(1, av) == self.axisdirection and abs(av) > 0.001:
            
                self.active = abs(av) * self.scalar
                
            else:
                
                self.active = 0.0
                
            self.prevpos = [0.5, 0.5]#logic.mouse.position

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
        
        self.events = {}
        self.bindings = {}
        
    def Add(self, bindingname, inputtype, keycode, group = "default", axisdir = 1, deadzone = 0.1, joyindex = 0, scalar = 1.0):
        
        """
        Add a key binding.
        
        bindingname = name of the binding to create (i.e. 'left', 'jump', 'run', 'interact'...)
        
        group = a string that designates what group to add this binding to. For example, you might add all of the joystick
        bindings to a 'joystick' group, and all of the keyboard bindings to a 'keyboard' group.
        
        The other arguments are just passed to the CInputKey class instance.
        """
        
        if not group in self.events:
                
            self.events[group] = {}
                
        if not bindingname in self.events[group]:
            
            #if not group in self.events:        # Set up the events dictionary
            
            #    self.events[group] = {}
                
            self.events[group][bindingname] = []
               
            self.bindings[bindingname] = 0
        
        self.events[group][bindingname].append(CInputKey(inputtype, keycode, axisdir, deadzone, joyindex, scalar))
        
    def Poll(self, group = "default"):
        
        """
        Poll the bindings for updates.
        """
        
        for binding in self.events[group]:
     
            self.bindings[binding] = 0
            
            for input in self.events[group][binding]:
                
                input.Poll()
               
                if input.active:
              
                    self.bindings[binding] = input.active
      