import hashlib
import string
import sys
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Random.random import randint

def DiffieHellmanKey(p:int,g:int):
    a=randint(1,p-2)
    b=randint(1,p-2)
    
    Alice=pow(g,a,p)
    Bob=pow(g,b,p)
    
    secret_Alice=pow(Bob,a,p)
    secret_Bob=pow(Alice,b,p)
    
    secret_Alice=str(secret_Alice).encode('utf-8')
    secret_Bob=str(secret_Bob).encode('utf-8')
    
    key_Alice=hashlib.sha256(secret_Alice).digest()
    key_Bob=hashlib.sha256(secret_Bob).digest()
    
    if key_Alice!=key_Bob:
        print("Error, the keys from Alice and Bob are different!")
        sys.exit(1)
    
    print("-----------------------------------------------")
    print("Alice key:")
    print(key_Alice)
    print("Bob Key:")
    print(key_Bob)
    print()
    
    key_Alice=key_Alice[:16]
    key_Bob=key_Bob[:16]
    
    message_Alice="Hi Bob!"
    message_Bob="Hi Alice!"
    
    iv=get_random_bytes(16)
    cipher_Alice=AES.new(key_Alice,AES.MODE_CBC,iv)
    cipher_Bob=AES.new(key_Bob,AES.MODE_CBC,iv)
    
    c_alice=cipher_Alice.encrypt(pad(message_Alice.encode('utf-8'),16,style='pkcs7'))
    c_bob=cipher_Bob.encrypt(pad(message_Bob.encode('utf-8'),16,style='pkcs7'))
    
    print("-----------------------------------------------")
    print("now the cipher from Alice:")
    print(c_alice)
    print("now the cipher from Bob:")
    print(c_bob)
    
    

def main():
    DiffieHellmanKey(37,5)
    
    large_p=("B10B8F96A080E01DDE92DE5EAE5D54EC52C99FBCFB"
             "06A3C69A6A9DCA52D23B616073E28675A23D189838E"
             "F1E2EE652C013ECB4AEA906112324975C3CD49B83BF"
             "ACCBDD7D90C4BD7098488E9C219A73724EFFD6FAE56"
             "44738FAA31A4FF55BCCC0A151AF5F0DC8B4BD45BF37D"
             "F365C1A65E68CFDA76D4DA708DF1FB2BC2E4A4371")
    
    large_g=("A4D1CBD5C3FD34126765A442EFB99905F8104DD258AC507F"
             "D6406CFF14266D31266FEA1E5C41564B777E690F5504F213"
             "160217B4B01B886A5E91547F9E2749F4D7FBD7D3B9A92EE1"
             "909D0D2263F80A76A6A24C087A091F531DBF0A0169B6A28A"
             "D662A4D18E73AFA32D779D5918D08BC8858F4DCEF97C2A24"
             "855E6EEB22B3B2E5")
    large_p=int(large_p,16)
    large_g=int(large_g,16)
    DiffieHellmanKey(large_p,large_g)
    
if __name__=='__main__':
    main()