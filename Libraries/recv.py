import socket
import ssl

def save_data(data):
    f = open('<path_to_Dist_Login>/Files/usb_chunk.txt', 'w+')
    received = (data.decode('utf-8')).rstrip()
    with f:
        f.write(received)

def receive_data(stream):
    data = stream.read()
    while data:
        if not save_data(data):
            break
        data = stream.read()

bindsocket = socket.socket()
bindsocket.bind(('', <server_port>))
bindsocket.listen(5)

while True:
    newsocket, fromaddr = bindsocket.accept()
    stream = ssl.wrap_socket(newsocket, server_side = True, certfile = "<path_to_Dist_Login>/Files/ssl/recv_server.crt", keyfile = "<path_to_Dist_Login>/Files/ssl/recv_server.key")
    try:
        print('Receiving usb key chunk')
        receive_data(stream)
    finally:
        stream.shutdown(socket.SHUT_RDWR)
        stream.close()
        print("Closed local file")

