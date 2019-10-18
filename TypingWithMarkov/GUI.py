import pygame
import pygame.freetype
import threading
import sys
import time
import stoppablethread
import textwrap
from pygame.locals import *



class AnimatedSprite(pygame.Surface, stoppablethread.StoppableThread):

	def __init__(self, pos, size):
		pygame.Surface.__init__(self, size)
		stoppablethread.StoppableThread.__init__(self)
		
		self.frames = []
		self.speed = 6 # frames per second
		self.frame_counter = 0
		self.background_color = (0,0,0)
		self.pos = pos
		
	
	def blit_on(self, surface):
		
		self.fill(self.background_color)
		self.blit(self.frames[self.frame_counter], (0,0))
		surface.blit(self, self.pos)
		
	def run(self):
		while not self.stopped():
			time.sleep(1. / self.speed)
			
			self.frame_counter += 1
			if self.frame_counter >= len(self.frames): self.frame_counter = 0
		


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
		#font = pygame.freetype.Font(None, self.font_size)
		#text_surface, rect = font.render(self.text, self.text_color)
		font = pygame.font.Font(None, self.font_size)
		text_surface = font.render(self.text, 1, self.text_color)

		self.blit(text_surface, (self.margin, self.margin))
		surface.blit(self, self.pos)

	def key_pressed(self, key):
		self.text += chr(key)

class TypeTextInput(TextInput):

	def __init__(self):
		TextInput.__init__(self, (10, 500), 30, (800, 100))
				

	def key_pressed(self, key, ctrl, shift):
		#print key

		if key == 13 or key == K_SPACE: # ENTER
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
					nCounter = 0;
					while currentLetter != " " and currentLetter != "":
						counter = counter - 1
						nCounter = counter * -1
						if nCounter <= len(self.text):
							currentLetter = self.text[counter]
							
						else:
							break
					self.text = self.text[:counter]
					if nCounter <= len(self.text):
						self.text = self.text + currentLetter
			else:
				self.text = self.text[:-1]
		elif key in range(256):
			if shift:
				self.text += chr(key).upper()
			else:
				self.text += chr(key)







class Caption(pygame.Surface):
	def __init__(self, pos, size, text, 
				 margin, text_color = (150,150,150),
				 background_color=(220,220,220)):
		pygame.Surface.__init__(self,size)

		
		self.text = text
		self.pos = pos
		self.size = size
		self.text_color = text_color
		self.background_color = background_color
		self.margin = margin
	
	def blit_on(self, surface):
		self.fill(self.background_color)
		font = pygame.font.Font(None, 30)
		text_surface = font.render(self.text, 1, self.text_color)
		self.blit(text_surface, (self.margin, self.margin))
		surface.blit(self, self.pos)

	def updateColor(self, color):
		self.text_color = color

	def updateBackgroundColor(self, color):
		self.background_color = color

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

		font = pygame.freetype.Font(None, 12) #replace none to get a font
		text_surface, rect = font.render(self.caption, self.text_color)
		self.blit(text_surface, (self.margin,self.margin))
		surface.blit(self, self.pos)

	def contains(self, pos):
		return (pos[0] >= self.pos[0] and\
				pos[1] >= self.pos[1] and\
				pos[0] <= self.pos[0]+self.size[0] and\
				pos[1] <= self.pos[1]+self.size[1])



