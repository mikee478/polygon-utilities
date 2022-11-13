import pygame
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN, K_BACKSPACE
from math import dist
from config import RED, GREEN, BLACK
from polygon_utils import segment_segment_intersect, is_ccw

class PolygonBuilder:

	MAX_SNAP_DIST = 15

	def __init__(self):
		self._polygon = []
		self._is_closed = False
		self._edge_intersections = set()

	def is_closed(self):
		return self._is_closed

	def is_simple(self):
		'Return true iff polygon is a simple polygon'''
		return self._is_closed and not self.intersections()

	def get_polygon(self):
		'''If the polygon is closed, return a list of tuples representing
		a ccw, closed polygon. Otherwise, a chain of points is returned'''
		p = self._polygon
		if self._is_closed:
			return p if is_ccw(p) else p[::-1]
		else:
			return p

	def add_vertex(self, pos):
		'Add a vertex to the polygon or close the polygon'
		if not self._is_closed and pos not in self._polygon:
			self._edge_intersections.clear()
			if len(self._polygon) >= 3 and dist(self._polygon[0], pos) <= PolygonBuilder.MAX_SNAP_DIST: 
				self._is_closed = True
			else:
				self._polygon.append(pos)

	def delete_vertex(self):
		'Delete the last added vertex'
		self._edge_intersections.clear()
		if self._polygon:
			if self._is_closed:
				self._is_closed = False
			else:
				del self._polygon[-1]

	def intersections(self):
		'Return a set of edge that have intersections'
		if self._edge_intersections:
			return self._edge_intersections

		self._edge_intersections.clear()

		n_edges = len(self._polygon)-1
		for i in range(n_edges):
			seg1 = (self._polygon[i],self._polygon[i+1])
			for j in range(i+2, n_edges):
				seg2 = (self._polygon[j],self._polygon[j+1])
				if segment_segment_intersect(seg1, seg2):
					self._edge_intersections.add(seg1)
					self._edge_intersections.add(seg2)

		if self._is_closed:
			seg1 = (self._polygon[-1],self._polygon[0])
			for i in range(1, n_edges-1):
				seg2 = (self._polygon[i],self._polygon[i+1])
				if segment_segment_intersect(seg1, seg2):
					self._edge_intersections.add(seg1)
					self._edge_intersections.add(seg2)

		return self._edge_intersections
