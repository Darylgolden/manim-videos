from manim import *

a_start = 0.5
a_end = 0.1
a_time = 10
b_start = 1
b_end = 7
b_time = 20

basic_preamble = r"""
\usepackage[english]{babel}
\usepackage{amsmath}
\usepackage{amssymb}
"""


def weierstrass(a,b,x):
	y = 0
	for i in range(100):
		y += (a**i)*np.cos((b**i)*PI*x)
	return y

def func_updater(func):
	func = FunctionGraph(lambda x: weierstrass(a,b_value.get_value(),x), x_min = -4, x_max=4, step_size=0.0001)

class Weierstrass(GraphScene):
	CONFIG = {
    	"y_max" : 2,
    	"y_min" : -2,
    	"x_max" : 4,
    	"x_min" : -4,
    	"x_axis_width" : 20,
    	"graph_origin" : 0*DOWN
	}

	def construct(self):
		self.setup_axes(animate=True)
		equation = MathTex(r"f(x)=\sum_{n=0} ^\infty a^n \cos(b^n \pi x)")
		equation.to_edge(UP+LEFT)
		a_value = ValueTracker(a_start)
		a_label = MathTex(r"a=")
		a_value_label = DecimalNumber(a_value.get_value()).add_updater(lambda v: v.set_value(a_value.get_value()))
		b_value = ValueTracker(b_start)
		b_label = MathTex(r"b=")
		b_value_label = DecimalNumber(b_value.get_value()).add_updater(lambda v: v.set_value(b_value.get_value()))
		labels = VGroup(a_label, a_value_label, b_label, b_value_label)
		VGroup(a_value_label, b_value_label).arrange_submobjects(DOWN)
		a_label.next_to(a_value_label,LEFT,buff=0.15)
		b_label.next_to(b_value_label,LEFT,buff=0.15)
		labels.to_edge(UP+RIGHT)

		func=self.get_graph(lambda x: weierstrass(a_value.get_value(),b_value.get_value(),x), x_min = -4, x_max=4, step_size=0.0001, stroke_width=1)
		func.set_color(BLUE)
		func.add_updater(
			lambda mob: mob.become(
				self.get_graph(lambda x: weierstrass(a_value.get_value(),b_value.get_value(),x), x_min = -4, x_max=4, step_size=0.0001, color=BLUE, stroke_width=1))
			)
		self.play(ShowCreation(func), run_time=2)
		self.wait()
		self.play(Write(equation),run_time=2)
		self.wait(0.5)
		self.play(Write(labels))
		self.play(b_value.set_value, b_end, rate_func=smooth, run_time=b_time)
		self.play(a_value.set_value, a_end, rate_func=smooth, run_time=a_time)
		self.wait()