# coding: utf-8
import serial
import serial.tools.list_ports
import time
import os
import pty
class Client:
    def __init__(self, port, bps, timeout = 1):
        self.connection = serial.Serial(port, bps, timeout=timeout)
        line = True
        while line:
            line = self.connection.readline()
            print(line)

    def __execute(self, command):
        #print(command)
        flag = bytes(command+"\n", "UTF-8")
        self.connection.write(flag)
        #print(self.connection.readline())


    def wash_pallet_with_water(self, time):
        command_string = f"COLOR N0 T{str(time).zfill(4)}"
        self.__execute(command_string)

    def wash_pallet_with_cleanser(self, time):
        command_string = f"COLOR N3 T{str(time).zfill(4)}"
        self.__execute(command_string)


    def tool(self, time):
        command_string = f"TOOL T{str(time)}"
        self.__execute(command_string)

    def cleaner(self, mode):
        mode_string = "ON" if mode else "OFF"
        command_sting = f"CLEANER {mode_string}"
        self.__execute(command_sting)

    def pump(self, n, time):
        command_string = f"PUMP N{str(n)} T{str(time)}"
        self.__execute(command_string)

    def __pallet(self, angle):
        command_string = f"PALLET D{str(angle)}"
        self.__execute(command_string)

    def pallet_dispose(self):
        self.__pallet(155)

    def pallet_feed(self):
        self.__pallet(50)

    def pallet_receive(self):
        self.__pallet(35)

    def close(self):
        self.connection.close()

    def __del__(self):
        self.connection.close()


class ColorDeviceClient:
    def __init__(self, port, bps, timeout = 1):
        self.connection = serial.Serial(port, bps, timeout=timeout)
        line = True
        while line:
            line = self.connection.readline()
            print(line)

    def __execute(self, command):
        print(command)
        flag = bytes(command+"\n", "UTF-8")
        self.connection.write(flag)
        print(self.connection.readline())

    def color_mix(self, c, m, y, k, w):
        amount = 0.75
        step_per_volume = 600
        cmykw = [c, m, y, k, w]
        total = sum(cmykw)
        standardized = [i/total for i in cmykw]
        steps = [str(int(i*amount*step_per_volume)) for i in standardized]
        command_string = f"COLOR C{steps[0].zfill(4)} M{steps[1].zfill(4)} Y{steps[2].zfill(4)} K{steps[3].zfill(4)} W{steps[4].zfill(4)} F"
        self.__execute(command_string)

    def __del__(self):
        self.connection.close()



if __name__ == "__main__":
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p)
    arduino_client = Client("/dev/cu.usbserial-1460", 115200, 1)
    arduino_client.fill_tube(9999)
