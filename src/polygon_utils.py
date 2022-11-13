import numpy as np
from operator import sub

# Set to true to work with Pygame 
INVERTED_Y_AXIS = True

def is_ccw(poly):
	'Return true iff polygon vertices are counterclockwise.'
	twice_area = 0
	n = len(poly)
	for i in range(len(poly)):
		a = poly[i]
		b = poly[(i+1)%n]
		twice_area += (b[0]-a[0])*(b[1]+a[1])
	return twice_area > 0 if INVERTED_Y_AXIS else twice_area < 0

def point_inside(poly, p, method='raycasting'):
	'Return true iff p is inside poly'
	if method == 'windingnumber':
		return not np.isclose(_winding_number(poly, p),0)
	elif method == 'raycasting':
		return _ray_casting_intersections(poly, p) % 2 == 1
	else:
		raise ValueError('method should be "windingnumber" or "raycasting"')

def _winding_number(poly, p):
	'Compute and return the winding number around p'
	poly = np.array(poly)
	poly -= p # center point on origin

	angles = np.arctan2(poly[:,1],poly[:,0]) # [-pi, pi]

	deltas = np.copy(angles)
	deltas[1:] -= angles[:-1]
	deltas[0] -= angles[-1]

	deltas[deltas <= -np.pi] += 2*np.pi
	deltas[deltas >= np.pi] -= 2*np.pi

	winding_num = np.rint(np.sum(deltas) / (2*np.pi))

	return winding_num

def _ray_casting_intersections(poly, p):
	'Return the number of ray (origin=p, dir=(1,0)) polygon intersections'
	q = (p[0]+1,p[1])
	count = 0
	n = len(poly)
	for i,a in enumerate(poly):
		b = poly[(i+1)%n]

		if not (p[1] == a[1] == b[1]): # ignore horizontal line seg
			if a[0] >= p[0] and a[1] == p[1]: # a on ray
				if _below_point(b,p): # b under ray
					count += 1
			elif b[0] >= p[0] and b[1] == p[1]: # b on ray
				if _below_point(a,p): # a under ray
					count += 1
			elif left_of_line((p,q), a) != left_of_line((p,q), b): # a and b on opp sides
				if (_below_point(a,b) and left_of_line((a,b), p) or
					_below_point(b,a) and left_of_line((b,a), p)):
					count += 1
	return count

def _below_point(a, b):
	'Return true iff point a is below point b'
	return a[1] > b[1] if INVERTED_Y_AXIS else a[1] < b[1]

def _tuple_sub(a, b):
	'Return the elementwise subtraction of tuples a and b'
	return tuple(map(sub, a, b))

def _cross_prod_2d(a, b):
	'Return the magnitude of the cross product of a and b as if they were vec3'
	return a[0]*b[1] - a[1]*b[0]

def left_of_line(line, p):
	'Return true iff p is to the left of the line'
	a,b = line
	val = _cross_prod_2d(_tuple_sub(b,a),_tuple_sub(p,a))
	return val < 0 if INVERTED_Y_AXIS else val > 0

def on_line(line, p):
	'Return true iff p is on the line'
	a,b = line
	return np.isclose(_cross_prod_2d(_tuple_sub(b,a),_tuple_sub(p,a)), 0)

def on_segment(seg, p):
	'Return true iff p is on the line segment'
	a,b = seg
	return (collinear(a,b,p) and 
	between(a[0],p[0],b[0]) and 
	between(a[1],p[1],b[1]))

def collinear(a, b, c):
	'Return true iff points a, b, and c are collinear'
	return np.isclose((a[1]-b[1])*(b[0]-c[0]),(b[1]-c[1])*(a[0]-b[0]))

def between(p, q, r):
	'Return true iff q is between p and r (inclusive)'
	return p <= q <= r or r <= q <= p

def segment_segment_intersect(seg1, seg2):
	'Return true iff the line segments intersect'
	return ((left_of_line(seg1,seg2[0]) != left_of_line(seg1,seg2[1]) and
			 left_of_line(seg2,seg1[0]) != left_of_line(seg2,seg1[1])) or
        	 on_segment(seg1,seg2[0]) or on_segment(seg1,seg2[1]) or
             on_segment(seg2,seg1[0]) or on_segment(seg2,seg1[1]))

