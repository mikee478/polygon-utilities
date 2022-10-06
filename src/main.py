import pygame
from pygame import QUIT, KEYDOWN
from pygame.locals import (
	K_ESCAPE, K_BACKSPACE, 
	K_t, K_r, MOUSEBUTTONDOWN)

from polygon_renderer import PolygonRenderer
from polygon_builder import PolygonBuilder

def main():
	pygame.init()

	builder = PolygonBuilder()
	renderer = PolygonRenderer(builder)

	while True:
		event = pygame.event.wait()

		if is_quit_event(event):
			break
		else:
			if event.type == MOUSEBUTTONDOWN:
				builder.add_vertex(event.pos)
				renderer.draw_polygon()
			if event.type == KEYDOWN:
				if event.key == K_BACKSPACE:
					builder.delete_vertex()
					renderer.draw_polygon()
				elif event.key == K_t:
					renderer.draw_triangulation()
				elif event.key == K_r:
					renderer.draw_random_points()

def is_quit_event(event):
	'Returns true iff event is a quit event'
	return event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE

if __name__ == '__main__':
	main()
