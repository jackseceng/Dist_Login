import socket
import ssl

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(s, ca_certs = "<path_to_Dist_Login>/Files/ssl/send_server.crt", cert_reqs = ssl.CERT_REQUIRED)

host = ('<server_ip') 
port = <server_port>

ssl_sock.connect((host, port))
f = open('<path_to_mounted_keydrive>/chunk.txt', 'r')

print('Connected')
with f:
    data = f.read(4096)
    print('Sending')
    ssl_sock.send(data.encode('utf-8'))
    print('Sent')

f.close()
ssl_sock.close()
print ('Connection closed')
