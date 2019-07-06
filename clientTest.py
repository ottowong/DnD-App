import socket, sys, time

TCP_IP = input("Connect to Local IP: ")
TCP_PORT = int(input("Connect to Local Port: "))
BUFFER_SIZE = 1024
running = True

def client(conn):
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data:
            break
        # broadcast
        for client in CLIENTS.values():
            client.send(data)

    # the connection is closed: unregister
    del CLIENTS[conn.fileno()]

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