class GUI(stoppablethread.StoppableThread):

	def __init__(self, size, suppliedText):
		stoppablethread.StoppableThread.__init__(self)
		pygame.init()
		pygame.freetype.Font.origin = True
		pygame.freetype.Font.pad = True
		self.screen = pygame.display.set_mode(size)
		self.time_start = time.time()
		self.correctWords = 0
		self.incorrectWords = 0
		self.active = False
		self.completed = False
		self.tempWord1 = ""
		self.tempWord2 = ""
		self.wordCounter = 0
		self.checkWord = False

		#self.text = "This is a much longer test string that hopefully goes off the screen and wraps. Oh look it's even longer now"
		self.text = suppliedText
		self.buttons = []
		self.captions = []
		self.sprites = []
		self.text_inputs = []
		self.background_image = None

		wrapper = textwrap.wrap(self.text, 75)
		
		self.line = []
		self.words = []
		offsetX = 0
		offsetY = 0
		renderedSizeX = 0
		renderedSizeY = 0
		for line in wrapper:
			self.line.append(line)
			words = line.split()
			for word in words:
				self.words.append(word)
				font = pygame.font.Font(None, 30)
				text_surface = font.render(word, 1, (0,0,0))
				renderedSizeX = text_surface.get_width()
				renderedSizeY = text_surface.get_height()
				self.word_caption = Caption((10 + offsetX, 150 + offsetY),
											(renderedSizeX + 10, renderedSizeY + 10),
											word, 1, (0,0,0), (255,255,255))
				self.captions.append(self.word_caption)
				offsetX += renderedSizeX
				offsetX += 10
			offsetX = 0
			offsetY += renderedSizeY
			offsetY += 30
		


		#exit_button = Button((700,10), (50,30), "EXIT", (0, 100, 200))
		#exit_button.onclick = self.exit
		#self.buttons.append(exit_button)



		#self.input_word = TypeTextInput()
		#self.input_word.active = True
		#self.text_inputs.append(self.input_word)

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
							button.onclick()
						button.pressed = False

				elif event.type == pygame.KEYDOWN:
					for text_input in self.text_inputs:
						if text_input.active:
							#handle the start time only when typing starts on a reset prompt
							if self.active == False:
								self.time_start = time.time()
							self.active = True
							

							pygame.event.pump()
							modKeys = pygame.key.get_mods()
							ctrl = False
							shift = False
							if (modKeys and KMOD_LCTRL) or modKeys and KMOD_RCTRL:
								ctrl = True
							if (modKeys and KMOD_LSHIFT) or (modKeys and KMOD_RSHIFT):
								shift = True
							if event.key == K_SPACE: #handle events triggered by advancing to next word
								self.wordCounter += 1
								self.checkWord = True
								if self.wordCounter < len(self.words):
									self.tempWord1 = self.words[self.wordCounter -1]
									self.tempWord2 = self.input_word.text

							if (event.key == K_r) and (ctrl == True):
								self.reset()
							else:
								text_input.key_pressed(event.key, ctrl, shift)
							

				elif event.type == pygame.KEYUP:
					pygame.event.clear()
			
			if self.wordCounter <= len(self.words):

				if self.wordCounter == len(self.words):
					self.active = False
					self.completed = True

				if self.wordCounter != len(self.words):
					currentWord = self.words[self.wordCounter]
					currentTypedWord = self.input_word.text
					sizeOfCurrent = len(currentTypedWord)
					if currentTypedWord != currentWord[:sizeOfCurrent]:
						self.captions[self.wordCounter].updateColor((255,0,0))

					else:
						self.captions[self.wordCounter].updateColor((0,0,0))
					self.captions[self.wordCounter].updateBackgroundColor((192,192,192))
			
				#if checkwork is true checks if the current word is correct after pressing space or enter
				#and updates the previous word's color accordingly
				if self.wordCounter > 0:
					if self.checkWord == True:
						if self.tempWord1 == self.tempWord2: #correct word
							self.captions[self.wordCounter - 1].updateColor((0,255,0))
							self.correctWords += 1
						else: #incorrect word
							self.captions[self.wordCounter - 1].updateColor((255,0,0))
							self.incorrectWords += 1
					self.checkWord = False
					self.captions[self.wordCounter - 1].updateBackgroundColor((255,255,255))
			else:
				self.wordCounter -= 1
				
				
					
			self.inloop()
			self.screen.fill((255,255,255))


			for button in self.buttons:
				button.blit_on(self.screen)
				
			for caption in self.captions:
				caption.blit_on(self.screen)

			for sprite in self.sprites:
				sprite.blit_on(self.screen)

			for text_input in self.text_inputs:
				text_input.blit_on(self.screen)

			pygame.display.flip()

	def reset(self):
		for caption in self.captions:
			caption.updateBackgroundColor((255,255,255))
			caption.updateColor((0,0,0))
			self.tempWord1 = ""
			self.tempWord2 = ""
			self.checkWord = False
			self.wordCounter = 0
			self.active = False
			self.correctWords = 0
			self.incorrectWords = 0
			self.time_start = 0
			self.completed = False

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