import utils.stroke_loader as stroke_loader
import matplotlib.pyplot as plt
import csv


if __name__ == "__main__":
    strokes = stroke_loader.load("./stroke_test/atom/stcoke.csv")
    for stroke in strokes:
        x = [i[0] for i in stroke.get_points_disp()]
        y = [i[1] for i in stroke.get_points_disp()]
        plt.plot(x, y, linewidth=4, color="black")

    plt.show()