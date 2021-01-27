from manim import *

x_start = -2
x_end = 2
y_start = -2
y_end = 2
x_time = 1
y_time = 1

class Test(ThreeDScene):

	def GraphFunction(self, u, v):
		# return np.array([u, v, 2+0.2*(np.cos(u)+np.sin(v))])
		return np.array([u, v, 2-0.5*(u**2+v**2)])


	def xyrect(self, x_min, x_max, y_min, y_max, **kwargs):
		obj = Polygon(np.array([x_min, y_min, 0]), np.array([x_min, y_max, 0]), np.array([x_max, y_max, 0]), np.array([x_max, y_min, 0]), **kwargs)
		return obj

	def xzrect(self, u_min = 0, u_max = 1, height = 1, offset = 0, **kwargs):
		obj = Polygon(np.array([u_min, offset, 0]), np.array([u_min, offset, height]), np.array([u_max, offset, height]), np.array([u_max, offset, 0]), **kwargs)
		return obj

	def yzrect(self, u_min = 0, u_max = 1, height = 1, offset = 0, **kwargs):
		obj = Polygon(np.array([offset, u_min, 0]), np.array([offset, u_min, height]), np.array([offset, u_max, height]), np.array([offset, u_max, 0]), **kwargs)
		return obj

	def xzunderfunc(self, func, **kwargs):
		obj = self.xzrect(**kwargs)
		obj.apply_function(lambda pt: np.array([pt[0], pt[1], pt[2]*func(pt[0], pt[1])[2]]))
		return obj

	def yzunderfunc(self, func, **kwargs):
		obj = self.yzrect(**kwargs)
		obj.apply_function(lambda pt: np.array([pt[0], pt[1], pt[2]*func(pt[0], pt[1])[2]]))
		return obj

	def get_volume(self, func, x_min, x_max, y_min, y_max, **kwargs):
		volume_group = VGroup()
		wall1 = self.xzunderfunc(func, offset = y_min, u_min = x_min, u_max = x_max, **kwargs)
		wall2 = self.xzunderfunc(func, offset = y_max, u_min = x_min, u_max = x_max, **kwargs)
		wall3 = self.yzunderfunc(func, offset = x_min, u_min = y_min, u_max = y_max, **kwargs)
		wall4 = self.yzunderfunc(func, offset = x_max, u_min = y_min, u_max = y_max, **kwargs)
		floor = self.xyrect(x_min, x_max, y_min, y_max, **kwargs)
		volume_group.add(wall1, wall2, wall3, wall4, floor)
		return volume_group

	def construct(self):
		axes = ThreeDAxes()
		self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
		surf = ParametricSurface(self.GraphFunction, u_min = -5, u_max = 5, v_min = -5, v_max = 5, fill_opacity=0.2)
		x_val = ValueTracker(x_start)
		y_val = ValueTracker(y_start)
		vol = self.get_volume(self.GraphFunction, x_start, x_val.get_value(), y_start, y_val.get_value(), fill_color = RED, stroke_color = RED, fill_opacity=0.3)
		vol.add_updater(
			lambda mob: mob.become(
				self.get_volume(self.GraphFunction, x_start, x_val.get_value(), y_start, y_val.get_value(), fill_color = RED, stroke_color = RED, fill_opacity=0.3)
				)
			)

		# vol = self.get_volume(self.GraphFunction, -2, 2, 0, 4, fill_opacity=0.3, fill_color = YELLOW, stroke_color = YELLOW_E)
		self.add(axes, vol, surf)
		self.play(x_val.animate.set_value(x_end), rate_func = smooth, run_time = x_time)
		self.play(y_val.animate.set_value(y_end), rate_func = smooth, run_time = y_time)
		self.wait()

	# def construct(self):
	# 	axes = ThreeDAxes()
	# 	graph = ParametricSurface(self.GraphFunction, u_min = -3, u_max = 3, v_min = -3, v_max = 3)
	# 	# riemanns = self.riemann_surfaces(self.GraphFunction, self.xzrect, 0, 1, 1, 0.1)
	# 	# riemanns.set_fill(opacity=0.5)
	# 	volume_test = self.get_volume(self.GraphFunction, -2, 2, -2, 2)
	# 	self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
	# 	self.add(axes)
	# 	self.add(graph)
	# 	# self.add(riemanns)
	# 	self.add(volume_test)
	# 	self.wait()