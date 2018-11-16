import socket
import sys

class Client():
    def __init__(self):
        pass
        print("Initialize Client Protocol!")

    def start(self):
        print("Client is starting!")

        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        server_address = ('localhost', 10000)
        print >> sys.stderr, 'connecting to %s port %s' % server_address

        try:
            sock.connect(server_address)

            try:

                # Send data
                message = 'This is the message.  It will be repeated.'
                print >> sys.stderr, 'sending "%s"' % message
                sock.sendall(message)

                # Look for the response
                amount_received = 0
                amount_expected = len(message)

                while amount_received < amount_expected:
                    data = sock.recv(16)
                    amount_received += len(data)
                    print >> sys.stderr, 'received "%s"' % data

            finally:
                print >> sys.stderr, 'closing socket'
                sock.close()
        except:
            sock.close()
            print >> sys.stderr, "Server isn't running! Please run server first!"