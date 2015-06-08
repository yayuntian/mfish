#!/usr/bin/env python

import socket
def udpClient():
    address=('localhost',8080)
    udpClientSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    while True:
        data=raw_input('>')
        if not data:
            break
        udpClientSocket.sendto(data,address)
        data,addr=udpClientSocket.recvfrom(2048)
        print data
    udpClientSocket.close()

if __name__ == '__main__':
    udpClient()
