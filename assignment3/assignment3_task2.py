from collections import Counter
from operator import xor
import sys
import os

def xor_encrypt(s1,s2):
    ret=""
    # for some reason, c1 is in str format, c2 is in int format.
    for c1,c2 in zip(s1,s2):
        to_add=ord(c1)^c2
        ret+=chr(to_add)
    return ret
        

def main():
    try:
        assert (len(sys.argv)>1), "User has to input the file name"
    except Exception as e:
        print(e)
        sys.exit(1)
    
    # read the plaintext and generate a random key
    file_name=sys.argv[1]
    read_file=open(file_name,'r')
    plaintext=read_file.read()
    random_key=os.urandom(len(plaintext))
    
    # encrypt the plaintext use the xor.
    encrypted=xor_encrypt(plaintext,random_key)
    
    # write the ciphertext into the output.txt file
    write_file=open("task2_output.txt",'w')
    write_file.write(encrypted)
    
    # now xor the key with the ciphertext 
    decrypted=xor_encrypt(encrypted,random_key)
    
    print("The following is to test if we can get the original plaintext back")
    print("------------------------------------------------------------------")
    print(decrypted)
    
    
    write_file.close()
    read_file.close()

if __name__=='__main__':
    main()
        
        