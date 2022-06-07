from binascii import unhexlify
import hashlib
import secrets
import string
import sys
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Random.random import randint
from Crypto.Util import number

def modinv(e,phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp = phi
    
    while e > 0:
        temp1 = temp//e
        temp2 = temp - temp1 * e
        temp = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp == 1:
        return d + phi

def KeyGeneration(bit_length: int):
    
    e=65537
    p=number.getPrime(bit_length//2)
    q=number.getPrime(bit_length-bit_length//2)
    
    while p%e==1:
        p=number.getPrime(bit_length/2)
        
    while q%e==1:
        q=number.getPrime(bit_length-bit_length/2)
    
    
    
    n=p*q
    phi=(p-1)*(q-1)
    d=modinv(e,phi)
    return n,e,d

def encrypt(message: str, e, n):
    hex_str=message.encode('utf-8').hex()
    
    msg_encr=int(hex_str,16)
    return pow(msg_encr,e,n)

def decrypt(cipher,d,n):
    msg_decr=pow(cipher,d,n)
    hex_msg=hex(msg_decr)
    return unhexlify(hex_msg[2:]).decode()

def show_mallory(cipher, d, n):
    ## F() change the cipher
    cipher=0
    msg_decr=pow(cipher,d,n)
    key=hashlib.sha256(str(msg_decr).encode('utf-8')).digest()[:16]
    
    me="Hi Bob!"
    iv=get_random_bytes(16)
    ci_obj=AES.new(key,AES.MODE_CBC,iv)
    en_ci=ci_obj.encrypt(pad(me.encode('utf-8'),16,style='pkcs7'))
    
    decipher=0
    attacker_key=hashlib.sha256(str(decipher).encode('utf-8')).digest()[:16]
    deci_obj=AES.new(attacker_key,AES.MODE_CBC,iv)
    print("Now we use the attacker's key to decrypt the message: ")
    print(unpad(deci_obj.decrypt(en_ci),16,style='pkcs7').decode())

def main():
    
    bitLength=int(input("Please input the bit length either 1024 or 2048:"))
    
    try:
        assert (bitLength==1024 or bitLength==2048), "The bit length must be either 1024 or 2048"
    except Exception as e:
        print(e)
        sys.exit(1)
    
    public_n, public_e, private_d=KeyGeneration(bitLength)
    
    en_cipher=encrypt("Meet me in the garden",public_e, public_n)
    de_cipher=decrypt(en_cipher,private_d,public_n)
    print("--------------------------------------------------------------")
    print("The decrypted message where no mallory exists is: "+de_cipher)
    print("\n\n")
    print("--------------------------------------------------------------")
    print("Now we have an attacker modify the cipher, F(c)= c' ==> c'=0")
    print("Since 0^d mod n =0, attacker now can easily get the secret key.\n\n")
    
    show_mallory(en_cipher,private_d,public_n)

    
if __name__=='__main__':
    main()