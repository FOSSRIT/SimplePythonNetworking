import socket,json
from threading import Thread
from urllib2 import urlopen

# returns your external IP Address
def GetIp():
    try:
        return json.load(urlopen('http://httpbin.org/ip'))['origin']
    except:
        print("Could not obtain IP Address")
        return "0.0.0.0"

class ClientThread(Thread):
    def __init__(self,socket,address):
        super(ClientThread, self).__init__()
        self.running = True
        self.conn = socket
        self.address = address
    def run(self):
        while self.running:
            try:
                data = self.conn.recv(2048)

                if data == "":
                    print("Client: " + self.address[0] + " disconnected.")
                    self.running = False
                else:
                    #process data here
                    print(self.address[0] + " said: " + data)
            except socket.error as msg:
                print(msg)
                self.running = False
        print("Closing " + self.address[0] + "'s connection.")
        self.conn.close()
        
class Server():
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET,          
                                    socket.SOCK_STREAM)
        self.host = GetIp()                                 # GetIp() returns your external IP Address
        self.port = 6119
        self.socket.bind((self.host, self.port))
        print(self.host + " Listening on port: " + str(self.port)+"\n")
        self.socket.listen(10)

        self.clients = {}
                
    def main(self):
        while True:
            try:
                connection, address = self.socket.accept()   #Note - this function blocks
                                                             #execution, the code below will
                                                             #not run until a client actually
                                                             #connects


                
                thread = ClientThread(connection,address)    #the connection socket should be
                                                             #stored in a thread, as the function
                                                             #that processes data sent by clients
                                                             #also blocks execution
                thread.start()
                self.clients[address[0]] = thread
                print(address[0] + " connected!")
                
            except socket.error as msg:
                print("Socket Error: " + msg)
                break

if __name__ == "__main__":
    server = Server()
    server.main()
