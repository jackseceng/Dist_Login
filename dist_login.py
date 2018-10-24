import getpass as get
import re
import sys

def validate(input):
	if len(input) > 1:
		print('Please use a single letter \'e\' or \'n\' to specify mode')
		sys.exit()

	elif not re.match("^[^ne]*(n|e){1}[^ne]*$", input):
		print('Please use the letter \'e\' or the letter \'n\' to specify mode')
		sys.exit()
	else:
		return(input)

def newu():
	print('Create new account')
	newu = input('New Username: ')
	newp = get.getpass('New Password: ')
	print(newu)
	print(newp)
	sys.exit()

def existu():
	uname = input('Username: ')
	paswd = get.getpass('Password: ')
	print(uname)
	print(paswd)
	sys.exit()

def selectmode(mode):
	if 'n' in mode:
		newu()
	elif 'e' in mode:
		existu()
	else:
		print('Please specify mode using the letter \'e\' or the letter \'n\'')

mode = input('Type \'e\' for existing user, or \'n\' for new user: ')
mode = validate(mode)
selectmode(mode)
