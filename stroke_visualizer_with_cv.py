import cv2
import numpy as np
import modules.utils.stroke_loader as stroke_loader
import csv

def normal(x, width):
    return (int)(x * (width - 1) + 0.5)

def draw(f, width=128,line_width=1.0):
    # print(f)
    x0, y0, x1, y1, x2, y2, z0, z2 = f
    z0, z2 = z0 * line_width , z2 * line_width
    x1 = x0 + (x2 - x0) * x1
    y1 = y0 + (y2 - y0) * y1
    x0 = normal(x0, width * 2)
    x1 = normal(x1, width * 2)
    x2 = normal(x2, width * 2)
    y0 = normal(y0, width * 2)
    y1 = normal(y1, width * 2)
    y2 = normal(y2, width * 2)
    z0 = (int)(1 + z0 * width // 2)
    z2 = (int)(1 + z2 * width // 2)
    canvas = np.zeros([width * 2, width * 2]).astype('float32')
    tmp = 1. / 100
    for i in range(100):
        t = i * tmp
        x = (int)((1-t) * (1-t) * x0 + 2 * t * (1-t) * x1 + t * t * x2)
        y = (int)((1-t) * (1-t) * y0 + 2 * t * (1-t) * y1 + t * t * y2)
        z = (int)((1-t) * z0 +  t * z2)
        cv2.circle(canvas, (y, x), z, 1, -1)
    return cv2.resize(canvas, dsize=(width, width))

def decode(x, canvas, width): # b * (10 + 3)
    stroke = 1 - draw(x[:8],width=width)
    stroke = stroke[:,:,None]
    color_stroke = stroke * x[-4:-1].reshape((1, 1, 3))
    canvas = canvas * (1 - stroke) + color_stroke
    return canvas

if __name__ == "__main__":
    with open("./stroke_test/monarch/imgid0_stroke_out.csv") as f:
        reader = csv.reader(f)
        data = [i for i in reader]
        data = [[float(j) for j in i] for i in data[1:]]
        strokes = np.asarray(data)

        width = 1024

        canvas = np.ones([width, width, 3])

        for i in range(strokes.shape[0]):
            canvas = decode(strokes[i], canvas, width)
            im2show = canvas.copy()
        cv2.imshow("stroke", canvas)
        cv2.waitKey(0)