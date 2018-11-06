import re as regular_expression
from getpass import getpass as get_password
from hashlib import sha256 as hash_data
from sys import exit


def validate_mode(arg):
    if len(arg) > 1:
        return 1

    elif not regular_expression.match('[n]|[e]', arg):
        return 2

    else:
        return 0


def validate_username(arg):
    if len(arg) > 100:
        return 1

    elif not regular_expression.match('[a-z]|[A-Z]|[0-9]', arg):
        return 2

    elif sql_inject_check(arg) is True:
        return 3

    else:
        return 0


def validate_password(arg):
    if len(arg) > 100:
        return 1

    elif sql_inject_check(arg) is True:
        return 2

    else:
        return 0


def sql_inject_check(arg):
    if arg in open('sql_inject_strings.txt').read():
        return True

    else:
        return False


def new_user():
    print('Create new account')
    new_username = input_username(1)
    new_password = input_password(1)
    hashed_password = hash_password(new_password)
    output_results(new_username, new_password, hashed_password)


def existing_user():
    print('Existing user login')
    existing_username = input_username(2)
    existing_password = input_password(2)
    hashed_password = hash_password(existing_password)
    output_results(existing_username, existing_password, hashed_password)


def input_username(mode):
    arg = ''
    error_token = 4
    if mode is 1:
        arg = input('New Username: ')
    elif mode is 2:
        arg = input('Existing Username: ')
    while error_token != 0:
        error_token = validate_username(arg)
        if error_token == 1:
            print('Username too long, please try again.')
            if mode is 1:
                arg = input('New Username: ')
            elif mode is 2:
                arg = input('Existing Username: ')
        elif error_token == 2:
            print('Username contains symbols, please try again.')
            if mode is 1:
                arg = input('New Username: ')
            elif mode is 2:
                arg = input('Existing Username: ')
        elif error_token == 3:
            print('Username contains forbidden string, please try again.')
            if mode is 1:
                arg = input('New Username: ')
            elif mode is 2:
                arg = input('Existing Username: ')
    return arg


def input_password(mode):
    arg = ''
    error_token = 4
    if mode is 1:
        arg = input('New Password: ')
    elif mode is 2:
        arg = input('Password: ')
    while error_token != 0:
        error_token = validate_password(arg)
        if error_token == 1:
            print('Password too long, please try again.')
            if mode is 1:
                arg = get_password('New Password: ')
            elif mode is 2:
                arg = get_password('Password: ')
        elif error_token == 2:
            print('Password contains forbidden string, please try again.')
            if mode is 1:
                arg = get_password('New Password: ')
            elif mode is 2:
                arg = get_password('Password: ')
    return arg


def select_mode():
    print('Select \'e\' for Existing User login, or \'n\' for New User account creation')
    mode = input('Select mode: ')
    error_token = 3
    while error_token != 0:
        error_token = validate_mode(mode)
        if error_token == 1:
            print("Please use the single letter \'n\' or \'e\' to choose mode.")
            mode = input('Select mode: ')
        elif error_token == 2:
            print("Please use \'n\' for New User account creation, or \'e\' for Existing User login.")
            mode = input('Select mode: ')

    if 'n' in mode:
        new_user()

    if 'e' in mode:
        existing_user()


def hash_password(arg):
    hashed_string = hash_data(arg.encode())
    return hashed_string.hexdigest()


def output_results(username, password, hashed_password):
    print(username)
    print(password)
    print(hashed_password)
    exit()


select_mode()
