import pygame
from pygame import QUIT, KEYDOWN
from pygame.locals import ( MOUSEBUTTONDOWN, MOUSEMOTION, 
	K_BACKSPACE, K_ESCAPE, K_t, K_r, K_h, K_v)

from polygon_renderer import PolygonRenderer
from polygon_builder import PolygonBuilder

def main():
	pygame.init()
	pygame.font.init()

	builder = PolygonBuilder()
	renderer = PolygonRenderer(builder)

	vis_polygon = False

	while True:
		event = pygame.event.wait()

		if is_quit_event(event):
			break
		else:
			if event.type == MOUSEBUTTONDOWN:
				builder.add_vertex(event.pos)
				renderer.draw_polygon()
				vis_polygon = False
			elif event.type == MOUSEMOTION:
				if vis_polygon:
					renderer.draw_visibility_polygon()
			elif event.type == KEYDOWN:
				if event.key == K_BACKSPACE:
					builder.delete_vertex()
					renderer.draw_polygon()
					vis_polygon = False
				elif event.key == K_t:
					renderer.draw_triangulation()
					vis_polygon = False
				elif event.key == K_r:
					renderer.draw_random_points()
					vis_polygon = False
				elif event.key == K_h:
					renderer.draw_convex_hull()
					vis_polygon = False
				elif event.key == K_v:
					vis_polygon = True
					renderer.draw_visibility_polygon()

def is_quit_event(event):
	'Returns true iff event is a quit event'
	return event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE

if __name__ == '__main__':
	main()
