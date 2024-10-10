import socket
import configparser
import hashlib
from PIL import Image
import struct
import sqlite3

class ReusedNonceDetector:
    def __init__(self, cpsr):
        self._connection = sqlite3.connect(cpsr["database"]["filename"])
        self._cursor = self._connection.cursor()

    def reused(self, nonce):
        rows = self._cursor.execute('SELECT * FROM used_nonces WHERE nonce_hex="' + str(nonce) + '";')
        if len(rows) == 0:
            return False
        return True

    def append_To_Used_List(nonce):
        self._cursor.execute('INSERT INTO used_nonces (nonce_hex) VALUES ("' + nonce + '");')

    def __del__(self):
        self._connection.close()


class Packet:
    def __unpack_Packet_Data(self):
        unpacked_Data = struct.unpack("!HHBBB", self._bytes)
        self._x, self._y, self._r, self._g, self._b = unpacked_Data

    def __get_packet(self):
        while self._bytes < 18:
            self._bytes = self._c.recv(18)
    
    def __init__(self, c, cpsr, rnd):
        self._c = c
        self._cpsr = cpsr
        self._bytes = bytes()
        self.__get_Packet()
        self.__unpack_Packet_Data()
        self.__rnd = rnd

    def get_Color_Tuplet(self):
        return (self._r, self._g, self._b)
    
    def get_Position_Tuplet(self):
        return (self._x, self._y)
    
    def __get_Leading_Zero_Count(self, hex_Digest):
        count = 0
        
        while hex_Digest[count] == "0":
            count += 1

        return count
    
    def check_Nonce_Hash(self):
        leading_Zeros = self._cpsr['nonce']['LeadingZeros']
        hash = hashlib.new('md5sum')
        hash.update(self._bytes)

        hex_Digest = hash.hexdigest()
        
        if self.__get_Leading_Zero_Count(hex_Digest) >= leading_Zeros and not self._rnd.reused(hex_Digest):
            self._rnd.append_To_Used_List(hex_Digest)
            return True

        return False

def open_Image_And_Plot(coord, color, cpsr):
    im = Image.open(cpsr['image']["filename"])
    im.putpixel(coord, color)
    im.save(cpsr['image']["filename"])

def read_Config():
    cpsr = configparser.ConfigParser()
    cpsr.read("tplace.ini")
    return cpsr

def create_Socket(cpsr):
    s = socket.socket()
    s.bind((cpsr['server']['BindIp'],int(cpsr['server']['BindPort'])))
    s.listen(1)
    return s

def main():
    cpsr = read_Config()
    s = create_Socket(cpsr)
    rnd = ReusedNonceDetector(cpsr)
    while True:
        c,a = s.accept()
        print("Connection accepted from: " + str(a))
        p = Packet(c, cpsr, rnd)
        if p.check_Nonce_Hash():
           open_Image_And_Plot(p.get_Position_Tuplet(), p.get_Color_Tuplet())
        c.close()

main()
