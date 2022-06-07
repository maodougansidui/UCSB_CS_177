from curses.ascii import isupper
from collections import Counter
from queue import PriorityQueue
import sys

letter_freq=[0.082,0.015,0.028,0.043,0.13,0.022,0.02,0.061,0.07,0.0015,0.0077,
                0.04,0.024,0.067,0.075,0.019,0.00095,0.06,0.063,0.091,0.028,0.0098,
                0.024,0.0015,0.02,0.00074]
remove_list=set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

def ioc(file):
    max_length=int(input("Enter the maximum key length user want:"))
    top_k=int(input("Enter the top k ioc user want to keep:"))
    
    od={}
    for length in range(1,max_length+1,1):
        average=0.0
        for index in range(length):
            seq=""
            for i in range(index,len(file),length):
                seq=seq+file[i]
            
            n=len(seq)
            counter=Counter(seq)
            tmp=0.0
            for letter in counter:
                cnt=counter[letter]
                tmp+=cnt*(cnt-1)
            tmp=tmp/(n*(n-1))
            average+=tmp
        average=average/length
        od[average]=length
    
    ret=[]
    for key in sorted(od,reverse=True):
        if top_k<=0:
            break
        ret.append((key,od[key]))
        top_k-=1
    return ret


def chi_square(key_length,file):
    ret=""
    for index in range(key_length):
        tmp=""
        chi_list=[]
        for i in range(index,len(file),key_length):
            tmp+=file[i]
        
        ## brute force try all the 26 key to decode the file.
        for key in range(26):
            decrypted=""
            chi_squared=0.0
            for letter in tmp:
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
            chi_list.append((chi_squared,(26-key)%26))
        chi_list.sort()
        if chi_list[0][1]==0:
            ret+=chr((ord('a')+25))
        else:
            ret+=chr((ord('a')+chi_list[0][1]-1))
        
    return [ret]

        

def main():
    try:
        assert (len(sys.argv)>1), "User has to input the file name"
    except Exception as e:
        print(e)
        sys.exit(1)
        
    file_name=sys.argv[1]
    encrypted_file=open(file_name,'r')
    
    encrypted=encrypted_file.read()
    encrypted_file.close()
    encrypted_file=open(file_name,'r')
    # tmp_list=[]
    # for line in encrypted_file.readlines():
    #     tmp_list.append(len(line))
        
    
    ## first we need to process the raw text, remove all characters except the letters.
    
    encrypted=''.join(filter(remove_list.__contains__,encrypted))
    
    ## now process the index of coincidence function
    
    top_length=ioc(encrypted)
    
    possible_keys=[]
    for i in range(len(top_length)):
        key_length=top_length[i][1]
        for candidate in chi_square(key_length,encrypted):
            possible_keys.append(candidate)
    
    for key in possible_keys:
        n=len(key)
        decrypted=""
        for i in range(len(encrypted)):
            cur_letter=ord(encrypted[i])
            keycode=ord(key[i%n])
            offset=cur_letter-keycode
            if offset==0:
                offset=26
            if offset<0:
                offset+=26
            decrypted+=chr(offset-1+97)
        
        tmp_idx=0
        tmp_output=""
        for c in encrypted_file.read():
            if c.isalpha():
                tmp_output+=decrypted[tmp_idx]
                tmp_idx+=1
            else:
                tmp_output+=c
        print(tmp_output)
        
        print("key = "+ key + " and decoded = " + decrypted)
        print("\n")
            
    
    encrypted_file.close()

if __name__=='__main__':
    main()
        
        