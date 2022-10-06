import pygame

from polygon_utils import triangulate, random_in_polygon
from config import (
	WINDOW_TITLE, WINDOW_SIZE, 
	RED, GREEN, BLACK, YELLOW)

class PolygonRenderer:
	EDGE_SIZE = 2
	VERTEX_SIZE = 3
	POINT_SIZE = 1

	def __init__(self, builder):
		pygame.display.set_caption(WINDOW_TITLE)
		self._screen = pygame.display.set_mode(WINDOW_SIZE)
		self._builder = builder

	def draw_polygon(self):
		'Draw polygon edges then vertices'
		polygon = self._builder.get_polygon()
		inter = self._builder.intersections()

		self._clear_screen()

		n_edges = len(polygon)-1
		for i in range(n_edges):
			v1 = polygon[i]
			v2 = polygon[i+1]
			color = RED if ((v1,v2) in inter or (v2,v1) in inter) else GREEN
			pygame.draw.line(self._screen, color, v1, v2, PolygonRenderer.EDGE_SIZE)
		
		if self._builder.is_closed():
			v1 = polygon[-1]
			v2 = polygon[0]
			color = RED if ((v1,v2) in inter or (v2,v1) in inter) else GREEN
			pygame.draw.line(self._screen, color, v1, v2, PolygonRenderer.EDGE_SIZE)

		for p in polygon:
			pygame.draw.circle(self._screen, RED, p, PolygonRenderer.VERTEX_SIZE)
		
		self._update_display()

	def draw_triangulation(self):
		'If the polygon is simple, draws a triangulation'
		if self._builder.is_simple():
			polygon = self._builder.get_polygon()
			diags, tris = triangulate(polygon)
			self._clear_screen()
			self.draw_polygon()
			for (i,j) in diags:
				pygame.draw.line(self._screen, YELLOW, polygon[i], polygon[j], PolygonRenderer.EDGE_SIZE)
			self._update_display()

	def draw_random_points(self, n=2500):
		'''If the polygon is simple, draws n, random, uniformly distributed 
		points from within the polygon'''
		if self._builder.is_simple():
			polygon = self._builder.get_polygon()
			points = random_in_polygon(polygon, n)
			self._clear_screen()
			self.draw_polygon()
			for p in points:
				pygame.draw.circle(self._screen, YELLOW, p, PolygonRenderer.POINT_SIZE)
			self._update_display()

	def _clear_screen(self):
		'Draw the screen black'
		self._screen.fill(BLACK)

	def _update_display(self):
		'Update the full display Surface to the screen'
		pygame.display.flip()
