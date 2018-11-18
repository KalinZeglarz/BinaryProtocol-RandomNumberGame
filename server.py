import struct
import random
from bitset import Bitset
from struct import *
import socket
import sys
import binascii
from functions import *
from operation import OPERATION


class Server():
    def __init__(self):
        pass
        print("Initialize Server Protocol!")

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
                    if data:
                        print >> sys.stderr, 'sending data back to the client'
                        if(message == secret_number):
                            data = 'You won!'
                        else:
                            data = 'Wrong choice! Try again!'
                        connection.sendall(data)
                    else:
                        print >> sys.stderr, 'no more data from', client_address
                    break

            finally:
                # Clean up the connection
                connection.close()

    def randomInt(self):
        number = random.randint(0,15)
        return number