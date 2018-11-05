import hashlib as hash
import getpass as get_password
import string
import re as regular_expression
import sys as system

def validate_mode(input):
	if len(input) > 1: return 1

	elif not regular_expression.match('[n]|[e]', input): return 2

	else: return 0

def validate_username(input):
	if len(input) > 100: return 1

	elif not regular_expression.match('[a-z]|[A-Z]|[0-9]', input): return 2

	elif sql_inject_check(input) == True: return 3

	else: return 0

def validate_password(input):
	if len(input) > 100: return 1

	elif sql_inject_check(input) == True: return 2

	else: return 0

def sql_inject_check(input):

	if input in open('sql_inject_strings.txt').read(): return True

	else: return False

def new_user():
	print('Create new account')
	error_token = 4
	while error_token != 0:
		new_username = input('New Username: ')
		error_token = validate_username(new_username)
		if error_token == 1:
			print('Username too long, please try again.')
		elif error_token == 2:
			print('Username contains symbols, please try again.')
		elif error_token == 3:
			print('Username contains forbidden string, please try again.')

	error_token = 4
	while error_token != 0:
		new_password = get_password.getpass('New Password: ')
		error_token = validate_password(new_password)
		if error_token == 1:
			print('Password too long, please try again.')
		elif error_token == 2:
			print('Password contains forbidden string, please try again.')

	print(new_username)
	print(new_password)
	encoded_password = encode(new_password)
	print(encoded_password)
	print(error_token)
	system.exit()

def existing_user():
	username = input('Username: ')
	password = get_password.getpass('Password: ')
	print(username)
	print(password)
	system.exit()

def select_mode():
	error_token = 3
	while error_token !=0:
		mode = input('Select mode: ')
		error_token = validate_mode(mode)
		if error_token == 1:
			print("Please use the single letter \'n\' or \'e\' to choose mode.")
		elif error_token == 2:
			print("Please use \'n\' for New User account creation, or \'e\' for Existing User login.")

	if 'n' in mode:
		new_user()
	elif 'e' in mode:
		existing_user()

def encode(string):
	encoded_password = hash.sha256(string.encode())
	return(encoded_password)

print('Select \'e\' for Existing User login, or \'n\' for New User account creation: ')
select_mode()
