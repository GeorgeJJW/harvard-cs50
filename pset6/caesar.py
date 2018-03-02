import sys
    
def main():
    
    # ensure proper usage
    if (len(sys.argv) != 2):
        print("Usage: ./caesar k")
        exit(1)
        
    # obtain text
    plain = input("plaintext: ")
    
    # obtain key
    k = int(sys.argv[1])
    
    # encrypt text with key
    print("ciphertext: ", end="")
    
    # iterate over each character in text
    for i in range(len(plain)):
        
        # convert uppercase letters from ASCII index to alphabetical index and back
        if ((plain[i].isalpha()) and (plain[i].isupper())):
            print(chr((((ord(plain[i]) - 65) + k) % 26) + 65), end="")
            
        # convert lowercase letters from ASCII index to alphabetical index and back
        elif ((plain[i].isalpha()) and (plain[i].islower())):
            print(chr((((ord(plain[i]) - 97) + k) % 26) + 97), end="")
        
        # leaving non-letter characters as they were
        else:
            print(plain[i], end="")
            
    # append newline
    print("\n", end="")
    
# initiate main function
if __name__ == "__main__":
    main()
        
        
    