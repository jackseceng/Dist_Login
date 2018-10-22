import getpass

print('Login mode selection. Press \'e\' for exisitng user, or \'n\' for new user.')

mode = input('Choose mode: ')

if 'n' in mode:
	print('Create new account')
	newu = input('New Username: ')
	newp = getpass.getpass('New Password: ')
	print(newu)
	print(newp)

elif 'e' in mode:
	uname = input('Username: ')
	paswd = getpass.getpass('Password: ')
	print(uname)
	print(paswd)

else:
	print('Unrecognised command, please specify mode')
