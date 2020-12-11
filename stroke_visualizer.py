import modules.utils.stroke_loader as stroke_loader
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d import Axes3D
import sys

def draw_disp(strokes):
    for stroke in strokes:
        x = [i[0] for i in stroke.get_points_disp()]
        y = [i[1] for i in stroke.get_points_disp()]
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        color = stroke.get_color()
        r, g, b = color.get_rgb()
        plt.plot(x, y, linewidth=10, color=[r, g, b])

    plt.show()

def draw_world(strokes):
    fig = plt.figure()
    ax = Axes3D(fig)
    for stroke in strokes:
        x = [i[0] for i in stroke.get_points_world()]
        y = [i[1] for i in stroke.get_points_world()]
        z = [i[2] for i in stroke.get_points_world()]
        color = stroke.get_color()
        r,g,b,a = color.get_rgba()
        ax.plot(x, y, z, linewidth=1, color=[r, g, b, a])

    plt.show()

if __name__ == "__main__":
    args = sys.argv
    strokes = stroke_loader.load(args[1])
    if args[2] == "--disp":
        draw_disp(strokes)
    elif args[2] == "--world":
        draw_world(strokes)