import struct
import random
import socket
import sys
#import binascii
from functions import *
from operation import OPERATION


class Server():
    def __init__(self):
        pass
        print("Initialize Server Protocol!")

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
        print("Server is starting!")

        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = ('localhost', 10000)
        print >> sys.stderr, 'starting up on %s port %s' % server_address
        sock.bind(server_address)

        # Listen for incoming connections

        sock.listen(1)

        # Picking a random integer
        secret_number = self.randomInt()
        print(secret_number)

        while True:
            # Wait for a connection
            print >> sys.stderr, 'waiting for a connection'
            connection, client_address = sock.accept()

            try:
                print >> sys.stderr, 'connection from', client_address

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(12)
                    #unpacked_data = unpacker.unpack(data)
                    message = self.unpack_message(data)
                    print(message)

                    print('received: ' ,message)
                    action = message[0]
                    if action == OPERATION.GET_ID:
                        token = random.randint(1,7)
                        token = self.pack_message(OPERATION.SEND_ID)
                        connection.sendall(token)
                        print()
                    elif action == OPERATION.SEND_ID:
                        print()
                    elif action == OPERATION.TRIES:
                        print()
                    elif action == OPERATION.GUESS:
                        print()
                    elif action == OPERATION.RESULT:
                        print()

                    break

            finally:
                # Clean up the connection
                connection.close()

    def randomInt(self):
        number = random.randint(0,15)
        return number