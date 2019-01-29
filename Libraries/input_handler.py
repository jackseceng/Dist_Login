import re as regular_expression
from getpass import getpass as get_password
from sys import exit
import data_handler


def input_username(mode):
    username = ''
    if mode is 1:
        username = input('New Username: ')
    elif mode is 2:
        username = input('Existing Username: ')
    else:
        print("Unknown error in username input, exiting...")
        exit()
    if len(username) > 100:
        print('Username too long, please try again.')
        input_username(mode)
    elif not regular_expression.match('[a-z]|[A-Z]|[0-9]', username):
        print('Username contains symbols, please try again.')
        input_username(mode)
    elif data_handler.sql_inject_check(username) is True:
        print('Username contains forbidden string, please try again.')
        input_username(mode)
    else:
        return username


def input_password(mode):
    password = ''
    if mode is 1:
        password = get_password('New Password: ')
    elif mode is 2:
        password = get_password('Password: ')
    if len(password) > 100:
        print('Password too long, please try again.')
        input_password(mode)
    elif data_handler.sql_inject_check(password) is True:
        print('Password contains forbidden string, please try again.')
        input_password(mode)
    else:
        return password


def select_group():
    group = input('Group: ')
    if len(group) > 1:
        print("Group not recognised, please use a single letter \'a\' or \'b\'.")
        select_group()
    elif not regular_expression.match('[a]|[b]', group):
        print("Group not recognised, please try again.")
        select_group()
    else:
        print("Group " + group + " selected")
        return group
