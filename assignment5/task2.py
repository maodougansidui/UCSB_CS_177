from binascii import unhexlify
import hashlib
import string
import itertools
import time
import sys
from base64 import b64decode, b64encode
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from numpy import true_divide

def submit(plaintext,key,iv):
    prepend="userid=456;userdata="
    append=";session-id=31337"
    
    plaintext=prepend+plaintext+append
    
    plaintext=plaintext.replace(";","%3B")
    plaintext=plaintext.replace("=","%3D")
    return CBC(key,plaintext,iv)

def CBC(key, plaintext, iv):
    padded=pad(plaintext.encode('utf-8'),16,style='pkcs7')
    cipher=AES.new(key,AES.MODE_CBC,iv)
    result=cipher.encrypt(padded)
    return result.hex()

def verify(cipher,key,iv):
    
    decipher=AES.new(key,AES.MODE_CBC,iv)
    paddedPam=decipher.decrypt(unhexlify(cipher))
    print(paddedPam)
    if b';admin=true;' in unpad(paddedPam,16,style='pkcs7'):
        return True
    else:
        return False
    

def main():
    
    try:
        assert (len(sys.argv)>1), "User has to input a random string"
    except Exception as e:
        print(e)
        sys.exit(1)
    
    # read the file 
    user_input=sys.argv[1]
    
    # random key
    key=get_random_bytes(16)
    
    # random iv
    iv=get_random_bytes(16)
    
   
    encrypted=submit(user_input,key,iv)
    
    print("--------------------------------------------------")
    print("The result before the hacking: \n")
    print(verify(encrypted,key,iv))
    
    # ## now we need to implement the hacking part.
    hack=";admin=true;"
    known_prefix="userid%3D456"
    iv_hex=iv.hex()
    hacked_en=""
    for i in range(len(hack)):
        xor=ord(hack[i])^ord(known_prefix[i])
        third=iv_hex[i*2 : (i+1)*2]
        # hacked_en+='{:02x}'.format(xor)
        hacked_en+=hex(int(iv_hex[i*2 : (i+1)*2],16)^xor)[2:]
    
    iv_hex=hacked_en+iv_hex[len(hacked_en):]
    iv=unhexlify(iv_hex)

    print("--------------------------------------------------")
    print("The result after the hacking: \n")
    print(verify(encrypted,key,iv))
    
    

if __name__=='__main__':
    main()