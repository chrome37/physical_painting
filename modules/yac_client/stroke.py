import numpy as np
import os
from natsort import natsorted
from . import positions
import math
import copy


class Stroke:
    def __init__(self, x0, y0, x1, y1, x2, y2, z0, z2, r, g, b, a):
        self.config = CoordConfig()
        self.color = StrokeColor(r, g, b, a)
        self.thickness = (z0 + z2) * 0.5
        point_num = 50
        t_array = np.arange(0, 1 + 1/point_num, 1/point_num)
        points_disp = []
        for t in t_array:
            points_disp.append(self.__bezier(
                x0, y0, x1, y1, x2, y2, z0, z2, t))
        self.points_disp = points_disp

        points_world = [self.__convert(
            i[0], i[1], i[2]) for i in points_disp]
        self.points_world = points_world

        self.points = [positions.RobotCoord(i[0], i[1], i[2], self.config.ROBOT_TIP_ROTATION[0],
                                            self.config.ROBOT_TIP_ROTATION[1], self.config.ROBOT_TIP_ROTATION[2], self.thickness) for i in points_world]

        start_point = copy.copy(self.points[0])
        start_point.x = -460123
        self.start_point = start_point

        end_point = copy.copy(self.points[-1])
        end_point.x = -460123
        self.end_point = end_point

        self.points.insert(0, start_point)
        self.points.append(end_point)

    def __bezier(self, x0, y0, x1, y1, x2, y2, z0, z2, t):
        x1 = x0 + (x2 - x0) * x1
        y1 = y0 + (y2 - y0) * y1
        x = ((1-t) * (1-t) * x0 + 2 * t * (1-t) * x1 + t * t * x2)
        y = ((1-t) * (1-t) * y0 + 2 * t * (1-t) * y1 + t * t * y2)
        z = ((1-t) * z0 + t * z2)
        return y, x, z, 0

    def __convert(self, x, y, z):
        R = np.array([
            [np.cos(self.config.EASEL_ANG), 0, -np.sin(self.config.EASEL_ANG)],
            [0, 1, 0],
            [np.sin(self.config.EASEL_ANG), 0, np.cos(self.config.EASEL_ANG)]])

        #x_new = x / config.IMG_X * config.CANVAS_X - config.CANVAS_X / 2
        #y_new = config.CANVAS_Y - (y / config.IMG_Y * config.CANVAS_Y) + config.CANVAS_MERGIN_BUTTON

        x_new = x * self.config.CANVAS_X - self.config.CANVAS_X / 2
        y_new = self.config.CANVAS_Y - (y * self.config.CANVAS_Y) + self.config.CANVAS_MERGIN_BUTTON
        c = [0, x_new, y_new]
        #  押し付け量の考慮

        new_easel_canvas_offset = [self.config.EASEL_CANVAS_OFFSET[0] - self.__thickness_to_press_regression(z), self.config.EASEL_CANVAS_OFFSET[1], self.config.EASEL_CANVAS_OFFSET[2]]

        return [int(i*1000) for i in self.config.EASEL_BASE_OFFSET + np.dot(new_easel_canvas_offset, R) + np.dot(c, R)]

    def __thickness_to_press_regression(self, thickness_degree):
        a = 0.981900452
        b = 0.007692308
        max_press = 17
        result = min(max_press, (thickness_degree * self.config.IMG_X / 10 - b) / a)
        #線画OpenCVの結果より明らかに太いため調整している
        return result * 0.6

    def __thickness_to_press_table_search(self, thickness_degree):
        z_step = []
        y = []
        for i in range(25):
            z_step.append(i*0.04)
        return thickness_degree * 12

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
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def get_rgba(self):
        return (self.r, self.g, self.b, self.a)

    def get_rgba_256(self):
        return (self.r * 255, self.g * 255, self.b*255, self.a)

    def get_rgb(self):
        r = 1 - self.a + self.a * self.r
        g = 1 - self.a + self.a * self.g
        b = 1 - self.a + self.a * self.b
        return (r, g, b)

    def get_rgb_256(self):
        r = 1 - self.a + self.a * self.r
        g = 1 - self.a + self.a * self.g
        b = 1 - self.a + self.a * self.b
        return (r * 255, g * 255, b * 255)

    def get_cmykw(self):
        r, g, b, a = self.get_rgba()
        k = min(1-r, 1-g, 1-b)
        w = min(r, g, b)
        if k == 1:
            c = m = y = w = 0
            k = 1
        else :
            c = (1 - r - k)/(1-k)
            m = (1 - g - k)/(1-k)
            y = (1 - b - k)/(1-k)

        return c, m, y, k, w

    def get_cmy(self):
        r, g, b = self.get_rgb()
        c = 1 - r
        m = 1 - g
        y = 1 - b
        k = 0
        w = 0

        return c, m, y, k, w




class CoordConfig:
    def __init__(self):
        # the angle of painter easel
        # -15 degree
        self.EASEL_ANG = -1 * math.radians(16)

        # mm
        #EASEL_LENGTH = 1000
        self.EASEL_LENGTH = 820

        # mm
        self.EASEL_THICKNESS = 11
        self.CANVAS_MERGIN_BUTTON = 50

        # mm
        # ROBOT_TIP_TO_PEN_TIP = 130 (実測値は105だったが130でうまく動いている、キャンバスの厚さもこの定数に含まれている？)
        #self.ROBOT_TIP_TO_PEN_TIP = 105
        #減らすと近く
        #紙一枚減らすと1減らす(大体)
        #self.ROBOT_TIP_TO_PEN_TIP = 127
        self.ROBOT_TIP_TO_PEN_TIP = 142

        # mm
        # キャンバス厚さ
        self.CANVAS_THICKNESS = 8

        self.ROBOT_TIP_ROTATION = [-1050000, 0, 900000]
        #ROBOT_TIP_ROTATION = [-1050000, 0, 900000]

        self.EASEL_BASE_OFFSET = np.array([-398, 0, -(360+510)])
        self.EASEL_CANVAS_OFFSET = np.array(
            [self.EASEL_THICKNESS + self.ROBOT_TIP_TO_PEN_TIP + self.CANVAS_THICKNESS, 0, self.EASEL_LENGTH])

        self.IMG_X = 200
        self.IMG_Y = 200
        self.CANVAS_X = 200
        self.CANVAS_Y = 200
