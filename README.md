# Distributed Login
Distributed login system using SQL databases and USB storage to distribute an authentication key as part of a 2FA system.

Tested with: Windows 10 build 17763

Requires: Python 3.7, MySQL 5.7.24 database(s), USB drive with at least 2MB of free space


Setup:

- Create MySQL databases required by the program, edit the provided "mysql_create*" text files in the Files directory of this project to your username/password/ip address specifications.

- Configure the USB storage device(s) for use, make sure it is named KEYDRIVE and has at least 2MB of free space. There needs to be one per user.



Running:

To run, simply point your python interpreter at the dist_login.py file in the Libraries directory of the project

- Example for Windows CMD: 
    C:\Python37> python.exe C:\Users\user\dist_login\Libraries\dist_login.py

- Example for Ubuntu 16.04(untested):
    bash:~$ python3 /home/dist_login/Libraries/dist_login.py
    
Developed by Jack:
https://jacksec.uk

