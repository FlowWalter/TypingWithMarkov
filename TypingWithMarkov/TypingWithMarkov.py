import pygame
import sys
import pygame.freetype
import GUI
import time
import textwrap
from pygame.locals import *

class TWMgui(GUI.GUI):

	def __init__(self):
		
		GUI.GUI.__init__(self, (800,600), "This is a smaller test")
		self.time_end = 0
		
		exit_button = GUI.Button((700,10), (50,30), "EXIT", (0, 100, 200))
		exit_button.onclick = self.exit
		self.buttons.append(exit_button)

		reset_button = GUI.Button((645,10), (55,30), "RESET", (0, 200, 100))
		reset_button.onclick = self.reset_button_clicked
		self.buttons.append(reset_button)

		self.info_caption = GUI.Caption((10, 10), (300, 50), "", 1, (0,0,0), (255,255,200))
		self.captions.append(self.info_caption)

		self.time_caption = GUI.Caption((10, 70), (250, 50), "0 seconds", 1, (0,0,0), (200,255,255))
		self.captions.append(self.time_caption)

		self.wordCount_caption = GUI.Caption((300, 10), (250, 50), "0 words out of " + str(len(self.words)) + " correct",  \
												1, (0,0,0), (200,255,255))
		self.captions.append(self.wordCount_caption)

		self.WPM_caption = GUI.Caption((300, 70), (300, 50), "0 WPM", 1, (0,0,0), (255,255,200))
		self.captions.append(self.WPM_caption)

		self.input_word = GUI.TypeTextInput()
		self.input_word.active = True
		self.text_inputs.append(self.input_word)

	def reset_button_clicked(self):
		self.input_word.active = True
		self.input_word.text = ""
		self.time_caption.text = "0 seconds"
		self.reset()

	def inloop(self): 		
		self.info_caption.text = "Words Typed: " + str(self.wordCounter) + \
								 " out of: " + str(len(self.words))
		
		self.wordCount_caption.text = str(self.correctWords) + " words out of " + str(len(self.words)) + " correct"
		if self.active == True: #correct 1 word correct plurality at some point
			self.time_end = (time.time() - self.time_start)
			self.time_caption.text = str(int(time.time() - self.time_start)) + " seconds"

		if self.completed == True:
			multiplier = 60 / self.time_end
			WPM = self.correctWords * multiplier
			self.WPM_caption.text = str(int(WPM)) + " WPM"
		


if __name__ == "__main__":

	twmGUI = TWMgui()
	twmGUI.run()