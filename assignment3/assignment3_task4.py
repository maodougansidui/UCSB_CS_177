from collections import Counter
from operator import xor
import sys
import os

def one_time_pad(s1,s2):
    return bytes([a^b for a,b in zip(s1,s2)])
        

def main():
    try:
        assert (len(sys.argv)>2), "User has to input the two bmp file"
    except Exception as e:
        print(e)
        sys.exit(1)
    
    # read the bmp file into byte string format.
    log1=open(sys.argv[1],'rb')
    log2=open(sys.argv[2],'rb')
    
    log1_plaintext=log1.read()
    log2_plaintext=log2.read()
    

    # because the length of two byte strings are the same
    # we can use the same key to encode them.
    
    random_key=os.urandom(len(log1_plaintext))
    
    # encrypt the byte strings
    encrypted_log1=one_time_pad(log1_plaintext,random_key)
    encrypted_log2=one_time_pad(log2_plaintext,random_key)
    
    
    # post processsing, we need to assume the bmp file header is 54 bytes
    
    encrypted_log1=log1_plaintext[:54]+encrypted_log1[54:]
    encrypted_log2=log2_plaintext[:54]+encrypted_log2[54:]
        

    # now we need to xor the two encrypted files again, (A xor K) xor (B xor K) = A xor B
    final_encrypted=one_time_pad(encrypted_log1,encrypted_log2)
    
    final_encrypted=encrypted_log1[:54]+final_encrypted[54:]
    
    output_final=open("task4_output_final.bmp",'wb')    
    
    output_log1=open("task4_output1.bmp",'wb')
    output_log2=open("task4_output2.bmp","wb")
    
    output_log1.write(encrypted_log1)
    output_log2.write(encrypted_log2)
    output_final.write(final_encrypted)
    
    log1.close()
    log2.close()
    output_log1.close()
    output_log2.close()
    output_final.close()

if __name__=='__main__':
    main()
        
        