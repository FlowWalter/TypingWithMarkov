import pygame
import pygame.freetype
import threading
import sys
import time
import stoppablethread
from pygame.locals import *

class Caption(pygame.Surface):
	def __init__(self, pos, font_size, size, text, margin=0, text_color = (150,150,150), background_color=(0,0,0)):
		pygame.Surface.__init__(self,size)

		self.text = text
		self.pos = pos
		self.size = size
		self.font_size = font_size
		self.text_color = text_color
		self.background_color = background_color
		self.margin = margin
	
	def blit_on(self, surface):
		self.fill(self.background_color)
		font = pygame.freetype.Font(None, self.font_size)
		text = font.render(self.text, self.text_color)
		self.blit(text, (self.margin, self.margin))
		surface.blit(self, self.pos)

class Button(pygame.Surface):
	def __init__(self, pos, size, caption="", color=(100,100,100), text_color = (0,0,0)):
		pygame.Surface.__init__(self,size)
		self.onclick = None
		self.pressed = False
		self.hover = False
		self.caption = caption
		self.pos = pos
		self.size = size
		self.color = color
		self.text_color = text_color

		self.margin = 10

		self.pressed_color = (min(self.color[0]+100,255),min(self.color[1]+100,255),min(self.color[2]+100,255))
		self.hover_color = (min(self.color[0]+50,255),min(self.color[1]+50,255),min(self.color[2]+50,255))

	def blit_on(self, surface):
		self.fill(self.color)
		if self.hover:
			self.fill(self.hover_color)
		if self.pressed:
			self.fill(self.pressed_color)

		font = pygame.freetype.Font(None, 16)
		text_surface, rect = font.render(self.caption, self.text_color)
		self.blit(text_surface, (self.margin,self.margin))
		surface.blit(self, self.pos)

	def contains(self, pos):
		return (pos[0] >= self.pos[0] and\
				pos[1] >= self.pos[1] and\
				pos[0] <= self.pos[0]+self.size[0] and\
				pos[1] <= self.pos[1]+self.size[1])



class GUI(stoppablethread.StoppableThread):

	def __init__(self, size):
		stoppablethread.StoppableThread.__init__(self)
		pygame.init()
		self.screen = pygame.display.set_mode(size)
		self.buttons = []
		self.captions = []
		self.sprites = []
		self.text_inputs = []
		self.background_image = None

		exit_button = Button((10,10), (50,30), "EXIT", (0, 100, 200))
		self.buttons.append(exit_button)

	def run(self):
		self.preloop()
		while not self.stopped():
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.exit()
				elif event.type == pygame.MOUSEMOTION:
					for button in self.buttons:
						if button.contains(event.pos):
							button.hover = True
						else:
							button.hover = False
							button.pressed = False
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					for button in self.buttons:
						if button.contains(event.pos):
							button.pressed = True


				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					for button in self.buttons:
						if button.pressed and button.onclick != None:
							button.onlick()
						button.pressed = False

			self.inloop()
			self.screen.fill((255,255,255))


			for button in self.buttons:
				button.blit_on(self.screen)
				
			for caption in self.captions:
				caption.blit_on(self.screen)

			pygame.display.flip()



	def exit(self):
		self.preexit()
		self.stop()

	def preloop(self):
		pass
		
	def inloop(self):
		pass	
		
	def preexit(self):
		pass
	
	def react(self, event):
		pass


if __name__ == "__main__":

	testgui = GUI((800,400))
	testgui.run()