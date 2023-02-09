# USER-SPACE MIMIC SENDER TEST

import os
from pickle import TRUE
import socket
import struct
import traceback
from argparse import ArgumentParser

NETLINK_TEST = 25
MSG = 2

def init_socket():
    s = socket.socket(socket.AF_NETLINK, socket.SOCK_RAW, NETLINK_TEST)
    s.bind((os.getpid(), 0))
    return s

def close_socket(sock):
        sock.close()

def create_netlink_msg(data="test"):
        payload = f'{data}\0'
        header_size = 16
        payload_size = len(payload)
        msg_len = header_size + payload_size
        header = struct.pack("=LHHLL", msg_len, 0, 0, 0, os.getpid())
        msg = header + payload.encode()
        return msg

def send_msg(msg, sock):
    sock.send(msg)

# def recv_msg():
#     try:
#         return socket.recv(512)
#         # return self.socket.recv()
#     except Exception as err:
#         print('\n')
#         print(traceback.format_exc())

#         # clear buffer
#         # self.socket.
#         return None

# def read_netlink_msg(self, msg):
#     value_len, value_type, value_flags, value_seq, value_pid = struct.unpack("=LHHLL", msg[:16])
#     data = msg[16:value_len]
#     return data

# def run():
#     # TODO: read the protocol from CLI
#     while True:
#         msg = create_netlink_msg(PROT)
#         send_msg(msg)
#         print("sending protocol ", PROT)


def main():
    parser = ArgumentParser()
    parser.add_argument("-p", "--prot", default=0)
    args = parser.parse_args()
    
    print("[DEBUG] Selected protocol:", args.prot)
    
    sock = init_socket()
    msg = create_netlink_msg(args.prot)
    send_msg(msg, sock)
    close_socket(sock)

if __name__=="__main__":
    main()