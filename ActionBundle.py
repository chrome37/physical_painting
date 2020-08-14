import yac_client.YAC_Client as YAC_Client
import yac_client.Requests as Requests
import yac_client.Actions as Actions
import arduino.client as arduino_client
import yac_client.Positions as Positions
import time
class ActionBundle:
    def __init__(self, actions_template, arduino_client, positions):
        self.actions = actions_template
        self.arduino = arduino_client
        self.positions = positions

    def initialize(self):
        self.actions.init_YAC()

    def __wait_moving(self, target_position):
        target_position_coords = target_position.get_list()
        current_position_coords = []
        while target_position_coords != current_position_coords:
            current_position_coords = self.actions.get_current_position().get_list()
            time.sleep(0.1)

    def __get_brush(self, position_brush_above, position_brush):
        self.actions.init_YAC()
        job_len = self.actions.set_job_len(6)
        self.actions.set_speed(self.actions.defined_speed["default"], job_len)
        self.actions.go_to(0, self.positions.i00)
        self.actions.go_to(1, position_brush_above)
        self.actions.go_to(2, position_brush)
        self.actions.go_to(3, position_brush_above)
        self.actions.go_to(4, self.positions.i00)
        self.actions.go_to(5, self.positions.i01)
        self.actions.start_job()
        self.actions.wait_job(job_len)



    def __put_brush(self, position_brush_above, position_brush):
        self.actions.init_YAC()
        job_len = self.actions.set_job_len(4)
        self.actions.set_speed(self.actions.defined_speed["default"], job_len)
        self.actions.go_to(0, self.positions.i01)
        self.actions.go_to(1, self.positions.i00)
        self.actions.go_to(2, position_brush_above)
        self.actions.go_to(3, position_brush)
        self.actions.start_job()

        self.__wait_moving(position_brush)

        self.arduino.tool(3000)

        self.actions.init_YAC()
        job_len = self.actions.set_job_len(1)
        self.actions.set_speed(self.actions.defined_speed["default"], job_len)
        self.actions.go_to(0, position_brush_above)
        self.actions.start_job()
        self.actions.wait_job(job_len)

    def get_brush_0(self):
        self.__get_brush(self.positions.b00, self.positions.b01)

    def get_brush_1(self):
        self.__get_brush(self.positions.b10, self.positions.b11)

    def get_brush_2(self):
        self.__get_brush(self.positions.b20, self.positions.b21)

    def get_brush_3(self):
        self.__get_brush(self.positions.b30, self.positions.b31)

    def get_brush_4(self):
        self.__get_brush(self.positions.b40, self.positions.b41)

    def get_brush_5(self):
        self.__get_brush(self.positions.b50, self.positions.b51)


    def put_brush_0(self):
        self.__put_brush(self.positions.b00, self.positions.b01)

    def put_brush_1(self):
        self.__put_brush(self.positions.b10, self.positions.b11)

    def put_brush_2(self):
        self.__put_brush(self.positions.b20, self.positions.b21)

    def put_brush_3(self):
        self.__put_brush(self.positions.b30, self.positions.b31)

    def put_brush_4(self):
        self.__put_brush(self.positions.b40, self.positions.b41)

    def put_brush_5(self):
        self.__put_brush(self.positions.b50, self.positions.b51)


    def get_color(self):
        self.arduino.pallet_feed()
        self.actions.init_YAC()
        job_len = self.actions.set_job_len(4)
        self.set_speed(self.actions.defined_speed["default"], job_len)
        self.actions.go_to(0, self.positions.p00)
        self.actions.go_to(1, self.positions.p01)
        self.actions.go_to(2, self.positions.p02)
        self.actions.go_to(3, self.positions.p03)
        self.actions.start_job()
        self.wait_job(job_len)

    def pallet_clear(self):
        self.arduino.pallet_dispose()
        time.sleep(3)
        self.arduino.pallet_receive()
        time.sleep(3)
        self.arduino.wash_pallet(2000)
        self.arduino.pallet_dispose()
        time.sleep(3)
        self.arduino.pallet_receive()

    def make_color(self, r, g, b):
        self.arduino.pallet_receive()
        time.sleep(3)
        self.arduino.color_mix(r, g, b)

if __name__ == "__main__":
    config = YAC_Client.Config(src_addr='10.0.0.10', src_port=10050, dest_addr='10.0.0.2', dest_port=10040)
    client = YAC_Client.Client(config)
    requests = Requests.Templates(client)
    actions = Actions.Templates(requests)


    arduino_client = arduino_client.Client("/dev/cu.usbserial-1460", 115200, 1)

    positions = Positions.DefinedPositions()
    actionBundle = ActionBundle(actions, arduino_client, positions)

    actionBundle.get_brush_0()
    actionBundle.put_brush_0()

    actionBundle.get_brush_1()
    actionBundle.put_brush_1()

    actionBundle.get_brush_2()
    actionBundle.put_brush_2()

    actionBundle.get_brush_3()
    actionBundle.put_brush_3()

    actionBundle.get_brush_4()
    actionBundle.put_brush_4()

    actionBundle.get_brush_5()
    actionBundle.put_brush_5()
