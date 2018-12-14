import re as regular_expression
from getpass import getpass as get_password
from hashlib import sha256 as sha256_hash_data
from hashlib import sha1 as sha1_hash_data
import datetime
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


def input_username(mode):
    arg = ''
    error_token = 4
    if mode is 1:
        arg = input('New Username: ')
    elif mode is 2:
        arg = input('Existing Username: ')
    while error_token is not 0:
        error_token = validate_username(arg)
        if error_token is 1:
            print('Username too long, please try again.')
            if mode is 1:
                arg = input('New Username: ')
            elif mode is 2:
                arg = input('Existing Username: ')
        elif error_token is 2:
            print('Username contains symbols, please try again.')
            if mode is 1:
                arg = input('New Username: ')
            elif mode is 2:
                arg = input('Existing Username: ')
        elif error_token is 3:
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
        arg = get_password('New Password: ')
    elif mode is 2:
        arg = get_password('Password: ')
    while error_token is not 0:
        error_token = validate_password(arg)
        if error_token is 1:
            print('Password too long, please try again.')
            if mode is 1:
                arg = get_password('New Password: ')
            elif mode is 2:
                arg = get_password('Password: ')
        elif error_token is 2:
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
    while error_token is not 0:
        error_token = validate_mode(mode)
        if error_token is 1:
            print("Please use the single letter \'n\' or \'e\' to choose mode.")
            mode = input('Select mode: ')
        elif error_token is 2:
            print("Please use \'n\' for New User account creation, or \'e\' for Existing User login.")
            mode = input('Select mode: ')

    if 'n' in mode:
        new_user()

    if 'e' in mode:
        existing_user()


def new_user():
    print('Create new account')
    new_username = input_username(1)
    new_password = input_password(1)
    key = hash_credentials(new_username, new_password, 2)
    fingerprint_key(key, 1)
    breakup_key(key)
    output_results(new_username, new_password)


def existing_user():
    print('Login to existing account')
    existing_username = input_username(2)
    existing_password = input_password(2)
    key = hash_credentials(existing_username, existing_password, 1)
    is_key_correct = fingerprint_key(key, 2)
    if is_key_correct is True:
        print("Key is correct, login verified.")
        output_results(existing_username, existing_password)
    else:
        print("Key not correct, exiting...")
        exit()


def read_credentials():
    extracted_chunk0 = open("chunk0.txt").read()
    extracted_chunk1 = open("chunk1.txt").read()
    timestamp = open("timestamp.txt").read()
    key = extracted_chunk0 + extracted_chunk1 + timestamp
    return key


def hash_credentials(username, password, mode):
    if mode is 1:
        time = open("timestamp.txt").read()
        credentials = username + password + time
        hashed_credentials = sha256_hash_data(credentials.encode())
        return hashed_credentials.hexdigest()
    if mode is 2:
        time = current_time()
        credentials = username + password + time
        hashed_credentials = sha256_hash_data(credentials.encode())
        return hashed_credentials.hexdigest()


def fingerprint_key(arg, mode):
    if mode is 1:
        fingerprint = sha1_hash_data(arg.encode())
        fingerprint_file = open("fingerprint.txt", "w")
        fingerprint_file.write(fingerprint.hexdigest())
        fingerprint_file.close()
    if mode is 2:
        fingerprint = sha1_hash_data(arg.encode())
        fingerprint_file = open("fingerprint.txt").read()
        if fingerprint_file == fingerprint.hexdigest():
            return True
        else:
            return False


def breakup_key(arg):
    chunks = regular_expression.findall('................................?', arg)
    chunk_file0 = open("chunk0.txt", "w")
    chunk_file0.write(chunks[0])
    chunk_file0.close()
    chunk_file1 = open("chunk1.txt", "w")
    chunk_file1.write(chunks[1])
    chunk_file1.close()


def current_time():
    hour = str(datetime.datetime.today().hour)
    minute = str(datetime.datetime.today().minute)
    time = hour + minute
    timestamp = open("timestamp.txt", "w")
    timestamp.write(time)
    timestamp.close()
    return time


def output_results(username, password):  # This function is for debugging
    print(" UsrNme", username)
    print(" PassWd", password)
    compiled_key = read_credentials()
    print("CompKey", compiled_key)  # Compiled key using the read_credentials function
    fingerprint_file = open("fingerprint.txt").read()
    print("FP File", fingerprint_file)  # Fingerprint of compiled key for verification


select_mode()
