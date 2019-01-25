import re as regular_expression
from getpass import getpass as get_password
from hashlib import sha256 as sha256_hash_data
from hashlib import sha1 as sha1_hash_data
from sys import exit
import subprocess
import os
import mysql.connector


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
    username = ''
    error_token = 4
    if mode is 1:
        username = input('New Username: ')
    elif mode is 2:
        username = input('Existing Username: ')
    while error_token is not 0:
        error_token = validate_username(username)
        if error_token is 1:
            print('Username too long, please try again.')
            if mode is 1:
                username = input('New Username: ')
            elif mode is 2:
                username = input('Existing Username: ')
        elif error_token is 2:
            print('Username contains symbols, please try again.')
            if mode is 1:
                username = input('New Username: ')
            elif mode is 2:
                username = input('Existing Username: ')
        elif error_token is 3:
            print('Username contains forbidden string, please try again.')
            if mode is 1:
                username = input('New Username: ')
            elif mode is 2:
                username = input('Existing Username: ')
    return username


def input_password(mode): # This does not  permanently store the users password, in any form, anywhere.
    password = ''
    error_token = 4
    if mode is 1:
        password = get_password('New Password: ')
    elif mode is 2:
        password = get_password('Password: ')
    while error_token is not 0:
        error_token = validate_password(password)
        if error_token is 1:
            print('Password too long, please try again.')
            if mode is 1:
                password = get_password('New Password: ')
            elif mode is 2:
                password = get_password('Password: ')
        elif error_token is 2:
            print('Password contains forbidden string, please try again.')
            if mode is 1:
                password = get_password('New Password: ')
            elif mode is 2:
                password = get_password('Password: ')
    return password


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
    keydrive = detect_keydrive()
    if keydrive is True:
        new_username = input_username(1)
        new_password = input_password(1)
        encrypted_password = fingerprint_data(new_username + new_password)
        sql_write_user_identifiers(new_username, encrypted_password)
        sql_write_username_timestamp(new_username)
        timestamp = sql_read_timestamp(new_username)
        key = generate_key(new_username + new_password + timestamp)
        fingerprint = fingerprint_data(key)
        store_key_fingerprint(new_username, key, fingerprint)
        output_results(new_username, new_password)
        session(0, new_username)  # Function for illustration purposes only
    else:
        input("KEYDRIVE not detected, insert KEYDRIVE then press enter to try again.")
        new_user()


def existing_user():
    print('Sign in to existing account')
    keydrive = detect_keydrive()
    if keydrive is True:
        existing_username = input_username(2)
        existing_password = input_password(2)
        encrypted_password = fingerprint_data(existing_username + existing_password)
        stored_identifier = sql_read_identifier(existing_username)
        is_sign_in_correct = identifier_check(encrypted_password, stored_identifier)
        if is_sign_in_correct is True:
            is_key_correct = fingerprint_check(existing_username)
            if is_key_correct is True:
                print("Key is correct, sign in verified.")
                output_results(existing_username, existing_password)
                session(1, existing_username)  # Function for illustration purposes
            else:
                print("Key is not correct, exiting...")
                exit()
        else:
            print("Password is not correct, exiting...")
            exit()
    else:
        input("KEYDRIVE not detected, insert KEYDRIVE then press enter to try again.")
        existing_user()


def session(mode, user):
    # This function is only for illustrating a successful session sign in, replace it with the sign in method required
    if mode is 0:
        print('Account created, exiting...')
        exit()
    elif mode is 1:
        input('Signed in successfully. Press enter to sign out.')
        user_sign_out(user)


def user_sign_out(username):
    keydrive = detect_keydrive()
    if keydrive is True:
        sql_write_timestamp(username)
        timestamp = sql_read_timestamp(username)
        key = generate_key(username + timestamp)
        fingerprint = fingerprint_data(key)
        store_key_fingerprint(username, key, fingerprint)
        print("Signed out successfully, you can now remove the KEYDRIVE. Exiting....")
        exit()
    else:
        input("KEYDRIVE not detected, insert KEYDRIVE then press enter to try again.")
        user_sign_out(username)


def generate_key(seed):
    generated_key = sha256_hash_data(seed.encode())
    return generated_key.hexdigest()


def fingerprint_data(arg):
    fingerprint = sha1_hash_data(arg.encode())
    return fingerprint.hexdigest()


def fingerprint_check(username):
    submitted_key = read_stored_key(username)
    submitted_key_fingerprint = fingerprint_data(submitted_key)
    stored_key_fingerprint = sql_read_fingerprint(username)
    if stored_key_fingerprint == submitted_key_fingerprint:
        return True
    else:
        return False


def read_stored_key(user):
    extracted_chunk0 = usb_read_write_chunk("read")
    extracted_chunk1 = str(sql_read_key_chunk(user))
    key = extracted_chunk0 + extracted_chunk1
    return key


def store_key_fingerprint(username, key, fingerprint):
    chunks = regular_expression.findall('................................?', key)
    usb_read_write_chunk(chunks[0])
    sql_write_chunk_fingerprint(username, chunks[1], fingerprint)


def identifier_check(submitted_identifier, stored_idetnifier):
    if submitted_identifier == stored_idetnifier:
        return True
    else:
        return False


