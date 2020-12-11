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
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p)
    arduino_client = arduino.Client("/dev/cu.usbserial-1460", 115200, 1)
    color_device_client = arduino.ColorDeviceClient("/dev/cu.usbmodem14301", 115200, 5)
    color_device_client.color_mix(0.48, 0.45, 0, 0.09, 0)
    '''
    arduino_client.pallet_receive()
    time.sleep(3)
    arduino_client.fill_tube(1000)
    arduino_client.pallet_dispose()
    '''