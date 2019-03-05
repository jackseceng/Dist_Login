#!/bin/bash
openssl genrsa -des3 server.orig.key 2048
openssl rsa -in server.orig.key -out server.key
openssl -req -new -key server.key -out server.csr
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
echo "Now copy server.crt to the server in the <path_to_Dist_Login_upper_directory>/Dist_Login/Files/ssl/ directory. and rename it to send_server.crt"
echo "Then run: 'Python3.7 <path_to_Libraries_directory>/client_recv.py' in a separate terminal, and leave it running (sudo priveleges required)"
