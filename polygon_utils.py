import numpy as np

def is_ccw(poly, inverted_y_axis=True):
	'Return true if polygon vertices are counterclockwise.'
	twice_area = 0
	n = len(poly)
	for i in range(len(poly)):
		a = poly[i]
		b = poly[(i+1)%n]
		twice_area += (b[0]-a[0])*(b[1]+a[1])
	return twice_area > 0 if inverted_y_axis else twice_area < 0

def point_inside(poly, p, method='raycasting'):
	'Return true if p is inside poly'
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
	'Return the number ray (origin=p, dir=(1,0)) polygon intersections'
	q = (p[0]+1,p[1])
	count = 0
	n = len(poly)
	for i,a in enumerate(poly):
		b = poly[(i+1)%n]

		if not (p[1] == a[1] == b[1]): # ignore horizontal line seg
			if a[0] >= p[0] and a[1] == p[1]: # a on ray
				if b[1] > p[1]: # b under ray
					count += 1
			elif b[0] >= p[0] and b[1] == p[1]: # b on ray
				if a[1] > p[1]: # a under ray
					count += 1
			elif left_of_line((p,q), a) != left_of_line((p,q), b): # a and b on opp sides
				if (a[1] > b[1] and left_of_line((a,b), p) or
					a[1] < b[1] and left_of_line((b,a), p)):
					count += 1
	return count

def left_of_line(line, p, inverted_y_axis=True):
	'Return true iff p is to the left of the line'
	a,b = line
	val = (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0])
	return val < 0 if inverted_y_axis else v > 0

def on_line(line, p):
	'Return true iff p is on the line'
	a,b = line
	return (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0]) == 0

def on_segment(seg, p):
	'Return true iff p is on the line segment'
	a,b = seg
	return (collinear(a,b,p) and 
	between(a[0],p[0],b[0]) and 
	between(a[1],p[1],b[1]))

def collinear(a, b, c):
	'Return true iff points a, b, and c are collinear'
	return (a[1]-b[1])*(b[0]-c[0]) == (b[1]-c[1])*(a[0]-b[0])

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
	'''Return a list of tuples of polygon indices representing diagonals
	for a triangulation'''
	if method == 'earclipping':
		return _ear_clipping_triangulation(poly)
	else:
		raise ValueError('method should be "earclipping"')

def _is_ear(poly, i):
	'Return true if vertex i of poly is an ear'
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

def _ear_clipping_triangulation(poly):
	'''Return a list of tuples of polygon indices representing diagonals
	for a ear clipping triangulation'''
	diags = []
	n = len(poly)
	cur_poly = list(poly)
	cur_idx = list(range(n))
	while len(diags) != n-3:
		cur_n = len(cur_poly)
		for i in range(cur_n):
			if _is_ear(cur_poly, i):
				diags.append((cur_idx[(i-1)%cur_n],cur_idx[(i+1)%cur_n]))
				del cur_poly[i]
				del cur_idx[i]
				break
	return diags

def random_in_polygon(poly, n, rand_method='rejectionsampling', point_inside_method='raycasting'):
	'Return n random, uniformly distributed points within the polygon'
	points = []
	if rand_method == 'rejectionsampling':
		poly = np.array(poly)
		mins = np.min(poly, axis=0)
		maxs = np.max(poly, axis=0)
		while len(points) < n:
			x = np.random.random_integers(mins[0],maxs[0])
			y = np.random.random_integers(mins[1],maxs[1])
			p = (x,y)
			if point_inside(poly, p, method=point_inside_method):
				points.append(p)
	else:
		raise ValueError('rand_method should be "rejectionsampling"')
	return points
