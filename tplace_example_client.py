import struct
import socket
import sys
import argparse

def create_Socket(args):
	s = socket.socket()
	s.connect((args.address, int(args.port)))
	return s

def send_Val(x,y,r,g,b,s):
	x = x % 1024
	y = y % 1024
	r = r % 256
	g = g % 256
	b = b % 256
	s.sendall(struct.pack("!HHBBB", x, y, r, g, b))

def add_Arguments(psr):
    psr.add_argument("address", type=str, help="The IP address of the tplace server")
    psr.add_argument("port", type=int, help="The port the tplace server is running on")
    psr.add_argument("x", type=int, help="The x coordinate of the point to plot (0-1023)")
    psr.add_argument("y", type=int, help="The y coordinate of the point to plot (0-1023) (Note: y = 0 is at the top of the canvas)")
    psr.add_argument("r", type=int, help="The red value of the pixel (0-255)")
    psr.add_argument("g", type=int, help="The green value of the pixel (0-255)")
    psr.add_argument("b", type=int, help="The blue value of the pixel (0-255)")

def main():
	psr = argparse.ArgumentParser(prog="tplace_example_client.py", description="This program sends plot requests to a tplace server.")
	add_Arguments(psr)
	args = psr.parse_args()
	
	s = create_Socket(args)
	send_Val(int(args.x), int(args.y), int(args.r), int(args.g), int(args.b), s)
	s.close()

main()
