import hashlib
import bcrypt
import random
import time
from nltk.corpus import words
        
def main():
    keys=words.words()
    keys=[w for w in keys if 6<=len(w)<=10]
    
    pw_hash=input("input the shadow file string:")
    list_splited=pw_hash.split(":",1)
    name=list_splited[0]
    pw_hash=list_splited[1]
    
    pw_hash=pw_hash.encode('utf-8')
    start_time=time.time()
    
    
    for w in keys:
        if bcrypt.checkpw(w.encode('utf-8'),pw_hash):
            print("for "+name+" the password is:")
            print(w)
            break
    
    end_time=time.time()
    print("the running time is: ")
    print(end_time-start_time)
if __name__=='__main__':
    main()    
