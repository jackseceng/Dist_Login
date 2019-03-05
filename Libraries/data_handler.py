import re as regular_expression
import time
import usb_handler
import group_a_mysql
import group_b_mysql


def sql_inject_check(arg):
    if arg in open('<path_to_Dist_Login>/Files/sql_inject_strings.txt').read():
        return True

    else:
        return False

def clear():
    f = open('<path_to_Dist_Login>/Files/usb_chunk.txt', 'w+')
    f.write('blank')
    f.close()

def check():
    f = open('<path_to_Dist_Login>/Files/usb_chunk.txt', 'r')
    contents = f.read()
    if regular_expression.fullmatch(("blank"), contents):
        f.close()
        return True
    else:
        return False

def fingerprint_check(username, group):
    stored_key_fingerprint = str("")
    submitted_key = read_stored_key(username, group)
    if submitted_key is 'blank':
        return False
    else:
        import crypto_handler
        submitted_key_fingerprint = crypto_handler.fingerprint_data(submitted_key)
        if group is 'a':
            stored_key_fingerprint = group_a_mysql.sql_read_fingerprint(username)
        elif group is 'b':
            stored_key_fingerprint = group_b_mysql.sql_read_fingerprint(username)

    if stored_key_fingerprint == submitted_key_fingerprint:
        return True
    else:
        return False


def read_stored_key(user, group):
    clear()
    blank = check()
    print("Insert KEYDRIVE into your machine and run 'send.py' now")
    while blank is True:
        blank = check()
        time.sleep(1)
    extracted_chunk0 = usb_handler.usb_read_write_chunk("read")
    extracted_chunk1 = str("")
    if group is 'a':
        extracted_chunk1 = str(group_a_mysql.sql_read_key_chunk(user))
        if extracted_chunk1 is 'blank':
            return extracted_chunk1
    elif group is 'b':
        extracted_chunk1 = str(group_b_mysql.sql_read_key_chunk(user))
        if extracted_chunk1 is 'blank':
            return extracted_chunk1
    key = extracted_chunk0 + extracted_chunk1
    return key


def store_key_fingerprint(username, key, fingerprint, group, mode):
    chunks = regular_expression.findall('................................?', key)
    if mode is "exist":
        usb_handler.usb_read_write_chunk(chunks[0])
    elif mode is "new":
        #print("init usb chunk with" + chunks[0]) #This is for debugging only
        usb_handler.init_usb_chunk(chunks[0])
    if group is 'a':
        group_a_mysql.sql_write_chunk_fingerprint(username, chunks[1], fingerprint)
    elif group is 'b':
        group_b_mysql.sql_write_chunk_fingerprint(username, chunks[1], fingerprint)


def identifier_check(submitted_identifier, stored_identifier):
    if submitted_identifier == stored_identifier:
        return True
    else:
        return False
