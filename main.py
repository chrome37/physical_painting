import yac_client.client as YAC_client
import yac_client.requests as requests
import yac_client.actions as actions
import yac_client.stroke as stroke
import arduino.client as arduino_client
import yac_client.positions as positions
import action_bundle
import brush
import utils.stroke_loader as stroke_loader

def make_action_bundle():
    config = YAC_client.Config(src_addr='10.0.0.10', src_port=10050, dest_addr='10.0.0.2', dest_port=10040)
    client = YAC_client.Client(config)
    requests = requests.Templates(client)
    actions = actions.Templates(requests)


    arduino_client = arduino_client.Client("/dev/cu.usbserial-1440", 115200, 1)

    defined_positions = positions.DefinedPositions()

    return action_bundle.ActionBundle(actions, arduino_client, defined_positions)

def brush_select(prev_brush, target_strokes):
    stroke_thickness = target_strokes[0].get_points()[0].thickness
    brush_thickness = "md"
    if stroke_thickness < 3.5:
        brush_thickness = "sm"
    elif stroke_thickness >= 12.5:
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
    strokes = stroke_loader.load("./stroke_test/atom/stcoke.csv")

    stroke_per_loop = 5
    loop_num = len(stroke) / stroke_per_loop
    target_strokes = strokes[0:stroke_per_loop]

    initial_brush = brush.brush_set[0]
    current_brush = initial_brush
    prev_brush = None

    for i in range(loop_num):
        if i == 0:
            action_bundle.initialize()
            action_bundle.get_brush(initial_brush.index)
            action_bundle.get_color()
            action_bundle.draw_strokes(strokes[target_strokes])
            action_bundle.put_brush(6)
            prev_brush = current_brush
        else :
            target_strokes = strokes[i * stroke_per_loop:(i + 1) * stroke_per_loop]
            current_brush = brush_select(prev_brush, target_strokes)
            action_bundle.get_brush(current_brush)
            action_bundle.get_color()
            action_bundle.draw_strokes(target_strokes)
            action_bundle.wash_brush(current_brush, prev_brush)
            prev_brush = current_brush

