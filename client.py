import os
import socket
import struct
import json
from threading import Thread
from datetime import datetime

def deco(funcion):
    
    def envolvente(*args):
         
        thread = Thread(target=funcion, args=args)

        thread.start()
        
        return thread
        
    return envolvente


class Conexion:

    def __init__(self, host, name):  

        self.host= host  

        self.name= name

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.client.connect((host, 6191))


class Client(Conexion):
 
    def client_rec(self,):

        mnj= self.client.recv(1024).decode('utf-8')

        return mnj    

    def client_send(self,):

        msj= json.dumps({'name': self.name, 'time': str(datetime.now()).replace(' ', '*')})

        self.client.send(msj.encode())    


    def send_file(self, filename):

        self.client_file = socket.create_connection((self.host, 6190))
  
        filesize = os.path.getsize(filename)
        
        self.client_file.sendall(struct.pack("<Q", filesize))
        
        with open(filename, "rb") as f:
        
            while read_bytes := f.read(1024):
        
                self.client_file.sendall(read_bytes)
 
