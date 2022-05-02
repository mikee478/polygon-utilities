import pygame
from pygame import QUIT, KEYDOWN
from pygame.locals import K_ESCAPE, K_RETURN

from polygon_builder import PolygonBuilder
from config import WINDOW_TITLE, WINDOW_SIZE, RED, BLUE, YELLOW
from polygon_utils import triangulate

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
			poly = poly_builder.get_polygon()
			if poly:
				print(f'polygon: {poly}\n')

				diag_idx = triangulate(poly)
				for i,j in diag_idx:
					pygame.draw.line(screen, YELLOW, poly[i], poly[j], 1)

				pygame.display.flip() # Update the display

def is_quit_event(event):
	'Returns true if event is a quit event'
	return event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE
		
if __name__ == '__main__':
	main()
