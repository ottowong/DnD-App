# import pyodbc
# conn = pyodbc.connect("""Driver=(SQL Server);
# Server = DESKTOP-LJJ0KBS\SQLEXPRESS;
# Trusted_Connection=yes""")
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM dbo.Tbl_user")
# for row in cursor:
#     print(row)
#

import pyodbc

import socketserver

import pickle
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-LJJ0KBS\\SQLEXPRESS;DATABASE=DB_dnd;Trusted_Connection=yes;')
cursor = cnxn.cursor()

cursor.execute("select * from Tbl_user")
rows = cursor.fetchall()

for row in rows:
    dumpData = pickle.dumps(row)


class Handler_TCPServer(socketserver.BaseRequestHandler):
    """
    The TCP Server class for demonstration.

    Note: We need to implement the Handle method to exchange data
    with TCP client.

    """


    def handle(self):
        # self.request - TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} sent:".format(self.client_address[0]))
        print(self.data)
        # just send back ACK for data arrival confirmation
        self.request.sendall(dumpData)




if __name__ == "__main__":
    HOST, PORT = "localhost", 42069
    print("server running")
    # Init the TCP server object, bind it to the localhost on 42069 port
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.

    tcp_server.serve_forever()
