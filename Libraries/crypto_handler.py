from hashlib import sha256 as sha256_hash_data
from hashlib import sha1 as sha1_hash_data


def generate_key(seed):
    generated_key = sha256_hash_data(seed.encode())
    return generated_key.hexdigest()


def fingerprint_data(arg):
    fingerprint = sha1_hash_data(arg.encode())
    return fingerprint.hexdigest()
