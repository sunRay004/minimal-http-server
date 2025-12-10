import os
import socket
from typing import Tuple
import re


def handleConect(connection: Tuple[socket.socket, Tuple[str, int]]):
    connectionSock = connection[0]
    returnAdress = connection[1]
    
    statCode = 0
    
    data = connectionSock.recv(2048).decode()
    
    # parse data with regex (needs to not break if recieving extra info)
    # check for errors in order 400 501 404 otherwise 200
    # if get send data, if head send only header
    # 501 for bad media types
    # head gets file size
    
    rematch = re.search(r'(?P<method>[a-zA-Z]+) /(?P<request>[^ ]*) (?P<protocol>HTTP\/1\.1)', data)
    print(data)
    
    statCode, statPhrase = getStatusCodePhrase(rematch)

    # print("Got method: {}".format(rematch.group('method')))
    # print("Got request: {}".format(rematch.group('request')))
    # print("Got protocol: {}".format(rematch.group('protocol')))

    
    # unimplementedMethods = ["POST","PUT","DELETE","CONNECT","OPTIONS","TRACE","PATCH"]
    # 

    
    # print(rematch.group('request'))
    # directory = os.path.join(os.path.curdir,"public_html")
    # print(directory)
    # requestedItemPath = os.path.join(directory,rematch.group('request'))
    # print(requestedItemPath)
    # print("requested item path is {}".format(requestedItemPath))
    


    # build responce
    
    # unformated responce and entity header line
    responce = "HTTP/1.1 {statusCode} {reasonPhrase} \r\n{entityHeader}\r\n" # entity header ends with one \r\n no mater the code
    entityHeaderLines = "Server: stupidServer/1.0.0\r\n"
    
    mBody = b''
    
    # only add length and type if 200, format on the spot
    
    if(statCode == 200):
        assert rematch is not None
        
        directory = os.path.join(os.path.curdir,"public_html")
        requestedItemPath = os.path.join(directory,rematch.group('request'))
        
        entityHeaderLinesValid = "Content-Length: {lengthOfResource}\r\nContent-Type: {typeOfResource}\r\n"
        entityHeaderLines = entityHeaderLines + entityHeaderLinesValid
        entityHeaderLines = entityHeaderLines.format(lengthOfResource=(os.path.getsize(requestedItemPath)),typeOfResource="AAAAAAAAAAAA") # TODO add type of resource
        
        # if get, then add body, otherwise dont
        if(rematch.group('method') == "GET"):
            with open(requestedItemPath,'rb') as file:
                mBody = file.read()
    
    
    # format final responce
    responce = responce.format(statusCode=statCode,reasonPhrase=statPhrase,entityHeader=entityHeaderLines)
    
    
    print("Sent message with status code {}".format(statCode))
    connectionSock.send(responce.encode())
    connectionSock.send(mBody)
    
    connectionSock.close()
    return


def getStatusCodePhrase(rematch: re.Match|None):
    if (rematch == None):
        return 400, "Malformed request"
    if (rematch.group("method") != "HEAD" and rematch.group("method") != "GET"):
        return 501, "Method not implemented"
    directory = os.path.join(os.path.curdir,"public_html")
    requestedItemPath = os.path.join(directory,rematch.group('request'))
    if (os.path.isfile(requestedItemPath) == False):
        return 404, "File not found"
    
    return 200, "Ok"
    

# current working dirrectory + uri
# responce: status line,
# Server: ServerName/ServerVersion
# Content-Length: lengthOfResource
# Content-Type: typeOfResource


if __name__ == "__main__":
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

