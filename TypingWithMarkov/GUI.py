import pygame
import pygame.freetype
import threading
import sys
import time
import stoppablethread
from pygame.locals import *



class TextInput(pygame.Surface):
	def __init__(self, pos, font_size, size,
				 text="", margin=0, text_color=(55,55,55), 
				 background_color=(200,200,200)):
		pygame.Surface.__init__(self,size)
		self.speed = 2
		self.text = text
		self.active = False
		self.pos = pos
		self.size = size
		self.font_size = font_size
		self.text_color = text_color
		self.background_color = background_color
		self.margin = margin

		self.active_bg_color = (min(self.background_color[0]+20,255), min(self.background_color[1]+20,255), min(self.background_color[2]+20,255))

	def onclick(self):
		self.active = True

	def contains(self, pos):
		return (pos[0] >= self.pos[0] and\
		 pos[1] >= self.pos[1] and\
		 pos[0] <= self.pos[0]+self.size[0] and\
		 pos[1] <= self.pos[1]+self.size[1])

	def blit_on(self,surface):
		if self.active:
			self.fill(self.active_bg_color)
		else:
			self.fill(self.background_color)
		font = pygame.freetype.Font(None, self.font_size)
		text_surface, rect = font.render(self.text, self.text_color)
		self.blit(text_surface, (self.margin, self.margin))
		surface.blit(self, self.pos)

	def key_pressed(self, key):
		self.text += chr(key)

class TypeTextInput(TextInput):

	def __init__(self):
		TextInput.__init__(self, (10, 300), 30, (800, 100))
				

	def key_pressed(self, key, ctrl):
		#print key

		if key == 13: # ENTER
			self.text = ""
		elif key == 8: # BACKSPACE
			if ctrl:
				counter = -1
				if len(self.text) > 0:
					currentLetter = self.text[counter]
					while currentLetter == " ":
						counter = counter - 1
						nCounter = counter * -1
						if nCounter < len(self.text):
							currentLetter = self.text[counter]
							
						else:
							break
					self.text = self.text[:counter]
					self.text = self.text + currentLetter
					while currentLetter != " " and currentLetter != "":
						counter = counter - 1
						nCounter = counter * -1
						if nCounter < len(self.text):
							currentLetter = self.text[counter]
							
						else:
							break
					self.text = self.text[:counter]
					self.text = self.text + currentLetter
			else:
				self.text = self.text[:-1]
		elif key in range(256):
			self.text += chr(key)

	def key_held(self, key):
		if key == 8:
			self.text = self.text[:-1]






class Caption(pygame.Surface):
	def __init__(self, pos, font_size, size, text, 
				 margin=0, text_color = (150,150,150),
				 background_color=(200,255,255)):
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
		text_surface, rect = font.render(self.text, self.text_color)
		self.blit(text_surface, (self.margin, self.margin))
		surface.blit(self, self.pos)

class Button(pygame.Surface):
	def __init__(self, pos, size, caption="",
				 color=(100,100,100), 
				 text_color = (0,0,0)):
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

		self.word_caption = Caption((10, 100), 100, (800, 100), "Test", 0, (0,0,0))
		self.captions.append(self.word_caption)

		self.input_word = TypeTextInput()
		self.input_word.active = True
		self.text_inputs.append(self.input_word)

	def run(self):
		pygame.key.set_repeat(300, 50)
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
					for text_input in self.text_inputs:
						if text_input.contains(event.pos):
							text_input.onclick()
						else:
							text_input.active = False

				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					for button in self.buttons:
						if button.pressed and button.onclick != None:
							button.onlick()
						button.pressed = False

				elif event.type == pygame.KEYDOWN:
					for text_input in self.text_inputs:
						if text_input.active:
							pygame.event.pump()
							modKeys = pygame.key.get_mods()
							ctrl = False
							if modKeys and KMOD_LCTRL:
								ctrl = True
							text_input.key_pressed(event.key, ctrl)

				elif event.type == pygame.KEYUP:
					pygame.event.clear()
							

			self.inloop()
			self.screen.fill((255,255,255))


			for button in self.buttons:
				button.blit_on(self.screen)
				
			for caption in self.captions:
				caption.blit_on(self.screen)

			for text_input in self.text_inputs:
				text_input.blit_on(self.screen)

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