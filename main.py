import pygame
from pygame import QUIT, KEYDOWN
from pygame.locals import K_ESCAPE, K_RETURN
import time

from polygon_builder import PolygonBuilder
from config import WINDOW_TITLE, WINDOW_SIZE, RED, BLUE, YELLOW
from polygon_utils import triangulate, random_in_polygon, _ear_clipping_triangulation, _ear_clipping_triangulation_old

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

				# diags, tris = triangulate(poly)
				# for i,j in diags:
					# pygame.draw.line(screen, YELLOW, poly[i], poly[j], 1)

				# screen.fill((0,0,0)) # Clear screen

				# for i,j,k in tris:
				# 	pygame.draw.lines(screen, YELLOW, True, (poly[i], poly[j], poly[k]), 3)

				# points = random_in_polygon(poly, 5000)
				# for p in points:
				# 	pygame.draw.circle(screen, YELLOW, p, 1)

				a = time.time()
				diags, tris = _ear_clipping_triangulation(poly)
				b = time.time()
				print(f'new: {b-a}')

				a = time.time()
				diags, tris = _ear_clipping_triangulation_old(poly)
				b = time.time()
				print(f'old: {b-a}')

				for i,j,k in tris:
					pygame.draw.lines(screen, YELLOW, True, (poly[i], poly[j], poly[k]), 3)

				pygame.display.flip() # Update the display

def is_quit_event(event):
	'Returns true if event is a quit event'
	return event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE
		
if __name__ == '__main__':
	main()
