from ..constants import *
from ..mobject.geometry import Square
from ..mobject.geometry import Tiling
from ..mobject.types.vectorized_mobject import VGroup
from ..mobject.types.vectorized_mobject import VMobject
from ..utils.iterables import tuplify
from ..utils.space_ops import z_to_vector

##############


class ThreeDVMobject(VMobject):
    CONFIG = {
        "shade_in_3d": True,
    }


class ParametricSurface(VGroup):
    CONFIG = {
        "u_min": 0,
        "u_max": 1,
        "v_min": 0,
        "v_max": 1,
        "resolution": 32,
        "surface_piece_config": {},
        "fill_color": BLUE_D,
        "fill_opacity": 1.0,
        "checkerboard_colors": [BLUE_D, BLUE_E],
        "stroke_color": LIGHT_GREY,
        "stroke_width": 0.5,
        "should_make_jagged": False,
        "pre_function_handle_to_anchor_scale_factor": 0.00001,
    }

    def __init__(self, func, **kwargs):
        VGroup.__init__(self, **kwargs)
        self.func = func
        self.setup_in_uv_space()
        self.apply_function(lambda p: func(p[0], p[1]))
        if self.should_make_jagged:
            self.make_jagged()

    def get_u_values_and_v_values(self):
        res = tuplify(self.resolution)
        if len(res) == 1:
            u_res = v_res = res[0]
        else:
            u_res, v_res = res
        u_min = self.u_min
        u_max = self.u_max
        v_min = self.v_min
        v_max = self.v_max

        u_values = np.linspace(u_min, u_max, u_res + 1)
        v_values = np.linspace(v_min, v_max, v_res + 1)

        return u_values, v_values

    def setup_in_uv_space(self):
        u_values, v_values = self.get_u_values_and_v_values()
        faces = VGroup()
        for i in range(len(u_values) - 1):
            for j in range(len(v_values) - 1):
                u1, u2 = u_values[i : i + 2]
                v1, v2 = v_values[j : j + 2]
                face = ThreeDVMobject()
                face.set_points_as_corners(
                    [[u1, v1, 0], [u2, v1, 0], [u2, v2, 0], [u1, v2, 0], [u1, v1, 0],]
                )
                faces.add(face)
                face.u_index = i
                face.v_index = j
                face.u1 = u1
                face.u2 = u2
                face.v1 = v1
                face.v2 = v2
        faces.set_fill(color=self.fill_color, opacity=self.fill_opacity)
        faces.set_stroke(
            color=self.stroke_color,
            width=self.stroke_width,
            opacity=self.stroke_opacity,
        )
        self.add(*faces)
        if self.checkerboard_colors:
            self.set_fill_by_checkerboard(*self.checkerboard_colors)

    def set_fill_by_checkerboard(self, *colors, opacity=None):
        n_colors = len(colors)
        for face in self:
            c_index = (face.u_index + face.v_index) % n_colors
            face.set_fill(colors[c_index], opacity=opacity)


# Specific shapes


class Sphere(ParametricSurface):
    CONFIG = {
        "resolution": (12, 24),
        "radius": 1,
        "u_min": 0.001,
        "u_max": PI - 0.001,
        "v_min": 0,
        "v_max": TAU,
    }

    def __init__(self, **kwargs):
        ParametricSurface.__init__(self, self.func, **kwargs)
        self.scale(self.radius)

    def func(self, u, v):
        return np.array([np.cos(v) * np.sin(u), np.sin(v) * np.sin(u), np.cos(u)])


class Cube(VGroup):
    CONFIG = {
        "fill_opacity": 0.75,
        "fill_color": BLUE,
        "stroke_width": 0,
        "side_length": 2,
    }

    def generate_points(self):
        for vect in IN, OUT, LEFT, RIGHT, UP, DOWN:
            face = Square(side_length=self.side_length, shade_in_3d=True,)
            face.flip()
            face.shift(self.side_length * OUT / 2.0)
            face.apply_matrix(z_to_vector(vect))

            self.add(face)


class Prism(Cube):
    CONFIG = {"dimensions": [3, 2, 1]}

    def generate_points(self):
        Cube.generate_points(self)
        for dim, value in enumerate(self.dimensions):
            self.rescale_to_fit(value, dim, stretch=True)


class Honeycomb(Tiling):
    """
    Inherits from Tiling and works in effectively the same way,
    just adding the third dimension.
    To achieve this __init__ and apply_transforms are extended,
    while tile_init_loop is overridden.
    Since it's 3D, Honeycomb also allows for tile_dictionary to be
    alternatively called as cell_dictionary.
    See Tiling for more details.

    Parameters
    ----------
    tile_prototype : Mobject or function(x,y,z) that returns a Mobject
    x_offset : nested list of Mobject methods and values
    y_offset : nested list of Mobject methods and values
    z_offset : nested list of Mobject methods and values
    x_range : range
    y_range : range
    z_range : range
    
    Example
    -------
    Honeycomb(Cube(),
              [[Mobject.shift,[2.1,0,0]]],
              [[Mobject.shift,[0,2.1,0]]],
              [[Mobject.shift,[0,0,2.1]]],
              range(-1,1),
              range(-1,1),
              range(-1,1))
    """

    def __init__(
        self,
        tile_prototype,
        x_offset,
        y_offset,
        z_offset,
        x_range,
        y_range,
        z_range,
        **kwargs
    ):
        self.z_range = range(z_range.start, z_range.stop + z_range.step, z_range.step)
        self.z_offset = z_offset
        super().__init__(tile_prototype, x_offset, y_offset, x_range, y_range, **kwargs)
        self.cell_dictionary = self.tile_dictionary

    def tile_init_loop(self):
        for x in self.x_range:
            self.tile_dictionary[x] = {}
            self.tile_dictionary[x] = {}
            for y in self.y_range:
                self.tile_dictionary[x][y] = {}
                for z in self.z_range:
                    if callable(self.tile_prototype):
                        tile = self.tile_prototype(x, y, z).deepcopy()
                    else:
                        tile = self.tile_prototype.deepcopy()
                    self.apply_transforms(x, y, z, tile)
                    self.add(tile)
                    self.tile_dictionary[x][y][z] = tile

    def apply_transforms(self, x, y, z, tile):
        super().apply_transforms(x, y, tile)
        self.transform_tile(z, self.z_offset, tile)
