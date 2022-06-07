from collections import Counter
from operator import xor
import sys

def xor_encrypt(s1,s2):
    n1=len(s1)
    n2=len(s2)
    
    # throw an error if the two strings are unequal length
    try:
        assert (n1==n2), "The xor two strings' lengths should be the same"
    except Exception as e:
        print(e)
        sys.exit(1)
    
    xor_list=[ord(a)^ord(b) for a,b in zip(s1,s2)]
    xored=""
    for digit in xor_list:
        xored+='{:02x}'.format(digit)
    
    
    return xored
    
        

def main():
    ret=xor_encrypt("Darlin dont you go","and cut your hair!")
    print(ret)

if __name__=='__main__':
    main()
        
        