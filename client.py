from bitset import Bitset
from functions import *
from operation import OPERATION
import struct
import socket
import sys
import binascii
from bitstring import BitArray

class Client():
    def __init__(self):
        pass
        print("Initialize Client Protocol!")

    def dec2bin(self, d):
        # dec -> bin
        b = bin(d)
        return b

    def intTObool(self, num):
        bin_string = format(num, '04b')
        return [x == '1' for x in bin_string[::-1]]

    # Packing Frame data to Binary
    def pack_message(self,OP,AN,ID):
        operation = OPERATION(OP)

        packer = struct.Struct('5? 4? 3?')
        message = intTOboolArr(operation.value, '05b') + intTOboolArr(AN, '04b') + intTOboolArr(ID, '03b')
        #print(message)
        packed_data = packer.pack(*message)

        return packed_data


    def start(self):
        print("Client is starting!")

        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 10000)
        print >> sys.stderr, 'connecting to %s port %s' % server_address
        sock.connect(server_address)
        print(struct.Struct('5? 4? 3?').size)

        try:
            #Packing Data to Binary
            message = self.pack_message(OPERATION.GET_ID, 2, 3)

            print >> sys.stderr, 'sending "%s"' % binascii.hexlify(message)
            sock.sendall(message)

            # Look for the response
            # amount_received = 0
            # amount_expected = len(message)
            #
            # while amount_received < amount_expected:
            #     data = sock.recv(12)
            #     amount_received += len(data)
            #     print >> sys.stderr, 'received "%s"' % binascii.hexlify(data)

        finally:
            print >> sys.stderr, 'closing socket'
            sock.close()