def triangulate(poly, method='earclipping'):
	'''Return a tuple containing a list of indices of diagonals and 
	a list of indices of triangles for a triangulation'''
	if method == 'earclipping':
		return _ear_clipping_triangulation(poly)
	else:
		raise ValueError('method should be "earclipping"')

def _is_ear(poly, i):
	'Return true iff vertex i of poly is an ear'
	n = len(poly)
	a = poly[(i-1)%n]
	b = poly[i]
	c = poly[(i+1)%n]

	# check convex
	if not left_of_line((a,b),c):
		return False

	# check vertex inside abc
	for p in poly:
		if p not in (a,b,c) and point_inside((a,b,c),p):
			return False

	return True

def _ear_clipping_triangulation_old(poly):
	'''Return a tuple containing a list of indices of diagonals and 
	a list of indices of triangles for an ear clipping triangulation.
	O(n^3) implementation'''
	diags = []
	tris = []
	n = len(poly)
	cur_poly = list(poly)
	cur_idx = list(range(n))
	while len(diags) != n-3:
		cur_n = len(cur_poly)
		for i in range(cur_n):
			if _is_ear(cur_poly, i):
				a,b = (i-1)%cur_n, (i+1)%cur_n
				diags.append((cur_idx[a],cur_idx[b]))
				tris.append((cur_idx[a],cur_idx[i],cur_idx[b]))
				del cur_poly[i]
				del cur_idx[i]
				break
	tris.append((cur_idx[0],cur_idx[1],cur_idx[2]))
	return diags, tris

def _ear_clipping_triangulation(poly):
	'''Return a tuple containing a list of indices of diagonals and 
	a list of indices of triangles for an ear clipping triangulation.
	O(n^2) implementation'''
	n = len(poly)
	cur_poly = list(poly)
	cur_idx = list(range(n))

	ear_idx = {i for i in range(n) if _is_ear(cur_poly, i)}
	nexts = [(i+1)%n for i in range(n)]
	prevs = [(i-1)%n for i in range(n)]

	diags = []
	tris = []
	while ear_idx and len(diags) != n-3:
		i = ear_idx.pop()
		cur_poly.remove(poly[i])

		prev_i, next_i = prevs[i], nexts[i]
		diags.append((prev_i, next_i))
		tris.append((prev_i, i, next_i))

		nexts[prev_i] = next_i
		prevs[next_i] = prev_i

		for j in (prev_i, next_i):
			is_ear = _is_ear(cur_poly, cur_poly.index(poly[j]))
			if is_ear and j not in ear_idx:
				ear_idx.add(j)
			elif not is_ear and j in ear_idx:
				ear_idx.remove(j)

	i = ear_idx.pop()
	tris.append((prevs[i], i, nexts[i]))

	return diags, tris

def _polygon_rejection_sampling(poly, n, point_inside_method='raycasting'):
	'''Return n random, uniformly distributed points within the polygon by
	generating points within a bounding rectangle and using rejection sampling'''
	points = []
	poly = np.array(poly)
	mins = np.min(poly, axis=0)
	maxs = np.max(poly, axis=0)
	while len(points) < n:
		x = np.random.random_integers(mins[0],maxs[0])
		y = np.random.random_integers(mins[1],maxs[1])
		p = (x,y)
		if point_inside(poly, p, point_inside_method):
			points.append(p)
	return points

def triangle_area(a,b,c):
	'Return the unsigned area of triangle abc'
	return abs(_cross_prod_2d(_tuple_sub(b,a),_tuple_sub(c,a))) / 2

def random_in_triangle(a,b,c):
	'''Return a random, uniformly distributed integer point within a triangle.
	Note: Due to integer rounding the point may fall slightly outside the triangle'''
	u,v = np.random.uniform(size=2)
	if u+v > 1: u,v = 1-u,1-v
	return np.rint(a + u*(b-a) + v*(c-a))

def _triangulation_sampling(poly, n):
	'''Return n random, uniformly distributed points within the polygon by
	triangulating, randomly choosing a triangle weighted by its area, and
	generating a point within the triangle'''
	diags, tris = triangulate(poly)

	poly = np.array(poly)

	areas = np.array([triangle_area(poly[i],poly[j],poly[k]) for i,j,k in tris])
	weights = areas / np.sum(areas)

	chosen_tris = np.random.choice(len(tris),size=n,p=weights)
	points = [random_in_triangle(poly[tris[i][0]],poly[tris[i][1]],poly[tris[i][2]]) for i in chosen_tris]
	return points

