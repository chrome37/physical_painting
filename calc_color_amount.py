import modules.utils.stroke_loader as stroke_loader
import sys

if __name__ == "__main__":
    args = sys.argv
    strokes = stroke_loader.load(args[1])

    colors = [i.get_color().get_cmykw() for i in strokes]
    c = sum([i[0] for i in colors])
    m = sum([i[1] for i in colors])
    y = sum([i[2] for i in colors])
    k = sum([i[3] for i in colors])
    w = sum([i[4] for i in colors])

    color_amount = 2
    sequence_count = 15

    total = c + m + y + k + w
    c, m, y, k, w = [color_amount * sequence_count * i / total for i in [c, m, y, k, w]]
    print(f'c:{int(c)} m:{int(m)} y:{int(y)} k:{int(k)} w:{int(w)}')