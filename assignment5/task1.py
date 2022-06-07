import hashlib
import string
import itertools
import time
import sys
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def ECB(key, plaintext):
    cipher=AES.new(key,AES.MODE_ECB)
    padded=pad(plaintext,AES.block_size,style='pkcs7')
    dist=len(padded)//16
    result=b''
    for i in range(dist):
        result+=cipher.encrypt(padded[i*16 : (i+1)*16])
    
    return result

def CBC(key, plaintext):
    iv=get_random_bytes(16)
    cipher=AES.new(key,AES.MODE_CBC,iv)
    padded=pad(plaintext,AES.block_size,style='pkcs7')
    dist=len(padded)//16
    result=b''
    for i in range(dist):
        result+=cipher.encrypt(padded[i*16 : (i+1)*16])
        cipher=AES.new(key,AES.MODE_CBC,result[i*16 : (i+1)*16])
        
    return result

def main():
    # AES-128 primitive
                                                                                                                                                                
    
    # take a (plaintext) file, generate a random key (and random IV, in the case of CBC), 
    # and write the encryption of the plaintext in a new file.
    
    try:
        assert (len(sys.argv)>1), "User has to input the bmp file"
    except Exception as e:
        print(e)
        sys.exit(1)
    
    # read the file 
    bmp_file=open(sys.argv[1],'rb')
    bmp_plaintext=bmp_file.read()
    
    # random key
    key=get_random_bytes(16)
    
    ecb_encrypted=ECB(key,bmp_plaintext)
    cbc_encrypted=CBC(key,bmp_plaintext)
    
    ecb_encrypted=bmp_plaintext[:54]+ecb_encrypted[54:]
    cbc_encrypted=bmp_plaintext[:54]+cbc_encrypted[54:]
    
    output_ecb=open("task1_output_ecb.bmp","wb")
    output_cbc=open("task1_output_cbc.bmp","wb")
    
    output_ecb.write(ecb_encrypted)
    output_cbc.write(cbc_encrypted)
    
    bmp_file.close()
    output_cbc.close()
    output_ecb.close()
    
    
    

if __name__=='__main__':
    main()