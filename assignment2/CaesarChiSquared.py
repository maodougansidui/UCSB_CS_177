from curses.ascii import isupper
from collections import Counter
import sys

from matplotlib import collections

if __name__=='__main__':
    try:
        assert (len(sys.argv)>1), "User has to input the file name"
    except Exception as e:
        print(e)
        sys.exit(1)
        
    file_name=sys.argv[1]
    encrypted_file=open(file_name,'r')
    
    letter_freq=[0.082,0.015,0.028,0.043,0.13,0.022,0.02,0.061,0.07,0.0015,0.0077,
                 0.04,0.024,0.067,0.075,0.019,0.00095,0.06,0.063,0.091,0.028,0.0098,
                 0.024,0.0015,0.02,0.00074]
    
    encrypted=encrypted_file.read()
    ## brute force try all the 26 key to decode the file.
    for key in range(26):
        decrypted=""
        chi_squared=0.0
        for letter in encrypted:
            if letter.isupper():
                decrypted+=chr((ord(letter)+key-65)%26+65)
            elif letter.islower():
                decrypted+=chr((ord(letter)+key-97)%26+97)
            else:
                decrypted+=letter
    
        cnt=len(decrypted)
        counter=Counter(decrypted)
        
        for letter in counter:
            value=counter[letter]
            if letter.isupper():
                freq=cnt*letter_freq[ord(letter)-65]
                chi_squared+=(value-freq)**2/freq
            if letter.islower():
                freq=cnt*letter_freq[ord(letter)-97]
                chi_squared+=(value-freq)**2/freq
        print("encryption key "+str((26-key)%26) + ", chi_squared "+str(chi_squared)+ " :" +decrypted)
    
    encrypted_file.close()
        
        