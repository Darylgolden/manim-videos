from manim import *

class Test(Scene):

	def construct(self):
		equation = Tex("$x^2$")
		self.play(Write(equation))
		self.wait()