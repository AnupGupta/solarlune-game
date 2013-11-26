
"""
Three-piece windows.
"""

import bgui

from bge import render

class CWindow(bgui.Widget):
	
	def __init__(self, parent, name, image, texco, chunksize = 0.05, size=[0.5, 0.5], pos=[0.0, 0.0], aspect=None, sub_theme='',
			options=bgui.BGUI_DEFAULT, interp_mode = bgui.image.BGUI_LINEAR):		
		"""
		Define a 3x3 window for the texco, and it will be split into thirds.
		"""

		self.chunks = {
			'bottomleft':None,
			'left':None,
			'topleft':None,
			
			'bottom':None,
			'middle':None,
			'top':None,
			
			'bottomright':None,
			'right':None,
			'topright':None,
		}
		
		self.win_size = list(size)
		self.win_pos = list(pos)
		self.chunksize = chunksize
		self.image = image
		self.interp_mode = interp_mode
		
		#print (self.interp_mode)

		bgui.Widget.__init__(self, parent, name, aspect, list(size), list(pos), sub_theme, options)
		
		self.FormWindow(texco)
		
		self._color = [1.0, 1.0, 1.0, 1.0]
		
	def FormWindow(self, texco, update = 0):
		
		"""
		Creates the images that form up the entire window.
		texco = The texture coordinates indicating the entire window, sliced into thirds (the borders, and a center piece)
		update = Whether to create the windows, or just update them
		"""
		
		texco_size = (texco[2][0] - texco[0][0], texco[2][1] - texco[0][1])

		x1 = texco[0][0]
		y1 = texco[0][1]
		
		if not update:
				
			if len(self.chunks) > 0:
				
				for c in self.chunks:
					
					if self.chunks[c] != None:
					
						del self.chunks[c]
						self.chunks[c] = None
		
		for x in range(3):
			
			xt = texco_size[0] / 3
			x2 = x1 + xt
				
			for y in range(3):
				
				yt = texco_size[1] / 3
				y2 = y1 + yt
				
				pos = [0.33 * x, 0.33 * y]
	
				if update:

					if x == 0 and y == 0:
						chunk = 'bottomleft'
					elif x == 1 and y == 0:
						chunk = 'bottom'
					elif x == 2 and y == 0:
						chunk = 'bottomright'
						
					elif x == 0 and y == 1:
						chunk = 'left'
					elif x == 1 and y == 1:
						chunk = 'middle'
					elif x == 2 and y == 1:
						chunk = 'right'
						
					elif x == 0 and y == 2:
						chunk = 'topleft'
					elif x == 1 and y == 2:
						chunk = 'top'
					elif x == 2 and y == 2:
						chunk = 'topright'
						
					self.chunks[chunk].texco = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
					
				else:
	
					aspect = None#render.getWindowWidth() / render.getWindowHeight()
				
					#size = [1.0, render.getWindowWidth() / render.getWindowHeight()]
					
					size = [1.0, 1.0]
					
					chunk = bgui.Image(self, self.image, self.name+'chunk'+str(x)+str(y), aspect = aspect, size = size, pos = pos, 
					texco = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]], interp_mode = self.interp_mode)
		
					#chunk.visible = 0
					
					c = self.chunks
					
					if x == 0 and y == 0:
						c['bottomleft'] = chunk
					elif x == 1 and y == 0:
						c['bottom'] = chunk
					elif x == 2 and y == 0:
						c['bottomright'] = chunk
						
					elif x == 0 and y == 1:
						c['left'] = chunk
					elif x == 1 and y == 1:
						c['middle'] = chunk
					elif x == 2 and y == 1:
						c['right'] = chunk
						
					elif x == 0 and y == 2:
						c['topleft'] = chunk
					elif x == 1 and y == 2:
						c['top'] = chunk
					elif x == 2 and y == 2:
						c['topright'] = chunk
						
				y1 += yt
	
			y1 = texco[0][1]
			x1 += xt	
			
		self.Update()

	def Update(self):
		"""
		Positions and scales the chunks to create a window.
		Also updates the chunks' colors.
		"""
		
		chunks = self.chunks
		
		asr = render.getWindowWidth() / render.getWindowHeight()
	
		#asr *= self.win_size[0] / self.win_size[1]
	
		#cs = ((self.chunksize / asr) / self.win_size[0], self.chunksize / self.win_size[1])

		ps = self.parent.user_size[0] / self.parent.user_size[1]
		
		cs = (self.chunksize / ps / asr / self.win_size[0], self.chunksize / self.win_size[1])

		chunks['bottomleft'].position = [0.0, 0.0]
		chunks['bottomleft'].size = list(cs)
		
		chunks['left'].position = [0.0, cs[1]]
		chunks['left'].size = [cs[0], 1.0 - (cs[1] * 2)]
		
		chunks['topleft'].position = [0.0, 1.0 - cs[1]]
		chunks['topleft'].size = list(cs)
		
		chunks['bottom'].position = [cs[0], 0.0]
		chunks['bottom'].size = [1.0 - (cs[0] * 2), cs[1]]
		
		chunks['middle'].position = list(cs)
		chunks['middle'].size = [1.0 - (cs[0] * 2), 1.0 - (cs[1] * 2)]
		
		chunks['top'].position = [cs[0], 1.0 - cs[1]]
		chunks['top'].size = [1.0 - (cs[0] * 2), cs[1]]
		
		chunks['bottomright'].position = [1.0 - cs[0], 0.0]
		chunks['bottomright'].size = list(cs)
		
		chunks['right'].position = [1.0 - cs[0], cs[1]]
		chunks['right'].size = [cs[0], 1.0 - (cs[1] * 2)]
		
		chunks['topright'].position = [1.0 - cs[0], 1.0 - cs[1]]
		chunks['topright'].size = list(cs)

	def Clicked(self, button = None):
		
		if button == None:
			b = events.LEFTMOUSE
		else:
			b = button
			
		state = [None, None, None]
		
		mouse_pos = list(logic.mouse.position)
		mouse_pos[1] = abs(mouse_pos[1] - 1)

		if logic.mouse.events[b] > 0 and \
		mouse_pos[0] >= self.win_pos[0] and mouse_pos[0] <= self.win_pos[0] + self.win_size[0] and \
		mouse_pos[1] >= self.win_pos[1] and mouse_pos[1] <= self.win_pos[1] + self.win_size[1]:
						
			state = [logic.mouse.events[b], mouse_pos]

		return state

	def _getColor(self):
		return self._color
	
	def _setColor(self, value):
		self._color = value
		
		for c in self.chunks:
			self.chunks[c].color = value

	color = property(_getColor, _setColor)