def sql_read_identifier(user):
    # print("sql read identifier") # Uncomment this for debugging
    sql_connection = mysql.connector.connect(
        user='<user>',
        password='<password>',
        host='<mysql_address>',
        database='passwords'
    sql_cursor = sql_connection.cursor()
    cmd = ("select identifier from identifiers where username = '%s'") % (user)
    sql_cursor.execute(cmd)
    stored_identifier = str(sql_cursor.fetchall())
    sql_connection.close()
    return stored_identifier.strip("()[],'")


def sql_write_user_identifiers(user, identifier):
    # print("sql write user identifiers") # Uncomment this for debugging
    sql_connection = mysql.connector.connect(
        user='<user>',
        password='<password>',
        host='<mysql_address>',
        database='passwords'
    sql_cursor = sql_connection.cursor()
    cmd = ("insert into identifiers (username, identifier) values ('%s', '%s')") % (user, identifier)
    sql_cursor.execute(cmd)
    sql_connection.commit()
    sql_connection.close()


def sql_write_username_timestamp(user):
    # print("sql write username and timestamp") # Uncomment this for debugging
    sql_connection = mysql.connector.connect(
        user='<user>',
        password='<password>',
        host='<mysql_address>',
        database='dist_login'
    sql_cursor = sql_connection.cursor()
    cmd = ("insert into credentials (username, timestamp) values ('%s', NOW())") % (user)
    sql_cursor.execute(cmd)
    cmd = ("insert into fingerprints (username) values ('%s')") % (user)
    sql_cursor.execute(cmd)
    sql_connection.commit()
    sql_connection.close()


def sql_write_timestamp(user):
    # print("sql write timestamp") # Uncomment this for debugging
    sql_connection = mysql.connector.connect(
        user='<user>',
        password='<password>',
        host='<mysql_address>',
        database='dist_login'
    sql_cursor = sql_connection.cursor()
    cmd = ("update credentials set timestamp = NOW() where username = '%s'") % (user)
    sql_cursor.execute(cmd)
    sql_connection.commit()
    sql_connection.close()


def sql_write_chunk_fingerprint(user, chunk, fingerprint):
    # print("sql write chunk and fingerprint") # Uncomment this for debugging
    sql_connection = mysql.connector.connect(
        user='<user>',
        password='<password>',
        host='<mysql_address>',
        database='dist_login'
    sql_cursor = sql_connection.cursor()
    cmd = ("update credentials set key_chunk=CONCAT('%s') where credentials.username = '%s'") % (chunk, user)
    sql_cursor.execute(cmd)
    cmd = ("update fingerprints set fingerprint=CONCAT('%s') where fingerprints.username =  '%s'") % (fingerprint, user)
    sql_cursor.execute(cmd)
    sql_connection.commit()
    sql_connection.close()


def sql_read_timestamp(user):
    # print("sql read timestamp") # Uncomment this for debugging
    sql_connection = mysql.connector.connect(
        user='<user>',
        password='<password>',
        host='<mysql_address>',
        database='dist_login'
    sql_cursor = sql_connection.cursor()
    cmd = ("select timestamp from credentials where username = '%s'") % (user)
    sql_cursor.execute(cmd)
    timestamp = str(sql_cursor.fetchall())
    sql_connection.close()
    return timestamp


def sql_read_key_chunk(user):
    # print("sql read key_chunk") # Uncomment this for debugging
    sql_connection = mysql.connector.connect(
        user='<user>',
        password='<password>',
        host='<mysql_address>',
        database='dist_login'
    sql_cursor = sql_connection.cursor()
    cmd = ("select key_chunk from credentials where username = '%s'") % (user)
    sql_cursor.execute(cmd)
    key_chunk = str(sql_cursor.fetchall())
    sql_connection.close()
    return key_chunk.strip("()[],'")


def sql_read_fingerprint(user):
    # print("sql read fingerprint") # Uncomment this for debugging
    sql_connection = mysql.connector.connect(
        user='<user>',
        password='<password>',
        host='<mysql_address>',
        database='dist_login'
    sql_cursor = sql_connection.cursor()
    cmd = ("select fingerprint from fingerprints where username = '%s'") % (user)
    sql_cursor.execute(cmd)
    fingerprint = str(sql_cursor.fetchall())
    sql_connection.close()
    return fingerprint.strip("()[],'")


def detect_keydrive():
        if os.name == 'nt':
            try:
                subprocess.check_output("wmic logicaldisk list brief | findstr KEYDRIVE", shell=True)
            except subprocess.CalledProcessError:
                return False
            return True
        elif os.name == 'posix':
            output = str(subprocess.check_output("lsblk -o MOUNTPOINT | grep KEYDRIVE", shell=True))
            if not output.find("KEYDRIVE"):
                return False
            else:
                return True


def usb_read_write_chunk(chunk):
    drive_path = ""
    output = ""
    if os.name == 'nt':
        try:
            output = str(subprocess.check_output("wmic logicaldisk list brief | findstr KEYDRIVE", shell=True))
        except subprocess.CalledProcessError:
            print("KEYDRIVE not found")
            exit()
        drive_path = (output[2:3] + ':\chunk.txt')
    elif os.name == 'posix':
        output = str(subprocess.check_output("lsblk -o MOUNTPOINT | grep KEYDRIVE", shell=True))
        if not output.find("KEYDRIVE"):
            print("KEYDRIVE not found")
            exit()
        else:
            output = (output[2:])
            output = (output[:-3])
            drive_path = (output + '/chunk.txt')
    if chunk is "read":
        keydrive_chunk = open(drive_path).read()
        return keydrive_chunk
    else:
        keydrive_file = open(drive_path, "w")
        keydrive_file.write(chunk)
        keydrive_file.close()
        return 0


def output_results(username, password):  # This function is for debugging only
    print("Username", username)
    print("Password", password)
    compiled_key = str(read_stored_key(username))
    print(" CompKey", compiled_key)
    compkey_fingerprint = fingerprint_data(compiled_key)
    print("KeyPrint", compkey_fingerprint)


select_mode()
