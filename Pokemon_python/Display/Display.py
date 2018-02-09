import pygame, sys
from pygame.locals import *
from Pokemon_python.GeneratorDB import get_image_path, get_sprite_path
from random import randint

SCALE = 1.5
FRONT_SPRITE_SCALE = 1.25
BACK_SPRITE_SCALE = 1.75
BACKGROUND_SCALE = 1.5


BAR_LENGTH = int (48 * SCALE * BACKGROUND_SCALE)
BAR_HEIGHT = int (2 * SCALE * BACKGROUND_SCALE)


LETTER_SIZE = int (15 * SCALE * BACKGROUND_SCALE)
BACKGROUND_SIZE = (256,144)
SPRITE_SIZE = (96,96)
LOG_SIZE = (256,46)
LOG_TEXT_SHIFT=(17,7)

BLACK = (0, 0, 0)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)


BACKGROUND_DIR = 'Backgrounds/'
ICON_NAME = 'icon'
LOG_NAME  = 'log'
HEALTH_NAME = 'health'
BACKGROUND_NAME = 'background_'+str(randint(0,11))
LETTER_TYPE = 'Courier New'

def get_background_path(name_file):
	return get_image_path(BACKGROUND_DIR+name_file)
def get_cell_path(name_file):
	return get_image_path(BACKGROUND_DIR+name_file)

def pair_mult_num(pair, num):
	return (int(pair[0]*num),int(pair[1]*num))
def scale(pair):
	return pair_mult_num(pair, SCALE)
def scale_bg(pair):
	return pair_mult_num(pair, SCALE*BACKGROUND_SCALE)
def center_to_top_left(pos, sprite_size):
	return (pos[0]-sprite_size[0]/2,pos[1]-sprite_size[1]/2)

_x, _y = SPRITE_SIZE
_b_x, _b_y = pair_mult_num(BACKGROUND_SIZE, BACKGROUND_SCALE)
POS_A1 = (_x/2, _b_y-_y/3)			#(48 ,184) for BG_SCALE = 1.5
POS_A2 = (3*_x/2, _b_y-_y/3)		#(144,184)
POS_F1 = (_b_x-3*_x/2, _b_y/2.1)		#(240,108)
POS_F2 = (_b_x-_x/2, _b_y/2.1)		#(336,108)

POS_BAR_F2 = scale_bg((57,22))
POS_BAR_F1 = scale_bg((50,51))
POS_BAR_A1 = scale_bg((189,107))
POS_BAR_A2 = scale_bg((196,136))

SCREEN_SIZE = pair_mult_num((BACKGROUND_SIZE[0],BACKGROUND_SIZE[1]+LOG_SIZE[1]), BACKGROUND_SCALE) # no es definitivo

pygame.init()
SCREEN = pygame.display.set_mode(scale(SCREEN_SIZE))
FONT = pygame.font.SysFont(LETTER_TYPE, LETTER_SIZE)

class mySprite(pygame.sprite.Sprite):
	def __init__(self, path_image, factor, tl_location):
		pygame.sprite.Sprite.__init__(self)
		image = pygame.image.load(path_image)
		self._image = pygame.transform.scale(image, scale(pair_mult_num(image.get_size(),factor)))
		self._location = scale(tl_location)

	def display(self):
		SCREEN.blit(self._image, self._location)

class Sprite (mySprite):
	def __init__(self, image_file, center):
		path = get_sprite_path(image_file)
		factor = BACK_SPRITE_SCALE if 'back' in image_file else FRONT_SPRITE_SCALE
		tl_location = center_to_top_left(center, pair_mult_num(SPRITE_SIZE, factor))
		mySprite.__init__(self, path, factor, tl_location)

class Background (mySprite):
	def __init__(self, image_file, top_left_location = (0,0)):
		path = get_background_path(image_file)
		tl_location = pair_mult_num(top_left_location, BACKGROUND_SCALE)
		mySprite.__init__(self, path, BACKGROUND_SCALE, tl_location)

class Log (Background):
	def __init__(self, top_left_location):
		Background.__init__(self, LOG_NAME, top_left_location)
		text_pos = (top_left_location[0]+LOG_TEXT_SHIFT[0],top_left_location[1]+LOG_TEXT_SHIFT[1])
		self._text_pos = scale(pair_mult_num(text_pos, BACKGROUND_SCALE))
		self.set_text('')

	def set_text(self, texts):
		self._text_img = [FONT.render(text, 0, BLACK) for text in texts]

	def display(self):
		Background.display(self)
		for i, t_img in enumerate(self._text_img):
			SCREEN.blit(t_img, (self._text_pos[0],self._text_pos[1]+LETTER_SIZE*0.75*i))

class Health (Background):
	def __init__(self):
		Background.__init__(self, HEALTH_NAME)
		self.bar_img_col = [
			(pygame.Rect(POS_BAR_F2[0],POS_BAR_F2[1], BAR_LENGTH, BAR_HEIGHT),GREEN),
			(pygame.Rect(POS_BAR_F1[0],POS_BAR_F1[1], BAR_LENGTH, BAR_HEIGHT),GREEN),
			(pygame.Rect(POS_BAR_A1[0],POS_BAR_A1[1], BAR_LENGTH, BAR_HEIGHT),GREEN),
			(pygame.Rect(POS_BAR_A2[0],POS_BAR_A2[1], BAR_LENGTH, BAR_HEIGHT),GREEN)]

	def set_health_of(indx, act_health, max_health):
		pct = act_health/max_health
		x, y = POS_BAR_F2
		fill = (pct/100.0 * BAR_LENGTH)
		color = GREEN if pct>0.5 else YELLOW if pct>0.25 else RED
		self.bar_img_col[indx] = (pygame.Rect(x, y, fill, BAR_HEIGHT), color)

	def display(self):
		Background.display(self)
		for bar_img, color in self.bar_img_col:
			pygame.draw.rect(SCREEN, color, bar_img)

class Window:
	def __init__(self):
		pygame.display.set_icon(pygame.image.load(get_image_path(ICON_NAME)))
		pygame.display.set_caption('POKEMON DOUBLE BATTLE')
		self.battle_bg = Background(BACKGROUND_NAME)
		self.log = Log((0,BACKGROUND_SIZE[1]))
		self.health = Health()

		poke1 = '1_bulbasaur'
		poke2 = '3_venusaur'
		#1_bulbasaur
		#3_venusaur
		pk_a1 = Sprite(poke1+'_back',  POS_A1)
		pk_a2 = Sprite(poke2+'_back',  POS_A2)
		pk_f1 = Sprite(poke1+'_front', POS_F1)
		pk_f2 = Sprite(poke2+'_front', POS_F2)

		self.visualize_items = [self.battle_bg, pk_f1, pk_f2, pk_a1, pk_a2, self.log, self.health]

	def set_text_log(self, text):
		self.log.set_text(text)

	def visualize(self):
		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
				print('QUIT GAME')
				pygame.quit()
				sys.exit()

			elif event.type == MOUSEBUTTONDOWN and event.button == 1:
				mouse = pygame.mouse.get_pos()
				print(mouse)
				#if Image[1].collidrect(mouse):

			elif event.type == KEYDOWN:
				#if the right arrow is pressed
				if event.key == K_RIGHT or event.key == K_d:
					print('right')
				elif event.key == K_LEFT or event.key == K_a:
					print('left')
				elif event.key == K_UP or event.key == K_w:
					print('up')
				elif event.key == K_DOWN or event.key == K_s:
					print('down')


		for surface in self.visualize_items:
			surface.display()

		pygame.display.update()
