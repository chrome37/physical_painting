import csv
import numpy as np
import sys


def bezier(x0, y0, x1, y1, x2, y2, z0, z2, t):
    x = ((1-t) * (1-t) * x0 + 2 * t * (1-t) * x1 + t * t * x2)
    y = ((1-t) * (1-t) * y0 + 2 * t * (1-t) * y1 + t * t * y2)
    z = ((1-t) * z0 + t * z2)
    return x, y, z, 0

if __name__ == "__main__":
    input_file_path = sys.argv[1]
    output_dir_path = sys.argv[2]

    point_num = 50
    with open(input_file_path) as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if i != 0:
                row = [float(i) for i in row]
                t_array = np.arange(0, 1, 1/point_num)
                points = []
                for t in t_array:
                    points.append(
                        bezier(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], t))
                with open(f"{output_dir_path}/{i-1:05d}.csv", mode="w") as f2:
                    writer = csv.writer(f2)
                    writer.writerows(points)