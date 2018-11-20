# Docs: https://pymotw.com/2/socket/tcp.html
import socket

from server import Server
from client import Client
import argparse

def menu(ip, client_B, server_B):
    loop = 1
    start = 0
    while loop == 1:
        start = input("Choose working mode (Server-1, User-2, Exit-0):")
        if start == 1:
            serv = Server()
            serv.start()
            loop = 0
        elif start == 2:
            cli = Client()
            cli.start()
            loop = 0
        elif start == 0:
            loop = 0
        else:
            print("Wrong choice. Choose again (type 1 for \"Server\" or 2 for \"User\" or 0 for Exit)")

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--addr", default=socket.gethostname(), help="provide vaid ip adrres for working")
parser.add_argument("-S","--server", action="store_true", default=False, help="working as server")
parser.add_argument("-C", "--client", action="store_true", default=True, help="working as client")
args = parser.parse_args()

print str(args)
menu(args.ip, args.client, args.server)