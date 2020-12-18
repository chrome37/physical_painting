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

def get_cmyk(r, g, b):

        k = min(1-r, 1-g, 1-b)
        if k == 1:
            c = m = y = w = 0
            k = 1
        else :
            c = (1 - r - k)/(1-k)
            m = (1 - g - k)/(1-k)
            y = (1 - b - k)/(1-k)

        return c, m, y, k

if __name__ == "__main__":
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p)
    arduino_client = arduino.Client("/dev/cu.usbserial-1460", 115200, 1)
    color_device_client = arduino.ColorDeviceClient("/dev/cu.usbmodem14301", 9600, 3)
    arduino_client.pallet_receive()
    time.sleep(5)
    c, m, y, k= get_cmyk(0.5, 0, 0.5)
    print(c, m, y, k)
    color_device_client.color_mix(c, m, y, k, 0)
    '''
    arduino_client.pallet_receive()
    time.sleep(3)
    arduino_client.fill_tube(1000)
    arduino_client.pallet_dispose()
    '''