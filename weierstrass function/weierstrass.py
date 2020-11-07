from manim import *

a = 0.5
b_start = 1
b_end = 7
time = 1
frame_rate=15
N=time*frame_rate

basic_preamble = r"""
\usepackage[english]{babel}
\usepackage{amsmath}
\usepackage{amssymb}
"""

def BTex(*args,**kwargs):
    return Tex(*args,tex_template=TexTemplate(preamble=basic_preamble),**kwargs)

def weierstrass(a,b,x):
	y = 0
	for i in range(100):
		y += (a**i)*np.cos((b**i)*PI*x)
	return y

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
		self.setup_axes()
		func= PangoText("Hi")
		value = PangoText("Hi")
		for i in range(N):
			b = b_start+(i)*(b_end-b_start)/N
			self.remove(func)
			self.remove(value)
			func=self.get_graph(lambda x: weierstrass(a,b,x), x_min = -4, x_max=4, step_size=0.0001)
			func.set_color(BLUE)
			b_string = "{:.2f}".format(b)
			value = PangoText(b_string)			
			self.add(func)
			self.add(value)
			self.wait(1/frame_rate)
		self.add(func)
		self.wait()