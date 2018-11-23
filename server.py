import binascii
import struct
import random
import socket
import sys
from bitstring import BitArray, ConstBitArray, ConstBitStream
#import binascii
import numpy as np
import bitarray as ba
import thread
import time

from functions import *
from operation import OPERATION


class Server:
    def __init__(self, addr):
        self.addr = addr
        print("Initialize Server Program!")

    # Packing Frame data to Binary
    def pack_message(self, OP, AN, ID):
        operation = OPERATION(OP)

        #Pakowanie do tablicy bool'i
        message = intTOboolArr(operation.value, '05b') + intTOboolArr(AN, '04b') + intTOboolArr(ID,'03b') + intTOboolArr(0, '04b')

        MESSAGE = boolList2BinString(message)
        bitstring = BitArray(MESSAGE)
        #print(str(bitstring))
        return bitstring.tobytes()

    # For unpacking massages from Binary to Frame structure
    def unpack_message(self, data):
        recvdata = bin(int(binascii.hexlify(data), 16))
        #print recvdata
        unpacked_data = recvdata[2:].zfill(16)
        #print recvdata
        unpacked_data = ba.bitarray(unpacked_data)
        unpacked_data = unpacked_data.tolist()

        #print unpacked_data

        OP = OPERATION(boolArrTOint(unpacked_data[:5]))
        AN = boolArrTOint(unpacked_data[5:9])
        ID = boolArrTOint(unpacked_data[9:12])
        return [OP, AN, ID]

    def newClient(self, connection, client_address, port, clients, secret_number, tries, client_nr):
        print "New Client: thread created"

        try:
            print 'Connection from', client_address, ":", port

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(2)
                # unpacked_data = unpacker.unpack(data)
                #print "Data len:",len(data)

                if len(data) != 0:
                    message = self.unpack_message(data)
                    # print(message)

                    print 'Received: ' + str(message)
                    action = message[0]
                    answer = message[1]
                    token = message[2]

                    if action == OPERATION.GET_ID:
                        print 'GET_ID from ' + str(client_address)
                        token = random.randint(1, 7)
                        for x in clients:
                            while token == x[0]:
                                token = random.randint(1, 7)
                        client = [token]
                        clients += [client]
                        message = self.pack_message(OPERATION.SEND_ID, 0, token)
                        connection.sendall(message)
                        print 'Responded with SEND_ID to' + str(client_address)

                    elif action == OPERATION.GET_ID_TRIES:
                        print 'GET_ID & TRIES from ' + str(client_address)
                        token = random.randint(1, 7)
                        for x in clients:
                            while token == x[0]:
                                token = random.randint(1, 7)
                        clients += [[token, answer, False]]

                        print 'ID:' + str(token) + ' GRANTED FOR ' + str(client_address)

                        if len(clients) > 1:
                            tries = (clients[0][1] + clients[1][1]) / 2
                            clients[0][1] = tries
                            clients[1][1] = tries
                            message = self.pack_message(OPERATION.SEND_ID_TRIES, tries, token)
                            connection.sendall(message)
                            print 'Responded with SEND_ID & TRIES to ' + str(client_address)
                        else:
                            message = self.pack_message(OPERATION.SEND_ID, 0, token)
                            connection.sendall(message)
                            print 'Responded with SEND_ID to ' + str(
                                client_address) + '. TRIES not send (Waiting for second player)!'

                        # while True:
                        #     if len(clients) < 1:
                        #         time.sleep(1)
                        #     else:
                        #         message = self.pack_message(OPERATION.TRIES, tries, token)
                        #         connection.sendall(message)

                    elif action == OPERATION.TRIES:
                        print 'TRIES from ' + str(client_address), ":", port
                        if answer == 0:
                            client_tries = 0 #moze powodowac error, ale na razie jest potrzebne
                            for x in clients:
                                if x[0] == token:
                                    client_tries = x[1]
                            message = self.pack_message(OPERATION.TRIES, client_tries, token)
                            connection.sendall(message)
                        elif answer == 1:
                            #print str(clients)
                            if len(clients) < 2:
                                message = self.pack_message(OPERATION.TRIES, 0, token)
                                connection.sendall(message)
                            else:
                                tries2 = (clients[0][1] + clients[1][1]) / 2
                                message = self.pack_message(OPERATION.TRIES, tries2, token)
                                connection.sendall(message)
                        print 'Responded with TRIES to ' + str(client_address), ":", port


                    elif action == OPERATION.GUESS:
                        print str(client_address) + " is GUESSing " + str(answer)
                        for client in clients:
                            if client[0] == token:
                                if answer == secret_number:
                                    client[2] = True
                                    message = self.pack_message(OPERATION.RESULT, 1, token)
                                    connection.sendall(message)
                                    print "RESULT send as it is GOOD answer to " + str(client_address)
                                else:
                                    client[1] -= 1
                                    message = self.pack_message(OPERATION.TRIES, client[1], token)
                                    connection.sendall(message)
                                    print "TRIES send as it is BAD answer to " + str(client_address)

                    else:
                        print('Error: Bad flags settings!')

                    #break

        finally:
            # Clean up the connection
            connection.close()

    def start(self):
        print("Server is starting!")

        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the port
        server_address = (self.addr, 8000)
        print >> sys.stderr, 'Starting up on %s port %s' % server_address
        sock.bind(server_address)

        # Listen for incoming connections

        sock.listen(2)

        # Picking a random integer
        secret_number = self.randomInt()
        print("Random secret number: " + str(secret_number))

        # Client variables
        tries = 0
        clients = []
        client_nr = 1

        while True:
            # Wait for a connection
            print >> sys.stderr, 'Waiting for a connection'
            connection, (client_address, port) = sock.accept()
            thread.start_new_thread(self.newClient, (connection, client_address, port, clients, secret_number, tries, client_nr))
            client_nr+=1

    def randomInt(self):
        number = random.randint(0,15)
        return number