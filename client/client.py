import socket
import pickle

host_ip, server_port = "localhost", 42069
data = "Hello how are you?\n"

# Initialize a TCP client socket using SOCK_STREAM
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Establish connection to TCP server and exchange data
    tcp_client.connect((host_ip, server_port))
    tcp_client.sendall(data.encode())

    # Read data from the TCP server and close the connection
    received = pickle.loads(tcp_client.recv(1024))
finally:
    tcp_client.close()


print ("Bytes Sent:     {}".format(data))
print ("Bytes Received: {}".format(pickle.loads(received)))
