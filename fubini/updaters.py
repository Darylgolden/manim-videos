class MmodNTracker(Scene):
    CONFIG = {
        "number_of_lines": 400,
        "gradient_colors":[RED,YELLOW,BLUE],
        "end_value":100,
        "total_time":180,
    }
    def construct(self):
        circle = Circle().set_height(FRAME_HEIGHT*0.9)
        mod_tracker = ValueTracker(0)
        lines = self.get_m_mod_n_objects(circle,mod_tracker.get_value())
        lines.add_updater(
            lambda mob: mob.become(
                self.get_m_mod_n_objects(circle,mod_tracker.get_value())
                )
            )
        self.add(circle,lines)
        self.wait(3)
        self.play(
            mod_tracker.set_value,self.end_value,
            rate_func=linear,
            run_time=self.total_time
            )
        self.wait(3)

    def get_m_mod_n_objects(self,circle,x,y=None):
        if y==None:
            y = self.number_of_lines
        lines = VGroup()
        for i in range(y):
            start_point = circle.point_from_proportion((i%y)/y)
            end_point = circle.point_from_proportion(((i*x)%y)/y)
            line = Line(start_point,end_point).set_stroke(width=1)
            lines.add(line)
        lines.set_color_by_gradient(*self.gradient_colors)
        return lines