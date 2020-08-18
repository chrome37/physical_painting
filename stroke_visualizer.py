import yac_client.stroke as stroke
import matplotlib.pyplot as plt
import csv


if __name__ == "__main__":
    with open("./stroke_test/atom/stcoke.csv") as f:
        reader = csv.reader(f)
        data = [i for i in reader]
        data = [[float(j) for j in i] for i in data[1:]]
        strokes = [stroke.Stroke(i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12]) for i in data]

        for stroke in strokes:
            x = [i[0] for i in stroke.get_points_disp()]
            y = [i[1] for i in stroke.get_points_disp()]
            plt.plot(x, y, linewidth=4, color="black")

        plt.show()