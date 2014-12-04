import socket,sys

class Client():
    def __init__(self):
        
        sys.stdout.write("Specify server ip to connect to: ")
        server = raw_input()
        sys.stdout.write("Specify port to connect to: ")
        port = raw_input()

        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection.connect((server, int(port)))
            self.running = True
        except:
            print("Could not connect to the server.")
            self.running = False
        
    def main(self):
        while self.running:
            userinput = raw_input()
            if userinput == "quit":
                print("Closing...")
                self.connection.close()
                break
            self.connection.send(userinput)
            
if __name__ == "__main__":
    client = Client()
    client.main()
