# This function is for debugging only

import data_handler
import crypto_handler


def output_results(username, password, group):
    print("Username", username)
    print("Password", password)
    print("   Group", group)
    compiled_key = data_handler.read_stored_key(username, group)
    print(" CompKey", compiled_key)
    compiled_key_fingerprint = crypto_handler.fingerprint_data(compiled_key)
    print("KeyPrint", compiled_key_fingerprint)
