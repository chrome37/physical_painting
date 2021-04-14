import modules.utils.stroke_loader as stroke_loader
import sys
import math

if __name__ == "__main__":
    args = sys.argv
    strokes = stroke_loader.load(args[1])

    colors = [i.get_color().get_cmykw() for i in strokes]
    c = sum([i[0] for i in colors])
    m = sum([i[1] for i in colors])
    y = sum([i[2] for i in colors])
    k = sum([i[3] for i in colors])
    w = sum([i[4] for i in colors])

    color_amount = 1.5
    sequence_count = 5

    total = c + m + y + k + w
    c, m, y, k, w = [color_amount * sequence_count * i / total for i in [c, m, y, k, w]]
    print(f'c:{math.ceil(c)} m:{math.ceil(m)} y:{math.ceil(y)} k:{math.ceil(k)} w:{math.ceil(w)}')
    print(f'c:{c} m:{m} y:{y} k:{k} w:{w}')

    water_rates = [3/4, 5/6, 3/4, 6/7, 3/4]