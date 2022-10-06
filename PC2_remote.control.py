import socket

# HOST = '192.168.31.152'
HOST = '39.108.68.235'
# PORT = 8000
PORT = 6000
BUFSIZE = 1024
ADDR = (HOST, PORT)
tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect(ADDR)
FLAG = True

while True:
    data = input('>>>')
    if not data:
        break
    tcp_client.send(data.encode())
    data = tcp_client.recv(BUFSIZE)
    if not data:
        FLAG = False
        break
    print(data)

tcp_client.close()