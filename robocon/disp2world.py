import numpy as np
import os
from .config import *
from tqdm import tqdm
from natsort import natsorted

def convert(x, y, z, img_x=200, img_y=300, canvas_x=210, canvas_y=297):
    R = np.array([
       [np.cos(EASEL_ANG), 0, -np.sin(EASEL_ANG)],
       [0, 1, 0],
       [np.sin(EASEL_ANG), 0, np.cos(EASEL_ANG)]])

    x_new = x/img_x*canvas_x - canvas_x/2
    y_new = canvas_y - (y/img_y*canvas_y) + CANVAS_MERGIN_BUTTON
    c = [0, x_new, y_new]

    #  押し付け量の考慮
    #EASEL_CANPAS_OFFSET[0] += z

    return EASEL_BASE_OFFSET + np.dot(EASEL_CANPAS_OFFSET, R) + np.dot(c, R)

def convert_all(input_dir, output_dir, img_x=200, img_y=200, canvas_x=150, canvas_y=150):
    os.makedirs(output_dir, exist_ok=True)
    for i, f in tqdm(enumerate(os.listdir(input_dir))):
        out = open(os.path.join(output_dir, f'{i:05d}.csv'), 'w')
        lines_csv_raw = open(os.path.join(input_dir, f)).readlines()
        # print(','.join([str(i) for i in ROBOT_INIT_POSITION]))
        out.write(','.join([str(i) for i in ROBOT_INIT_POSITION]))
        out.write('\n')
        count = 0
        for line_csv_raw in lines_csv_raw:
            tmp = line_csv_raw.split(',')
            # print(convert(float(tmp[0])*255, float(tmp[1])*255))
            v = convert(float(tmp[0])*img_x, float(tmp[1])*img_y, float(tmp[2]),img_x=img_x, img_y=img_y, canvas_x=canvas_x, canvas_y=canvas_y) 
            v = (v * 1000).astype(np.int32)
            out.write(f'r,{v[0]},{v[1]},{v[2]},{ROBOT_TIP_ROTATION[0]},{ROBOT_TIP_ROTATION[1]},{ROBOT_TIP_ROTATION[2]}')
            # out.write(convert(float(tmp[0])*255, float(tmp[1])*255))
            out.write('\n')
            count += 1
            if count >= 98:
                break
        # print(','.join([str(i) for i in ROBOT_INIT_POSITION]))
        out.write(','.join([str(i) for i in ROBOT_INIT_POSITION]))
        out.close()


if __name__ == '__main__':
    import sys
    lines_csv_raw = open(sys.argv[1]).readlines()
    print(','.join([str(i) for i in ROBOT_INIT_POSITION]))
    for line_csv_raw in lines_csv_raw:
        tmp = line_csv_raw.split(',')
        print(convert(float(tmp[0])*255, float(tmp[1])*255))
    print(','.join([str(i) for i in ROBOT_INIT_POSITION]))

