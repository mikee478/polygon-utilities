import numpy as np

def is_ccw(poly, inverted_y_axis = True):
	twice_area = 0
	n = len(poly)
	for i in range(len(poly)):
		a = poly[i]
		b = poly[(i+1)%n]
		twice_area += (b[0]-a[0])*(b[1]+a[1])
	return twice_area > 0 if inverted_y_axis else twice_area < 0

def point_inside(poly, p, method='winding number'):
	if method == 'winding number':
		return not np.isclose(_winding_number(poly, p),0)
	elif method == 'ray casting':
		return _ray_casting_intersections(poly, p) % 2 == 1
	else:
		raise ValueError('Variable method should be "winding number" or "ray casting"')

def _winding_number(poly, p):
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
	'''Return the number ray polygon intersections where the origin
	 of the ray is p and the direction is positive x'''
	q = (p[0]+1,p[1])
	count = 0
	n = len(poly)
	for i,a in enumerate(poly):
		b = poly[(i+1)%n]

		if not (p[1] == a[1] == b[1]): # ignore horizontal line seg
			if (a[0] >= p[0] and a[1] == p[1]): # a is on the ray
				if b[1] > p[1]: # b is below the ray
					count += 1
			elif left_of_line((p,q), a) != left_of_line((p,q), b): # a and b on opp sides of ray
				if b[1] < a[1]: # a is the lower point
					a,b = b,a
				if(left_of_line((a,b), p)):
					count += 1
	return count


def left_of_line(line, p):
	'Return true iff p is to the left of the line'
	a,b = line
	return (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0]) > 0

def on_line(line, p):
	'Return true iff p is on the line'
	a,b = line
	return (b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0]) == 0

def on_segment(seg, p):
	'Return true iff p is on the line segment'
	a,b = seg
	return collinear(a,b,p) and between(a[0],p[0],b[0]) and between(a[1],p[1],b[1])

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
