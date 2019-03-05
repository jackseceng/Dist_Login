# Distributed Login - Ssh Implementation
Distributed login system using SQL databases and USB storage to distribute an authentication key as part of a 2FA system for ssh servers.

Tested with: Ubuntu 18.04

Requires: Python 3.7, MySQL 5.7.24 database(s), USB drive with at least 2MB of free space


Setup:

- Create MySQL databases required by the program, edit the provided "mysql_create*" text files in the Files directory of this project to your username/password/ip address specifications.

- Configure the USB storage device(s) for use, make sure it is named KEYDRIVE and has at least 2MB of free space. There needs to be one per user.

- On the server, edit the 'server_ssl_setup.sh' script in the Files/ssl/ directory, and input the correct path to the dist_login.py file in your directory structure for the ~/.bashrc edit. Then run the script and any follow prompts.

- On the client run the 'client_ssl_setup.sh' script in the Files/ssl/ driectory, then follow prompts.


Running:

To run, simply log in to the sevrer via ssh from the configured client with the ssh user on the server. The project is designed to launch automatically upon ssh login. 
> (passwordless ssh is recommended. See: https://askubuntu.com/questions/46930/how-can-i-set-up-password-less-ssh-login)
    
Developed by Jack:
https://jacksec.uk

