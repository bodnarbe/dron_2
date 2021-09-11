import socket

HOST = '192.168.4.1'  # The server's hostname or IP address
PORT = 80

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'LEDS ON' + b'#')
    data = s.recv(1024)

print('Received', repr(data))