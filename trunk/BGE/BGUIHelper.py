
import bgui, time

class AnimatedImage(bgui.Image):
    
    def __init__(self, parent, img, name=None, aspect=None, size=[0, 0], pos=[0, 0],
                 coords=[(0, 0), (1, 0), (1, 1), (0, 1)], interp_mode=bgui.BGUI_LINEAR, sub_theme='', options=bgui.BGUI_DEFAULT):
        
        self.coords = coords
        
        self.anim = [0]
        self.anim_fps = 15
        self.anim_timer = time.clock()
        self.anim_frame = 0
                 
        super().__init__(parent, img, name, aspect, size, pos, coords, interp_mode, sub_theme)
        
    @property
    def coords(self):
        """The type of image filtering to be performed on the texture."""
        return self.coords
    
    @coords.setter
    def coords(self, value):
        self._coords = value
        self.texco = value
        self._orig_texco = list(value)
        self._orig_texcosize = [value[0][0] - value[2][0], value[2][1] - value[0][1]]
        
    def _draw(self):
    
        if self.anim_fps == 0:  # Pause the timer
            
            self.anim_timer += 1 / logic.getLogicTicRate()
            
        else:
            
            if time.clock() - self.anim_timer > 1 / abs(self.anim_fps):
                
                self.anim_timer = time.clock()
                                
                if self.anim_fps > 0:
                    self.anim_frame += 1
                elif self.anim_fps < 0:
                     self.anim_frame -= 1
            
                if self.anim_frame >= len(self.anim) - 1:
                    
                    self.anim_frame -= len(self.anim)
                
                elif self.anim_frame < 0:
                    
                    self.anim_frame += len(self.anim)
  
                new_texco = []
                            
                for x in self._orig_texco:

                    new_texco.append([x[0], x[1] + (self._orig_texcosize[1] * self.anim[self.anim_frame])])
                    
                self.texco = new_texco
                
        super()._draw()   
