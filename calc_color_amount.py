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

    color_amount =  1.5
    sequence_count = 6

    total = c + m + y + k + w
    cmykw = [color_amount * sequence_count * i / total for i in [c, m, y, k, w]]
    #print(f'c:{c} m:{m} y:{y} k:{k} w:{w}')

    a = 0.5
    #アクリル b = [2, 4, 2, 2, 2]
    b = [2, 3, 2, 5, 2]
    base_amount = 1
    colors = ["C", "M", "Y", "K", "W"]
    cmykw = [i+base_amount for i in cmykw]
    c,m,y,k,w = cmykw
    print(f'c:{math.ceil(c*10)/10} m:{math.ceil(m*10)/10} y:{math.ceil(y*10)/10} k:{math.ceil(k*10)/10} w:{math.ceil(w*10)/10}')
    for i in range(len(cmykw)):
       color = cmykw[i] /(a+b[i])
       water = (cmykw[i]*b[i])/(a+b[i])

       print(f"{colors[i]}:{math.ceil(color*10)/10}, 水:{math.ceil(water*10)/10}")