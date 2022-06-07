import sys

if __name__=='__main__':
    try:
        assert (len(sys.argv)>1), "User has to input the file name"
    except Exception as e:
        print(e)
        sys.exit(1)
        
    file_name=sys.argv[1]
    encrypted_file=open(file_name,'r')
    
    encrypted=encrypted_file.read()
    ## brute force try all the 26 key to decode the file.
    for key in range(26):
        decrypted=""
    
        for letter in encrypted:
            if letter.isupper():
                decrypted+=chr((ord(letter)+key-65)%26+65)
            elif letter.islower():
                decrypted+=chr((ord(letter)+key-97)%26+97)
            else:
                decrypted+=letter
    
        print("encryption key "+str((26-key)%26) + ": "+decrypted)
    
    encrypted_file.close()
        
        