import hashlib
def hashing_256(password):
    result = hashlib.sha256(password.encode())
    return (result.hexdigest())
