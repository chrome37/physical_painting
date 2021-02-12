from . import client
import pandas as pd
import numpy as np
import binascii
import re
import time
import binascii


class Templates():

    def __init__(self, yac_client):
        self._client = yac_client

    def _base_request(self, data_size, command, data_index, request_num, compute, payload):
        request = client.Request()
        request.set_header(data_size=data_size)
        request.set_subheader(command, data_index, request_num, compute)
        request.set_payload(payload)
        self._client.execute(request)
        recv, addr = self._client.get_answer()
        return recv, addr

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


    def servo_on(self):
        data_size = "<04><00>"
        command = "<83><00>"
        data_index = "<02><00>"    # max: 99
        request_num = "<01>"    # fixed
        compute = "<10>"    # Set_Attribute_Single ：0x10
        payload = "<01><00><00><00>"

        self._base_request(data_size, command, data_index, request_num, compute, payload)

    def set_b000_to_0(self):
        data_size = "<01><00>"
        command = "<7A><00>"    # byte type
        data_index = "<00><00>"    # B000
        request_num = "<01>"    # fixed
        compute = "<02>"    # read: Set_Attribute_All ：0x02
        payload = "<00>"
        self._base_request(data_size, command, data_index, request_num, compute, payload)

    def set_b002_to_0(self):
        data_size = "<01><00>"
        command = "<7A><00>"    # byte type
        data_index = "<02><00>"    # B002
        request_num = "<01>"    # fixed
        compute = "<02>"    # read: Set_Attribute_All ：0x02
        payload = "<00>"
        self._base_request(data_size, command, data_index, request_num, compute, payload)

    def set_b001(self, df_len):
        data_size="<01><00>"
        command = "<7A><00>"    # byte type
        data_index = "<01><00>"    # B001
        request_num = "<01>"    # fixed
        compute = "<02>"    # read: Set_Attribute_All ：0x02
        payload = "<" + '{:02X}'.format(df_len) + ">"

        self._base_request(data_size, command, data_index, request_num, compute, payload)

    def start_job(self):
        data_size = "<04><00>"
        command = "<86><00>"
        data_index = "<01><00>"    # dynamic: fixed
        request_num = "<01>"    # fixed
        compute = "<10>"    # Set_Attribute_Single ：0x10
        job_start = "<01><00><00><00>"

        self._base_request(data_size, command, data_index, request_num, compute, job_start)

    def get_b002(self):
        data_size = "<00><00>"
        command = "<7A><00>"    # byte type
        data_index = "<02><00>"    # B002
        request_num = "<00>"    # fixed
        compute = "<01>"    # read: Get_Attribute_All ：0x01
        payload = ""

        self._base_request(data_size, command, data_index, request_num, compute, payload)

    def set_speed(self, speed, set_range=10):
        #print('set speed:', speed)

        for count in range(set_range):
            data_size = "<02><00>"      # dynamic (fixed: 2 byte for speed)
            command = "<7B><00>"
            data_index = "<" + '{:02X}'.format(count) + ">" + "<00>"    # max: 99
            request_num = "<01>"    # fixed
            compute = "<02>"    # Set_Attribute_All ：0x02
            padding = "<00><00>"

            # data
            speed_value = self._to_ascii(np.int64(speed), 2)
            #speed_value = "<F4><01>"    # 500: <F4><01>
            #speed_value = "<C4><09>"   # 2500
            #speed_value = "<88><13>"   # 5000
            data = speed_value

            self._base_request(data_size, command, data_index, request_num, compute, data)

        #print('set speed done')

    def set_smoothness_level(self, value, set_range):
        for count in range(set_range):
            data_size = "<04><00>"
            command = "<7C><00>"
            data_index = "<" + '{:02X}'.format(count) + ">" + "<00>"
            request_num = "<01>"
            compute = "<02>"
            padding = "<00><00>"

            data = smoothness_level = self._to_ascii(np.int64(value), 4)
            self._base_request(data_size, command, data_index, request_num, compute, data)

    def set_position(self, i, x, y, z, r_x, r_y, r_z, e, r_or_p):

        data_size = "<34><00>"      # dynamic (fixed: 52 byte for position)

        # sub header
        command = "<7F><00>"    # dynamic
        data_index = i    # dynamic: max: 99
        request_num = "<00>"    # dynamic (fixed: robot coordinate value 17)
        compute = "<02>"    # dynamic: Set_Attribute_All ：0x02
        padding = "<00><00>"

        # data
        # robot or pulse
        if r_or_p == 'p':
            data_type = "<00><00><00><00>"  # fixed
        else:
            data_type = "<11><00><00><00>"  # fixed
        form = "<00><00><00><00>"  # fixed
        tool_num = "<00><00><00><00>"  # fixed
        user_coor_num = "<00><00><00><00>"  # fixed
        custom_form = "<00><00><00><00>"  # fixed
        data_common_part = data_type + form + tool_num + user_coor_num + custom_form
        coor1 = x  # dynamic
        coor2 = y  # dynamic
        coor3 = z  # dynamic
        coor4 = r_x  # dynamic
        coor5 = r_y  # dynamic
        coor6 = r_z  # dynamic
        if r_or_p == 'p':
            coor7 = e
        else:
            coor7 = "<00><00><00><00>"  # fixed
        coor8 = "<00><00><00><00>"  # fixed
        coors = coor1 + coor2 + coor3 + coor4 + coor5 + coor6 + coor7 + coor8
        data = data_common_part + coors

        self._base_request(data_size, command, data_index, request_num, compute, data)

    def get_position(self):
        data_size = "<00><00>"
        command = "<75><00>"
        data_index = "<01><00>"
        request_num = "<00>"
        compute = "<01>"
        payload = ""

        recv, addr = self._base_request(data_size, command, data_index, request_num, compute, payload)
        return recv, addr

    def wait_job_complete(self, df_len):
        ### WAIT JOB COMPLETE START ###
        while True:
            print("wait for job completion")
            for wait_time in range(10): # Delay for 1s
                print('.', end='', flush=True)
                time.sleep(0.1)
            print()

            print("check job status")
            # header
            data_size = "<00><00>"      # dynamic (fixed: 0 byte for byte type read)

            # sub header
            command = "<7A><00>"    # byte type
            data_index = "<00><00>"    # B000
            request_num = "<01>"    # fixed
            compute = "<01>"    # read: Get_Attribute_All ：0x01
            padding = "<00><00>"

            # data
            data = ""   # no data for read

            # send data
            recv_data, addr = self._base_request(data_size, command, data_index, request_num, compute, data)
            result_flag = binascii.hexlify(recv_data)[-4:]
            #print('took ' + str(time.time() - start))

            if int(result_flag, 16) == df_len:
                print('complete!')
                print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
                print()
                time.sleep(0.1)
                break
        ### WAIT JOB COMPLETE END ###