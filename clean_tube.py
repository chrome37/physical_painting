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
import serial
import serial.tools.list_ports


if __name__ == "__main__":
    arduino_client = arduino.Client(config.serial_port, config.baudrate, 1)

    arduino_client.pallet_receive()
    time.sleep(5)
    arduino_client.wash_pallet_with_cleanser(1000)
    arduino_client.pallet_dispose()