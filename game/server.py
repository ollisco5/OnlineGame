"""
Created on 2020-02-20

Project: OnlineGame
@author: ollejernstrom
"""
import socket
from _thread import start_new_thread
import sys

# Local ipv4ish (Server adress)
server = '192.168.43.7'
print(server)
port = 6969

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(2)
print('Server Started, Waiting for connections')


def threaded_client(conn):
    # While client connected

    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print('Disconnected')
                break

            else:
                # Print aquired data
                print('Recived: ', reply)
                print('Sending: ', reply)

            conn.sendall(str.encode(reply))

        except Exception as e:
            print(e)
            print('Disconnected')
            break


player = 0
while True:
    # conn is a socket object?
    conn, addr = s.accept()
    if conn:
        conn.send(str.encode(str(player)))
        player += 1
    print('Connected to', addr)

    start_new_thread(threaded_client, (conn,))
