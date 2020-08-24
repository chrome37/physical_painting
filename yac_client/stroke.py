import numpy as np
import os
from natsort import natsorted
from . import positions


class Stroke:
    def __init__(self, x0, y0, x1, y1, x2, y2, z0, z2, r, g, b, thickness):
        config = CoordConfig()
        self.color = StrokeColor(r, g, b)
        self.thickness = thickness
        point_num = 20
        t_array = np.arange(0, 1, 1/point_num)
        points_disp = []
        for t in t_array:
            points_disp.append(self.__bezier(
                x0, y0, x1, y1, x2, y2, z0, z2, t))
        self.points_disp = points_disp

        points_world = [self.__convert(
            i[0], i[1], i[2], config) for i in points_disp]
        self.points_world = points_world

        self.points = [positions.RobotCoord(i[0], i[1], i[2], config.ROBOT_TIP_ROTATION[0],
                                            config.ROBOT_TIP_ROTATION[1], config.ROBOT_TIP_ROTATION[2], thickness) for i in points_world]

    def __bezier(self, x0, y0, x1, y1, x2, y2, z0, z2, t):
        x = ((1-t) * (1-t) * x0 + 2 * t * (1-t) * x1 + t * t * x2)
        y = ((1-t) * (1-t) * y0 + 2 * t * (1-t) * y1 + t * t * y2)
        z = ((1-t) * z0 + t * z2)
        return y, x, z, 0

    def __convert(self, x, y, z, config):
        R = np.array([
            [np.cos(config.EASEL_ANG), 0, -np.sin(config.EASEL_ANG)],
            [0, 1, 0],
            [np.sin(config.EASEL_ANG), 0, np.cos(config.EASEL_ANG)]])

        #x_new = x / config.IMG_X * config.CANVAS_X - config.CANVAS_X / 2
        #y_new = config.CANVAS_Y - (y / config.IMG_Y * config.CANVAS_Y) + config.CANVAS_MERGIN_BUTTON

        x_new = x * config.CANVAS_X - config.CANVAS_X / 2
        y_new = config.CANVAS_Y - (y * config.CANVAS_Y) + config.CANVAS_MERGIN_BUTTON
        c = [0, x_new, y_new]

        #  押し付け量の考慮
        #EASEL_CANVAS_OFFSET[0] += z

        return [int(i*1000) for i in config.EASEL_BASE_OFFSET + np.dot(config.EASEL_CANVAS_OFFSET, R) + np.dot(c, R)]

    def get_points(self):
        return self.points

    def get_points_disp(self):
        return self.points_disp

    def get_points_world(self):
        return self.points_world

    def get_color(self):
        return self.color

    def get_thickness(self):
        return self.thickness


class StrokeColor:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b


class CoordConfig:
    def __init__(self):
        # the angle of painter easel
        # -15 degree
        self.EASEL_ANG = -np.pi / 12

        # mm
        #EASEL_LENGTH = 1000
        self.EASEL_LENGTH = 820

        # mm
        self.EASEL_THICKNESS = 11
        self.CANVAS_MERGIN_BUTTON = 50

        # mm
        # ROBOT_TIP_TO_PEN_TIP = 130 (実測値は105だったが130でうまく動いている、キャンバスの厚さもこの定数に含まれている？)
        #self.ROBOT_TIP_TO_PEN_TIP = 105
        self.ROBOT_TIP_TO_PEN_TIP = 130

        # mm
        # キャンバス厚さ
        self.CANVAS_THICKNESS = 9

        self.ROBOT_TIP_ROTATION = [-1050000, 0, 900000]
        #ROBOT_TIP_ROTATION = [-1050000, 0, 900000]

        self.EASEL_BASE_OFFSET = np.array([-398, 0, -(360+510)])
        self.EASEL_CANVAS_OFFSET = np.array(
            [self.EASEL_THICKNESS + self.ROBOT_TIP_TO_PEN_TIP + self.CANVAS_THICKNESS, 0, self.EASEL_LENGTH])

        self.IMG_X = 200
        self.IMG_Y = 200
        self.CANVAS_X = 200
        self.CANVAS_Y = 200


if __name__ == "__main__":
    stroke = Stroke(0.13449928, 0.47401235, 0.98125505, 0.8168494,
                    0.15215716, 0.45815855, 1.0, 1.0, 0.8443417, 0.8312879, 0.7027973, 0.40457433)
    for i in stroke.points:
        print(i.get_list())
