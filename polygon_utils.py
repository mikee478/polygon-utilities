import numpy as np

def is_ccw(poly, inverted_y_axis = True):
	twice_area = 0
	n = len(poly)
	for i in range(len(poly)):
		a = poly[i]
		b = poly[(i+1)%n]
		twice_area += (b[0]-a[0])*(b[1]+a[1])
	return twice_area > 0 if inverted_y_axis else twice_area < 0

def point_inside(poly, point, method='winding number'):
	if method == 'winding number':
		return not np.isclose(_winding_number(poly, point),0)
	elif method == 'ray casting':
		pass
	else:
		raise ValueError('Variable method should be "winding number" or "ray casting"')

def _winding_number(poly, point):
	poly = np.array(poly)
	poly -= point # center point on origin
	
	angles = np.arctan2(poly[:,1],poly[:,0]) # [-pi, pi]
	
	deltas = np.copy(angles)
	deltas[1:] -= angles[:-1]
	deltas[0] -= angles[-1]
	
	deltas[deltas <= -np.pi] += 2*np.pi
	deltas[deltas >= np.pi] -= 2*np.pi

	winding_num = np.rint(np.sum(deltas) / (2*np.pi))

	return winding_num