import pygame
from pygame.locals import K_ESCAPE, KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_BACKSPACE, K_p
from math import dist

class PolygonBuilder:
    
    EDGE_SIZE = 2
    VERTEX_SIZE = 3
    MAX_SNAP_DISTANCE = 15

    RED = (255,0,0)
    GREEN = (0,255,0)
    BLACK = (0,0,0)

    def __init__(self, window_size = (650,650)):
        pygame.init()
        pygame.display.set_caption('Polygon Builder')
        self.screen = pygame.display.set_mode(window_size)
        self.polygon = []
        self.polygon_closed = False
        self.needs_draw = True

    def run(self):
        pygame.event.clear()

        while True:

            if self.needs_draw:
                self.needs_draw = False;
                self._draw_screen()
            
            event = pygame.event.wait()
            if event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self._add_vertex(pos)
                self.needs_draw = True
            elif event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE: # Quit
                break
            elif event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    self._delete_vertex()
                    self.needs_draw = True

        if self.polygon_closed and not any(self._get_self_intersections()):
            return self.polygon[:-1]

    def _draw_screen(self):
        self.screen.fill(PolygonBuilder.BLACK) # Clear screen
        self._draw_polygon()
        pygame.display.flip() # Update the display

    def _draw_polygon(self):
        has_intersection = self._get_self_intersections()
        for i in range(len(self.polygon) - 1):
            edge_color = PolygonBuilder.RED if has_intersection[i] else PolygonBuilder.GREEN
            pygame.draw.line(self.screen, edge_color, self.polygon[i], self.polygon[i+1], PolygonBuilder.EDGE_SIZE)
        for p in self.polygon:
            pygame.draw.circle(self.screen, PolygonBuilder.RED, p, PolygonBuilder.VERTEX_SIZE)

    def _add_vertex(self, pos):
        if not self.polygon_closed:
            if len(self.polygon) >= 3 and dist(self.polygon[0], pos) <= PolygonBuilder.MAX_SNAP_DISTANCE: 
                pos = self.polygon[0]
                self.polygon_closed = True
            self.polygon.append(pos)

    def _delete_vertex(self):
        if self.polygon:
            del self.polygon[-1]
            self.polygon_closed = False

    def _get_self_intersections(self):
        n = len(self.polygon) - 1

        idx = [False]*n
        for i in range(n):
            for j in range(i+2, n):
                if not (self.polygon_closed and (j+1)%n == i) and self._has_intersection(i, j):
                    idx[i] = True
                    idx[j] = True
        return idx

    def _has_intersection(self, i, j):
        n = len(self.polygon)

        a = self.polygon[i]
        b = self.polygon[(i+1)%n]
        c = self.polygon[j]
        d = self.polygon[(j+1)%n]

        return ((self._left_of_line(c,a,b) != self._left_of_line(d,a,b) and
                self._left_of_line(a,c,d) != self._left_of_line(b,c,d)) or
                self._on_line(c,a,b) or self._on_line(d,a,b) or self._on_line(a,c,d) or self._on_line(b,c,d))

    def _left_of_line(self, c,a,b):
        return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]) > 0

    def _on_line(self, c,a,b):
        return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0]) == 0
