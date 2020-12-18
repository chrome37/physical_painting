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
import pty
import os
import socket


def make_action_bundle():
    client_config = YAC_client.Config(
        src_addr=config.src_addr, src_port=config.src_port, dest_addr=config.dest_addr, dest_port=config.dest_port)
    client = YAC_client.Client(client_config)
    requests_template = requests.Templates(client)
    actions_template = actions.Templates(requests_template)

    arduino_client = arduino.Client(config.serial_port, config.baudrate, 1)
    color_device_client = arduino.ColorDeviceClient(
        config.serial_port_2, config.baudrate_2, 5)

    defined_positions = positions.DefinedPositions()

    return action_bundle.ActionBundle(actions_template, arduino_client, color_device_client, defined_positions), actions_template, arduino_client


if __name__ == "__main__":

    action_bundle, actions_template, arduino_client = make_action_bundle()
    action_bundle.initialize()
    action_bundle.go_to_position(action_bundle.positions.w00)
