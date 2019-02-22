import socket
import sys

host = ('192.168.152.135')
port = 1337
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(3)
finish = False

print('Server listening on port ' + str(port))

try:
    while finish is False:
        client, ip = s.accept()
        print('Connection made')
        data = client.recv(4096)
        with file('usb_chunk.txt', 'w+') as f:
            f.write(data)
        client.close()
        print('Connection closed')
        finish = True
except KeyboardInterrupt as e:
    print e
