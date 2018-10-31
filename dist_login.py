import hashlib as hash
import getpass as get
import re
import sys

def validate_mode(input):
	if len(input) > 1:
		print('Please use a single letter \'e\' or \'n\' to specify mode')
		sys.exit()

	elif not re.match("^[^ne]*(n|e){1}[^ne]*$", input):
		print('Please use the letter \'e\' or the letter \'n\' to specify mode')
		sys.exit()
	else:
		return(input)

def new_user():
	print('Create new account')
	new_username = input('New Username: ')
	new_password = get.getpass('New Password: ')
	print(new_username)
	print(new_password)
	encoded_password = encode(new_password)
	print(encoded_password)
	sys.exit()

def existing_user():
	username = input('Username: ')
	password = get.getpass('Password: ')
	print(username)
	print(password)
	sys.exit()

def select_mode(mode):
	if 'n' in mode:
		new_user()
	elif 'e' in mode:
		existing_user()
	else:
		print('Please specify mode using the letter \'e\' or the letter \'n\'')

def encode(string):
	encoded_password = hash.sha256(string.encode())
	return(encoded_password)

mode = input('Type \'e\' for existing user, or \'n\' for new user: ')
mode = validate_mode(mode)
select_mode(mode)
