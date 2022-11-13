import pygame

from polygon_utils import triangulate, random_in_polygon, compute_convex_hull, compute_visibility_polygon
from config import WINDOW_TITLE, WINDOW_SIZE, RED, GREEN, BLACK, YELLOW, WHITE

class PolygonRenderer:
	EDGE_SIZE = 2
	VERTEX_SIZE = 3
	POINT_SIZE = 1

	def __init__(self, builder):
		pygame.display.set_caption(WINDOW_TITLE)
		self._screen = pygame.display.set_mode(WINDOW_SIZE)
		self._builder = builder

		self._font = pygame.font.SysFont('arial', 14)
		self._controls = [
			'Click = Add Vertex',
			'Delete = Remove Last Vertex',
			'T = Triangulate',
			'R = Random Points',
			'H = Convex Hull',
			'V = Visibility Polygon'
		]

		self.bounds = [
			(-1,-1),
			(-1,WINDOW_SIZE[1]+1),
			(WINDOW_SIZE[0]+1,WINDOW_SIZE[1]+1),
			(WINDOW_SIZE[0]+1,-1)
		]

		self._clear_screen()
		self._draw_controls()
		self._update_display()

	def _clear_screen(self):
		'Draw the screen black'
		self._screen.fill(BLACK)

	def _update_display(self):
		'Update the full display Surface to the screen'
		pygame.display.flip()

	def _draw_controls(self):
		'Draw the controls'
		for i,s in enumerate(self._controls):
			self._screen.blit(self._font.render(s, True, WHITE), (4,2+i*14))

	def _draw_polygon(self):
		'Draw the polygon'''
		polygon = self._builder.get_polygon()
		inter = self._builder.intersections()

		n_edges = len(polygon)-1
		for i in range(n_edges):
			p1 = polygon[i]
			p2 = polygon[i+1]
			color = RED if ((p1,p2) in inter or (p2,p1) in inter) else GREEN
			pygame.draw.line(self._screen, color, p1, p2, PolygonRenderer.EDGE_SIZE)

		if self._builder.is_closed():
			p1 = polygon[-1]
			p2 = polygon[0]
			color = RED if ((p1,p2) in inter or (p2,p1) in inter) else GREEN
			pygame.draw.line(self._screen, color, p1, p2, PolygonRenderer.EDGE_SIZE)

		for p in polygon:
			pygame.draw.circle(self._screen, RED, p, PolygonRenderer.VERTEX_SIZE)

	def draw_polygon(self):
		'Clear screen, draw polygon, draw controls, and update the screen'
		self._clear_screen()
		self._draw_polygon()
		self._draw_controls()
		self._update_display()

	def draw_triangulation(self):
		'If the polygon is simple, draws a triangulation'
		self._clear_screen()
		self._draw_polygon()

		if self._builder.is_simple():
			polygon = self._builder.get_polygon()
			diags, tris = triangulate(polygon)
			for (i,j) in diags:
				pygame.draw.line(self._screen, YELLOW, polygon[i], polygon[j], PolygonRenderer.EDGE_SIZE)

		self._draw_controls()
		self._update_display()

	def draw_random_points(self, n=2500):
		'''If the polygon is simple, draws n, random, uniformly distributed 
		points from within the polygon'''
		self._clear_screen()
		self.draw_polygon()

		if self._builder.is_simple():
			polygon = self._builder.get_polygon()
			points = random_in_polygon(polygon, n)
			for p in points:
				pygame.draw.circle(self._screen, YELLOW, p, PolygonRenderer.POINT_SIZE)

		self._draw_controls()
		self._update_display()

	def draw_convex_hull(self):
		'If the polygon is simple, draws its convex hull'
		self._clear_screen()
		self.draw_polygon()

		if self._builder.is_simple():
			polygon = self._builder.get_polygon()
			conv_hull = compute_convex_hull(polygon)
			n = len(conv_hull)
			for i in range(n):
				p1 = conv_hull[i]
				p2 = conv_hull[(i+1)%n]
				pygame.draw.line(self._screen, YELLOW, p1, p2, PolygonRenderer.EDGE_SIZE)

		self._draw_controls()
		self._update_display()

	def draw_visibility_polygon(self):
		'Draw the visibility polygon'''
		self._clear_screen()
		self._draw_polygon()

		p = pygame.mouse.get_pos()
		poly = self._builder.get_polygon()
		is_closed = self._builder.is_closed()
		points = compute_visibility_polygon(p, poly, is_closed, self.bounds)
		for p2 in points:
			pygame.draw.line(self._screen, YELLOW, p, p2, PolygonRenderer.EDGE_SIZE)

		self._draw_controls()
		self._update_display()
