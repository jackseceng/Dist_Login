import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ('192.168.152.134') 
port = 1337
s.connect((host, port))

print('Connected')
with file('/media/user/KEYDRIVE/test.txt', 'rU') as f:
    data = f.read(4096)
    print('Sending')
    s.send(data.encode('utf-8'))
    print('Sent')

s.close()
print ('Connection closed')
