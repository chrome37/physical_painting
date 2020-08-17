import numpy as np
import matplotlib.pyplot as plt
import csv
import sys

if __name__ == "__main__":
    csv_path = sys.argv[1]
    with open(csv_path) as f:
        reader = csv.reader(f)
        data = [i for i in reader if i[0] != "p"]
        x = [float(i[1]) for i in data]
        y = [float(i[2]) for i in data]
        #plt.xlim(0, 1)
        #plt.ylim(0, 1)
        plt.plot(x, y)
        plt.show()