from . import Requests
from . import YAC_Client
from . import Positions
import numpy as np
import binascii

class Templates():
    def __init__(self, request_template):
        self.requests = request_template
        self.positions = Positions.DefinedPositions()
        self.defined_speed = {"slow": 500, "default": 2500, "high": 5000}

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
        self.requests.set_b001(df_len)

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

    def _set_position(self, position, index):
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

    def init_YAC(self):
        self.requests.set_b000_to_0()
        self.requests.servo_on()

    def refresh(self):
        self.requests.set_b000_to_0()

    def draw_strokes(self, dir_name, speed=5000):
        self.requests.set_speed(speed, 100)
        self._run(dir_name)

    def go_to(self, index, position):
        self._set_position(position, index)

    def start_job(self):
        self.requests.start_job()

    def set_job_len(self, n):
        self.requests.set_b001(n)
        return n

    def set_speed(self, speed, range):
        self.requests.set_speed(speed, range)

    def get_current_position(self):
        recv, addr = self.requests.get_position()
        answer = binascii.hexlify(recv).decode("utf-8")
        position = []
        for i in range(7):
            hexstr = ""
            if i == 0:
                hexstr = answer[-8:]
            else:
                hexstr = answer[-8*(i+1):-8*i]
            bytes_be = bytes.fromhex(hexstr)
            bytes_le = bytes_be[::-1]
            hex_le = bytes_le.hex()
            x = int(hex_le, 16)
            position.insert(0, np.int32(x))
        return Positions.PulseCoord(position[0], position[1], position[2], position[3], position[4], position[5], position[6])

    def wait_job(self, job_len):
        self.requests.wait_job_complete(job_len)


if __name__ == "__main__":
    config = YAC_Client.Config(src_addr='10.0.0.10', src_port=10050, dest_addr='10.0.0.2', dest_port=10040)
    client = YAC_Client.Client(config)
    requests = Requests.Templates(client)
    actions = Templates(requests)

    # sequence
    actions.init_YAC()
    current = actions.get_current_position()
    print(current.get_list())
    '''
    job_len = actions.set_job_len(4)
    actions.set_speed(actions.defined_speed.HIGH, job_len)
    actions.go_to_p00(0)
    actions.go_to_p01(1)
    actions.go_to_p02(2)
    actions.go_to_p03(3)
    actions.start_job()
    '''

