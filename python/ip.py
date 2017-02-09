#!/usr/bin/env python


import socket
import struct

print socket.ntohl(struct.unpack("I",socket.inet_aton(str(123.138.71.228)))[0])

print socket.inet_ntoa(struct.pack('I',socket.htonl(620382275)))


class IP:

    def process(self, ip):
        re.findall(r'\d+.\d+.\d+.\d+', ip);
