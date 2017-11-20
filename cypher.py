import base64
import string
import random
import hashlib
import time
import struct
from Crypto.Cipher import AES
import socket
import importlib
import config.cypher as config
import ast

block_size = 32
aes_key = base64.b64decode(config.aes_key)

def encrypt(data, userid):
    if not isinstance(data, dict):
        raise RuntimeError('Invalid data type')
    data = str(data)
    sample = string.digits + string.ascii_letters
    rand_str = ''.join(random.sample(sample, 16))
    data = data.encode('utf-8')
    data = bytes(rand_str, 'utf-8') + struct.pack('I', socket.htonl(len(data))) + data + bytes(userid, 'utf-8')
    data_length = len(data)
    pad_length = block_size - (data_length % block_size)
    pad = bytes(chr(pad_length), 'utf-8')
    data = data + pad * pad_length
    ase_cryptor = AES.new(aes_key, AES.MODE_CBC, aes_key[:16])
    cipher = ase_cryptor.encrypt(data)
    return base64.b64encode(cipher).decode('ascii')

def decrypt(data):
    try:
        ase_cryptor = AES.new(aes_key, AES.MODE_CBC, aes_key[:16])
        plain_text = ase_cryptor.decrypt(base64.b64decode(data))
        pad_length = plain_text[-1]
        content = plain_text[16:-pad_length]
        data_length = socket.ntohl(struct.unpack('I', content[:4])[0])
        return ast.literal_eval(content[4:4+data_length].decode('utf-8')), content[4+data_length:].decode('utf-8')
    except Exception as err:
        return {}, ''

def get_signature(*arg):
    signature_param = list(arg)
    signature_param.sort()
    return hashlib.sha1(''.join(signature_param).encode('utf-8')).hexdigest()

if __name__ == '__main__':
    encrypt_data = encrypt('fuck you', 'admin')
    decrypt_data = decrypt(encrypt_data)
    print(encrypt_data, decrypt_data)
