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
        print("Random secret number: " + str(secret_number))

        # Client variables
        tries = 0
        clients = []

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
                    #print(message)


                    print('received: ' ,message)
                    action = message[0]
                    answer = message[1]
                    token = message[2]

                    if action == OPERATION.GET_ID:
                        print('GET_ID from ' + client_address)
                        token = random.randint(1,7)
                        for x in clients:
                            while token == x[0]:
                                token = random.randint(1, 7)
                        client = [token]
                        clients += [client]
                        message = self.pack_message(OPERATION.SEND_ID, 0, token)
                        connection.sendall(message)
                        print('GET_ID responsed to' + client_address)

                    elif action == OPERATION.GET_ID_TRIES:
                        print('GET_ID & TRIES from ' + client_address)
                        token = random.randint(1, 7)
                        for x in clients:
                            while token == x[0]:
                                token = random.randint(1, 7)
                        if clients[0]:
                            tries = (clients[0][1] + clients[1][1]) / 2
                            clients[0][1] = tries
                            clients[1][1] = tries
                            message = self.pack_message(OPERATION.SEND_ID_TRIES, tries, token)
                        client = [token, tries]
                        clients += [client]
                        connection.sendall(message)
                        print('GET_ID & TRIES responsed to ' + client_address)

                    elif action == OPERATION.TRIES:
                        print('TRIES from ' + client_address)
                        for x in clients:
                            if x[0] == token:
                                tries = x[1]
                        message = self.pack_message(OPERATION.TRIES, tries, token)
                        connection.sendall(message)
                        print('TRIES responsed to ' + client_address)

                    elif action == OPERATION.GUESS:
                        print(client_address + " is GUESSing " + answer)
                        for client in clients:
                            if client[0] == token:
                                if answer == secret_number:
                                    client[2] = True
                                    message = self.pack_message(OPERATION.RESULT, 0, token)
                                    connection.sendall(message)
                                    print("RESULT send as it is GOOD answear to " + client_address)
                                else:
                                    client[1] -= 1
                                    message = self.pack_message(OPERATION.TRIES, client[1], token)
                                    connection.sendall(message)
                                    print("TRIES send as it is BAD answear to " + client_address)


                    else:
                        print('Bad flags settings!')

                    break

            finally:
                # Clean up the connection
                connection.close()

    def randomInt(self):
        number = random.randint(0,15)
        return number