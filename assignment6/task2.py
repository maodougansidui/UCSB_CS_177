import hashlib
import string
import sys
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Random.random import randint

def MitM_g(p):
    return p

def MitM_A_B(p: int):
    return p,p


def DiffieHellmanKey(p:int,g:int, command: str):
    a=randint(1,p-2)
    b=randint(1,p-2)
    
    ## now the attacker can modify the value of g on public channels.
    if command=='g to 1': 
        g=MitM_g(1)
    elif command== 'g to p':
        g=MitM_g(p)
    elif command=='g to p-1': 
        g=MitM_g(p-1)
        
    
    Alice=pow(g,a,p)
    Bob=pow(g,b,p)
    
    
    ## now the attacker will modify the value on the public channels
    
    if command=="A and B":
        Alice, Bob= MitM_A_B(p) 
    
    secret_Alice=pow(Bob,a,p)
    secret_Bob=pow(Alice,b,p)
    
    secret_Alice=str(secret_Alice).encode('utf-8')
    secret_Bob=str(secret_Bob).encode('utf-8')
    
    key_Alice=hashlib.sha256(secret_Alice).digest()
    key_Bob=hashlib.sha256(secret_Bob).digest()
    
    if key_Alice!=key_Bob:
        print("Error, the keys from Alice and Bob are different!")
        sys.exit(1)
    else:
        print("\nAlice's key and Bob's key are the same")
    
    key_Alice=key_Alice[:16]
    key_Bob=key_Bob[:16]
    
    message_Alice="Hi Bob!"
    message_Bob="Hi Alice!"
    
    iv=get_random_bytes(16)
    cipher_Alice=AES.new(key_Alice,AES.MODE_CBC,iv)
    cipher_Bob=AES.new(key_Bob,AES.MODE_CBC,iv)
    
    c_alice=cipher_Alice.encrypt(pad(message_Alice.encode('utf-8'),16,style='pkcs7'))
    c_bob=cipher_Bob.encrypt(pad(message_Bob.encode('utf-8'),16,style='pkcs7'))
    
    print("now the cipher from Alice:")
    print(c_alice)
    print("now the cipher from Bob:")
    print(c_bob)
    
    ## now we test if we decrypt the message by attacker.
    
    print("\nnow we test if we can decrypt the message by attacker.")
    intercepted_Alice=0
    intercepted_Bob=0
    
    ## For A and B change, if p^a mod p, then the result is always 0
    if command=="A and B":
        print("For A and B change, if p^a mod p, then the result is always 0")
        intercepted_Alice=0
        intercepted_Bob=0
    ## if change g to 1, then 1^a mod p = 1
    elif command=='g to 1':
        print("if change g to 1, then 1^a mod p = 1")
        intercepted_Alice=1
        intercepted_Bob=1
    ## if change g to p, then p^ab mod p = 0
    elif command== 'g to p':
        print("if change g to p, then p^ab mod p = 0")
        intercepted_Alice=0
        intercepted_Bob=0
    ## if change g to p-1, then there are only two possibilities, (p-1)^ab mod p= p-1 or 1
    elif command== 'g to p-1':
        print("if change g to p-1, then there are only two possibilities, (p-1)^ab mod p= p-1 or 1")
        intercepted_Alice=1
        intercepted_Bob=1
        print('\n')
        print("Now we decrypt the message from Alice and Bob")
        try:
            key_attacker_alice=hashlib.sha256(str(intercepted_Alice).encode('utf-8')).digest()[:16]
            key_attacker_bob=hashlib.sha256(str(intercepted_Bob).encode('utf-8')).digest()[:16]
            
            decipher_alice=AES.new(key_attacker_alice,AES.MODE_CBC,iv)
            decipher_bob=AES.new(key_attacker_bob,AES.MODE_CBC,iv)
            
            print("\n")
            print("The Alice message decrypted by attacker could be: " + unpad(decipher_alice.decrypt(c_alice),16,style='pkcs7').decode())
            print("\n")
            print("The Bob message decrypted by attacker could be: " + unpad(decipher_bob.decrypt(c_bob),16,style='pkcs7').decode())
        except:
            print("secret key is not 1")
        
        intercepted_Alice=p-1
        intercepted_Bob=p-1
        
        try:
            key_attacker_alice=hashlib.sha256(str(intercepted_Alice).encode('utf-8')).digest()[:16]
            key_attacker_bob=hashlib.sha256(str(intercepted_Bob).encode('utf-8')).digest()[:16]
            
            decipher_alice=AES.new(key_attacker_alice,AES.MODE_CBC,iv)
            decipher_bob=AES.new(key_attacker_bob,AES.MODE_CBC,iv)
            
            print("\n")
            print("The Alice message decrypted by attacker could be: " + unpad(decipher_alice.decrypt(c_alice),16,style='pkcs7').decode())
            print("\n")
            print("The Bob message decrypted by attacker could be: " + unpad(decipher_bob.decrypt(c_bob),16,style='pkcs7').decode())
        except:
            print("secret key is not p-1")
        
        return
            
    ## handle other case that not g=p-1
    
    print('\n')
    print("Now we decrypt the message from Alice and Bob")
    key_attacker_alice=hashlib.sha256(str(intercepted_Alice).encode('utf-8')).digest()[:16]
    key_attacker_bob=hashlib.sha256(str(intercepted_Bob).encode('utf-8')).digest()[:16]
    
    decipher_alice=AES.new(key_attacker_alice,AES.MODE_CBC,iv)
    decipher_bob=AES.new(key_attacker_bob,AES.MODE_CBC,iv)
    
    print("\n")
    print("The Alice message decrypted by attacker is: " + unpad(decipher_alice.decrypt(c_alice),16,style='pkcs7').decode())
    print("\n")
    print("The Bob message decrypted by attacker is: " + unpad(decipher_bob.decrypt(c_bob),16,style='pkcs7').decode())


def main():
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
    
    
    print("-----------------------------------------------")
    ## Now we test with MITM attack with change of A and B to p
    print("MITM Attack changing A and B\n \n \n")
    DiffieHellmanKey(37,5, "A and B")
    
    DiffieHellmanKey(large_p,large_g, "A and B")
    
    print("-----------------------------------------------")
    ## Now we test with MITM attack with change of g to 1
    print("MITM Attack changing g to 1 \n \n \n")
    DiffieHellmanKey(37,5, 'g to 1')
    
    DiffieHellmanKey(large_p,large_g, 'g to 1')
    
    print("-----------------------------------------------")
    ## Now we test with MITM attack with change of g to p
    print("MITM Attack changing g to p \n \n \n")
    DiffieHellmanKey(37,5, 'g to p')
    
    DiffieHellmanKey(large_p,large_g, 'g to p')
    
    print("-----------------------------------------------")
    ## Now we test with MITM attack with change of g to p-1
    print("MITM Attack changing g to p-1 \n \n \n")
    DiffieHellmanKey(37,5, 'g to p-1')
    
    DiffieHellmanKey(large_p,large_g, 'g to p-1')
    
if __name__=='__main__':
    main()