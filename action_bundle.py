import yac_client.client as YAC_client
import yac_client.requests as requests
import yac_client.actions as actions
import yac_client.stroke as stroke
import arduino.client as arduino_client
import yac_client.positions as positions
import time
import utils.stroke_loader as stroke_loader
class ActionBundle:
    def __init__(self, actions_template, arduino_client, positions):
        self.actions = actions_template
        self.arduino = arduino_client
        self.positions = positions
        self.holder_index_map = [
            [self.positions.b00, self.positions.b01],
            [self.positions.b10, self.positions.b11],
            [self.positions.b20, self.positions.b21],
            [self.positions.b30, self.positions.b31],
            [self.positions.b40, self.positions.b41],
            [self.positions.b50, self.positions.b51],
            [self.positions.w00, self.positions.w01],
            [self.positions.w02, self.positions.w03],
        ]

    def initialize(self):
        self.actions.init_YAC()

    def __wait_moving(self, target_position):
        target_position_coords = target_position.get_list()
        current_position_coords = []
        while target_position_coords != current_position_coords:
            current_position_coords = self.actions.get_current_position().get_list()
            time.sleep(0.1)

    def get_brush(self, holder_index):
        position_brush_above = self.holder_index_map[holder_index][0]
        position_brush = self.holder_index_map[holder_index][1]
        self.actions.refresh()
        job_len = self.actions.set_job_len(5)
        self.actions.set_speed(self.actions.defined_speed["default"], job_len)
        self.actions.go_to(0, self.positions.i00)
        self.actions.go_to(1, position_brush_above)
        self.actions.go_to(2, position_brush)
        self.actions.go_to(3, position_brush_above)
        self.actions.go_to(4, self.positions.i00)
        self.actions.start_job()
        self.actions.wait_job(job_len)

    def get_brush_from_washer(self):
        self.actions.init_YAC()
        job_len = self.actions.set_job_len(8)
        self.actions.set_speed(self.actions.defined_speed["default"], job_len)
        self.actions.go_to(0, self.positions.i00)
        self.actions.go_to(1, self.positions.w00)
        self.actions.go_to(2, self.positions.w01)
        self.actions.go_to(3, self.positions.w00)
        self.actions.go_to(4, self.positions.w02)
        self.actions.go_to(5, self.positions.w03)
        self.actions.go_to(6, self.positions.w02)
        self.actions.go_to(7, self.positions.i00)
        self.actions.start_job()
        self.actions.wait_job(job_len)

    def put_brush(self, holder_index):
        position_brush_above = self.holder_index_map[holder_index][0]
        position_brush = self.holder_index_map[holder_index][1]

        self.actions.refresh()
        job_len = self.actions.set_job_len(3)
        self.actions.set_speed(self.actions.defined_speed["default"], job_len)
        self.actions.go_to(0, self.positions.i00)
        self.actions.go_to(1, position_brush_above)
        self.actions.go_to(2, position_brush)
        self.actions.start_job()

        self.__wait_moving(position_brush)

        self.arduino.tool(1000)

        self.actions.refresh()
        job_len = self.actions.set_job_len(2)
        self.actions.set_speed(self.actions.defined_speed["default"], job_len)
        self.actions.go_to(0, position_brush_above)
        self.actions.go_to(1, self.positions.i00)
        self.actions.start_job()
        self.actions.wait_job(job_len)

    def get_color(self):
        self.arduino.pallet_feed()
        self.actions.init_YAC()
        job_len = self.actions.set_job_len(7)
        self.actions.set_speed(self.actions.defined_speed["default"], job_len)
        self.actions.go_to(0, self.positions.i01)
        self.actions.go_to(1, self.positions.p00)
        self.actions.go_to(2, self.positions.p01)
        self.actions.go_to(3, self.positions.p02)
        self.actions.go_to(4, self.positions.p03)
        self.actions.go_to(5, self.positions.p00)
        self.actions.go_to(6, self.positions.i01)
        self.actions.start_job()
        self.actions.wait_job(job_len)

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
        time.sleep(3)

    def wash_brush(self, current_brush_index, previous_brush_index):
        self.put_brush(current_brush_index)
        self.get_brush_from_washer()
        self.put_brush(previous_brush_index)
        self.get_brush(current_brush_index)
        self.put_brush(6)

    def draw_strokes(self, strokes):
        for stroke in strokes:
            points_num = len(stroke.get_points())
            self.actions.init_YAC()
            job_len = self.actions.set_job_len(points_num + 2)
            self.actions.set_speed(self.actions.defined_speed["high"], job_len)
            self.actions.go_to(0, self.positions.i01)
            self.actions.draw_stroke(1, stroke)
            self.actions.go_to(points_num + 1, self.positions.i01)
            self.actions.start_job()
            self.actions.wait_job(job_len)


if __name__ == "__main__":
    config = YAC_client.Config(src_addr='10.0.0.10', src_port=10050, dest_addr='10.0.0.2', dest_port=10040)
    client = YAC_client.Client(config)
    requests = requests.Templates(client)
    actions = actions.Templates(requests)


    arduino_client = arduino_client.Client("/dev/cu.usbserial-1440", 115200, 1)

    defined_positions = positions.DefinedPositions()
    actionBundle = ActionBundle(actions, arduino_client, defined_positions)
    strokes = stroke_loader.load("./stroke_test/atom/stcoke.csv")
    actionBundle.initialize()

    '''
    for point in strokes[0].get_points():
        print(point.get_list())
    '''

    current_brush_index = 0
    prev_brush_index = 0
    for i in range(1):
        if i == 0:
            actionBundle.get_brush(0)
            actionBundle.get_color()
            actionBundle.draw_strokes(strokes[10:15])
            actionBundle.put_brush(6)
        else :
            actionBundle.get_brush(i)
            actionBundle.get_color()
            actionBundle.draw_strokes(strokes[i*5+10:(i+1)*5+10])
            actionBundle.wash_brush(i, i-1)

