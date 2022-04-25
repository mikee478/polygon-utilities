import pygame
from pygame import QUIT, KEYDOWN
from pygame.locals import K_ESCAPE, K_RETURN

from polygon_builder import PolygonBuilder
from config import WINDOW_TITLE, WINDOW_SIZE

from polygon_utils import is_ccw

def main():
	pygame.init()
	pygame.display.set_caption(WINDOW_TITLE)
	screen = pygame.display.set_mode(WINDOW_SIZE)

	poly_builder = PolygonBuilder(screen)

	while True:
		event = pygame.event.wait()
		poly_builder.update(event)

		if is_quit_event(event):
			break
		elif event.type == KEYDOWN and event.key == K_RETURN:
			polygon = poly_builder.get_polygon()
			if polygon:
				print(f'is_ccw {is_ccw(polygon)}')

def is_quit_event(event):
	return event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE
		
if __name__ == '__main__':
	main()