#!/usr/bin/env python
import socket
from time import ctime

def udpServer():
    buffer = 2048
    address=('127.0.0.1', 8080)
    udpsock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udpsock.bind(address)
    while True:
        print 'wait for message...'
        data, addr=udpsock.recvfrom(buffer)
        udpsock.sendto('[%s]%s' %(ctime(),data),addr)
        print '...received from and retuned to:', addr
    udpsock.close()

if __name__ == '__main__':
    udpServer()
