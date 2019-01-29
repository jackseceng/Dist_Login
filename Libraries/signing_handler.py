import crypto_handler
import identifier_mysql
import group_a_mysql
import group_b_mysql
import usb_handler
import data_handler
import output


def new_user():
    print('Create new account')
    keydrive = usb_handler.detect_keydrive()
    if keydrive is True:
        import input_handler
        new_username = input_handler.input_username(1)
        new_password = input_handler.input_password(1)
        encrypted_password = crypto_handler.fingerprint_data(new_username + new_password)
        identifier_mysql.sql_write_user_identifiers(new_username, encrypted_password)
        group_a_mysql.sql_write_username_timestamp(new_username)
        timestamp = group_a_mysql.sql_read_timestamp(new_username)
        key = crypto_handler.generate_key(new_username + new_password + timestamp)
        fingerprint = crypto_handler.fingerprint_data(key)
        data_handler.store_key_fingerprint(new_username, key, fingerprint, 'a')
        group_b_mysql.initiate_new_user(new_username)
        output.output_results(new_username, new_password, 'a')
        session(0, new_username, 'a')  # Function for illustration purposes only
    elif keydrive is False:
        input("KEYDRIVE not detected, insert KEYDRIVE then press enter to try again.")
        new_user()


def existing_user():
    print('Sign in to existing account')
    keydrive = usb_handler.detect_keydrive()
    if keydrive is True:
        import input_handler
        existing_username = input_handler.input_username(2)
        existing_password = input_handler.input_password(2)
        print("Please state the group you last signed out from.")
        group = input_handler.select_group()
        encrypted_password = crypto_handler.fingerprint_data(existing_username + existing_password)
        stored_identifier = identifier_mysql.sql_read_identifier(existing_username)
        is_sign_in_correct = data_handler.identifier_check(encrypted_password, stored_identifier)
        if is_sign_in_correct is True:
            is_key_correct = data_handler.fingerprint_check(existing_username, group)
            if is_key_correct is True:
                import input_handler
                print("Key is correct, sign in verified.")
                output.output_results(existing_username, existing_password, group)
                print("Select group you are signing in to")
                # This function does not need to be implemented if the script is optimised for the group, see the readme
                group = input_handler.select_group()
                session(1, existing_username, group)  # Function for illustration purposes
            elif is_key_correct is False:
                input("The provided group or key is incorrect. Press any key to try again")
                existing_user()
        elif is_sign_in_correct is False:
            input("Username or password is incorrect. Press any key to try again")
            existing_user()
    elif keydrive is False:
        input("KEYDRIVE not detected, please insert KEYDRIVE. Press any key to try again.")
        existing_user()


def user_sign_out(username, group):
    print("Signing out...")
    keydrive = usb_handler.detect_keydrive()
    if keydrive is True:
        if group is 'a':
            group_a_mysql.sql_write_timestamp(username)
            timestamp = group_a_mysql.sql_read_timestamp(username)
            key = crypto_handler.generate_key(username + timestamp)
            fingerprint = crypto_handler.fingerprint_data(key)
            data_handler.store_key_fingerprint(username, key, fingerprint, group)
            group_b_mysql.clear_group_b(username)
        elif group is 'b':
            group_b_mysql.sql_write_timestamp(username)
            timestamp = group_b_mysql.sql_read_timestamp(username)
            key = crypto_handler.generate_key(username + timestamp)
            fingerprint = crypto_handler.fingerprint_data(key)
            data_handler.store_key_fingerprint(username, key, fingerprint, group)
            group_a_mysql.clear_group_a(username)
        print("Signed out of group " + group + " successfully, you can now remove the KEYDRIVE.")
        import dist_login
        dist_login.select_mode()
    elif keydrive is False:
        input("KEYDRIVE not detected, insert KEYDRIVE then press enter to try again.")
        user_sign_out(username, group)


def session(mode, user, group):
    # This function is only for illustrating a successful session sign in, replace it with the sign in method required
    if mode is 0:
        input("Account created, sign in to group a to use your account. Press any key to continue.")
        import dist_login
        dist_login.select_mode()
    elif mode is 1:
        input("Signed in to group " + group + " successfully. Press any key to sign out.")
        user_sign_out(user, group)
