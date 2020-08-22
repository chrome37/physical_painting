import yac_client.client as YAC_client
import yac_client.requests as requests
import yac_client.actions as actions
import yac_client.stroke as stroke
import arduino.client as arduino
import yac_client.positions as positions
import action_bundle
import brush
import utils.stroke_loader as stroke_loader
import config
import serial
import serial.tools.list_ports

if __name__ == "__main__":
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        print(p)
    arduino_client = arduino.Client(config.serial_port, config.baudrate, 1)
    arduino_client.fill_tube()