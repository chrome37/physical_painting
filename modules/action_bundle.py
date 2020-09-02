import time
class ActionBundle:
    def __init__(self, actions_template, arduino_client, positions):
        self.config = ActionBundleConfig()
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
            time.sleep(self.config.check_position_interval)

    def get_brush(self, holder_index):
        position_brush_above = self.holder_index_map[holder_index][0]
        position_brush = self.holder_index_map[holder_index][1]
        self.actions.refresh()
        job_len = self.actions.set_job_len(5)
        self.actions.set_speed(self.config.get_brush_speed, job_len)
        self.actions.set_smoothness(self.config.get_brush_smoothness, job_len)
        self.actions.go_to(0, self.positions.i00)
        self.actions.go_to(1, position_brush_above)
        self.actions.go_to(2, position_brush)
        self.actions.go_to(3, position_brush_above)
        self.actions.go_to(4, self.positions.i00)
        self.actions.start_job()
        self.actions.wait_job(job_len)

    def get_brush_from_washer(self, brush_thickness):

        washer_edge_inside = self.positions.w05
        washer_edge_outside = self.positions.w06

        if brush_thickness == "lg":
            washer_edge_inside = self.positions.w05_large
            washer_edge_outside = self.positions.w06_large

        self.actions.init_YAC()
        job_len = self.actions.set_job_len(32)
        self.actions.set_speed(self.config.get_brush_speed, job_len)
        self.actions.set_smoothness(self.config.get_brush_smoothness, job_len)
        self.actions.go_to(0, self.positions.i00)
        self.actions.go_to(1, self.positions.w00)
        self.actions.go_to(2, self.positions.w01)
        self.actions.go_to(3, self.positions.w00)
        self.actions.go_to(4, self.positions.w02)
        self.actions.go_to(5, self.positions.w03)
        self.actions.go_to(6, self.positions.w02)

        self.actions.go_to(7, self.positions.w04)
        self.actions.go_to(8, washer_edge_inside)
        self.actions.go_to(9, washer_edge_outside)
        self.actions.go_to(10, self.positions.w07)

        self.actions.go_to(11, self.positions.w08)
        self.actions.go_to(12, washer_edge_inside)
        self.actions.go_to(13, washer_edge_outside)
        self.actions.go_to(14, self.positions.w07)

        self.actions.go_to(15, self.positions.w08)
        self.actions.go_to(16, washer_edge_inside)
        self.actions.go_to(17, washer_edge_outside)
        self.actions.go_to(18, self.positions.w07)

        self.actions.go_to(19, self.positions.w08)
        self.actions.go_to(20, washer_edge_inside)
        self.actions.go_to(21, washer_edge_outside)
        self.actions.go_to(22, self.positions.w07)

        self.actions.go_to(23, self.positions.w08)
        self.actions.go_to(24, washer_edge_inside)
        self.actions.go_to(25, washer_edge_outside)
        self.actions.go_to(26, self.positions.w07)

        self.actions.go_to(27, self.positions.w08)
        self.actions.go_to(28, washer_edge_inside)
        self.actions.go_to(29, washer_edge_outside)
        self.actions.go_to(30, self.positions.w07)

        self.actions.go_to(31, self.positions.i00)
        self.actions.start_job()
        self.actions.wait_job(job_len)

    def put_brush(self, holder_index):
        position_brush_above = self.holder_index_map[holder_index][0]
        position_brush = self.holder_index_map[holder_index][1]

        self.actions.refresh()
        job_len = self.actions.set_job_len(3)
        self.actions.set_speed(self.config.put_brush_speed, job_len)
        self.actions.set_smoothness(self.config.put_brush_smoothness, job_len)
        self.actions.go_to(0, self.positions.i00)
        self.actions.go_to(1, position_brush_above)
        self.actions.go_to(2, position_brush)
        self.actions.start_job()

        self.__wait_moving(position_brush)

        self.arduino.tool(self.config.tool_detach_time)
        time.sleep(0.5)

        self.actions.refresh()
        job_len = self.actions.set_job_len(2)
        self.actions.set_speed(self.config.put_brush_speed, job_len)
        self.actions.set_smoothness(self.config.put_brush_smoothness, job_len)
        self.actions.go_to(0, position_brush_above)
        self.actions.go_to(1, self.positions.i00)
        self.actions.start_job()
        self.actions.wait_job(job_len)

    def get_color(self):
        self.arduino.pallet_feed()
        self.actions.init_YAC()
        job_len = self.actions.set_job_len(4)
        self.actions.set_speed(self.config.get_color_speed, job_len)
        self.actions.set_smoothness(self.config.get_color_smoothness, job_len)
        self.actions.go_to(0, self.positions.i01)
        self.actions.go_to(1, self.positions.p00)
        self.actions.go_to(2, self.positions.p01)
        self.actions.go_to(3, self.positions.p01_take)
        self.actions.start_job()
        self.__wait_moving(self.positions.p01_take)
        time.sleep(1)

        self.actions.refresh()
        job_len = self.actions.set_job_len(8)
        self.actions.go_to(0, self.positions.p02)
        self.actions.go_to(1, self.positions.p03)
        self.actions.go_to(2, self.positions.p04)
        self.actions.go_to(3, self.positions.p05)
        self.actions.go_to(4, self.positions.p02)
        self.actions.go_to(5, self.positions.p03)
        self.actions.go_to(6, self.positions.p00)
        self.actions.go_to(7, self.positions.i01)
        self.actions.start_job()
        self.actions.wait_job(job_len)

    def pallet_clear(self):
        self.arduino.pallet_dispose()
        time.sleep(self.config.pallet_move_wait_time)
        self.arduino.pallet_receive()
        time.sleep(self.config.pallet_move_wait_time)
        '''
        self.arduino.wash_pallet(self.config.wash_pallet_time)
        time.sleep(5)
        self.arduino.pallet_dispose()
        time.sleep(self.config.pallet_move_wait_time)
        self.arduino.pallet_receive()
        '''


    def make_color(self, color):
        c, m, y, k, w = color.get_cmykw()
        self.arduino.pallet_receive()
        time.sleep(self.config.pallet_move_wait_time)
        self.arduino.color_mix(c, m, y, k, w)
        time.sleep(self.config.pallet_move_wait_time)

    def wash_brush(self, current_brush, previous_brush):
        current_brush_index = current_brush.index
        previous_brush_index  = previous_brush.index
        self.put_brush(current_brush_index)
        self.get_brush_from_washer(previous_brush.thickness)
        self.put_brush(previous_brush_index)
        self.get_brush(current_brush_index)
        self.put_brush(6)

    def draw_strokes(self, strokes):
        for stroke in strokes:
            points_num = len(stroke.get_points())
            self.actions.init_YAC()
            job_len = self.actions.set_job_len(points_num + 2)
            self.actions.set_speed(self.config.draw_strokes_speed, job_len)
            self.actions.set_smoothness(self.config.draw_strokes_smoothness, job_len)
            self.actions.go_to(0, self.positions.i01)
            self.actions.draw_stroke(1, stroke)
            self.actions.go_to(points_num + 1, self.positions.i01)
            self.actions.start_job()
            self.actions.wait_job(job_len)

    def test(self):
        self.arduino.pallet_feed()
        self.actions.init_YAC()
        job_len = self.actions.set_job_len(5)
        self.actions.set_speed(self.config.get_color_speed, job_len)
        self.actions.set_smoothness(self.config.get_color_smoothness, job_len)

        self.actions.go_to(0, self.positions.i01)
        self.actions.go_to(1, self.positions.p00)
        self.actions.go_to(2, self.positions.p01)
        self.actions.go_to(3, self.positions.p02)
        self.actions.go_to(4, self.positions.p03)

        self.actions.start_job()
        self.actions.wait_job(job_len)

class ActionBundleConfig:
    def __init__(self):
        self.check_position_interval = 0.1
        self.get_brush_speed = 2500
        self.get_brush_smoothness = 0

        self.put_brush_speed = 2500
        self.put_brush_smoothness = 0

        self.draw_strokes_speed = 2500
        self.draw_strokes_smoothness = 5

        self.get_color_speed = 2500
        self.get_color_smoothness = 0

        self.tool_detach_time = 3000
        self.wash_pallet_time = 2000
        self.pallet_move_wait_time = 5