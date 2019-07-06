import socket, time, sys
import threading

TCP_IP = input("Host IP: ")
TCP_PORT = int(input("Host Port: "))
BUFFER_SIZE = 1024
CLIENTS = {}
def client(conn):
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        conn.send(data)  # simple ping

def listener():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP,TCP_PORT))
    s.listen(5)
    while True:
        conn, addr = s.accept()
        # register client
        CLIENTS[conn.fileno()] = conn
        threading.Thread(target=client, args=(conn,)).start()

if __name__ == '__main__':
    listener()
