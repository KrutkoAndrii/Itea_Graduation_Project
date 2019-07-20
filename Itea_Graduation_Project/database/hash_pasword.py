'''create/check hash password'''
import hashlib


def create_hash_password(password):
    '''create password sha256 '''
    new_password = hashlib.sha256(bytes(password, encoding='utf-8'))
    return new_password.hexdigest()


def is_check_hash_password(hash_password, password):
    '''check user password'''
    user_password = hashlib.sha256(bytes(password, encoding='utf-8'))
    if hash_password == user_password.hexdigest():
        return True
    else:
        return False


if __name__ == "__main__":
    print(" This module not for running!")
