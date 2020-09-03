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
        print(command)
        flag = bytes(command+"\n", "UTF-8")
        self.connection.write(flag)
        print(self.connection.readline())

    def __cmyk_to_time(self, cmykw):
        total = sum(cmykw)
        standardized = [i/total for i in cmykw]
        amount = 1.5
        speed = 2.5
        times = [int((i*amount/speed)*1000) for i in standardized]
        return times

    def color_mix(self, c, m, y, k, w):
        cmykw = [c, m, y, k, w]
        times = self.__cmyk_to_time(cmykw)

        for i in range(len(times)):
            command_string = f"COLOR N{str(i)} T{str(times[i]).zfill(4)}"
            self.__execute(command_string)

    def fill_tube(self, time):
        for i in range(5):
            command_string = f"COLOR N{str(i)} T{str(time)}"
            self.__execute(command_string)

    def wash_pallet(self, time):
        command_string = f"COLOR N4 T{str(time)}"
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
        self.__pallet(70)

    def pallet_receive(self):
        self.__pallet(10)

    def close(self):
        self.connection.close()

    def __del__(self):
        self.connection.close()

    def color_test(self, n, time):
        self.__execute(f"COLOR N{str(n)} T{str(time).zfill(4)}")

if __name__ == "__main__":
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p)
    arduino_client = Client("/dev/cu.usbserial-1460", 115200, 1)
    arduino_client.fill_tube(9999)
