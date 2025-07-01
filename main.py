import pygame
import sys
pygame.font.init()
from words import words
import random
import os

WIDTH, HEIGHT = 900, 600

WORDS_LEN = len(words)

HANGMAN_IMGS = [pygame.image.load('images/'+img) for img in os.listdir('images/')]

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

main_font = pygame.font.SysFont('comicsans', 30)
current_img = 0

spaces_pos = []

letters_player_get = []

class Letters:
	def __init__(self):
		self.letters = [chr(i) for i in range(65, 91)]
		self.letters_surfaces = [main_font.render(letter, 1, 'black') for letter in self.letters] # using assci to draw letters
		self.circles_center = []
		self.letters_rects = [] # this hold a tuple of (rect, letter)
		self.add = True
		

	def draw(self, window):
		letter_x, letter_y = 130, 450

		for i in range(len(self.letters_surfaces)):
			'''
			So look at me first of all i'll draw the letter surf on the screen then,
			i will add the center of the rectangle (of the letter surf) which is the top left of it is (letter_x, letter_y) to get the 
			center of the letter and why i'm getting the center to pass it to self.circles_center to draw the circles (letters edges)
			'''

			window.blit(self.letters_surfaces[i], (letter_x, letter_y))
			if self.add:
				self.circles_center.append(self.letters_surfaces[i].get_rect(topleft=(letter_x, letter_y)).center)

			if i == 12: # Do Another Row
				letter_y += 50
				letter_x = 130
			else:
				letter_x += 50
		
		self.draw_letters_edges(window, self.add)
		self.add = False

	def draw_letters_edges(self, window, add):
		for i in range(len(self.circles_center)):
			rect = pygame.draw.circle(window, 'black', self.circles_center[i], 20, 3, True, True, True, True)
			if add:
				self.letters_rects.append((rect, self.letters[i]))

letters = Letters()

def draw(window, letters, hangman_img, letters_player_get, add):
	letters.draw(window)
	window.blit(hangman_img, (120, 200))

	start_x, end_x = 370, 400
	for l in word:
		rect = pygame.draw.line(window, 'black', (start_x, 300), (end_x, 300), 3)
		if add:
			spaces_pos.append(rect)
			add = False
		start_x += 40
		end_x += 40
		

	for surf, pos in range(len(letters_player_get)):
		window.blit(surf, (pos.x, pos.y - 50))

def choose_random_word():
	while True:
		if len(words[random.randint(0, WORDS_LEN-1)]) >= 13:
			return words[random.randint(0, WORDS_LEN-1)]

def creat_empty_spaces(word):
	for l in word:
		pygame.draw.line()

def check_letter(player_letter, current_img):
	letter_indices = []
	if player_letter in word:
		letter_indices = [i for i, letter in enumerate(word) if letter[i] == player_letter]
	else:
		current_img += 1

	for l_index in letter_indices:
		letters_player_get.append((main_font.render(player_letter, 1, 'black'), spaces_pos[l_index]))

word = choose_random_word()
add = True

while True:

	WIN.fill((255, 255, 255))

	draw(WIN, letters, HANGMAN_IMGS[current_img], letters_player_get, add)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = pygame.mouse.get_pos()
			for rect, letter in letters.letters_rects:
				if rect.collidepoint(mouse_pos):
					check_letter(letter, current_img)

	clock.tick(FPS)
	pygame.display.update()