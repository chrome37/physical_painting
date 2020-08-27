import binascii
import socket
import re
from contextlib import contextmanager

class Config():
    def __init__(self, src_addr: str, src_port: int, dest_addr: str, dest_port: int):
        """ initialize udp connection config object

        Arguments:
            src_addr {str} -- client address
            src_port {int} -- client port
            dest_addr {str} -- server address
            dest_port {int} -- server port
        """
        self._src_addr = src_addr
        self._src_port = src_port
        self._dest_addr = dest_addr
        self._dest_port = dest_port

    def get_src_addr(self):
        return self._src_addr

    def get_src_port(self):
        return self._src_port

    def get_dest_addr(self):
        return self._dest_addr

    def get_dest_port(self):
        return self._dest_port


class Request():
    def get_header(self):
        return self._header

    def set_header(self, yerc: str = "<59><45><52><43>", header_size: str = "<20><00>", data_size: str = "<00><00>", reserved1: str = "<03><01><00><00>", blocked: str = "<00><00><00><00>", reserved2: str = "<39><39><39><39><39><39><39><39>"):
        """ set udp header for yac

        Keyword Arguments:
            yerc {str} -- fixed (default: {"<59><45><52><43>"})
            header_size {str} -- fixed (default: {"<20><00>"})
            data_size {str} -- dynamic (default: {"<00><00>"})
            reserved1 {str} -- fixed (default: {"<03><01><00><00>"})
            blocked {str} -- fixed (default: {"<00><00><00><00>"})
            reserved2 {str} -- fixed (default: {"<39><39><39><39><39><39><39><39>"})
        """
        self._yerc = yerc
        self._header_size = header_size
        self._data_size = data_size
        self._reserved1 = reserved1
        self._blocked = blocked
        self._reserved2 = reserved2
        self._header = self._yerc + self._header_size + self._data_size + \
            self._reserved1 + self._blocked + self._reserved2

    def set_subheader(self, command: str = "", data_index: str = "", request_num: str = "", compute: str = "", padding: str = "<00><00>"):
        """ set udp subheader for yac
        Keyword Arguments:
            command {str} --  (default: {""})
            data_index {str} --  (default: {""})
            request_num {str} --  (default: {""})
            compute {str} --  (default: {""})
            padding {str} -- (default: {"<00><00>"})
        """
        self._command = command
        self._data_index = data_index
        self._request_num = request_num
        self._compute = compute
        self._padding = padding
        self._subheader = self._command + self._data_index + \
            self._request_num + self._compute + self._padding

    def get_subheader(self):
        return self._subheader

    def set_payload(self, payload):
        self._payload = payload

    def get_payload(self):
        return self._payload

    def get_raw_request(self):
        return self._header + self._subheader + self._payload

    def get_request(self):
        ascii_str = self._header + self._subheader + self._payload
        data = bytearray()
        matches = re.findall(r'[0-9A-Z]{2}', ascii_str.upper())
        for match in matches:
            data += bytearray.fromhex(match)
        return data


class Client():
    def __init__(self, config: Config):
        """ initialize udp communication client for yac with config

        Arguments:
            config {Config} -- Config object
        """
        self._config = config
        self._client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._client.bind((self._config.get_src_addr(),
                           self._config.get_src_port()))

    def set_config(self, config: Config):
        self._config = config

    def execute(self, request: Request):
        self._client.sendto(request.get_request(), (self._config.get_dest_addr(), self._config.get_dest_port()))
        #print("sent>> ", binascii.hexlify(request.get_request()))

    def get_answer(self, buf_size: int = 4096):
        recv_data, addr = self._client.recvfrom(buf_size)
        #print("recv<< ", binascii.hexlify(recv_data))
        return recv_data, addr

    def close(self):
        self._client.close()