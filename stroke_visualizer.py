import utils.stroke_loader as stroke_loader
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d import Axes3D
import sys

def draw_disp(strokes):
    for stroke in strokes:
        x = [i[0] for i in stroke.get_points_disp()]
        y = [i[1] for i in stroke.get_points_disp()]
        color = stroke.get_color()
        plt.plot(x, y, linewidth=6, color=[color.b, color.g, color.r])

    plt.show()

def draw_world(strokes):
    fig = plt.figure()
    ax = Axes3D(fig)
    for stroke in strokes:
        x = [i[0] for i in stroke.get_points_world()]
        y = [i[1] for i in stroke.get_points_world()]
        z = [i[2] for i in stroke.get_points_world()]
        color = stroke.get_color()
        ax.plot(x, y, z, linewidth=4, color=[color.r, color.g, color.b])

    plt.show()

if __name__ == "__main__":
    args = sys.argv
    strokes = stroke_loader.load(args[1])

    if args[2] == "--disp":
        draw_disp(strokes)
    elif args[2] == "--world":
        draw_world(strokes)