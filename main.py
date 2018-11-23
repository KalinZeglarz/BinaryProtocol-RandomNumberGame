# Docs: https://pymotw.com/2/socket/tcp.html
import socket

from server import Server
from client import Client
import argparse

def menu(addr):
    loop = 1
    start = 0
    while loop == 1:
        start = input("Choose working mode (Server-1, User-2, Exit-0):")
        if start == 1:
            serv = Server(addr)
            serv.start()
            loop = 0
        elif start == 2:
            cli = Client(addr)
            cli.start()
            loop = 0
        elif start == 0:
            loop = 0
        else:
            print("Wrong choice. Choose again (type 1 for \"Server\" or 2 for \"User\" or 0 for Exit)")

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--addr", default="localhost", help="valid ip address for working")
parser.add_argument("-S","--server", action="store_true", default=False, help="working as server")
parser.add_argument("-C", "--client", action="store_true", default=False, help="working as client")
args = parser.parse_args()

#print str(args.addr) + str(args.client) + str(args.server)
try:
    if args.client and args.server:
        raise Exception("Bad args: Client and server cannot be combined!")

    elif args.server:
        server = Server(args.addr)
        server.start()

    elif args.client:
        client = Client(args.addr)
        client.start()
    else:
        menu(args.addr)
except Exception as err:
    print str(err)