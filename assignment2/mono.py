from curses.ascii import isupper
from collections import Counter
from queue import PriorityQueue
import sys

letter_freq=[0.082,0.015,0.028,0.043,0.13,0.022,0.02,0.061,0.07,0.0015,0.0077,
                0.04,0.024,0.067,0.075,0.019,0.00095,0.06,0.063,0.091,0.028,0.0098,
                0.024,0.0015,0.02,0.00074]

        

def main():
    try:
        assert (len(sys.argv)>1), "User has to input the file name"
    except Exception as e:
        print(e)
        sys.exit(1)
        
    file_name=sys.argv[1]
    encrypted_file=open(file_name,'r')
    
    encrypted=encrypted_file.read()
    
    # I am trying to use the simple technique -- frequency analysis 
    # however, the rest of work is based on my manual work, 
    # there are some very sophisitcated tool online, but I cannot understand
    # the source code, thus I will do this manually.
    
    char_counter=Counter(encrypted)
    freq_list=[]
    english_letter_freq=[]
    n=len(encrypted)
    for key in char_counter:
        value=char_counter[key]
        if key.isalpha():
            freq_list.append((value/n,key))
            
    for i in range(26):
        english_letter_freq.append((letter_freq[i],chr(i+65)))
        
    english_letter_freq.sort(reverse=True)
            
    freq_list.sort(reverse=True)
    
    
    
    print("The cipher text frequency is\n --------------------------------")
    print(freq_list)
    print("--------------------------------------------------------------")
    print("The normal english frequency is \n-----------------------------")
    print(english_letter_freq)
    
    map_letter={}
    for i in range(len(freq_list)):
        print(english_letter_freq[i][1] + " --> " + freq_list[i][1])
        map_letter[freq_list[i][1]]=english_letter_freq[i][1]
    
    print("--------------------------------------------------------------")
    print("The possible output is \n-------------------------------------")
    
    decrypted=""
    for letter in encrypted:
        if letter.isalpha():
            decrypted+=map_letter[letter]
        else:
            decrypted+=letter
    print(decrypted)
    
    encrypted_file.close()

if __name__=='__main__':
    main()
        
        