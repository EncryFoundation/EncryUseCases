import hashlib
import secrets

if __name__ == '__main__':
    secret = secrets.token_bytes(32)
    h_secret = hashlib.sha256(secret)
    print('Secret: \n{}\nHashed secret: \n{}'.format(secret.hex(), h_secret.hexdigest()))
