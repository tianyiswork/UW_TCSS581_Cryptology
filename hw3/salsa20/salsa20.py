# Rc4 Python Implementation
# Authors:
# Dustin Ray
# Tianyi Li
# TCSS 581 - Spring 2020


#global variable for number of rounds
ROUNDS = 20

#rotating function
def ROTL(b, r):

    s = (((b << r)) | (b >> (32 - r))) 
    return s

# quarter round function
def QR(a, b, c, d):

    b ^= ROTL(a + d, 7) 
    c ^= ROTL(b + a, 9) 
    d ^= ROTL(c + b, 13)    
    a ^= ROTL(d + c, 18)


# salsa20 algorithm takes in_16 as input which is 16 bit
# plaintext to be encrypted
def main(in_16, nonce, counter, key):


    k = [(key[4 * i : 4 * i + 4]) for i in range(8)]
    n = [(nonce[4 * i : 4 * i + 4]) for i in range(2)]
    b = [(counter[4 * i : 4 * i + 4]) for i in range(2)]

    in_16 = [16]
    x = [16]
    i = 0

    x = [in_16[0], k[0], k[1], k[2], 
    k[3], in_16[1], n[0], n[1],
    b[0], b[1], in_16[2], k[4], 
    k[5], k[6], k[7], in_16[3]]


    while i < ROUNDS:
        
        # run quarter round alg on columns
        QR(x[0], x[4], x[8], x[12]) 
        QR(x[5], x[9], x[13], x[1])
        QR(x[10], x[14], x[2], x[6])
        QR(x[15], x[3], x[7], x[11])

        # run QR alg on rows
        QR(x[ 0], x[ 1], x[ 2], x[ 3])
        QR(x[ 5], x[ 6], x[ 7], x[ 4])
        QR(x[10], x[11], x[ 8], x[ 9])
        QR(x[15], x[12], x[13], x[14])

        i += 2

    # final loop combines original input with
    # ciphertext
    for el in x:
        x[el] + in_16[el]
    
    return x

if __name__ == "__main__":
    

    #empty the output file, if there was one
    with open('encrypted.txt', 'w'): 
        pass

    #define the plaintext path
    #in_16 = 'This is a cryptology class'
    #in_16 = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
    bible_path = "pg10.txt"
    cypher = "encrypted.txt"
    nonce = [3,1,4,1,5,9,2,6]
    counter = [7,0,0,0,0,0,0,0]
    key = '1b27556473e985d462cd51197a9a46c76009549eac6474f206c4ee0844f68389'
    output = open(cypher, "w")

    #print (main(in_16, nonce, counter, key))
    
    with open(bible_path, "rb") as bible:
        in_16 = bible.read(16)
        while in_16 != b'':
            print(main(in_16, nonce, counter, key), file = output)
    
    bible.close()
    output.close()