def random_in_polygon(poly, n, rand_method='triangulationsampling', point_inside_method='raycasting'):
	'Return n random, uniformly distributed points within the polygon'
	if rand_method == 'rejectionsampling':
		return _polygon_rejection_sampling(poly, n, point_inside_method)
	elif rand_method == 'triangulationsampling':
		return _triangulation_sampling(poly, n)
	else:
		raise ValueError('rand_method should be "rejectionsampling" or "triangulationsampling"')

def compute_convex_hull(poly, method='grahamscan'):
	'Return a list representing the indicies of points on the convex hull'
	if method == 'giftwrapping':
		return _gift_wrapping(poly)
	elif method == 'grahamscan':
		return _graham_scan(poly)
	else:
		raise ValueError('method should be "giftwrapping" or "grahamscan"')

def _gift_wrapping(poly):
	'''Return a list of tuples representing the points on the convex hull
	using the gift wrapping algorithm'''
	cur = poly[0]
	for p in poly:
		if p[0] < cur[0] or p[0] == cur[0] and p[1] < cur[1]:
			cur = p
	hull = []
	while True:
		hull.append(cur)
		cur = poly[0]
		for p in poly:
			if hull[-1] == cur or left_of_line((hull[-1],cur), p):
				cur = p
		if hull[0] == cur: # looped around
			break
	return hull

def _graham_scan(poly):
	'''Return a list of tuples representing the points on the convex hull
	using Graham's scan'''
	cur = poly[0]
	for p in poly:
		if p[0] < cur[0] or p[0] == cur[0] and p[1] < cur[1]:
			cur = p
	# sort by angle then decreasing distance
	ordered = sorted(poly, reverse=True, key=lambda x:
		(np.arctan2(x[1]-cur[1],x[0]-cur[0]), -(x[1]-cur[1])**2-(x[0]-cur[0])**2))
	hull = [cur]
	for p in ordered:
		if p == cur: continue
		# remove points until left test works
		while len(hull) > 1 and not left_of_line((hull[-2],hull[-1]),p):
			hull.pop()
		hull.append(p)
	return hull

def ray_segment_intersection(ray, seg):
	'''Returns a scalar u where ray[0]+u*ray[1]=p. If ray and line segment
	do not intersect float('inf') is returned.'''
	a = ray[0]
	b = ray[1]-ray[0]
	c = seg[0]
	d = seg[1]-seg[0]

	if on_segment(seg, ray[0]):
		return 0

	denom = d[1]*b[0]-d[0]*b[1]
	if not np.isclose(denom, 0):
		v = ((c[0]-a[0])*b[1]-(c[1]-a[1])*b[0]) / denom

		if not np.isclose(b[0], 0):
			u = (c[0]+v*d[0]-a[0]) / b[0]
		elif not np.isclose(b[1], 0):
			u = (c[1]+v*d[1]-a[1]) / b[1]

		if u >= 0 and 0 <= v <= 1:
			return u
	elif collinear(ray[0], seg[0], seg[1]):
		i = 0 if not np.isclose(b[0], 0) else 1

		u0 = (seg[0][i] - ray[0][i]) / b[i]
		u1 = (seg[1][i] - ray[0][i]) / b[i]

		if u0 >= 0 and u1 >= 0:
			return min(u0,u1)
		elif u0 * u1 <= 0:
			return 0

	return float('inf')

def compute_visibility_polygon(p, poly, is_closed, bounds):
	points = []
	n = 100
	for i in range(n):
		theta = i/n*2*np.pi
		ray = np.array(((0,0),(np.cos(theta),np.sin(theta))))
		ray += p

		min_t = float('inf')

		n_verts = len(poly)
		n_edges = n_verts if is_closed else n_verts-1
		for i in range(n_edges):
			seg = np.array((poly[i],poly[(i+1)%n_verts]))
			t = ray_segment_intersection(ray, seg)
			min_t = min(t,min_t)

		n_verts = len(bounds)
		for i in range(n_verts):
			seg = np.array((bounds[i],bounds[(i+1)%n_verts]))
			t = ray_segment_intersection(ray, seg)
			min_t = min(t,min_t)

		if min_t != float('inf'):
			points.append(ray[0]+(ray[1]-ray[0])*min_t)
	return points
