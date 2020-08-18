import math
import numpy as np
import sys
def circle(r, theta, x0, y0):
    return (r*math.cos(theta)+x0, r*math.sin(theta)+y0)

output_path = sys.argv[1]
points_num = 98
r = 0.5
x0 = 0.5
y0 = 0.5
z0 = 0

thetas = np.arange(0, 2 * math.pi, 2*math.pi/points_num)

points = [circle(r, i, x0, y0) for i in thetas]

with open(output_path, mode="w") as f :
    for i in points:
        f.write(f"{str(i[0])}, {str(i[1])}, {str(z0)}, 0\n")
