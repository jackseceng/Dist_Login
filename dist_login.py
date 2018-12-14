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
    time = current_time()
    key = generate_key(new_username + new_password + time)
    fingerprint = fingerprint_key(key)
    store_key_fingerprint(key, fingerprint)
    output_results(new_username, new_password, key)


def existing_user():
    print('Login to existing account')
    existing_username = input_username(2)
    existing_password = input_password(2)
    previous_timestamp = open("timestamp.txt").read()
    key = generate_key(existing_username + existing_password + previous_timestamp)
    is_key_correct = fingerprint_check(key)
    if is_key_correct is True:
        print("Key is correct, login verified.")
        output_results(existing_username, existing_password, key)
    else:
        print("Key not correct, exiting...")
        exit()


def generate_key(arg):
    hashed_key = sha256_hash_data(arg.encode())
    return hashed_key.hexdigest()


def fingerprint_key(arg):
    fingerprint = sha1_hash_data(arg.encode())
    return fingerprint.hexdigest()


def fingerprint_check(arg):
    stored_key = read_stored_key()
    stored_key_fingerprint = fingerprint_key(stored_key)
    submitted_key_fingerprint = fingerprint_key(arg)
    if stored_key_fingerprint == submitted_key_fingerprint:
        return True
    else:
        return False


def read_stored_key():
    extracted_chunk0 = open("chunk0.txt").read()
    extracted_chunk1 = open("chunk1.txt").read()
    key = extracted_chunk0 + extracted_chunk1
    return key


def store_key_fingerprint(key, fingerprint):
    chunks = regular_expression.findall('................................?', key)
    chunk_file0 = open("chunk0.txt", "w")
    chunk_file0.write(chunks[0])
    chunk_file0.close()
    chunk_file1 = open("chunk1.txt", "w")
    chunk_file1.write(chunks[1])
    chunk_file1.close()
    fingerprint_file = open("fingerprint.txt", "w")
    fingerprint_file.write(fingerprint)
    fingerprint_file.close()


def current_time():
    hour = str(datetime.datetime.today().hour)
    minute = str(datetime.datetime.today().minute)
    time = hour + minute
    timestamp = open("timestamp.txt", "w")
    timestamp.write(time)
    timestamp.close()
    return time


def output_results(username, password, key):  # This function is for debugging
    print(" UsrNme", username)
    print(" PassWd", password)
    print("  InKey", key)  # The key passed into the output results function from existing or new user function
    compiled_key = read_stored_key()
    print("CompKey", compiled_key)  # Compiled key using the read_stored_key function
    fingerprint_file = open("fingerprint.txt").read()
    print("FP File", fingerprint_file)  # Fingerprint stored in fingerprint file


select_mode()
