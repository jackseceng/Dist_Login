import signing_handler
import group_a_mysql
import group_b_mysql
import re as regular_expression


def select_mode():
    mode = input('Select \'e\' for Existing User, \'n\' for New User or \'q\' to quit: ')
    if len(mode) > 1:
        print("Please use the single letter \'n\', \'q\' or \'e\'")
        select_mode()
    elif not regular_expression.match('[n]|[e]|[q]', mode):
        print("Please use the single letter \'n\', \'q\' or \'e\'")
        select_mode()
    else:
        if 'n' in mode:
            signing_handler.new_user()
        elif 'e' in mode:
            signing_handler.existing_user()
        elif 'q' in mode:
            group_a_mysql.sql_close_connection()
            group_b_mysql.sql_close_connection()
            print("Quitting login system...")
            exit()


select_mode()
