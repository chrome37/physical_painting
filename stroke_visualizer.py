from matplotlib import markers
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
        r, g, b, a = color.get_rgba()
        plt.plot(x, y, linewidth=stroke.thickness * 20, color=[r, g, b, a])

    plt.show()

def draw_world(strokes):
    fig = plt.figure()
    ax = Axes3D(fig)
    for stroke in strokes:
        x = [i.get_list()[0] for i in stroke.get_points()][1:-1]
        y = [i.get_list()[1] for i in stroke.get_points()][1:-1]
        z = [i.get_list()[2] for i in stroke.get_points()][1:-1]
        color = stroke.get_color()
        r,g,b,a = color.get_rgba()
        ax.scatter(x[0], y[0], z[0], marker="*", color=[r, g, b, a])
        ax.scatter(x[-1], y[-1], z[-1], marker="+", color=[r, g, b, a])
        ax.plot(x, y, z, linewidth=1, color=[r, g, b, a])
        #ax.plot(x[1:-1], y[1:-1], z[1:-1], marker=".", color=[r, g, b, a])

    plt.show()

if __name__ == "__main__":
    args = sys.argv
    strokes = stroke_loader.load(args[1])
    print([v.get_list() for i, v in enumerate(strokes[0].get_points()) if i <= 5])
    if args[2] == "--disp":
        draw_disp(strokes)
    elif args[2] == "--world":
        draw_world(strokes)