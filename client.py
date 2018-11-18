import struct
import socket
import sys
import binascii
from functions import *
from operation import OPERATION

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
        packed_data = packer.pack(*message)

        return packed_data

    #For unpacking massages from Binary to Frame structure
    def unpack_message(self, data):
        unpacker = struct.Struct('5? 4? 3?')
        unpacked_data = unpacker.unpack(data)
        OP = OPERATION(boolArrTOint(unpacked_data[:5]))
        AN = boolArrTOint(unpacked_data[5:9])
        ID = boolArrTOint(unpacked_data[9:])
        return [OP,AN,ID]


    def start(self):
        print("Client is starting!")

        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 10000)
        print >> sys.stderr, 'connecting to %s port %s' % server_address
        sock.connect(server_address)
        #print(struct.Struct('5? 4? 3?').size)

        #Zmienne Clienta
        ID=0

        try:
            #Packing Data to Binary
            number = input ('Try to guess the number. Pick one from 0 to 15:')
            message = self.pack_message(OPERATION.GET_ID_TRIES, number, ID)

            #print >> sys.stderr, 'sending "%s"' % binascii.hexlify(message)
            sock.sendall(message)

            #Receive response with ID OR ID&TRIES
            data = sock.recv(12)
            received = self.unpack_message(data)
            #print(received)



            #Look for the response
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