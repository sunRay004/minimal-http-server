import socket
from typing import Tuple
import re


def handleConect(connection: Tuple[socket.socket, Tuple[str, int]]):
    connectionSock = connection[0]
    returnAdress = connection[1]
    
    data = connectionSock.recv(2048).decode()
    
    # parse data with regex (needs to not break if recieving extra info)
    # check for errors in order 400 501 404 otherwise 200
    # if get send data, if head send only header
    
    rematch = re.search(r'(?P<method>GET|HEAD)\s(?P<request>)\s(?P<protocol>)', data)
    
    print("Matched {}".format(rematch.group('method')))
    return


localHostAdress = ("127.0.0.1",12345)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(localHostAdress)
sock.listen()



while True:
    try:
        print("Ready to recieve connection")
        conect = sock.accept()

        handleConect(conect)
    except Exception as e:
        print("got error: ")
        print(e)

