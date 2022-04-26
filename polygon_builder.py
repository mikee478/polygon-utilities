import pygame
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, K_BACKSPACE
from math import dist
from config import RED, GREEN, BLACK
from polygon_utils import left_of_line, on_segment, segment_segment_intersect

class PolygonBuilder:
	
	EDGE_SIZE = 2
	VERTEX_SIZE = 3
	MAX_SNAP_DIST = 15

	def __init__(self, screen):
		self._polygon = []
		self._polygon_closed = False
		self._needs_draw = True
		self._screen = screen

	def update(self, event):
		if self._needs_draw:
			self._needs_draw = False;
			self._draw_screen()
		
		if event.type == MOUSEBUTTONDOWN:
			pos = pygame.mouse.get_pos()
			self._add_vertex(pos)
			self._needs_draw = True
		elif event.type == KEYDOWN and event.key == K_BACKSPACE:
				self._delete_vertex()
				self._needs_draw = True

	def get_polygon(self):
		if self._polygon_closed and not self._intersections():
			return self._polygon[:-1]

	def _draw_screen(self):
		self._screen.fill(BLACK) # Clear screen
		self._draw_polygon()
		pygame.display.flip() # Update the display

	def _draw_polygon(self):
		inter = self._intersections()
		for i in range(len(self._polygon) - 1):
			edge_color = RED if i in inter else GREEN
			pygame.draw.line(self._screen, edge_color, self._polygon[i], self._polygon[i+1], PolygonBuilder.EDGE_SIZE)
		
		for p in self._polygon:
			pygame.draw.circle(self._screen, RED, p, PolygonBuilder.VERTEX_SIZE)

	def _add_vertex(self, pos):
		if not self._polygon_closed:
			if len(self._polygon) >= 3 and dist(self._polygon[0], pos) <= PolygonBuilder.MAX_SNAP_DIST: 
				pos = self._polygon[0]
				self._polygon_closed = True
			self._polygon.append(pos)

	def _delete_vertex(self):
		if self._polygon:
			del self._polygon[-1]
			self._polygon_closed = False

	def _intersections(self):
		n_edges = len(self._polygon) - 1

		idx = set()
		for i in range(n_edges):
			for j in range(i+2, n_edges):
				if not (self._polygon_closed and (j+1)%n_edges == i):
					seg1 = (self._polygon[i],self._polygon[i+1])
					seg2 = (self._polygon[j],self._polygon[j+1])
					if segment_segment_intersect(seg1, seg2):
						idx.add(i)
						idx.add(j)
		return idx
