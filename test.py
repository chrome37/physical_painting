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
import socket

def make_action_bundle():
    client_config = YAC_client.Config(src_addr=config.src_addr, src_port=config.src_port, dest_addr=config.dest_addr, dest_port=config.dest_port)
    client = YAC_client.Client(client_config)
    requests_template = requests.Templates(client)
    actions_template = actions.Templates(requests_template)

    arduino_client = arduino.Client(config.serial_port, config.baudrate, 1)

    defined_positions = positions.DefinedPositions()

    return action_bundle.ActionBundle(actions_template, arduino_client, defined_positions)


if __name__ == "__main__":

    action_bundle = make_action_bundle()
    strokes = stroke_loader.load(config.stroke_file_path)
    r, g, b = strokes[0].get_color().get_rgb()
    action_bundle.make_color(r, g, b)