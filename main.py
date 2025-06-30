import pygame
import sys
pygame.font.init()

WIDTH, HEIGHT = 800, 600

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

main_font = pygame.font.SysFont('comicsans', 30)

class Letters:
	def __init__(self):
		self.letters = [chr(i) for i in range(65, 91)]
		self.letters_surfaces = [main_font.render(letter, 1, 'black') for letter in self.letters] # using assci to draw letters
		self.circles_center = []
		self.letters_rects = [] # this hold a tuple of (rect, letter)
		

	def draw(self, window):
		letter_x, letter_y = 90, 450

		for i in range(len(self.letters_surfaces)):
			'''
			So look at me first of all i'll draw the letter surf on the screen then,
			i will add the center of the rectangle (of the letter surf) which is the top left of it is (letter_x, letter_y) to get the 
			center of the letter and why i'm getting the center to pass it to self.circles_center to draw the circles (letters edges)
			'''

			window.blit(self.letters_surfaces[i], (letter_x, letter_y))
			self.circles_center.append(self.letters_surfaces[i].get_rect(topleft=(letter_x, letter_y)).center)

			if i == 12: # Do Another Row
				letter_y += 50
				letter_x = 90
			else:
				letter_x += 50
		
		self.draw_letters_edges(window)

	def draw_letters_edges(self, window):
		for i in range(len(self.circles_center)):
			rect = pygame.draw.circle(window, 'black', self.circles_center[i], 20, 3, True, True, True, True)
			self.letters_rects.append((rect, self.letters[i]))

letters = Letters()

def draw(window, letters):
	letters.draw(window)


while True:

	WIN.fill((255, 255, 255))

	draw(WIN, letters)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				pygame.quit()
				sys.exit()
			

	clock.tick(FPS)
	pygame.display.update()