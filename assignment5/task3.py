import sys


import hashlib
import string
import itertools
import time
import matplotlib.pyplot as plt
import numpy as np

def main():
    
    try:
        assert (len(sys.argv)>2), "User has to input two files"
    except Exception as e:
        print(e)
        sys.exit(1)
    
    rsa_file=open(sys.argv[1],'r')
    aes_file=open(sys.argv[2],'r')
    
    rsa_data=rsa_file.readlines()[5:]
    aes_data=aes_file.readlines()[5:]
    
    rsa_key_size=[]
    rsa_throughput=[]
    aes_block_size=aes_data[0].split()
    aes_throughput=aes_data[3].split()[2:]
    
    
    for line in rsa_data:
        li=line.split()
        rsa_key_size.append(int(li[1]))
        rsa_throughput.append(float(li[5]))
    
    aes_block_size=[int(x) for x in aes_block_size if x.isdigit()]
    aes_throughput=[float(x[:-1]) for x in aes_throughput]
    
    rsa_key_size=np.array(rsa_key_size)
    rsa_throughput=np.array(rsa_throughput)
    aes_block_size=np.array(aes_block_size)
    aes_throughput=np.array(aes_throughput)
    
    plt.figure(1)
    
    plt.plot(rsa_key_size,rsa_throughput,linewidth=2)
    plt.xlabel("rsa key size in bits")
    plt.ylabel("rsa sign/s")
    
    plt.figure(2)
    
    plt.plot(aes_block_size,aes_throughput,linewidth=2)
    plt.xlabel("aes in bytes")
    plt.ylabel("aes operation in k(1000)")
    
    plt.legend()
    plt.show()
    

if __name__=='__main__':
    main()