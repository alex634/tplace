import os
import socket
import struct
from PIL import Image
import configparser
import argparse

class Packet:
	def __unpack(self):
		self._x, self._y, self._r, self._g, self._b  = struct.unpack("!HHBBB", self._data)
		print(self._data)
	
	def __init__(self, data):
		self._data = data
		self.__unpack()
	
	def get_Position(self):
		return (self._x % 1024, self._y % 1024)

	def get_Pixel_Color(self):
		return (self._r, self._g, self._b)

def create_Socket(cpsr):
	s = socket.socket()
	s.bind((cpsr["server"]["ip"], int(cpsr["server"]["port"])))
	s.listen(1)
	return s

def receive_Seven(c):
	data = bytes()
	print("Waiting on bytes...")
	while len(data) < 7:
		data = c.recv(7)
	return data
	print("Received Data +")

def modify_Image(p, cpsr):
	im = Image.open(cpsr["canvas"]["filename"])
	print("Plotting pixel at (x,y): " + str(p.get_Position()))
	print("Color of pixel (r,g,b): " + str(p.get_Pixel_Color()))
	im.putpixel(p.get_Position(), p.get_Pixel_Color())
	im.save(cpsr["canvas"]["filename"])
	im.close()

def handler_Loop(s, cpsr):
	while True:
		c,a = s.accept()
		c.settimeout(5)
		print("Received connection from: " + str(a))
		try:
			data = receive_Seven(c)
			p = Packet(data)
			modify_Image(p, cpsr)
		except:
			print("Timeout reached on connection")
		c.close()
		
def create_Canvas(cpsr):
    blank_Image = Image.new("RGB", (1024,1024), (255,255,255))
    blank_Image.save(cpsr["canvas"]["filename"])
    blank_Image.close()
    

def add_Arguments(psr):
    psr.add_argument("--config", default="tplace.ini", help="The configuration file location for this program")
    psr.add_argument("--clear", default=False, action="store_true", help="Clear the canvas pointed to by the ini file or create it if it doesn't exist")

def main():
    psr = argparse.ArgumentParser()
    add_Arguments(psr)
    args = psr.parse_args()
    
    cpsr = configparser.ConfigParser()
    cpsr.read(args.config)
	    
    if args.clear or not os.path.isfile(cpsr["canvas"]["filename"]):
        create_Canvas(cpsr)
	
    s = create_Socket(cpsr)
    handler_Loop(s, cpsr)

main()
