import modules.yac_client.client as YAC_client
import modules.yac_client.requests as requests
import modules.yac_client.actions as actions
import modules.yac_client.stroke as stroke
import modules.arduino.client as arduino
import modules.yac_client.positions as positions
import modules.action_bundle as action_bundle
import modules.brush as brush
import modules.utils.stroke_loader as stroke_loader
import config
import pty, os
import time
from tqdm import tqdm

def make_action_bundle():
    client_config = YAC_client.Config(src_addr=config.src_addr, src_port=config.src_port, dest_addr=config.dest_addr, dest_port=config.dest_port)
    client = YAC_client.Client(client_config)
    requests_template = requests.Templates(client)
    actions_template = actions.Templates(requests_template)

    arduino_client = arduino.Client(config.serial_port, config.baudrate, 1)

    defined_positions = positions.DefinedPositions()

    return action_bundle.ActionBundle(actions_template, arduino_client, defined_positions)

def brush_select(prev_brush, target_strokes):
    stroke_thickness = max([i.get_thickness() for i in target_strokes]) * config.image_size
    brush_thickness = "md"
    if stroke_thickness < config.small_brush_boundary:
        brush_thickness = "sm"
    elif stroke_thickness >= config.large_brush_boundary:
        brush_thickness = "lg"

    current_brush = None
    if prev_brush.thickness == brush_thickness:
        if prev_brush.index % 2 == 0:
            current_brush = brush.brush_set[prev_brush.index + 1]
        else :
            current_brush = brush.brush_set[prev_brush.index - 1]
    else :
        current_brush = [i for i in brush.brush_set if i.thickness == brush_thickness][0]

    return current_brush

if __name__ == "__main__":
    action_bundle = make_action_bundle()
    strokes = stroke_loader.load(config.stroke_file_path)

    stroke_per_loop = config.stroke_per_loop
    loop_num = int(len(strokes) / stroke_per_loop)
    target_strokes = strokes[0:stroke_per_loop]

    current_brush = brush_select(brush.brush_set[0], target_strokes)
    prev_brush = None
    for i in tqdm(range(loop_num)):
        if i == 0:
            action_bundle.initialize()
            print(current_brush.index, current_brush.thickness)

            color  = target_strokes[0].get_color()
            action_bundle.make_color(color)
            action_bundle.get_brush(current_brush.index)
            action_bundle.get_color()
            action_bundle.draw_strokes(target_strokes)
            action_bundle.pallet_clear()
            action_bundle.put_brush(6)
            prev_brush = current_brush
            time.sleep(120)
        else :
            print(f"current_loop: {i}/{loop_num}")
            target_strokes = strokes[i * stroke_per_loop:(i + 1) * stroke_per_loop]
            current_brush = brush_select(prev_brush, target_strokes)
            print(current_brush.index, current_brush.thickness)
            if current_brush.index == prev_brush.index:
                break

            color  = target_strokes[0].get_color()
            action_bundle.make_color(color)
            action_bundle.get_brush(current_brush.index)
            action_bundle.get_color()
            action_bundle.draw_strokes(target_strokes)
            action_bundle.pallet_clear()
            action_bundle.wash_brush(current_brush, prev_brush)
            prev_brush = current_brush
            time.sleep(180)

