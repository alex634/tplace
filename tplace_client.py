import socket
import sys
import struct

def create_Socket(host, port):
    s = socket.socket()
    s.connect(host, port)
    return s

#python3 tplace_client.py x y r g b host port

def create_Packet(x,y,r,g,b):
    return (struct.pack("!HHBBB") + b'\x00\x00\x00\x00\x00\x00\x00')


def main():
    x,y,r,g,b,host,port = (int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6], int(sys.argv[7]))
    bytes = create_Packet(x,y,r,g,b)
    
    s = create_Socket()
    
    s.sendall(bytes)
    s.close()
    
