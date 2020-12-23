from manim import *

plane_config = dict(
            axis_config = { 
                "include_tip": True, "include_numbers" : True,
                "include_ticks" : True, "line_to_number_buff" : 0.01,
                "stroke_color" : WHITE, "stroke_width": 1,
                "number_scale_val" : 0.4,
                "tip_scale": 0.5
            },
            x_axis_config = {
                "exclude_zero_from_default_numbers": True,
                "label_direction" : DOWN, "stroke_color" : WHITE,
                "x_min" : -1, "x_max" : 4, "unit_size": 1
            },
            y_axis_config = {
                "exclude_zero_from_default_numbers": True,
                "label_direction" : UR, "stroke_color" : WHITE,
                "x_min" : -1, # not y_min
                "x_max" : 6,  # not y_max
                "unit_size": 1
            },
            background_line_style = {
                "stroke_width" : 1, "stroke_opacity" : 1,
                "stroke_color" : GOLD,
            }  
        )

class Test(Scene):
	def construct(self):
		plane = NumberPlane(**plane_config)
        
        # rotate y labels
		for label in plane.y_axis.numbers:
			label.rotate(PI)
            
		self.play(Write(plane))
		self.wait()