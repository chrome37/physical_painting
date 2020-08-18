import utils.stroke_loader as stroke_loader
import matplotlib.pyplot as plt
import csv
from mpl_toolkits.mplot3d import Axes3D

def draw_disp(strokes):
    for stroke in strokes:
        x = [i[0] for i in stroke.get_points_disp()]
        y = [i[1] for i in stroke.get_points_disp()]
        color = stroke.get_color()
        plt.plot(x, y, linewidth=4, color=[color.r, color.g, color.b])

    plt.show()

def draw_world(strokes):
    fig = plt.figure()
    ax = Axes3D(fig)
    for stroke in strokes:
        x = [i[0] for i in stroke.get_points_world()]
        y = [i[1] for i in stroke.get_points_world()]
        z = [i[2] for i in stroke.get_points_world()]
        ax.plot(x, y, z, linewidth=4, color="black")

    plt.show()

if __name__ == "__main__":
    strokes = stroke_loader.load("./stroke_test/atom/stcoke.csv")
    draw_disp(strokes)