from matplotlib import markers
import modules.utils.stroke_loader as stroke_loader
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d import Axes3D
import sys

def draw_disp(strokes):
    for stroke in strokes:
        x = [i[0] for i in stroke.get_points_disp()[1:-2]]
        y = [i[1] for i in stroke.get_points_disp()[1:-2]]
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        color = stroke.get_color()
        #print([i * 600 for i in color.get_cmykw()])
        r, g, b, a = color.get_rgba()
        plt.plot(x, y, linewidth=stroke.thickness * 10, color=[r, g, b, 0.7])
        #plt.scatter(x, y, color=[r, g, b, a])

    plt.show()

def draw_disp_with_press(strokes):
    fig = plt.figure()
    ax = Axes3D(fig)
    for stroke in strokes:
        x = [i[0] for i in stroke.get_points_disp()]
        y = [i[1] for i in stroke.get_points_disp()]
        z = [i[2] for i in stroke.get_points_disp()]
        color = stroke.get_color()
        r,g,b,a = color.get_rgba()
        ax.plot(x, y, z, linewidth=stroke.thickness * 15, color=[r, g, b, a])
    plt.show()


def draw_world(strokes):
    fig = plt.figure()
    ax = Axes3D(fig)
    for stroke in strokes:
        x = [i.get_list()[0] for i in stroke.get_points()]
        y = [i.get_list()[1] for i in stroke.get_points()]
        z = [i.get_list()[2] for i in stroke.get_points()]
        color = stroke.get_color()
        r,g,b,a = color.get_rgba()
        #ax.scatter(x[0], y[0], z[0], marker="*", color=[r, g, b, a])
        #ax.scatter(x[-1], y[-1], z[-1], marker="+", color=[r, g, b, a])
        ax.set_xlim(-600000, -400000)
        ax.set_ylim(-100000, 100000)
        ax.set_zlim(0, 200000)
        ax.plot(x, y, z, linewidth=stroke.thickness * 10, color=[r, g, b, a])
        #ax.plot(x[1:-1], y[1:-1], z[1:-1], marker=".", color=[r, g, b, a])

    plt.show()

if __name__ == "__main__":
    args = sys.argv
    strokes = stroke_loader.load(args[1])
    #print([v.get_list() for i, v in enumerate(strokes[0].get_points()) if i <= 5])
    if args[2] == "--disp":
        draw_disp(strokes)
    elif args[2] == "--disp_3D":
        draw_disp_with_press(strokes)
    elif args[2] == "--world":
        draw_world(strokes)