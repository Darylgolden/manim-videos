from manim import *

x_start = -2
x_end = 2
y_start = -2
y_end = 2
x_time = 1
y_time = 1

class Test(ThreeDScene):

	def GraphFunction(self, u, v):
		return np.array([u, v, 2+0.2*(np.cos(u)+np.sin(v))])

	def xyfunc(self, u, v):
		return np.array([u, v, 0])

	def xzfunc(self, u, v):
		return np.array([u, 0, v])

	def yzfunc(self, u, v):
		return np.array([0, u, v])

	def xyrect(self, offset, **kwargs):
		obj = ParametricSurface(self.xyfunc, **kwargs)
		obj.shift(np.array([0, 0, offset]))
		return obj

	def xzrect(self, offset, **kwargs):
		obj = ParametricSurface(self.xzfunc, **kwargs)
		obj.shift(np.array([0, offset, 0]))
		return obj

	def yzrect(self, offset, **kwargs):
		obj = ParametricSurface(self.yzfunc, **kwargs)
		obj.shift(np.array([offset, 0, 0]))
		return obj

	def xzunderfunc(self, func, const, **kwargs):
		obj = self.xzrect(const, **kwargs)
		obj.apply_function(lambda pt: np.array([pt[0], pt[1], pt[2]*func(pt[0], pt[1])[2]]))
		return obj

	def yzunderfunc(self, func, const, **kwargs):
		obj = self.yzrect(const, **kwargs)
		obj.apply_function(lambda pt: np.array([pt[0], pt[1], pt[2]*func(pt[0], pt[1])[2]]))
		return obj

	def get_volume(self, func, x_min, x_max, y_min, y_max, wall_color=YELLOW, floor_color=BLUE, **kwargs):
		volume_group = VGroup()
		wall1 = self.xzunderfunc(func, y_min, u_min=x_min, u_max=x_max, checkerboard_colors=[wall_color, wall_color], **kwargs)
		wall2 = self.xzunderfunc(func, y_max, u_min=x_min, u_max=x_max, checkerboard_colors=[wall_color, wall_color], **kwargs)
		wall3 = self.yzunderfunc(func, x_min, u_min=y_min, u_max=y_max, checkerboard_colors=[wall_color, wall_color], **kwargs)
		wall4 = self.yzunderfunc(func, x_max, u_min=y_min, u_max=y_max, checkerboard_colors=[wall_color, wall_color], **kwargs)
		floor = self.xyrect(0, u_min = x_min, u_max = x_max, v_min = y_min, v_max = y_max, checkerboard_colors=[floor_color, floor_color], **kwargs)
		volume_group.add(wall1, wall2, wall3, wall4, floor)
		return volume_group

	def construct(self):
		axes = ThreeDAxes()
		self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
		surf = ParametricSurface(self.GraphFunction, u_min = -5, u_max = 5, v_min = -5, v_max = 5, fill_opacity=0.2)
		x_val = ValueTracker(x_start)
		y_val = ValueTracker(y_start)
		vol = self.get_volume(self.GraphFunction, x_start, x_val.get_value(), y_start, y_val.get_value(), wall_color = YELLOW, floor_color = BLUE, fill_opacity=0.3, stroke_width=0)
		vol.add_updater(
			lambda mob: mob.become(
				self.get_volume(self.GraphFunction, x_start, x_val.get_value(), y_start, y_val.get_value(), wall_color = YELLOW, floor_color = BLUE, fill_opacity=0.3, stroke_width=0)
				)
			)

		# vol = self.get_volume(self.GraphFunction, -2, 2, 0, 4, wall_color = YELLOW, floor_color = BLUE, fill_opacity=0.3, stroke_width=0)
		self.add(axes, vol, surf)
		self.play(x_val.set_value, x_end, rate_func = smooth, run_time = x_time)
		self.play(y_val.set_value, y_end, rate_func = smooth, run_time = y_time)
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

