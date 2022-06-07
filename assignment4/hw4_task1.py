import hashlib
import string
import itertools
import time
import matplotlib.pyplot as plt
import numpy as np

def sha256_trunc(s:string, bits: int):
    hash_sha256=hashlib.sha256(s.encode('utf-8')).hexdigest()
    trunc=bin(int(hash_sha256,16))[2:].zfill(256)
    
    # need to convert it back to int because the memory cannot hold strings
    # for 50 bit collision test
    return int(trunc[:bits],2)

def conllision_test(number_bits: int):
    ## return the collision time and the number of input strings it need
    
    ## I am using the Birthday Problem Methods.
    dict_set=set()
    collision_time=0.0
    str_length=1
    target=string.ascii_letters
    while True:
        # measure the execution time
        start=time.time()
        for x in itertools.product(target,repeat=str_length):
            s=''.join(x)
            hashed=sha256_trunc(s,number_bits)
            # if the collision found
            if hashed in dict_set:
                collision_time+=time.time()-start
                # because the number of input strings are already found + this collision found
                return collision_time,len(dict_set)+1
            dict_set.add(hashed)
        
        # if not found, then continue
        collision_time+=time.time()-start
        str_length+=1
    
    # this will never execute, but just in case
    return collision_time, len(dict_set)+1
    


def main():
    graph_data=[]
    graph_digest=[i for i in range(8,51,2)]
    for bits in graph_digest:
        col_time, number_inputs=conllision_test(bits)
        graph_data.append([col_time,number_inputs])
    
    
    graph_data=np.array(graph_data)
    graph_digest=np.array(graph_digest)
    
    plt.figure(1)
    
    plt.plot(graph_digest,graph_data[:,0],linewidth=2)
    plt.xlabel('digest size')
    plt.ylabel('collision time')
    
    plt.figure(2)
    plt.plot(graph_digest,graph_data[:,1],linewidth=2)
    plt.xlabel('digest size')
    plt.ylabel('number of inputs')
    
    plt.legend()
    plt.show()
    
if __name__=='__main__':
    main()    