from manim import *

def riemann_surfaces(function, min, max, constant, dx=0.0001):
	x_range = np.arange(min, max, dx)
	y_val = np.array([])
	for x in x_range:
		y = function(x, constant)
		y_val = np.append(y_val, y)
	values = list(zip(x_range, y_val))
	return values

def GraphFunction(u, v):
	return np.array([u, v, u**2+v**2])

test = riemann_surfaces(GraphFunction, 0, 1, 1)
print(test[3000][0], test[3000][1])