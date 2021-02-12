from . import positions
import numpy as np
import binascii

class Templates():
    def __init__(self, request_template):
        self.requests = request_template
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

    def _set_position(self, position, index):
        #print(f"set position: {position.get_list()}")
        v = np.array(position.get_list()).astype(np.int64)
        self.requests.set_position(self._to_ascii(np.int64(index), 2),
                self._to_ascii(v[0], 4), self._to_ascii(v[1], 4),
                self._to_ascii(v[2], 4), self._to_ascii(v[3], 4),
                self._to_ascii(v[4], 4), self._to_ascii(v[5], 4),
                self._to_ascii(v[6], 4), position.mode)

    def init_YAC(self):
        self.requests.set_b000_to_0()
        self.requests.set_b002_to_0()
        self.requests.servo_on()

    def refresh(self):
        self.requests.set_b000_to_0()
        self.requests.set_b002_to_0()

    def draw_stroke(self, start_index, stroke):
        points = stroke.get_points()
        for i in range(len(points)):
            print(f"drawing stroke index: {i}")
            self._set_position(points[i], start_index + i)

    def go_to(self, index, position):
        self._set_position(position, index)

    def start_job(self):
        self.requests.start_job()

    def set_job_len(self, n):
        self.requests.set_b001(n)
        return n

    def set_speed(self, speed, set_range):
        self.requests.set_speed(speed, set_range)

    def set_smoothness(self, level, set_range):
        self.requests.set_smoothness_level(level, set_range)

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
        return positions.PulseCoord(position[0], position[1], position[2], position[3], position[4], position[5], position[6])

    def wait_job(self, job_len):
        self.requests.wait_job_complete(job_len)