import numpy as np
import os
from natsort import natsorted
from . import positions
import math
import copy
from PIL import ImageCms, Image
import os


class Stroke:
    def __init__(self, x0, y0, x1, y1, x2, y2, z0, z2, r, g, b, a):
        self.config = CoordConfig()
        self.color = StrokeColor(r, g, b, a)
        self.thickness = (z0 + z2) * 0.5
        point_num = 1000
        t_array = np.arange(0, 1 + 1/point_num, 1/point_num)

        points_disp_uneven = []
        for t in t_array:
            ##!!!!!!!_bezier_basicはテスト用!!!!!!!!!!!######
            points_disp_uneven.append(self.__bezier_custom(
                x0, y0, x1, y1, x2, y2, z0, z2, t))

        points_disp = self.__filter_points(points_disp_uneven)
        points_disp = self.__curvature_modify(points_disp)
        points_disp = self.__thickness_to_press_convert(points_disp)

        #print(len(points_disp))
        #points_disp = points_disp[2:]

        start_point2 = list(copy.copy(points_disp[0]))
        vec2 = [points_disp[1][0] - points_disp[0][0],
                points_disp[1][1] - points_disp[0][1]]
        vec2_standard = self.__vec_standardize(vec2)
        # 0.1:キャンバスに対するストローク太さひ比率が0.1だから, 0.5:直径を半径に
        start_point2[0] -= vec2_standard[0] * z0 * \
            self.config.THICKNESS_FACTOR * 0.1 * 0.5 * 0.1
        start_point2[0] = self.__cut_off(start_point2[0])
        start_point2[1] -= vec2_standard[1] * z0 * \
            self.config.THICKNESS_FACTOR * 0.1 * 0.5 * 0.1
        start_point2[1] = self.__cut_off(start_point2[1])

        # 空間変換後に手前に引く点
        start_point1 = list(copy.copy(points_disp[0]))
        start_point1[0] -= vec2_standard[0] * z0 * \
            self.config.THICKNESS_FACTOR * 0.1 * 0.5 * 2.1
        start_point1[0] = self.__cut_off(start_point1[0])
        start_point1[1] -= vec2_standard[1] * z0 * \
            self.config.THICKNESS_FACTOR * 0.1 * 0.5 * 2.1
        start_point1[1] = self.__cut_off(start_point1[1])
        start_point1[2] = start_point1[2] * -2

        points_disp.insert(0, tuple(start_point2))
        points_disp.insert(0, tuple(start_point1))

        end_point2 = list(copy.copy(points_disp[-1]))
        vec3 = [points_disp[-1][0] - points_disp[-2][0],
                points_disp[-1][1] - points_disp[-2][1]]
        vec3_standard = self.__vec_standardize(vec3)
        end_point2[0] += vec3_standard[0] * z0 * \
            self.config.THICKNESS_FACTOR * 0.1 * 0.5 * 2
        end_point2[0] = self.__cut_off(end_point2[0])
        end_point2[1] += vec3_standard[1] * z0 * \
            self.config.THICKNESS_FACTOR * 0.1 * 0.5 * 2
        end_point2[1] = self.__cut_off(end_point2[1])

        # 空間変換後に手前に引く点
        end_point1 = list(copy.copy(points_disp[-1]))
        end_point1[0] += vec3_standard[0] * z0 * \
            self.config.THICKNESS_FACTOR * 0.1 * 0.5 * 2
        end_point1[0] = self.__cut_off(end_point1[0])
        end_point1[1] += vec3_standard[1] * z0 * \
            self.config.THICKNESS_FACTOR * 0.1 * 0.5 * 2
        end_point1[1] = self.__cut_off(end_point1[1])

        points_disp.append(tuple(end_point2))
        points_disp.append(tuple(end_point1))

        self.points_disp = points_disp

        points_world = [self.__convert(
            i[0], i[1], i[2]) for i in points_disp]
        self.points_world = points_world

        self.points = [positions.RobotCoord(i[0], i[1], i[2], self.config.ROBOT_TIP_ROTATION[0],
                                            self.config.ROBOT_TIP_ROTATION[1], self.config.ROBOT_TIP_ROTATION[2], self.thickness) for i in points_world]

        #start_foreground = copy.copy(self.points[0])
        #start_foreground.x = -460123
        #start_foreground.x = -480081
        #self.points[0] = start_foreground

        end_foreground = copy.copy(self.points[-1])
        #end_foreground.x = -460123
        #end_foreground.x = -480081
        end_foreground.x = -605707
        self.points[-1] = end_foreground

    def __bezier_custom(self, x0, y0, x1, y1, x2, y2, z0, z2, t):
        #stroke_len_ratio = 0.2
        #stroke_len_ratio = 1
        stroke_len_ratio = 1
        x2 = x0 + (x2 - x0) * stroke_len_ratio
        y2 = y0 + (y2 - y0) * stroke_len_ratio
        x1 = x0 + (x2 - x0) * x1
        y1 = y0 + (y2 - y0) * y1
        x = ((1-t) * (1-t) * x0 + 2 * t * (1-t) * x1 + t * t * x2)
        y = ((1-t) * (1-t) * y0 + 2 * t * (1-t) * y1 + t * t * y2)
        z = ((1-t) * z0 + t * z2)
        return y, x, z, 0

    def __bezier_basic(self, x0, y0, x1, y1, x2, y2, z0, z2, t):
        x = ((1-t) * (1-t) * x0 + 2 * t * (1-t) * x1 + t * t * x2)
        y = ((1-t) * (1-t) * y0 + 2 * t * (1-t) * y1 + t * t * y2)
        z = ((1-t) * z0 + t * z2)
        return y, x, z, 0

    def __filter_points(self, points):
        result = [points[0]]
        total = 0
        for i in range(1, len(points)-1):
            curr = points[i]
            prev = points[i-1]
            d = math.sqrt((curr[0] - prev[0])**2 + (curr[1] - prev[1])**2)
            total += d

            if total >= 0.025:
                total = 0
                result.append(points[i])
        result.append(points[-1])
        return result

    def __curvature_modify(self, points):
        start_point = points[0]
        end_point = points[-1]
        x0 = start_point[0]
        y0 = start_point[1]
        x2 = end_point[0]
        y2 = end_point[1]

        center_relative = np.array([(x2 - x0)*0.5, (y2 - y0)*0.5])

        modified = []
        for i, point in enumerate(points):
            x = point[0]
            y = point[1]
            z = point[2]
            target = np.array([x, y])
            target_relative = target - np.array([x0, y0])
            direction_vector = target_relative - center_relative
            direction_vector /= np.linalg.norm(direction_vector)
            expand_size = (z / 20) * math.tanh((i/5) * (1)) * \
                self.config.EXPAND_RATE * self.config.THICKNESS_FACTOR
            new_target_relative = target_relative + direction_vector * expand_size
            new_target = new_target_relative + np.array([x0, y0])
            x = new_target[0]
            y = new_target[1]
            modified.append((x, y, z))
        return modified

    def __thickness_to_press_convert(self, points):
        converted = []
        for point in points:
            x = point[0]
            y = point[1]
            press = self.__thickness_to_press_regression(point[2])
            converted.append((x, y, -press))
        return converted

    def __convert(self, x, y, z):
        R = np.array([
            [np.cos(self.config.EASEL_ANG), 0, -np.sin(self.config.EASEL_ANG)],
            [0, 1, 0],
            [np.sin(self.config.EASEL_ANG), 0, np.cos(self.config.EASEL_ANG)]])

        #x_new = x / config.IMG_X * config.CANVAS_X - config.CANVAS_X / 2
        #y_new = config.CANVAS_Y - (y / config.IMG_Y * config.CANVAS_Y) + config.CANVAS_MERGIN_BUTTON

        x_new = x * self.config.CANVAS_X - self.config.CANVAS_X / 2
        y_new = self.config.CANVAS_Y - \
            (y * self.config.CANVAS_Y) + self.config.CANVAS_MERGIN_BUTTON
        c = [z, x_new, y_new]
        #  押し付け量の考慮

        #new_easel_canvas_offset = [self.config.EASEL_CANVAS_OFFSET[0] - self.__thickness_to_press_regression(z), self.config.EASEL_CANVAS_OFFSET[1], self.config.EASEL_CANVAS_OFFSET[2]]
        new_easel_canvas_offset = [self.config.EASEL_CANVAS_OFFSET[0],
                                   self.config.EASEL_CANVAS_OFFSET[1], self.config.EASEL_CANVAS_OFFSET[2]]

        return [int(i*1000) for i in self.config.EASEL_BASE_OFFSET + np.dot(new_easel_canvas_offset, R) + np.dot(c, R)]

    def __thickness_to_press_regression(self, thickness_degree):
        x = thickness_degree * self.config.IMG_X * self.config.THICKNESS_FACTOR / 10
        a = 0.8937
        b = 0.1101
        y = a*x + b

        max_press = 17
        result = min(max_press, y)
        # 線画OpenCVの結果より明らかに太いため調整している
        return result

    def __thickness_to_press_quadratic(self, thickness_degree):
        x = thickness_degree * self.config.IMG_X * self.config.THICKNESS_FACTOR / 10
        a1 = 0.0283
        a2 = 0.2191
        a3 = -0.1456
        y = a1 * x**2 + a2 * x + a3
        y = x
        max_press = 17
        result = min(max_press, y)
        return result

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

    def __cut_off(self, x):
        if x < 0:
            return 0
        elif x > 1:
            return 1
        else:
            return x

    def __vec_standardize(self, vec):
        size = math.sqrt(sum([i**2 for i in vec]))
        return [i/size for i in vec]


