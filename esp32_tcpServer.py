import socket

class tcp_server:
    def __init__(self,ip,port) -> None:
        self.ip=ip
        self.port=port
        self.connection_status=False
        try:
            self.tcpSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        except Exception as e:
            print("Err while socket creation:",e)

    def connect_to_esp(self):
        try:
            self.tcpSocket.connect((self.ip,self.port)) 
            self.connection_status=True;
        except Exception as e:
            print("Err while connecting to esp32:",e)

    def send_data(self,data):
        self.tcpSocket.send(data.encode('utf-8'))

    def receive_data(self):
        message=self.tcpSocket.recv(1024).decode().rstrip()
        try:
            #return self.parse_message(message)
            return message
        except:
            pass

    def parse_message(self,message):
        match message[0]:
            case "*":
                sensor_id, sensor_data=message[1:].split('_')
                d_type="sensor"
                return d_type,sensor_id,sensor_data
            case "?":
                _,card_id=message[1:].split('_')
                d_type="card"
                return d_type,card_id
            
if __name__ == "__main__":
    connection_line = tcp_server("192.168.4.1",2024)
    connection_line.connect_to_esp()
    while(1):
        connection_line.receive_data()