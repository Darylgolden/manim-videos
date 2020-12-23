from manim import *

class Test(ThreeDScene):
	def construct(self):
		axes = ThreeDAxes()
		ahh = PlaneXY()
		b = PlaneXZ(checkerboard_colors=[GREEN,GREEN])
		c = PlaneYZ(checkerboard_colors=[YELLOW, YELLOW])
		self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
		self.add(axes)
		self.add(ahh, b, c)
		self.wait()