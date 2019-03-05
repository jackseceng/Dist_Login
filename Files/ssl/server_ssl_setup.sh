#!/bin/bash
openssl genrsa -des3 server.orig.key 2048
openssl rsa -in server.orig.key -out server.key
openssl -req -new -key server.key -out server.csr
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
echo "if [[ -n $SSH_CONNECTION ]] ; then python3.7 /home/user/Dist_Login/Libraries/dist_login.py fi" >> ~/.bashrc
echo "Now copy server.crt to the client in the '<path_to_Dist_Login_upper_directory>/Dist_Login/Files/ssl/' directory, and rename it to send_server.crt (It is recommended to transfer the certificates via a USB storage device)"
echo "Then run 'Python3.7 <path_to_Libraries_directory>/recv.py' in a separate terminal and leave it running"