class StrokeColor:
    def __init__(self, r, g, b, a):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def get_rgba(self):
        return (self.r, self.g, self.b, self.a)

    def get_rgba_256(self):
        return (int(self.r * 255), int(self.g * 255), int(self.b*255), self.a)

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

    '''
    def get_cmykw(self):
        r, g, b, a = self.get_rgba()
        k = min(1-r, 1-g, 1-b)
        w = min(r, g, b)
        if k == 1:
            c = m = y = w = 0
            k = 1
        else:
            c = (1 - r - k)/(1-k)
            m = (1 - g - k)/(1-k)
            y = (1 - b - k)/(1-k)
        print(c, m, y, k)
        return c, m, y, k, w
    '''

    def get_cmykw(self):
        r, g, b, a = self.get_rgba_256()
        srgb = ImageCms.createProfile("sRGB")
        img = Image.new("RGB", (1, 1), color=(r, g, b))
        img = ImageCms.profileToProfile(
            img, srgb, '/Users/Takumi.Hongo@ibm.com/Desktop/repository/robotart/src/modules/yac_client/JapanColor2011Coated.icc',
            renderingIntent=ImageCms.INTENT_RELATIVE_COLORIMETRIC,
            outputMode="CMYK")
        cmyk = np.array(img.getdata()) / 255
        c, m, y, k = cmyk[0]
        w = (3 - (c + m + y)) / 4
        #w = min(r, g, b) / 255
        #w = (c + m + y + k) * 0.5
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
        self.EASEL_ANG = -1 * math.radians(16.4)

        # mm
        #EASEL_LENGTH = 1000
        self.EASEL_LENGTH = 820

        # mm
        self.EASEL_THICKNESS = 11
        self.CANVAS_MERGIN_BUTTON = 50

        # mm
        # ROBOT_TIP_TO_PEN_TIP = 130 (実測値は105だったが130でうまく動いている、キャンバスの厚さもこの定数に含まれている？)
        #self.ROBOT_TIP_TO_PEN_TIP = 105
        # 減らすと近く
        # 紙一枚減らすと1減らす(大体)
        #self.ROBOT_TIP_TO_PEN_TIP = 127
        self.ROBOT_TIP_TO_PEN_TIP = 142 - 135 + 5

        # mm
        # キャンバス厚さ
        self.CANVAS_THICKNESS = 8

        self.ROBOT_TIP_ROTATION = [-1065000, 0, 900000]
        #ROBOT_TIP_ROTATION = [-1050000, 0, 900000]

        self.EASEL_BASE_OFFSET = np.array([-398, 0, -(360+510)])
        self.EASEL_CANVAS_OFFSET = np.array(
            [self.EASEL_THICKNESS + self.ROBOT_TIP_TO_PEN_TIP + self.CANVAS_THICKNESS, 0, self.EASEL_LENGTH])

        self.IMG_X = 200
        self.IMG_Y = 200
        self.CANVAS_X = 200
        self.CANVAS_Y = 200

        self.THICKNESS_FACTOR = 0.6
        self.EXPAND_RATE = 0.5
