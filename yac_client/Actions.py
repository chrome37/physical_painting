import Requests
import YAC_Client
import Positions
import numpy as np

class Templates():
    DEFINED_SPEED = {"SLOW:": 500, "DEFAULT": 2500, "HIGH": 5000}
    def __init__(self, client):
        self.client = client
        self.requests = Requests.Templates(self.client)
        self.positions = Positions.DefinedPositions()

    def _to_ascii(self, dec, n_byte):
        hex_str = self._to_hex_le(dec, n_byte)
        li = [(i+j) for (i,j) in zip(hex_str[::2], hex_str[1::2])]
        ascii_code = '<' + '><'.join(li) + '>'
        return ascii_code

    def _to_hex_le(self, dec, n_byte):
        # numpy int to premitive int
        dec = np.asscalar(dec)

        if n_byte is 2:
            return dec.to_bytes(2, 'little', signed=True).hex().upper()
        elif n_byte is 4:
            return dec.to_bytes(4, 'little', signed=True).hex().upper()
        elif n_byte is 8:
            return dec.to_bytes(8, 'little', signed=True).hex().upper()
        else:
            return 'error'

    def _set_data_to_yac(self, dir_name, file_name):
        ### LOAD CSV FILE START ###
        file_path = os.path.join(dir_name, file_name)
        print('check ', file_path)

        if 'csv' not in file_name:
            print("->file is not csv")
            return False

        if not os.path.exists(file_path):
            print("->file not exist")
            return False

        print('loading...')

        # use csvreader instead
        # robot coord and pulse column does not have the same column number
        with open(file_path,'r') as csvfile:
            reader = csv.reader(csvfile)
            df = list(reader)
        #df = pd.read_csv(file_path, header=None)
        ### LOAD CSV FILE END ###

        df_len = len(df)
        self.requests.set_b001(df_len, client)

        ### SET P START ###
        # 1 loop is 1 line
        print('Writing position data...')
        for i in range(df_len):
            v = df[i]
            r_or_p = v[0]
            del v[0]

            v = np.array(v).astype(np.int64)
            if r_or_p == 'p':
                e = v[6]
            else:
                e = np.int64(0)

            self.requests.set_position(self._to_ascii(np.int64(i), 2),
                self._to_ascii(v[0], 4), self._to_ascii(v[1], 4),
                self._to_ascii(v[2], 4), self._to_ascii(v[3], 4),
                self._to_ascii(v[4], 4), self._to_ascii(v[5], 4),
                self._to_ascii(e, 4), r_or_p)
        print('done')
        ### SET P END ###

        return True, df_len

    def _set_position(self, position, index=0):
        print(position.get_list())
        v = np.array(position.get_list()).astype(np.int64)
        self.requests.set_position(self._to_ascii(np.int64(index), 2),
                self._to_ascii(v[0], 4), self._to_ascii(v[1], 4),
                self._to_ascii(v[2], 4), self._to_ascii(v[3], 4),
                self._to_ascii(v[4], 4), self._to_ascii(v[5], 4),
                self._to_ascii(v[6], 4), position.mode)

    def _get_listdir(self, dir_name):
        files = sorted([i for i in os.listdir(dir_name) if os.path.splitext(i)[1] == ".csv"])
        #for i in sorted(os.listdir(dir_name)):
        #    files.append(i)
        return files

    def _run(self, dir_name):
        # check all files in the directory
        files = self._get_listdir(dir_name)
        for file_name in files:
            point_set_success, df_len = self._set_data_to_yac(dir_name, file_name)
            if not point_set_success:
                continue
            self.requests.start_job()
            self.requests.wait_job_complete(df_len)

    def init_YAC(self, speed=DEFINED_SPEED["DEFAULT"], set_range=100):
        self.requests.set_b000_to_0()
        self.requests.servo_on()
        #self.requests.set_speed(speed, set_range)

    def draw_strokes(self, dir_name, speed=5000):
        self.requests.set_speed(speed, 100)
        self._run(dir_name)

    def go_to_i01(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.i01, index=index)

    def go_to_i00(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.i00, index=index)

    def go_to_b00(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.b00, index=index)

    def go_to_b01(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.b01, index=index)

    def go_to_b10(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.b10, index=index)

    def go_to_b11(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.b11, index=index)

    def go_to_b20(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.b20, index=index)

    def go_to_b21(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.b21, index=index)

    def go_to_b30(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.b30, index=index)

    def go_to_b31(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.b31, index=index)

    def go_to_b40(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.b40, index=index)

    def go_to_b41(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.b41, index=index)

    def go_to_b50(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.b50, index=index)

    def go_to_b51(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.b51, index=index)

    def go_to_w00(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.w00, index=index)

    def go_to_w01(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.w01, index=index)

    def go_to_w02(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.w02, index=index)

    def go_to_w03(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.w03, index=index)

    def go_to_p00(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.p00, index=index)

    def go_to_p01(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.p01, index=index)

    def go_to_p02(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.p02, index=index)

    def go_to_p03(self, index=0, speed=DEFINED_SPEED["DEFAULT"]):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.p03, index=index)

    def start_job(self):
        self.requests.start_job()

    def set_job_len(self, n):
        self.requests.set_b001(n)

    '''
    def go_to_b00(self, index=0, speed=self.defined_speed.high):
        self.requests.set_speed(speed, 100)
        self._set_position(self.positions.b00, index=index)
        self.requests.start_job()
    '''


if __name__ == "__main__":
    config = YAC_Client.Config(src_addr='10.0.0.10', src_port=10050, dest_addr='10.0.0.2', dest_port=10040)
    client = YAC_Client.Client(config)
    actions = Templates(client)

    # sequence
    actions.init_YAC()
    actions.set_job_len(4)
    #actions.go_to_i00(index=0, speed=500)
    actions.go_to_p00(index=0, speed=500)
    actions.go_to_p01(index=1, speed=500)
    actions.go_to_p02(index=2, speed=500)
    actions.go_to_p03(index=3, speed=500)
    actions.start_job()

