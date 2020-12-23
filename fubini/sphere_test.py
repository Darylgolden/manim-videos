from manim import *

class Test(ThreeDScene):
	def construct(self):
		test = Sphere()
		self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
		self.play(ShowCreation(test))
		self.wait()