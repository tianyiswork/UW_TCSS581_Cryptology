# Rc4 Python Implementation
# Authors:
# Dustin Ray
# Tianyi Li
# TCSS 581 - Spring 2020


# Key Scheduling Alg accepts a keyseed as input
# and expands it to keystream. 

import sys

def KSA(key):

    keylength = len(key)

    # define S
    S = list(range (256))

    # define j
    j = 0

    # scheduling loop
    for i in range(256):
        j = (j + S[i] + key[i % keylength]) % 256
        
        # swap values
        S[i], S[j] = S[j], S[i]

    return S

# function accepts S from above and generates a 
# pseudorandom number output to be used for encryption
def PRNGA(S):

    #define i and j    
    i = 0
    j = 0

    # this is broken, we need a way to loop 
    # infinitely here.
    idx = 0
    while idx <= len(S):
        
        # advance bit i + 1
        i = (i + 1) % 256

        # advance bit j + S[i]
        j = (j + S[i]) % 256
        
        # swap just like above
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        
        # since a stream is being generated, 
        # use yield instead of return
        yield K



# driver of this implmentation
# of RC4. Accepts key as input and calls other functions. 
def mainAlg(key):

    #expand key using KSA defined above
    S = KSA(key)

    # generate pseudorandom output using function
    # defined above. 
    PRGA = PRNGA(S)

    return PRGA


# convert key to Unicode code
def prepare_key(key):
    
    return [ord(i) for i in key]


if __name__ == "__main__":
    
    #empty the output file, if there was one
    with open('encrypted.txt', 'w'): 
        pass

    #define the key
    key = 'crypto'

    #define the plaintext path
    #plaintext = 'This is a cryptology class'
    bible_path = "pg10.txt"
    bible = open(bible_path, "r")
    plaintext = bible.read()
    bible.close()

    #convert key
    key = prepare_key(key)

    #wake up the main function
    key_stream = mainAlg(key)
    
    #write the output cyphertext to a .txt file
    with open('encrypted.txt','w') as output:
        for c in plaintext:
            print("%02X" % (ord(c) ^ key_stream.__next__()), file = output)



