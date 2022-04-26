import pygame
from pygame import QUIT, KEYDOWN
from pygame.locals import K_ESCAPE, K_RETURN

from polygon_builder import PolygonBuilder
from config import WINDOW_TITLE, WINDOW_SIZE, RED, BLUE

from polygon_utils import is_ccw, point_inside

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

				for x in range(0,WINDOW_SIZE[0],1):
					for y in range(0,WINDOW_SIZE[1],1):
						p = (x,y)
						color = BLUE if point_inside(polygon, p) else RED
						screen.set_at(p, color)
				pygame.display.flip() # Update the display

def is_quit_event(event):
	return event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE
		
if __name__ == '__main__':
	main()
